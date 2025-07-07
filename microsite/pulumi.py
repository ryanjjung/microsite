import tb_pulumi
import pulumi.automation

class PulumiProject():
    def __init__(self):
        '''
        Need to handle:

        - Steps:
          - Create new Pulumi stack
          - Add config.stack.yaml
          - Automate preview/up
        '''

        self.project = tb_pulumi.ThunderbirdPulumiProject()
        self.workspace = pulumi.automation.Workspace()