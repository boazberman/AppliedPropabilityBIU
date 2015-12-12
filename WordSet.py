from collections import Counter
class WordSet:
    def __init__(self, words, vocabularySize):
        self.wordAppearanceCounter = Counter(words)
        self.length = len(words)
        self.distinctLength = len(self.wordAppearanceCounter.keys())
        # self.pLidstone = {}
        self.vocabularySize = vocabularySize

    def distinctItems(self):
        return self.wordAppearanceCounter.iteritems()

    def countAppearances(self, word):
        return self.wordAppearanceCounter[word]

    def pLidstone(self, word, lamda):
        return (self.wordAppearanceCounter[word] + lamda) / (self.length + self.vocabularySize * lamda)

    def pMaximumLikelihoodEstimate(self, word):
        return float(self.wordAppearanceCounter[word]) / self.length

    def pLidstoneByFreq(self, lamda , freq):
        return (freq + lamda) / (self.length + self.vocabularySize * lamda)
