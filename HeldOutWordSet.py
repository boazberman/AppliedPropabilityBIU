from collections import Counter

class HeldOutWordSet:
    '''
    An object describing an Held Out discount. This kind of build allows using presetted methods on the model.
    '''
    def __init__(self, trainingWordSet, heldOutWordSet):
        '''
        :param trainingWordSet: Instance of {WordSet} that is used as our training set.
        :param heldOutWordSet: Instance of {WordSet} that is used as our Held Out set.
        :return: {HeldOutWordSet}
        '''
        self.trainingWordSet = trainingWordSet
        self.heldOutWordSet = heldOutWordSet
        self.tr, self.nr = self.calctTRandNR()

    def pHeldOut(self, word):
        '''
        The propability of {word} to appear after applying it Held Out discount.
        :param word:
        :return:
        '''
        return float(self.tr[self.trainingWordSet.wordAppearanceCounter[word]]) / (
        self.heldOutWordSet.length * self.nr[self.trainingWordSet.wordAppearanceCounter[word]])

    def calctTRandNR(self):
        '''
        Calculated Tr and Nr:
            Tr is the count of all appearances of words in the Held Out set that appeared r times in the training set.
            Nr is the number of words that appeared r times in the training set.
        :return: Tr, Nr
        '''
        # counts all the words in held-out set and maps it to a list, each item is like : (word : freq)
        heldOutCounter = self.heldOutWordSet.wordAppearanceCounter
        # counts all the words in training set and maps it to a list, each item is like : (word : freq)
        trainingSetCounter = self.trainingWordSet.wordAppearanceCounter
        # holds a list that each item is like: (freq:counts how many words in that freq).
        # it has been calculated with the heldOutSet & trainingSet
        tr = Counter()
        # holds a list that each item is like: (freq:counts how many words in that freq)
        # it has been calculated only with the trainingSet
        nr = Counter()
        for word, count in trainingSetCounter.items():
            # for each word with freq r (in the trainingSet) -> add to tr[r] the freq of word in heldOutSet
            tr[count] += heldOutCounter[word]
            # for each word with freq r (in the trainingSet) -> add
            nr[count] += 1

        # unseen words
        notInTrainingSetWords = set(heldOutCounter.keys()) - set(trainingSetCounter.keys())
        for word in notInTrainingSetWords:
            tr[0] += heldOutCounter[word]

        nr[0] = self.heldOutWordSet.vocabularySize - len(trainingSetCounter.keys())

        return tr, nr

    def validateHeldOut(self, trainingWordSet):
        '''
        A validation for the Held Out. 1.0 is the wanted value.
        :param trainingWordSet: The list of words to validate the Held Out discount on.
        :return: the total of propabilities
        '''
        p = ((self.heldOutWordSet.vocabularySize - trainingWordSet.distinctLength) * self.pHeldOut("unseen-word"))
        prop = [self.pHeldOut(word) for word, amount in trainingWordSet.distinctItems()]

        return sum(prop) + p