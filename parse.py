from __future__ import division
import os, re, string, node, nltk, math, sys
import custom_methods, prm
import email
from nltk.corpus import stopwords
from email import message_from_file
from nltk import word_tokenize

"""------------------------"""
#Program Execution
"""------------------------"""
inputType = outputType = inputPath = outputPath = ""
if len(sys.argv) > 2:
    for p in sys.argv:
        if inputType == "input":
            inputPath = p
            inputType = ""
        if p == "-input":
            inputType = "input"
        if outputType == "output":
            outputPath = p 
            outputType = ""
        if p == "-output":
            outputType = "output"
else:
    print "Please use this program with parameter!"

stopWords = set(stopwords.words(prm.language))
all_documents = []

if sys.argv[1] != "-input":
    print "Use -input parameter to parse the emails first!"
    sys.exit()

if __name__ == '__main__':
    #return and count all words
    for i in range(1,prm.mailCount+1):
        fileName = inputPath + str(i) + ".eml" 
        word_document = ""

        if(custom_methods.mail_exists(fileName)):
            fileOpen = open(fileName) #file open
            fileRead = fileOpen.read()
            body     = custom_methods.get_mail_body(fileRead)
            body     = custom_methods.cleanhtml(body)
            wordList = word_tokenize(body) #tokenize

            for word in wordList:
                word = word.strip()
                if word not in stopWords and not word.isdigit() and word is not custom_methods.isLineEmpty(word) and word not in prm.numbers and word is not None:
                    word = re.sub('[^A-Za-z0-9]+', '', word)

                    if word != '':
                        word_document = word_document + "," + word

            all_documents.append(word_document)
            fileOpen.close()

print all_documents