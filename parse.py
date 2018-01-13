# encoding=utf8  
from __future__ import division
from email.parser import Parser
import os, re, string, node, nltk, math, io
import custom_methods, prm
import email
from email import message_from_file
from nltk import word_tokenize
import sys  

def genarate_clean_mail(inputDir, outputDir, mailType):
    inputPath = inputDir + mailType + '/'
    outputPath = outputDir + mailType + '/'

    mailCount = len(os.listdir(inputPath))
    count = 0
    parser = Parser()

    if not os.path.exists(outputPath):
        os.makedirs(outputPath)

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
    genarate_clean_mail(inputDir, outputDir, "ham")
    genarate_clean_mail(inputDir, outputDir, "phishing")
