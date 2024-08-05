from colorama import Fore, Back, Style

from Logger import Logger
from Games.Game import Game
from tqdm import tqdm

class Wordle(Game):

    WORD_LENGTH = 5
    ATTEMPTS = 6

    def __init__(self, wgUtils, wgHandler):
        super().__init__(wgUtils, wgHandler)
        self.logger = Logger().getLogger(name=__name__)
        self.gameName = 'wordle'
        self.wordleDict = {'word': list('_'*5), 'in-word': {}, 'not-in-word': []}

    def displayUsageInstructions(self):
        self.wgUtils.colouramaOutput("Instructions:", Fore.BLUE, Back.BLACK, Style.BRIGHT)
        self.wgUtils.colouramaOutput("1. For every attempt, enter your word when asked in the prompt.")
        self.wgUtils.colouramaOutput("2. Enter the result of the attempt in the next prompt.")
        self.wgUtils.colouramaOutput(f"\t2.1 For letters that didn't match, enter a corresponding {self.wgUtils.getColoramaText('_', Fore.RED, Back.BLACK, Style.BRIGHT)} character.")
        self.wgUtils.colouramaOutput(f"\t2.2 For letters that matched but are not in the correct position, enter a corresponding {self.wgUtils.getColoramaText('*', Fore.YELLOW, Back.BLACK, Style.BRIGHT)} character.")
        self.wgUtils.colouramaOutput(f"\t2.3 For letters that matched and are in the correct position, enter a corresponding {self.wgUtils.getColoramaText('+', Fore.GREEN, Back.BLACK, Style.BRIGHT)} character.")
        self.wgUtils.colouramaOutput("3. Keep going until you get the word right or you run out of attempts.")
        self.wgUtils.addHR()        

    # @override
    def gameHelper(self, solverMode=False):
        self.displayUsageInstructions()

        # Game logic
        for attempt in range(Wordle.ATTEMPTS):
            # Process user inputs
            currentWord, result = self.processAttemptData()
            self.logger.info(f"Attempt {attempt+1}: {currentWord}, {result}, {self.wordleDict}")
            
            # Generate all combinations of known letters in the unfilled blanks
            validCombinations = self.generateKnownLetterCombinations(self.wordleDict['in-word'], self.wordleDict['word'])
            self.logger.info(f"Valid combinations: {validCombinations}")

            # Find words from the valid combinations
            possibleAnswers = self.findWords(validCombinations, attempt)
            self.wordleDict['possible-answers'] = possibleAnswers
            self.logger.info(f"Possible answers: {possibleAnswers}")

            if len(possibleAnswers) == 1:
                self.wgUtils.colouramaOutput(f"THE ONLY REMAINING POSSIBILITY IS", colour=Fore.BLUE, style=Style.BRIGHT)
                self.wgUtils.displayBanner(possibleAnswers[0], font=self.wgHandler.bannerFont, colour=self.wgHandler.bannerColor, style=Style.BRIGHT)
                self.wgUtils.clearColourama()
                if input("Was it correct? (y/n): ").lower() == 'y':
                    self.wgUtils.colouramaOutput(f"Congratulations! You got it right!", colour=Fore.GREEN, style=Style.BRIGHT)
                else:
                    self.wgUtils.colouramaOutput(f"Sorry! Looks like the word of the day isn't in my dictionary :(", colour=Fore.RED, style=Style.BRIGHT)
                break
            else:  
                # Print the possible answers
                self.wgUtils.colouramaOutput(f"Possible answers for attempt {attempt+1}:", Fore.BLUE, Back.BLACK, Style.BRIGHT)
                self.prettyPrintWordList(possibleAnswers)
                self.wgUtils.clearColourama()
            
            # if solverMode:
            #     self.wordFinder(self.wordleDict)
            # else:
            #     pass
        

    # Wordle helper functions
    # -----------------------
    def processAttemptData(self):
        currentWord = list(input("Enter your word: ").lower())
        result = list(input("Enter the result (): ").lower())
        for i in range(Wordle.WORD_LENGTH):
            if result[i] == '+':
                self.wordleDict['word'][i] = currentWord[i]
                # Remove words from the possible answers that don't have the correct letter in the correct position
                if 'possible-answers' in self.wordleDict.keys():
                    self.wordleDict['possible-answers'] = [word for word in self.wordleDict['possible-answers'] if word[i] == currentWord[i]]
                # Clear the list of possible positions for the letter
                if currentWord[i] in self.wordleDict['in-word']:
                    self.wordleDict['in-word'].pop(currentWord[i])
                # remove the current index in any of the known alphabet index lists if present
                for _, indices in self.wordleDict['in-word'].items():
                    if i in indices:
                        indices.remove(i)
            elif result[i] == '*':
                if currentWord[i] not in self.wordleDict['in-word']:
                    if self.wordleDict['word'] == list('_' * 5): # Check if no index has a locked alphabet yet
                        initList = list(range(5)) # initialise a new list with all indices
                        initList.remove(i)
                        self.wordleDict['in-word'][currentWord[i]] = initList
                    else:
                        missingAlphaIndices = self.getSpaceIndices(self.wordleDict['word'])
                        missingAlphaIndices.remove(i)
                        self.wordleDict['in-word'][currentWord[i]] = missingAlphaIndices # Create a new list containing indices of possible positions for the letter i.e., by excluding the current position.
                else:
                    self.wordleDict['in-word'][currentWord[i]].remove(i) # Remove the index of the wrong position for the letter from the existing list
            else:
                self.wordleDict['not-in-word'].append(currentWord[i])
        return currentWord, result
    
    
    def generateKnownLetterCombinations(self, inWordDict, wordRepresentation):
        validCombos = []
        stack = [(inWordDict, list(wordRepresentation))]

        while stack:
            currentInWordDict, currentWordRepresentation = stack.pop()

            if len(currentInWordDict) == 0:
                validCombos.append(currentWordRepresentation)
                continue

            inWordDictCopy = currentInWordDict.copy()
            letters = list(inWordDictCopy.keys())
            currentLetterIndices = inWordDictCopy.pop(letters[0])

            for index in currentLetterIndices:
                if currentWordRepresentation[index] == '_':
                    newWordRepresentation = currentWordRepresentation.copy()
                    newWordRepresentation[index] = letters[0]
                    stack.append((inWordDictCopy, newWordRepresentation))

        return validCombos
        
    def getAllAlphaCombinations(self, word, alphaIndices, possibelStrings):
        allowedAlphas = [alpha for alpha in self.wgUtils.ALPHABETS if alpha not in self.wordleDict['not-in-word']]
        return self.generateAlphaCombinations(word, alphaIndices, allowedAlphas, possibelStrings, 0)

    def generateAlphaCombinations(self, word, alphaIndices, allowedAlphas, possibleStrings, index):
        if index == len(alphaIndices):
            possibleStrings.add(''.join(word))
            return possibleStrings
        for alpha in allowedAlphas:
            word[alphaIndices[index]] = alpha
            self.generateAlphaCombinations(word, alphaIndices, allowedAlphas, possibleStrings, index + 1)
            word[alphaIndices[index]] = '_'  # reset the word for the next iteration
        return possibleStrings
        
    # Get meta data from custom list
    def getSpaceIndices(self, word):
        missingAlphaIndices = [i for i, alpha in enumerate(word) if alpha == '_']
        self.logger.info(f"Missing indices: {missingAlphaIndices}")
        return missingAlphaIndices
    
    def findWords(self, wordList, attempt):
        finalWordList = []
        # Generate all possible string combinations and check against dictionary
        if attempt == 0:
            self.wgUtils.colouramaOutput(f"Generating all possible words from the given inputs...", colour=Fore.BLUE)
            self.wgUtils.clearColourama()
            possibleStrings = set()
            for word in wordList:
                spaceIndices = self.getSpaceIndices(word)
                possibleStrings = self.getAllAlphaCombinations(word, spaceIndices, possibleStrings)
            self.logger.info(f"Possible strings: {possibleStrings}")
            for string in tqdm(possibleStrings):
                if string not in finalWordList and self.wgUtils.wordExists(string):
                    self.logger.info(f"Word found: {string}")
                    finalWordList.append(string)
        # Only need to eliminate possibilities from the existing list of valid words generated from the first attempt
        else:
            for string in self.wordleDict['possible-answers']:
                invalidWord = False
                for alpha in self.wordleDict['not-in-word']:
                    if alpha in string:
                        invalidWord = True
                        break
                if not invalidWord:
                    self.logger.info(f"Word found: {string}")
                    finalWordList.append(string)

        return finalWordList
    
    def prettyPrintWordList(self, wordList):
        for word in wordList:
            self.wgUtils.colouramaOutput(word, colour=Fore.GREEN, style=Style.BRIGHT)