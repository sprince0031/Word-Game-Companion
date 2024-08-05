from Logger import Logger
from colorama import Fore, Back, Style

# Description: Base class for all games
class Game():

    def __init__(self, wgUtils, wgHandler):
        self.wgUtils = wgUtils
        self.wgHandler = wgHandler
        self.logger = Logger().getLogger(name=__name__)
        if not self.wgHandler.helperAvailable:
            self.wgUtils.displayUnderConstruction()
            self.logger.info(f"Helper not available for {self.wgHandler.gameName}")
            exit(0)
        self.solveMode = False

    def gameHelper(self, solverMode=False):
        pass

    def displayUsageInstructions(self):
        # Display game specific instructions
        pass