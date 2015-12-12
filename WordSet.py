from collections import Counter
class WordSet:
    '''
    Describes a stream of words (as our events), allowing needed methods on them.
    '''
    def __init__(self, words, vocabularySize):
        '''
        :param words: A list of words .
        :param vocabularySize: a natural number setting the threshold of our vocabulary size.
        :return: a {WordSet} item
        '''
        self.wordAppearanceCounter = Counter(words)
        self.length = len(words)
        self.distinctLength = len(self.wordAppearanceCounter.keys())
        self.vocabularySize = vocabularySize

    def distinctItems(self):
        '''
        :return: An iterable of all distinct words from the words given to the {WordSet}
        '''
        return self.wordAppearanceCounter.iteritems()

    def countAppearances(self, word):
        '''
        :param word: The word to check number of appearances of.
        :return: The number of times it appear in the word list.
        '''
        return self.wordAppearanceCounter[word]

    def pLidstone(self, word, lamda):
        '''
        The propability of {word} to appear after applying it a lidstone discount with the given {lamda}.
        :param word:
        :param lamda:
        :return:
        '''
        return (self.wordAppearanceCounter[word] + lamda) / (self.length + self.vocabularySize * lamda)

    def pMaximumLikelihoodEstimate(self, word):
        '''
        The propability of {word} to appear as defined by the Maximum Likelihod Estimate method.
        :param word:
        :return:
        '''
        return float(self.wordAppearanceCounter[word]) / self.length

    def pLidstoneByFreq(self, lamda , freq):
        return (freq + lamda) / (self.length + self.vocabularySize * lamda)
