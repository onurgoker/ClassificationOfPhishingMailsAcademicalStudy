from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from textblob import TextBlob as tb
import math, sys, prm, os, time, custom_methods, argparse, pandas as pd

reload(sys)
sys.setdefaultencoding('utf8')


def tf(word, blob):
    return float(blob.words.count(word)) / int(len(blob.words))


def n_containing(word, bloblist):
    return sum(1 for blob in bloblist if word in blob)


def idf(word, bloblist):
    return math.log(len(bloblist) / (1 + n_containing(word, bloblist)))


def tfidf(word, blob, bloblist):
    return tf(word, blob) * idf(word, bloblist)


def generate_output_file(outputPath, mailType, inputPath):
    arrList = []
    mailCount = len(os.listdir(inputPath))
    # ham output
    for i in range(1, mailCount + 1):
        outputFileName = inputPath + str(i) + ".eml"

        if(custom_methods.mail_exists(outputFileName)):
            readFile = open(outputFileName, 'r')
            text = str(readFile.read())

            arrList.append(text)

    # convert texts to blob text
    bloblist = []
    for i in arrList:
        bloblist.append(tb(i))

    outputPath = outputPath.replace('/dict.txt', '/' + mailType + '/dict.txt')
    writeFile = open(outputPath, "w+")

    for i, blob in enumerate(bloblist):
        #res = "Document {}".format(i + 1)
        #writeFile.write(res + "\n")
        scores = {word: tfidf(word, blob, bloblist) for word in blob.words}
        sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True)

        for word, score in sorted_words:
            res = word.decode('utf-8') + " " + str(score)

            if len(word) > 1:
                writeFile.write(res + "\n")

    writeFile.close()
    sys.exit()


def order_output_keyword_list_output(outputPath, mailType):
    outputPath = outputPath.replace('/dict.txt', '/' + mailType + '/dict.txt')

    f = open(outputPath, "r")
    words = f.readlines()

    # Strip the words of the newline characters (you may or may not want to do this):
    words = [word.strip() for word in words]

    # sort the list:
    sortedLines = sorted(words)

    f = open(outputPath, "w+")
    f.truncate()

    for line in sortedLines:
        f.write(line + "\n")

    f.close()

def average_tfid_dictionary(inputPath):
    with open(inputPath + 'dict.txt') as lines:
        lineArray = {}
        for line in lines:
            rowArray = line.split()
            if rowArray[0] in lineArray:
                lineArray[rowArray[0]] = lineArray[rowArray[0]] + " " + rowArray[1]
            else:
                lineArray[rowArray[0]] = rowArray[1]

    for key,val in lineArray.items():
        if " " in val:
            valArr = val.split()
            count = len(valArr)
            sum = 0

            for i in valArr:
                sum = sum + float(i)

            lineArray[key] = float(sum/count)

    f = open(inputPath + 'dict.txt', 'w+')
    f.truncate()
    for key,val in lineArray.items():
        if not key.isdigit():
            f.write(key + " " + str(val) + "\n")
    f.close()

# Define Paths
parser = argparse.ArgumentParser()

parser.add_argument('-ham', dest='ham')
parser.add_argument('-phishing', dest='phishing')
parser.add_argument('-output', dest='output')

results = parser.parse_args()
hamInputPath = results.ham
phishingInputPath = results.phishing
outputPath = results.output
# End of Path Definition

"""------------------------"""
# Program Execution
"""------------------------"""

if __name__ == '__main__':
    print("Please wait...")
    time.sleep(2)
    
    # print("Cleaning stop words for ham data...")
    # custom_methods.write_without_stopwords(hamInputPath)

    # print("Executing ham output files...")
    # generate_output_file(outputPath, 'ham', hamInputPath)

    # print("Calculating average TFIDF score list for ham data...")
    # average_tfid_dictionary(hamInputPath)

    # print("Executing ham output word sorting...")
    # order_output_keyword_list_output(outputPath, 'ham')

    # print("Cleaning stop words for phishing data...")
    # custom_methods.write_without_stopwords(phishingInputPath)

    print("Executing phishing output files...")
    generate_output_file(outputPath, 'phishing', phishingInputPath)

    print("Calculating average TFIDF score list for phishing data...")
    average_tfid_dictionary(phishingInputPath)

    print("Executing phishing output word sorting...")
    order_output_keyword_list_output(outputPath, 'phishing')