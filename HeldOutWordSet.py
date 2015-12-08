from collections import Counter


class HeldOutWordSet:
    def __init__(self, heldOutWordSet, trainingWordSet):
        self.heldOutWordSet = heldOutWordSet
        self.trainingWordSet = trainingWordSet
        self.tr, self.nr = self.calctTRandNR()

    def pHeldOut(self, word):
        return float(self.tr[self.trainingWordSet.wordAppiearanceCounter[word]]) / (
        self.heldOutWordSet.distinctLength * self.nr[self.trainingWordSet.wordAppearanceCounter[word]])

    # calculates nr and tr for a given heldOutSet & trainingSet
    def calctTRandNR(self):
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

    def validateHeldOut(self, trainingSet):
	p = ((self.heldOutWordSet.vocabularySize - len(set(trainingSet))) * self.pHeldOut("unseen-word"))
	prop = [self.pHeldOut(word) for word in set(trainingSet)]

	return sum(prop) + p