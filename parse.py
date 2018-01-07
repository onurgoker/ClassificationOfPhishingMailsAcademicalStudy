# encoding=utf8  
from __future__ import division
import os, re, string, node, nltk, math, io
import custom_methods, prm
import email
from nltk.corpus import stopwords
from email import message_from_file
from nltk import word_tokenize
import sys  

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
    print("Please use this program with parameter!")

stopWords = set(stopwords.words(prm.language))
count = 0

if sys.argv[1] != "-input":
    print("Use -input parameter to parse the emails first!")
    sys.exit()

if __name__ == '__main__':
    #return and count all words
    for i in range(1,prm.mailCount+1):
        inputFileName = inputPath + str(i) + ".eml" 
        outputFileName = outputPath

        if(custom_methods.mail_exists(inputFileName)):
            readFile = open(inputFileName, 'r')
            body     = str(custom_methods.get_mail_body(readFile.read()))
            wordList = custom_methods.cleanhtml(body)
            wordList = word_tokenize(wordList) #tokenize
            readFile.close() 


        if(custom_methods.mail_exists(outputFileName)):
            writeFile       = open(outputFileName, 'w+')

            for word in wordList:
                if word not in stopWords and not word.isdigit() and word is not custom_methods.isLineEmpty(word) and word not in prm.numbers and word is not None:
                    word = re.sub('[^A-Za-z0-9]+', '', word)
                    writeFile.writelines("fdsf\n")

            writeFile.close()