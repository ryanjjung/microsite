import jinja2
import logging
import shutil

from abc import ABC, abstractclassmethod
from microsite.util import AttrDict, Engine
from pathlib import Path
from pulumi import automation as pulumi_automation
from tempfile import TemporaryDirectory

log = logging.getLogger(__name__)


class PublishEngine(ABC, Engine):
    """
    Abstract class representing common features of a publishing engine.

    :param name: The name of the engine.
    :type name: str

    :param config: A dict containing operating parameters for this engine.
    :type config: dict
    """

    def __init__(self, name: str, source_dir: str, config: AttrDict, dry_run: bool):
        self.name = name
        self.source_dir = source_dir
        self.config = config
        self.dry_run = dry_run

    @abstractclassmethod
    def publish(self):
        """
        Absract function representing a PublishEngine's publication process.

        :param source_dir: Directory containing the content to publish. This may be the
            ``target_dir`` of a rendering engine.
        :type source_dir: str

        :param target: Value describing the target. This may vary between publish engines.
        :type target: str
        """

        pass


class PulumiPublishEngine(PublishEngine):
    def __init__(self, name: str, source_dir: str, config: AttrDict, dry_run: bool):
        super().__init__(name=name, source_dir=source_dir, config=config, dry_run=dry_run)
        self.use_temp_work_dir = False if self.config.work_dir else True

        # If we used a temporary working directory, default to not persisting it
        # If a work_dir was specified by the user, default to persisisting it
        # Always allow the user to override the setting
        default_persist_work_dir = False if self.use_temp_work_dir else True
        self.persist_work_dir = self.config.get('persist_work_dir', default_persist_work_dir)

        # Set up a temporary working environment if need be
        if self.use_temp_work_dir:
            self.temp_work_dir = TemporaryDirectory(dir='.', prefix='pulumi_')
            self.config.work_dir = self.temp_work_dir.name
        else:
            self.temp_work_dir = None

        # Jinja environment for other functions to operate in
        template_dir = Path('microsite/publish/static/pulumi/templates').resolve()
        _j2_loader = jinja2.FileSystemLoader(searchpath=template_dir)
        self.pulumi_templates = jinja2.Environment(loader=_j2_loader)

        self.work_dir = Path(self.config.work_dir).resolve()
        self.work_dir_str = str(self.work_dir)

        # Templated files
        self.file_main_py = self.work_dir / '__main__.py'
        self.file_requirements_txt = self.work_dir / 'requirements.txt'
        self.file_pulumi_yaml = self.work_dir / 'Pulumi.yaml'
        self.filename_pulumi_stack_yaml = f'Pulumi.{self.config.pulumi_stack_name}.yaml'
        self.file_pulumi_stack_yaml = self.work_dir / self.filename_pulumi_stack_yaml

        self.stack = None

        self.pulumi_environment = self.__build_pulumi_environment()

    def __build_pulumi_environment(self):
        env_vars = {}

        if self.config.pulumi_state_backend == 's3':
            pass
        elif self.config.pulumi_state_backend == 'cloud':
            with open(self.config.pulumi_access_token_file, 'r') as file:
                env_vars['PULUMI_CONFIG_ACCESS_TOKEN'] = file.read().strip()

        with open(self.config.pulumi_passphrase_file, 'r') as file:
            env_vars['PULUMI_CONFIG_PASSPHRASE'] = file.read().strip()

        # Always suppress tb_pulumi's stack-level protection
        env_vars['TBPULUMI_DISABLE_PROTECTION'] = 'True'

        log.debug(f'DEBUG -- env_vars: {env_vars}')

        return env_vars

    def ensure_work_dir(self):
        log.info(f'Ensuring the working directory {self.work_dir_str} exists.')
        if self.work_dir.exists():
            log.debug(f'Working directory {self.work_dir_str} already exists.')
            if not self.persist_work_dir:
                log.debug('Deleting and recreating it to ensure a clean working environment.')
                shutil.rmtree(self.work_dir_str)
                self.work_dir.mkdir(parents=True)
            else:
                log.debug('Leaving the working directory alone.')
        else:
            self.work_dir.mkdir(parents=True)

    def validate_work_dir(self):
        if not self.file_main_py.exists():
            raise IOError(f'No __main__.py file exists in {self.work_dir_str}')
        if not self.file_requirements_txt.exists():
            raise IOError(f'No requirements.txt file exists in {self.work_dir_str}')
        return True

    def construct_pulumi_yaml(self):
        log.debug('Rendering Pulumi.yaml.j2')
        template = self.pulumi_templates.get_template('Pulumi.yaml.j2')
        if self.config.pulumi_state_backend == 's3':
            state_url = f's3://{self.config.pulumi_state_s3_bucket}'
        elif self.config.pulumi_state_backend == 'cloud':
            state_url = 'https://api.pulumi.com'
        content = template.render(
            {
                'project_name': self.config.project_name or 'project_name',
                'project_description': self.config.project_description or 'project_description',
                'state_url': state_url,
            }
        )

        with self.file_pulumi_yaml.open('w') as file:
            file.write(content)

    def construct_pulumi_stack_yaml(self):
        log.debug(f'Rendering {self.filename_pulumi_stack_yaml}')
        template = self.pulumi_templates.get_template('Pulumi.stack.yaml.j2')
        content = template.render(
            {
                'aws_region': self.config.aws_region or 'us-east-1',
            }
        )

        with self.file_pulumi_stack_yaml.open('w') as file:
            file.write(content)

    def publish(self):
        log.info('Publishing using Pulumi')
        self.construct_pulumi_yaml()
        self.construct_pulumi_stack_yaml()

        log.debug(f'Getting Pulumi set up on stack {self.config.pulumi_stack_name}')
        stack = pulumi_automation.create_or_select_stack(
            stack_name=self.config.pulumi_stack_name,
            work_dir=self.work_dir,
            opts=pulumi_automation.LocalWorkspaceOptions(env_vars=self.pulumi_environment),
        )

        pulumi_log = self.config.pulumi_log or 'pulumi.log'
        pulumi_error_log = self.config.pulumi_error_log or 'pulumi.err'
        if self.dry_run:
            log.info(
                f'Generating a preview of changes in {pulumi_log}. '
                f'Errors will be shown in {pulumi_error_log}'
            )
            response = stack.preview()
        else:
            log.info(
                f'Deploying the site. See {pulumi_log} for progress, {pulumi_error_log} for errors.'
            )
            response = stack.up()

            with open(pulumi_log, 'w') as file:
                file.write(response.stdout)
            with open(pulumi_error_log, 'w') as file:
                file.write(response.stderr)

    def cleanup(self):
        if not self.persist_work_dir:
            log.info(f'Deleting working directory {self.work_dir_str}')
            if self.use_temp_work_dir:
                self.temp_work_dir.cleanup()
            else:
                shutil.rmtree(self.work_dir_str)


class TBPulumiPublishEngine(PulumiPublishEngine):
    def __init__(self, name: str, source_dir: str, config: AttrDict, dry_run: bool):
        super().__init__(name=name, source_dir=source_dir, config=config, dry_run=dry_run)

    def validate_work_dir(self):
        super().validate_work_dir()
        config_yaml_filename = f'config.{self.config.pulumi_stack_name}.yaml'
        config_yaml = self.work_dir / config_yaml_filename
        if not config_yaml.exists():
            raise IOError(f'No {config_yaml_filename} file exists in {self.work_dir_str}')

    def publish(self):
        super().publish()
