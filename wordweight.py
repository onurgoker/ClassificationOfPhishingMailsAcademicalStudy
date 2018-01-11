from nltk.corpus import stopwords
import sys, prm, os, custom_methods, argparse


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
stopWords = set(stopwords.words(prm.language))

#clean stop words

def write_without_stopwords(inputPath, outputPath):
    mailCount = len(os.listdir(inputPath))

    for i in range(1,mailCount+1):
        inputFileName = inputPath + str(i) + ".eml" 

        if(custom_methods.mail_exists(inputFileName)):
            readFile    = open(inputFileName, 'r')
            text        = str(readFile.read())
            read        = custom_methods.remove_stopwords(text)

            writeFile = open(inputFileName, "w+")
            writeFile.write(read) #write without stopwords
            writeFile.close()

if __name__ == '__main__':
    write_without_stopwords(hamInputPath, outputPath)
    write_without_stopwords(phishingInputPath, outputPath)
    