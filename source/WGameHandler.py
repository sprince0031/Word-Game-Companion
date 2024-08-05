import random
from colorama import Fore, Back, Style
from WGUtils import WGUtils
from Logger import Logger
from Games.Wordle import Wordle
from Games.Strands import Strands
from Games.LetterBoxed import LetterBoxed

class WGameHandler():
    def __init__(self, gameName, solveMode):
        self.logger = Logger().getLogger(name=__name__)
        self.wgUtils = WGUtils()
        self.gameName = gameName
        self.solveMode = solveMode
        self.bannerFonts = ['marquee', 'script', 'nscript', '08', 'os2', 'pebbles', 'computer']

    def run(self):
        self.processGameMetaData()
        self.displayGameBanner()
        self.checkSolverAvailability()
        
        # Passing control to individual game modules
        if self.gameName == 'wordle':
            Wordle(wgUtils=self.wgUtils, wgHandler=self).gameHelper(solverMode=self.solveMode)
        elif self.gameName == 'letter-boxed':
            LetterBoxed(wgUtils=self.wgUtils, wgHandler=self).gameHelper(solverMode=self.solveMode)
        elif self.gameName == 'strands':
            Strands(wgUtils=self.wgUtils, wgHandler=self).gameHelper(solverMode=self.solveMode)
        
        # Add more games here

        else:
            self.logger.error(f"Game mode {self.gameName} not found.")
            self.wgUtils.colouramaOutput(f"Game mode {self.gameName} not found. Please pass a valid game mode. Run the program with -h or --help for more information.", colour=Fore.RED, style=Style.BRIGHT)

    def processGameMetaData(self):
        if self.gameExists(self.gameName):
            # Set game specific data
            if 'bannerFont' in self.wgUtils.getGameMetaItem(key=None):
                self.bannerFont = random.choice(self.wgUtils.getGameMetaItem('bannerFont'))
            else:
                self.bannerFont = random.choice(self.bannerFonts)
            self.bannerColor = self.wgUtils.getGameMetaItem('bannerColour')
            self.solverAvailable = self.wgUtils.getGameMetaItem('solverAvailable')
            self.helperAvailable = self.wgUtils.getGameMetaItem('helperAvailable')
            self.logger.info(f"{self.gameName} meta loaded: {self.wgUtils.getGameMetaItem(key=None)}")
        else:
            self.logger.error(f"Game data not found for: {self.gameName}")
            self.wgUtils.colouramaOutput(f"Game mode {self.gameName} does not exist. Please pass a valid game mode. Run the program with -h or --help for more information.", colour=Fore.RED, style=Style.BRIGHT)
            exit(0)
    
    def gameExists(self, gameName):
        self.logger.info(f"Checking if game exists: {gameName}")
        self.wgUtils.setGameName(gameName)
        try:
            self.wgUtils.getGameMetaItem(key=None)
            return True
        except Exception as e:
            return False
        
    def displayGameBanner(self):
        self.wgUtils.colouramaOutput("Chosen game:", colour=Fore.RED, style=Style.BRIGHT)
        self.wgUtils.displayBanner(self.gameName, font=self.bannerFont, colour=self.bannerColor, style=Style.BRIGHT)
        self.wgUtils.colouramaOutput("Description:", colour=Fore.WHITE, style=Style.BRIGHT)
        self.wgUtils.colouramaOutput(self.wgUtils.getGameMetaItem('description'), colour=Fore.WHITE, style=Style.NORMAL)
        self.wgUtils.colouramaOutput(self.wgUtils.getGameMetaItem('url'), colour=Fore.WHITE, style=Style.NORMAL)
        self.wgUtils.addHR()

    # Handle solver mode
    def checkSolverAvailability(self):
        if self.solveMode:
            if self.solverAvailable:
                self.logger.info("Solver mode is enabled. The program will attempt to solve the game.")
            else:
                self.logger.error("Solver mode is not available for this game.")
                self.wgUtils.colouramaOutput("Solver mode is not available for this game. Defaulting to helper mode.", colour=Fore.LIGHTRED_EX, style=Style.BRIGHT)
                self.solveMode = False
        
        
