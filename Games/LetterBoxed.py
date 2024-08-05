from Logger import Logger
from Games.Game import Game

class LetterBoxed(Game):

    def __init__(self, wgUtils, wgHandler):
        super().__init__(wgUtils, wgHandler)
        self.logger = Logger().getLogger(name=__name__)

    # @override
    def displayUsageInstructions(self):
        pass

    # @override
    def gameHelper(self, solverMode=False):
        pass