from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from textblob import TextBlob as tb
import math, sys, prm, os, custom_methods, argparse, pandas as pd

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
    #ham output
    for i in range(1, mailCount + 1):
        outputFileName = inputPath + str(i) + ".eml"

        if(custom_methods.mail_exists(outputFileName)):
            readFile = open(outputFileName, 'r')
            text = str(readFile.read())

            arrList.append(text)

    #convert texts to blob text
    bloblist = []
    for i in arrList:
        bloblist.append(tb(i))

    outputPath = outputPath.replace('/dict.txt','/' + mailType + '/dict.txt')
    writeFile = open(outputPath, "w+")
    
    for i, blob in enumerate(bloblist):
        #res = "Document {}".format(i + 1)
        #writeFile.write(res + "\n")
        scores = {word: tfidf(word.decode('utf-8'), blob, bloblist) for word in blob.words}
        sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        for word, score in sorted_words:
            res = word.decode('utf-8') + " " + str(score)

            if len(word) > 1:
                writeFile.write(res + "\n")
    
    writeFile.close()

def order_output_keyword_list_output(outputPath, mailType):
    outputPath = outputPath.replace('/dict.txt','/' + mailType + '/dict.txt')

    f = open(outputPath, "r");
    words = f.readlines()

    #Strip the words of the newline characters (you may or may not want to do this):
    words = [word.strip() for word in words]

    #sort the list:
    sortedLines = sorted(words)

    f = open(outputPath, "w+")
    f.truncate()

    for line in sortedLines:
        f.write(line + "\n")

    f.close()

#Define Paths
parser = argparse.ArgumentParser()

parser.add_argument('-ham', dest='ham')
parser.add_argument('-phishing', dest='phishing')
parser.add_argument('-output', dest='output')

results = parser.parse_args()
hamInputPath = results.ham
phishingInputPath = results.phishing
outputPath = results.output
#End of Path Definition

"""------------------------"""
#Program Execution
"""------------------------"""

if __name__ == '__main__':
    print("Please wait...")
    #clean stop words
    #custom_methods.write_without_stopwords(hamInputPath, outputPath, mailCount)
    #custom_methods.write_without_stopwords(phishingInputPath, outputPath, mailCount)

    print("Executing ham output files...")
    generate_output_file(outputPath, 'ham', hamInputPath)

    print("Executing ham output word sorting...")
    order_output_keyword_list_output(outputPath, 'ham')
    
    print("Executing phishing output files...")
    generate_output_file(outputPath, 'phishing', phishingInputPath)

    print("Executing phishing output word sorting...")
    order_output_keyword_list_output(outputPath, 'phishing')

    #TODO: take average of each word's TFIDF
