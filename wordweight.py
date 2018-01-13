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

def generate_output_file(outputPath, mailType):
    outputPath = outputPath.replace('/dict.txt','/' + mailType + '/dict.txt')
    writeFile = open(outputPath, "w+")
    
    for i, blob in enumerate(bloblist):
        res = "Document {}".format(i + 1)
        writeFile.write(res + "\n")
        scores = {word: tfidf(word, blob, bloblist) for word in blob.words}
        sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        for word, score in sorted_words:
            res = word.decode('utf-8') + " " + str(score)

            if len(word) > 1:
                writeFile.write(res + "\n")
    
    writeFile.close()

def order_output_keyword_list_output(outputPath, mailType):
    outputPath = outputPath.replace('/dict.txt','/' + mailType + '/dict.txt')

    with open(outputPath, 'w+') as f:
        words = f.readlines()

        #Strip the words of the newline characters (you may or may not want to do this):
        words = [word.strip() for word in words]

        #sort the list:
        sortedLines = words.sort()
        print(sortedLines)
        sys.exit()
        f.truncate()
        f.write(sortedLines)
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
mailCount = len(os.listdir(hamInputPath))

"""------------------------"""
#Program Execution
"""------------------------"""

if __name__ == '__main__':
    #clean stop words
    #custom_methods.write_without_stopwords(hamInputPath, outputPath, mailCount)
    #custom_methods.write_without_stopwords(phishingInputPath, outputPath, mailCount)

    arrList = []

    #ham output
    for i in range(1,mailCount+1):
        outputFileName = hamInputPath + str(i) + ".eml"

        if(custom_methods.mail_exists(outputFileName)):
            readFile    = open(outputFileName, 'r')
            text        = str(readFile.read())

            arrList.append(text)

    #convert texts to blob text
    bloblist = []
    for i in arrList:
        bloblist.append(tb(i))

    #create unique keyword list and tfid in data/output/{parameter}/output.txt
    generate_output_file(outputPath, 'ham')
    generate_output_file(outputPath, 'phishing')
    print(outputPath)
    sys.exit()

    #sort ham and phishing files alphabetically
    order_output_keyword_list_output(outputPath, 'ham')
    order_output_keyword_list_output(outputPath, 'phishing')
