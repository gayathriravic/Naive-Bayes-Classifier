import collections
from collections import defaultdict
import json
import string
import itertools
import operator
import sys


priorProbabilities = {}
conditionalProbabilities = {}
conditionalProbabilities[''] = {}
setOfClasses = []
wordProb = {}
wordProb[''] = {}
global totalCount

def loadFile():
    file = open(sys.argv[1],'r', encoding="utf-8")
    return file

def priorProbability(file):  #calculate prior probabilities of the class.
    countOfClass = 0
    totalCount=0
    for lines in file:
        totalCount += 1
    file.seek(0)

    for lines in file:
        line = lines.strip("\n").split(" ")
        for i in range(1,3):
            classname = line[i]
            if classname in priorProbabilities:
                    priorProbabilities[classname] += 1
            else:
                    priorProbabilities[classname] = 1

    print("prior" + str(priorProbabilities))
    for classname in priorProbabilities:
        priorProbabilities[classname] /= (totalCount*2)

    #print(priorProbabilities)
    return priorProbabilities

def conditionalProbability(file): #conditioned on the class. P(w|c) for every c
    #{{class{word:probability}}
    setOfClasses = []
    file.seek(0)
    for lines in file:
       #translator = str.maketrans('','',string.punctuation)   #remove punctuations
       translator = str.maketrans(string.punctuation, ' ' * len(string.punctuation))  # map punctuation to space
       lines=lines.translate(translator)
       line = lines.strip("\n").split(" ")
       for i in range (1,3):
           word=line[i]
           setOfClasses.append(word)
    setOfClasses=set(setOfClasses)  #set of classes


    for classname in setOfClasses:
        conditionalProbabilities[classname]={}

    file.seek(0)

    #file = open('train-labeled.txt', 'r', encoding="utf-8" )
    for lines in file:
        for classname in setOfClasses:
            #translator = str.maketrans(string.punctuation, '', string.punctuation)  # remove punctuations
            translator = str.maketrans(string.punctuation, ' ' * len(string.punctuation))  # map punctuation to space
            lines = lines.translate(translator)
            line = lines.strip("\n").split()
            for i in range(3,len(line)):
                    word = line[i].lower()
                    if classname == line[1] or classname == line[2]:
                        if word in conditionalProbabilities[classname]:
                            conditionalProbabilities[classname][word] += 1
                        else:
                            conditionalProbabilities[classname][word] = 1

    uniqueWords = {}
    for classname in setOfClasses:
        for word in conditionalProbabilities[classname]:
            uniqueWords[word] = 1
    listOfUniqueWords = set(uniqueWords)  #list of unique words in the training data
    return conditionalProbabilities, uniqueWords, setOfClasses


def wordProbability(classes , conditional):
   for classname in conditional:
       word = conditional[classname]
       for every_word in word:
           wordProb[every_word]={}

   for classname in conditional:
        word = conditional[classname]
        for every_word in word:
            wordProb[every_word][classname]=word[every_word]

   return wordProb

totalWordCount = {}


def totalWordProb(file):
    file.seek(0)
    for lines in file:
            #translator = str.maketrans(string.punctuation, '', string.punctuation)  # remove punctuations
            translator = str.maketrans(string.punctuation, ' ' * len(string.punctuation))  # map punctuation to space
            lines = lines.translate(translator)
            line = lines.strip("\n").split()
            for i in range(3,len(line)):
                word = line[i]
                if word in totalWordCount:
                    totalWordCount[word]  +=1
                else:
                    totalWordCount[word] =1
    stopWords = {}
    stopWords = dict(sorted(totalWordCount.items(), key=operator.itemgetter(1), reverse=True)[:20])
    return stopWords
    #print(totalWordCount)

def writeToFile(conditionalProbabilities , uniqueWords, prior , wordProb,stopWords):
    combinedProbability = {"conditional" : conditionalProbabilities, "unique" : uniqueWords ,"word" : wordProb , "stop":stopWords, "prior" :prior }
    with open('nbmodel.txt' , 'w') as outfile:
        json.dump(combinedProbability , outfile , indent = 4)


if __name__ == '__main__':

    file = loadFile()
    prior = priorProbability(file)
    conditional , uniqueWords , classes= conditionalProbability(file)
    wordProb = wordProbability(classes , conditional)
    stopWords = totalWordProb(file)
    writeToFile(conditional ,uniqueWords, prior, wordProb,stopWords )
