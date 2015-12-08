from collections import Counter
import math
from WordSet import WordSet

def sample(range , strToPrint):
	print strToPrint
	print range

	for boaz in range(4):
		print boaz


def generateOutputFile(developmentSetFilename, testSetFilename, inputWord, outputFilename):
	print 1
	vocabularySize = 300000
	ouptFilename = 'D:\Git\AppliedPropabilityBIU\output.txt'
	file = open(ouptFilename,"w+")
	file.write("Output1: " + developmentSetFilename + "\n")
	file.write("Output2: " + testSetFilename + "\n")
	file.write("Output3: " + inputWord + "\n")
	file.write("Output4: " + outputFilename + "\n")
	file.write("Output5: " + str(vocabularySize) + "\n")
	file.write("Output6: " + str(calcPuniform(vocabularySize)) + "\n")

	# Lidstone model
	words = eventsInFile(developmentSetFilename)
	cuttingIndex = int(round(len(words)*0.9))
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
	file.write("Output16: " + str(perplexity(trainingWordSet, validationWordSet, 0.01)) + "\n")
	file.write("Output17: " + str(perplexity(trainingWordSet, validationWordSet, 0.1)) + "\n")
	file.write("Output18: " + str(perplexity(trainingWordSet, validationWordSet, 1.0)) + "\n")

	minperplexity, minlamda = minimumPerplexityZeroToTwo(trainingWordSet, validationWordSet)

	file.write("Output19: " + str(minlamda) + "\n")
	file.write("Output20: " + str(minperplexity) + "\n")


	# HeldOut model
	heldOutTrainingSet = eventsInFile(developmentSetFilename)[:numEventsTrainingSetHeldOut(len(words))]
	heldOutSet = eventsInFile(developmentSetFilename)[numEventsTrainingSetHeldOut(len(words)):]
	file.write("Output21: " + str(len(heldOutTrainingSet)) + "\n")
	file.write("Output22: " + str(len(heldOutSet)) + "\n")


	file.write("Output25: " + str(len(eventsInFile(testSetFilename))) + "\n")
	file.close

	print 3



def validateLidstone(testWordSet, lamda):
	allunseenpropability = (testWordSet.vocabularySize - testWordSet.distinctLength) * testWordSet.pLidstone('unseen-word' , lamda)
	eventspropabilities = [testWordSet.pLidstone(word, lamda) for word in testWordSet.distinctItems()]

	return sum(eventspropabilities) + allunseenpropability

def minimumPerplexityZeroToTwo(trainingWordSet, validationWordSet):
	lamdagen = lamdaGenerator(0.01, 2, 0.01)
	minlamda = lamdagen.next()
	minperplexity = perplexity(trainingWordSet, validationWordSet, minlamda)
	for lamda in lamdagen:
		currperplexity = perplexity(trainingWordSet, validationWordSet, lamda)
		if currperplexity < minperplexity:
			minperplexity = currperplexity
			minlamda = lamda

	return minperplexity, minlamda

def lamdaGenerator(start, end, jump):
	current = start;
	while current < end:
		yield current
		current += jump

def perplexity(trainingWordSet , validationWordSet, lamda):
	logs = [math.log(trainingWordSet.pLidstone(word, lamda))*appearances for word, appearances in validationWordSet.distinctItems() if True]

	return math.pow(math.e, -1*sum(logs)/validationWordSet.length)

def calcPuniform(vocabolarySize):
	return 1/float(vocabolarySize)

def numEventsTrainingSetHeldOut(numberOfEvents):
	return int(round(numberOfEvents*0.5))

def eventsInFile(developmentSetFilename):
	with open(developmentSetFilename,"r") as f:
		words = [word for line in f for word in line.split()]
		return words


def main():
	generateOutputFile("develop.txt","test.txt",
		"the","saar")

if __name__ == '__main__':
	main()