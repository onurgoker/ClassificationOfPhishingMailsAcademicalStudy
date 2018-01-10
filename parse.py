# encoding=utf8  
from __future__ import division
from email.parser import Parser
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
inputType = outputType = inputDir = outputDir = ""
if len(sys.argv) > 2:
    for p in sys.argv:
        if inputType == "input":
            inputDir = p
            inputType = ""
        if p == "-input":
            inputType = "input"
        if outputType == "output":
            outputDir = p 
            outputType = ""
        if p == "-output":
            outputType = "output"
else:
    print("Please use this program with parameter!")

stopWords = set(stopwords.words(prm.language))

for directory in os.listdir(inputDir):
    inputPath = inputDir + directory + '/'
    outputPath = outputDir + directory + '/'
    mailCount = len(os.listdir(inputPath))
    count = 0
    parser = Parser()

    if not os.path.exists(outputPath):
        os.makedirs(outputPath)

    if sys.argv[1] != "-input":
        print("Use -input parameter to parse the emails first!")
        sys.exit()

    if __name__ == '__main__':
        for i in range(1,mailCount+1):
            inputFileName = inputPath + str(i) + ".eml" 
            outputFileName = outputPath + str(i) + ".eml"

            if(custom_methods.mail_exists(inputFileName)):
                readFile    = open(inputFileName, 'r')
                read        = readFile.read()
                body        = str(custom_methods.get_mail_body(read))
                body        = custom_methods.cleanhtml(re.sub(r'http\S+', '', body))
                title       = str(custom_methods.get_mail_title(read)) + "\n"

                readFile.close()

                writeFile = open(outputFileName, "w+")
                writeFile.write(title) #write title
                writeFile.write(body) #write title
                writeFile.close()

            """
                #wordList = custom_methods.cleanhtml(body)
                #wordList = word_tokenize(wordList) #tokenize

            #print the words
            if(custom_methods.mail_exists(outputFileName)):
                with open(outputFileName, 'a') as the_file:
                    for word in wordList:
                        word = re.sub('[^A-Za-z0-9]+', '', word)
                        if word and word and not word.isdigit() and word is not custom_methods.isLineEmpty(word) and word not in prm.numbers and word is not None and word.strip() != " " and word.strip() != "\n" and len(word) > 2:
                            the_file.write(word + '\n')"""