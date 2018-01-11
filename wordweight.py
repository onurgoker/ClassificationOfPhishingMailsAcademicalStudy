from nltk.corpus import stopwords
import sys, prm, os

"""------------------------"""
#Program Execution
"""------------------------"""
inputType = outputType = inputPath = outputPath = ""
if len(sys.argv) > 2:
    for p in sys.argv:
        if inputType == "input":
            inputPath = p
            inputType = ""
        if p == "-ham" or p == "-spam":
            inputType = "input"
        if outputType == "output":
            outputPath = p 
            outputType = ""
        if p == "-output":
            outputType = "output"
else:
    print("Please use this program with parameter!")

stopWords = set(stopwords.words(prm.language))
mailCount = len(os.listdir(inputPath))
count = 0

parser = Parser()

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

            print(read)