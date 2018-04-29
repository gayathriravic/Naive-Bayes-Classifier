import string
import sys
import collections
from collections import defaultdict
import json
import math

def readTestFile():
    file = open('test.txt','r',encoding="utf-8")
    return file

def readTrainedFile():
    data = json.load(open('nbmodel.txt'))
    return data

def getClassNames() :
    class_list=[]
    for classnames in data["prior"]:
        class_list.append(classnames)
    print(class_list)

def writeToFile(res):
    with open("nboutput.txt", 'w', encoding='utf-8') as file:
        file.write(res)

stop = ["a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are", "as", "at", "be", "because", "been", "before", "being", "below", "between", "both", "but", "by", "could", "did", "do", "does", "doing", "down", "during", "each", "few", "for", "from", "further", "had", "has", "have", "having", "he", "he'd", "he'll", "he's", "her", "here", "here's", "hers", "herself", "him", "himself", "his", "how", "how's", "i", "i'd", "i'll", "i'm", "i've", "if", "in", "into", "is", "it", "it's", "its", "itself", "let's", "me", "more", "most", "my", "myself", "nor", "of", "on", "once", "only", "or", "other", "ought", "our", "ours", "ourselves", "out", "over", "own", "same", "she", "she'd", "she'll", "she's", "should", "so", "some", "such", "than", "that", "that's", "the", "their", "theirs", "them", "themselves", "then", "there", "there's", "these", "they", "they'd", "they'll", "they're", "they've", "this", "those", "through", "to", "too", "under", "until", "up", "very", "was", "we", "we'd", "we'll", "we're", "we've", "were", "what", "what's", "when", "when's", "where", "where's", "which", "while", "who", "who's", "whom", "why", "why's", "with", "would", "you", "you'd", "you'll", "you're", "you've", "your", "yours", "yourself", "yourselves"]


def calculate(testFile,data) :
    testFile.seek(0)
    result =""
    for lines in testFile :
        #wordProbability = 0
        #maxProbability = -1
        translator = str.maketrans(string.punctuation, ' ' * len(string.punctuation)) # map punctuation to space.
        lines = lines.translate(translator)
        line = lines.strip("\n").split(" ")
        identifier= line[0]  #unique identifier for that sentence
        #positive/negative and true/fake
        positiveClass = 0
        negativeClass = 0
        trueClass =0
        fakeClass = 0
        
        for i in range(1, len(line)):   # for every word in the sentence.
                word = line[i].lower()
                if word in data["stop"]:
                    continue
                if word not in data["word"]:   # skip unknown words
                    continue
                if word not in data["stop"]:
                    if "Pos" not in data["word"][word]:
                        positiveClass +=math.log(float(1 / (sum(data["conditional"]["Pos"].values()) + len(data["unique"])))) # smoothing
                    else:
                        positiveClass += math.log(float((data["word"][word]["Pos"]+1)/ (sum(data["conditional"]["Pos"].values()) + len(data["unique"]))))

                    if "Neg" not in data["word"][word]:
                        negativeClass += math.log(float(1 / (sum(data["conditional"]["Neg"].values()) + len(data["unique"]))))  # smoothing
                    else:
                        negativeClass += math.log(float((data["word"][word]["Neg"]+1) / (sum(data["conditional"]["Neg"].values()) + len(data["unique"]))))

                    if "Fake" not in data["word"][word]:
                        fakeClass += math.log(float(1 / (sum(data["conditional"]["Fake"].values()) + len(data["unique"])))) # smoothing
                    else:
                        fakeClass += math.log(float((data["word"][word]["Fake"]+1) / (sum(data["conditional"]["Fake"].values()) + len(data["unique"]))))

                    if "True" not in data["word"][word]:
                        trueClass += math.log(float(1 / (sum(data["conditional"]["True"].values()) + len(data["unique"])))) # smoothing
                    else:
                        trueClass += math.log(float((data["word"][word]["True"]+1 )/ (sum(data["conditional"]["True"].values()) + len(data["unique"]))))

        trueClass += math.log(data["prior"]["True"])
        fakeClass += math.log(data["prior"]["Fake"])
        positiveClass += math.log(data["prior"]["Pos"])
        negativeClass += math.log(data["prior"]["Neg"])
        if trueClass > fakeClass :
            maxClass1 = trueClass
            label1 = "True"
        else :
            maxClass1 = fakeClass
            label1 = "Fake"
        if positiveClass > negativeClass :
            maxClass2 = positiveClass
            label2 = "Pos"
        else:
            maxClass2 = negativeClass
            label2 = "Neg"
        result += identifier +" " + label1 + " "+ label2 + "\n"

    writeToFile(result)


if __name__ == '__main__':
    testFile = readTestFile()
    data = readTrainedFile()
    getClassNames()
    calculate(testFile, data)
