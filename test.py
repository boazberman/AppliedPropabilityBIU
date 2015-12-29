from collections import Counter
import math
import sys

from pip.utils import outdated

from WordSet import WordSet
from HeldOutWordSet import HeldOutWordSet
from WordSet import WordSet


def generateOutputFile(developmentSetFilename, testSetFilename, inputWord, outputFilename):
    print "Started with:"
    print "\tDevelopment set filename: %s" % developmentSetFilename
    print "\tTest set filename: %s" % testSetFilename
    print "\tInput word: %s" % inputWord
    print "\tOutput filename: %s" % outputFilename

    vocabularySize = 300000

    file = open(outputFilename, "w+")
    file.write("#Students:\tSaar Arbel (315681775), Boaz Berman (311504401)\n")
    file.write("Output1: " + developmentSetFilename + "\n")
    file.write("Output2: " + testSetFilename + "\n")
    file.write("Output3: " + inputWord + "\n")
    file.write("Output4: " + outputFilename + "\n")
    file.write("Output5: " + str(vocabularySize) + "\n")
    file.write("Output6: " + str(calcPuniform(vocabularySize)) + "\n")

    # Lidstone model
    with open(developmentSetFilename, 'rb') as input_file:
        input_file_data = input_file.read()
    words = parse_file_data(input_file_data)

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

    print "Lidstone validation: " + str(validateLidstone(validationWordSet, 0.1))

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
    heldOutTrainingWordSet, heldOutWordSet = WordSet(heldOutTrainingSet, vocabularySize), WordSet(heldOutSet,
                                                                                                  vocabularySize)
    heldOut = HeldOutWordSet(heldOutTrainingWordSet, heldOutWordSet)
    file.write("Output21: " + str(len(heldOutTrainingSet)) + "\n")
    file.write("Output22: " + str(len(heldOutSet)) + "\n")
    file.write("Output23: " + str(heldOut.pHeldOut(inputWord)) + "\n")
    file.write("Output24: " + str(heldOut.pHeldOut("unseen-word")) + "\n")
    print "Held Out validation: " + str(heldOut.validateHeldOut(heldOutTrainingWordSet))

    with open(testSetFilename, 'rb') as input_file_test:
        input_file_data_test = input_file_test.read()
    testWords = parse_file_data(input_file_data_test)

    testTrainingSet = WordSet(testWords, vocabularySize)
    file.write("Output25: " + str(len(testWords)) + "\n")
    # find out if the perplexity should be done on testTrainingSet with the old trainingWordSet that we
    # calculate with him the minLamda
    lidstonPerplexityVar = lidstonPerplexity(trainingWordSet, testTrainingSet, minlamda)
    heldOutPerplexityVar = heldOutPerplexity(heldOut, testTrainingSet)
    file.write("Output26: " + str(lidstonPerplexityVar) + "\n")
    file.write("Output27: " + str(heldOutPerplexityVar) + "\n")
    file.write("Output28: " + ('L' if lidstonPerplexityVar < heldOutPerplexityVar else 'H') + "\n")
    file.write("Output29:")
    file.write(printTable(heldOut, trainingWordSet , minlamda))

    file.close

    print "Ended"


def validateLidstone(testWordSet, lamda):
    '''
    A validation for the Lidstone discount. 1.0 is the wanted value.
    :param testWordSet: The list of words to validate the Lidstone discount on. Instance of {WordSet}.
    :param lamda: To test the discount with.
    :return: the total of propabilities
    '''
    allunseenpropability = (testWordSet.vocabularySize - testWordSet.distinctLength) * testWordSet.pLidstone(
        'unseen-word', lamda)
    eventspropabilities = [testWordSet.pLidstone(word, lamda) for word, amount in testWordSet.distinctItems()]

    return sum(eventspropabilities) + allunseenpropability


def minimumPerplexityZeroToTwo(trainingWordSet, validationWordSet):
    '''
    Calculating the perplexity of each of the lambdas in (0, 2] with jumps of 0.01. Then return the minimum perplexity
     from between the perplexity caculated and its matching lambda.
    :param trainingWordSet: Instance of {WordSet}.
    :param validationWordSet: Instance of {WordSet}.
    :return: min-perplexity, min-lambda
    '''
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
    '''
    An iterable generating a lambda from [{start}, {end}] with jumps of {jump}.
    :param start: A positive rational number.
    :param end: A positive rational number.
    :param jump: A positive rational number.
    :return: lambda
    '''
    current = start
    while current < end:
        yield current
        current += jump


def lidstonPerplexity(trainingWordSet, validationWordSet, lamda):
    '''
    Iterate each distinct word in {testSet} and sum his Lidstone discount's propability with the given {lamda lambda}
     multiplied by the times it appeared.
    :param trainingWordSet: Instance of {WordSet}.
    :param validationWordSet: Instance of {WordSet}.
    :param lamda: A rational positive number.
    :return:
    '''
    logs = [math.log(trainingWordSet.pLidstone(word, lamda)) * appearances for word, appearances in
            validationWordSet.distinctItems() if True]

    return math.pow(math.e, -1 * sum(logs) / validationWordSet.length)

def heldOutPerplexity(heldOut, testWorkSet):
    '''
    Iterate each distinct word in {testSet} and calculates his propability with Held Out discount.
    :param heldOut: Instance of {HeldOutWordSet}.
    :param testWorkSet: Instance of {WordSet}.
    :return:
    '''
    logs = [math.log(heldOut.pHeldOut(word)) * appearances for word, appearances in testWorkSet.distinctItems() if True]

    return math.pow(math.e, -1 * sum(logs) / testWorkSet.length)


def calcPuniform(vocabolarySize):
    '''
    :param vocabolarySize: A natural number.
    :return: The uniform propability of a word giving the vocabulary size.
    '''
    return 1 / float(vocabolarySize)


def parse_file_data(file_data):
    '''
    parses the input file to a sequence (list) of words
    @param file_data: the input file text
    @return: a list of the files words
    '''
    # starting from the 3rd line, every 4th line is an article
    file_lines = file_data.splitlines()[2::4]
    # every article ends with a trailing space,
    # so we get a string with all the words separated by one space
    words = ''.join(file_lines)
    # remove the last trailing space
    words = words[:-1]
    # create a list of all the words
    return words.split(' ')

def printTable(heldOutModel , lidatonModel, minLamda):
    outputLine = '\n'
    for frequncy in xrange(10):
        outputLine += str(frequncy) + '\t' + str(round(lidatonModel.pLidstoneByFreq(minLamda,frequncy) * lidatonModel.length , 5))
        outputLine += '\t' + str(round(heldOutModel.pHeldOutByFreq(frequncy)  * heldOutModel.trainingWordSet.length , 5))
        outputLine += '\t' + str(heldOutModel.nr[frequncy]) + '\t' + str(heldOutModel.tr[frequncy])
        outputLine += '\n'
    return outputLine

def main():
    # Validate the inputs.
    if len(sys.argv) != 5:
        print "How to use: " + sys.argv[
            0] + " < development_set_filename > < test_set_filename > < INPUT WORD > < output_filename >"
        sys.exit(1)

    development_file_path = sys.argv[1]
    test_file_path = sys.argv[2]
    input_word = sys.argv[3]
    output_file_path = sys.argv[4]

    generateOutputFile(development_file_path, test_file_path, input_word, output_file_path)

if __name__ == '__main__':
    main()