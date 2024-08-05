import json
import os
import re
import art
from colorama import Fore, Back, Style
from Logger import Logger

class WGUtils():
    DICTIONARY_EN_US = "en_us"
    DICTIONARY_EN_US_NAME = "american-english"
    DICTIONARY_EN_GB = "en_gb"
    DICTIONARY_EN_GB_NAME = "british-english"
    LOG_FILE = "log.txt"
    GAME_META_FILE = "gameMeta.json"
    HR = '=-='*20
    ALPHABETS = 'abcdefghijklmnopqrstuvwxyz'
    logger = None
    dictionary = None
    gameMeta = None
    gameName = None

    def __init__(self):
        self.logger = Logger().getLogger(name=__name__)

    def clearLogs(self):
        with open(self.LOG_FILE, 'w') as f:
            f.write('')
   
    def displayBanner(self, title, font=art.DEFAULT_FONT, colour=Fore.WHITE, background=Back.RESET, style=Style.NORMAL):
        # Generate ASCII art
        ascii_art = art.text2art(title, font=font)
        self.colouramaOutput(ascii_art, colour, background, style)

    def colouramaOutput(self, text, colour=Fore.WHITE, background=Back.RESET, style=Style.NORMAL):
        print(colour + background + style + text)
    
    def getColoramaText(self, text, colour=Fore.WHITE, background=Back.RESET, style=Style.NORMAL):
        return colour + background + style + text + Style.RESET_ALL
    
    def clearColourama(self):
        print(Style.RESET_ALL)

    def loadGameMetaData(self):
        if self.gameMeta is None:
            try:
                with open(WGUtils.GAME_META_FILE, 'r') as fHand:
                    self.gameMeta = json.load(fHand)
            except Exception as e:
                self.logger.error(f"Error loading game meta: {e}", exc_info=1, stack_info=True)
            self.logger.info(f"Master meta loaded.")
        return self.gameMeta
    
    def getGameMetaItem(self, key):
        if self.gameMeta is None:
            self.loadGameMetaData()
        gameData = self.gameMeta[self.gameName]
        return gameData if key is None else gameData[key]
    
    def writeGameMeta(self, gameName, key, value):
        if self.gameMeta is None:
            self.loadGameMetaData()
        gameName = self.sluggify(gameName)
        self.gameMeta[gameName][key] = value
        with open(WGUtils.GAME_META_FILE, 'w') as fHand:
            json.dump(self.gameMeta, fHand, indent=4)

    def setGameName(self, gameName):
        self.gameName = self.sluggify(gameName)

    def initDictionary(self, type=None):
        if type == self.DICTIONARY_EN_US:
            self.dictFileName = self.DICTIONARY_EN_US_NAME
        elif type == self.DICTIONARY_EN_GB:
            self.dictFileName = self.DICTIONARY_EN_GB_NAME
        else:
            self.logger.warn("Invalid dictionary type. Using default dictionary.")
            self.dictFileName = 'words'
        self.logger.info(f'Dictionary file name: {self.dictFileName}')
            
        filePath = "/usr/share/dict/" + self.dictFileName
        if os.path.exists(filePath):
            self.logger.info(f"Dictionary file exists at {filePath}")
            try:
                with open(filePath, "r") as fHand:
                    self.dictionary = re.sub("[^\w]", " ",  fHand.read()).split()
                    self.logger.info(f"Dictionary initialised.")
            except Exception as e:
                self.logger.error(f"Error reading dictionary file: {e}", exc_info=1, stack_info=True)
        else:
            self.logger.error("Dictionary file does not exist.", exc_info=1)
    
    def wordExists(self, word):
        if self.dictionary is None:
            self.initDictionary()
        return word in self.dictionary

    def sluggify(self, text):
        return re.sub(r'\W+', '-', text.lower())
    
    def addHR(self):
        self.colouramaOutput(WGUtils.HR, Fore.WHITE, Back.RESET, Style.BRIGHT)
        print(Style.RESET_ALL)
    
    def displayUnderConstruction(self):
        self.displayBanner("OOPS!", font='computer', colour=Fore.YELLOW, style=Style.BRIGHT)
        self.colouramaOutput("Under construction", colour=Fore.RED, style=Style.BRIGHT)
        self.colouramaOutput("Please check back later.", colour=Fore.RED)