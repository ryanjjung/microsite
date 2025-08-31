import jinja2
import logging

from microsite.util import AttrDict
from microsite.publish import TBPulumiPublishEngine
from pathlib import Path

log = logging.getLogger(__name__)


class TbPulumiS3Website(TBPulumiPublishEngine):
    """
    Publishes a site using Thunderbird Pulumi's S3Website pattern.
    """

    def __init__(self, name: str, source_dir: str, config: AttrDict, dry_run: bool, destroy: bool):
        super().__init__(
            name=name, source_dir=source_dir, config=config, dry_run=dry_run, destroy=destroy
        )

        # These variables change when developers can test the changes and generally shouldn't be
        # adjustable by the end user.
        self.python_dependencies = [
            'pulumi_aws>=6.65.0,<7',
            'tb_pulumi @ git+https://github.com/thunderbird/pulumi.git@v0.0.15',
        ]
        _module_dir = '/'.join(__file__.split('/')[0:-1])
        tpl_path_internal = Path(
            f'{_module_dir}/static/pulumi/tb_pulumi/s3_website/templates'
        ).resolve()

        # Jinja environment for other functions to operate in
        _j2_loader = jinja2.FileSystemLoader(searchpath=tpl_path_internal)
        self.microsite_templates = jinja2.Environment(loader=_j2_loader)

        # These variables adjust according to user input
        self.filename_config_stack_yaml = f'config.{self.config.pulumi_stack_name}.yaml'
        self.file_config_stack_yaml = self.work_dir / self.filename_config_stack_yaml
        self.file_main_py = self.work_dir / '__main__.py'
        self.file_requirements_txt = self.work_dir / 'requirements.txt'

    def construct_config_stack_yaml(self):
        """
        Constructs the ``config.$stack.yaml`` file required by tb_pulumi.
        """

        template = self.microsite_templates.get_template('config.stack.yaml.j2')
        source_dir = str(Path(self.source_dir).expanduser().resolve())
        content = template.render(
            {
                's3_bucket_name': self.config.publish_bucket,
                'source_dir': source_dir,
            }
        )

        with self.file_config_stack_yaml.open('w') as file:
            file.write(content)

    def construct_main_py(self):
        """
        Constructs the __main__.py file that defines the build pattern.
        """

        template = self.microsite_templates.get_template('__main__.py.j2')
        content = template.render(
            {
                'acm_certificate_arn': self.config.acm_certificate_arn,
                'domain': self.config.domain,
                'route53_zone_id': self.config.route53_zone_id,
                'subdomain': self.config.subdomain,
            }
        )

        with self.file_main_py.open('w') as file:
            file.write(content)

    def construct_requirements_txt(self):
        """
        Constructs the ``requirements.txt`` file that installs the right providers.
        """

        with self.file_requirements_txt.open('w') as file:
            file.write('\n'.join(self.python_dependencies))

    def publish(self):
        """
        Publishes the site as a ``tb_pulumi.s3.S3Website``.
        """
        self.ensure_work_dir()
        self.construct_requirements_txt()
        self.construct_config_stack_yaml()
        self.construct_main_py()
        self.validate_work_dir()
        super().publish()
