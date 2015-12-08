from collections import Counter
import math
from WordSet import WordSet
from HeldOutWordSet import HeldOutWordSet


def sample(range, strToPrint):
    print strToPrint
    print range

    for boaz in range(4):
        print boaz


def generateOutputFile(developmentSetFilename, testSetFilename, inputWord, outputFilename):
    print 1
    vocabularySize = 300000
    ouptFilename = 'C:\Git\Probablity2\output.txt'
    file = open(ouptFilename, "w+")
    file.write("Output1: " + developmentSetFilename + "\n")
    file.write("Output2: " + testSetFilename + "\n")
    file.write("Output3: " + inputWord + "\n")
    file.write("Output4: " + outputFilename + "\n")
    file.write("Output5: " + str(vocabularySize) + "\n")
    file.write("Output6: " + str(calcPuniform(vocabularySize)) + "\n")

    # Lidstone model
    words = eventsInFile(developmentSetFilename)
    cuttingIndex = int(round(len(words) * 0.9))
    trainingSet, validationSet = words[:cuttingIndex], words[cuttingIndex:]
    trainingWordSet, validationWordSet = WordSet(trainingSet, vocabularySize), WordSet(validationSet, vocabularySize)

    file.write("Output7: " + str(len(words)) + "\n")
    file.write("Output8: " + str(validationWordSet.length) + "\n")
    file.write("Output9: " + str(trainingWordSet.length) + "\n")
    file.write("Output10: " + str(trainingWordSet.distinctLength) + "\n")
    file.write("Output11: " + str(trainingWordSet.countAppearances(inputWord)) + "\n")
    file.write("Output12: " + str(trainingWordSet.pMaximumLikelihoodEstimate(inputWord)) + "\n")
    file.write("Output13: " + str(trainingWordSet.pMaximumLikelihoodEstimate("unseen-word")) + "\n")
    file.write("Output14: " + str(trainingWordSet.pLidstone(inputWord, 0.1)) + "\n")
    file.write("Output15: " + str(trainingWordSet.pLidstone("unseen-word", 0.1)) + "\n")
    file.write("Output16: " + str(lidstonPerplexity(trainingWordSet, validationWordSet, 0.01)) + "\n")
    file.write("Output17: " + str(lidstonPerplexity(trainingWordSet, validationWordSet, 0.1)) + "\n")
    file.write("Output18: " + str(lidstonPerplexity(trainingWordSet, validationWordSet, 1.0)) + "\n")

    minperplexity, minlamda = minimumPerplexityZeroToTwo(trainingWordSet, validationWordSet)

    file.write("Output19: " + str(minlamda) + "\n")
    file.write("Output20: " + str(minperplexity) + "\n")

     # HeldOut model
    cuttingHeldOutIndex = int(round(len(words) * 0.5))
    heldOutTrainingSet, heldOutSet = words[:cuttingHeldOutIndex], words[cuttingHeldOutIndex:]
    heldOutTrainingWordSet, heldOutWordSet = WordSet(heldOutTrainingSet, vocabularySize), WordSet(heldOutSet, vocabularySize)

    heldOut = HeldOutWordSet(heldOutTrainingWordSet, heldOutWordSet)
    file.write("Output21: " + str(len(heldOutTrainingSet)) + "\n")
    file.write("Output22: " + str(len(heldOutSet)) + "\n")
    file.write("Output23: " + str(heldOut.pHeldOut(inputWord)) + "\n")
    file.write("Output24: " + str(heldOut.pHeldOut("unseen-word")) + "\n")

    testWords = eventsInFile(testSetFilename)
    #file.write("Output25: " + str(len(testWords)) + "\n")
    print "saar validate:" +str(heldOut.validateHeldOut(testWords))
    # 26
    # file.write("Output27: " + str(heldOutPerplexity(heldOutSet,trainingSet,vocabularySize,testWords)) + "\n")

    file.close
    print 3

def validateLidstone(testWordSet, lamda):
    allunseenpropability = (testWordSet.vocabularySize - testWordSet.distinctLength) * testWordSet.pLidstone(
        'unseen-word', lamda)
    eventspropabilities = [testWordSet.pLidstone(word, lamda) for word in testWordSet.distinctItems()]

    return sum(eventspropabilities) + allunseenpropability


def minimumPerplexityZeroToTwo(trainingWordSet, validationWordSet):
    lamdagen = lamdaGenerator(0.01, 2, 0.01)
    minlamda = lamdagen.next()
    minperplexity = lidstonPerplexity(trainingWordSet, validationWordSet, minlamda)
    for lamda in lamdagen:
        currperplexity = lidstonPerplexity(trainingWordSet, validationWordSet, lamda)
        if currperplexity < minperplexity:
            minperplexity = currperplexity
            minlamda = lamda

    return minperplexity, minlamda


def lamdaGenerator(start, end, jump):
    current = start;
    while current < end:
        yield current
        current += jump


def lidstonPerplexity(trainingWordSet, validationWordSet, lamda):
    logs = [math.log(trainingWordSet.pLidstone(word, lamda)) * appearances for word, appearances in
            validationWordSet.distinctItems() if True]

    return math.pow(math.e, -1 * sum(logs) / validationWordSet.length)


# iterate each word in testSet and calculates his Pheldout according to the developmentSet:
# [heldOutSet,trainingSet]
def heldOutPerplexity(heldOut, testWorkSet):

    logs = [math.log(heldOut.pHeldOut(word)) * appearances for word, appearances in testWorkSet.distinctItems() if True]
    # logs = [math.log(pHeldOut(heldOutWorkSet,trainingSet,word,vocabolarySize)) for word in testSet]

    return math.pow(math.e, -1 * sum(logs) / testWorkSet.length)


def calcPuniform(vocabolarySize):
    return 1 / float(vocabolarySize)

def eventsInFile(developmentSetFilename):
    with open(developmentSetFilename, "r") as f:
        words = [word for line in f for word in line.split()]
        return words


def main():
    generateOutputFile("develop.txt", "test.txt",
                       "the", "saar")


if __name__ == '__main__':
    main()
