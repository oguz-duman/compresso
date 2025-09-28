from toolboxes.toolbox import Toolbox
import constants

class ToHexToolBox(Toolbox):
    def __init__(self):
        super().__init__(constants.TOOLBOXES['TO_HEX']['NAME'])


    def execute(self, data):
        return data.hex()
    