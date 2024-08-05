#Program to find lexical word cominations to find words with missing letters
import argparse
from WGUtils import WGUtils
from WGameHandler import WGameHandler
from Logger import Logger

class WGHandler():
	PROGRAM_TITLE = 'Word Play'
	def __init__(self):
		self.logger = Logger().getLogger(name=__name__)
		self.wgutils = WGUtils()
		self.wgutils.clearLogs()
		self.parser = argparse.ArgumentParser(description="Your word game companion! Use this tool to find word meanings, unscramble words " + 
										"and get help with specific word games. The available game modes are:" +
										"\n1. wordle" +
										"\n2. letter-boxed" +
										"\n3. strands")
		self.args = None
		self.wgutils.addHR()
		self.wgutils.displayBanner(self.PROGRAM_TITLE)
		self.wgutils.addHR()
		self.logger.info("WGHandler initialized.")		

	def addArguments(self):
		self.parser.add_argument('-g', '--game-mode', metavar='<game name>', help='Pass the game name. Available game modes: wordle, letter-boxed')
		self.parser.add_argument('-s', '--solve', action='store_true', help='Solves the game for you instead of helping with hints if this flag is set')
		self.parser.add_argument('-d', '--dict-check', metavar='<word>', action='append', help='Get word meaning and usage')
		self.parser.add_argument('-D', '--dict-set', metavar='<dict name>', help='Set the dictionary to use. Available dictionaries: en-us, en-gb')
		self.parser.add_argument('-u', '--unscramble', metavar='<scrambled string>', help='Unscramble letters to get a potential combination that make up a lexical word')

	def parseArguments(self):
		self.args = self.parser.parse_args()

	def run(self):
		self.addArguments()
		self.parseArguments()
		self.logger.info(f"Passed args: {self.args}")

if __name__ == '__main__':
	try:
		wordGameHelper = WGHandler()
		wordGameHelper.run()
		runFlag = False
		# If a custom dictionary is to be used, pass the dictionary name as an argument
		if wordGameHelper.args.dict_set:
			wordGameHelper.wgutils.initDictionary(wordGameHelper.args.dict_set)
		else:
			wordGameHelper.wgutils.initDictionary(WGUtils.DICTIONARY_EN_US)

		# If dict checker is called, get the meaning of the word
		if wordGameHelper.args.dict_check:
			wordGameHelper.wgutils.getWordMeaning(wordGameHelper.args.dict_check)
			runFlag = True
		
		# If unscramble is called, find the possible words
		if wordGameHelper.args.unscramble:
			wordGameHelper.wgutils.findWords(wordGameHelper.args.unscramble)
			runFlag = True

		# If game mode is passed, pass the game name to the WGameHandler class
		if wordGameHelper.args.game_mode:
			wordGame = WGameHandler(wordGameHelper.args.game_mode, wordGameHelper.args.solve)
			wordGame.run()
			runFlag = True

		if not runFlag:
			print("No valid arguments passed. Please pass valid arguments to run the program.")
			wordGameHelper.logger.info("No valid arguments passed. Exiting program.")
			wordGameHelper.parser.print_help()
			
	except Exception as e:
		wordGameHelper.logger.error(f"Error in main: {e}", exc_info=1, stack_info=True)
		print("An error occured. Please look at logs for further information. :(")
		exit(1)