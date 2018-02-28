# encoding=utf8  
from __future__ import division
from email.parser import Parser
import os, re, string, node, nltk, math, io
import custom_methods, prm
import email
from email import message_from_file
from nltk import word_tokenize
import sys, codecs

def genarate_clean_mail(mailCount, inputDir, outputDir, mailType):
    print("Generating " + mailType + " mails...\n")

    inputPath = inputDir + mailType + '/'
    outputPath = outputDir + mailType + '/'

    #mailCount = len(os.listdir(inputPath))
    count = 0
    parser = Parser()

    if not os.path.exists(outputPath):
        os.makedirs(outputPath)

    for i in range(1,mailCount):
        inputFileName = inputPath + str(i) + ".txt" 
        outputFileName = outputPath + str(i) + ".txt"

        if(custom_methods.mail_exists(inputFileName)):
            with codecs.open(inputFileName, "r",encoding='utf-8', errors='ignore') as fdata:
                body        = fdata.read()
                #body        = str(custom_methods.get_mail_body(read))
                body        = custom_methods.cleanhtml(re.sub(r'http\S+', '', body))
            fdata.close()

            writeFile = open(outputFileName, "w+")
            #writeFile.write(title) #write title
            writeFile.write(body) #write title
            writeFile.close()

    print(mailType.upper() + " mails are generated!\n")

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

if sys.argv[1] != "-input":
    print("Use -input parameter to parse the emails first!")
    sys.exit()

if __name__ == '__main__':
    mailCount = input("Enter mail count: ")

    if not mailCount.isdigit():
        print("Enter number!")
        sys.exit()

    mailCount = int(mailCount)

    genarate_clean_mail(mailCount, inputDir, outputDir, "ham")
    genarate_clean_mail(mailCount, inputDir, outputDir, "phishing")
