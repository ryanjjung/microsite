import logging
import tb_pulumi
import pulumi.automation
import shutil

from pathlib import Path

log = logging.getLogger(__name__)


class PulumiProject:
    def __init__(self, stack_name: str, workdir: str):
        """
        Need to handle:

        - Steps:
          - Make a working folder
            - __main__.py
            - config.live.yaml
          - Create new Pulumi stack
          - Set any config values in Pulumi.live.yaml
          - Automate preview/up
        """

        self.project = tb_pulumi.ThunderbirdPulumiProject()
        self.stack_name = stack_name
        self.workdir = workdir
        self.ensure_clean_workdir()

    def ensure_clean_workdir(self):
        """
        Ensures the Pulumi working directory exists.
        """

        workdir = Path(self.workdir).expanduser().resolve()
        if workdir.exists:
            log.debug(
                f'Working directory {str(workdir)} exists. '
                'Deleting it to ensure a clean working environment.'
            )
            shutil.rmtree()

        workdir.mkdir(parents=True)

    def populate_workdir(self):
        return NotImplementedError

    def run_pulumi(self):
        pulumi.automation.create_or_select_stack(stack_name=self.stack_name, work_dir=self.workdir)
