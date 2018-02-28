from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from textblob import TextBlob as tb
import nltk, re, math, sys, prm, os, time, custom_methods, codecs, argparse, collections, string, pandas as pd

def tf(word, blob):
    return float(blob.count(word)) / int(len(blob.split()))

def n_containing(word, bloblist):
    return sum(1 for blob in bloblist if word in blob)

def idf(word, bloblist):
    return math.log(len(bloblist) / (1 + n_containing(word, bloblist)))

def tfidf(word, blob, bloblist):
    return tf(word, blob) * idf(word, bloblist)

def generate_output_file(outputPath, mailType, inputPath):
    print("Starting job: Generating output file...")
    time.sleep(2)
    arrList = []
    mailCount = len(os.listdir(inputPath))

    # ham output
    for i in range(1, mailCount):
        outputFileName = inputPath + str(i) + ".txt"

        if(custom_methods.mail_exists(outputFileName)):
            with codecs.open(outputFileName, "r",encoding='utf-8', errors='ignore') as fdata:
                text = fdata.read()

            arrList.append(text)

    blobListArr = []

    print("Reading Files...")
    count = 1
    for i in arrList:
        print("Generating output file > Reading Files > File: " + str(count))
        count = count + 1

        arrWordList = i.split()
        tempArrWordList = []
        for j in arrWordList:
            j = j.replace("=","")
            j = j.strip(' \t\n\r')
            j = re.sub(r'^https?:\/\/.*[\r\n]*', '', j, flags=re.MULTILINE)
            j = custom_methods.remove_tags(j)

            if custom_methods.remove_nonascii(j) and len(j) < 30 and len(j) > 2 and not j.isdigit():
                tempArrWordList.append(j)

        empty = " "
        tempArrWordList = empty.join(tempArrWordList)
        blobListArr.append(tempArrWordList)
        
    print("End of file read...")

    # convert texts to blob text
    print("Generating blob list")
    bloblist = []
    count = 1
    for i in blobListArr:
        bloblist.append(tb(i))
        print("Generating output file > Generating blob list > File: " + str(count))
        count = count + 1

    outputPath = outputPath.replace('/dict.txt', '/' + mailType + '/dict.txt')
    writeFile = open(outputPath, "w+")

    print("\nCALCULATING TFIDF SCORES\n")
    count = 1
    for i, blob in enumerate(bloblist):
        print("Generating output file > Calculating TFIDF scores > File: " + str(i))

        blob = custom_methods.cleanhtml(str(blob))
        blobList = blob.split()
        scores = {word: tfidf(word, blob, bloblist) for word in blobList}
        sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True)

        for word, score in sorted_words:
            res = word + " " + str(score)

            if len(word) > 1:
                writeFile.write(res + "\n")

    writeFile.close()
    print("Finishing job: Generating output file...")

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

def average_tfid_dictionary(outputPath):
    outputPath = outputPath.replace("input","output")

    with open(outputPath + 'dict.txt') as lines:
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

    f = open(outputPath + 'dict.txt', 'w+')
    f.truncate()
    for key,val in lineArray.items():
        if not key.isdigit():
            f.write(key + " " + str(val) + "\n")
    f.close()

def get_diff_of_vectors(outputPath):
    hamArr = phishingArr = mergeDict = {}

    with open(outputPath.replace("output/","output/ham/")) as hamLines:
        for hamLine in hamLines:
            lineH = hamLine.split()
            hamArr[lineH[0]] = lineH[1]

    with open(outputPath.replace("output/","output/phishing/")) as phishingLines:
        for phishingLine in phishingLines:
            lineP = phishingLine.split()

            if lineP[0] in hamArr: #in both list
                hamValue = hamArr[lineP[0]]
                phishingValue = lineP[1]
                newValue = float(hamValue)-float(phishingValue)
                hamArr[lineP[0]] = newValue

    #filter array
    filterArr = {}
    p = re.compile("^(0[1-9]|1[012])[- /.](0[1-9]|[12][0-9]|3[01])[- /.](19|20)\d\d$")

    for key,val in hamArr.items():
        if float(val) < 1 and float(val) > -1 and not p.match(str(val)):
            filterArr[key] = round(float(val), 4)
    result = dict(zip(filterArr.values(), filterArr.keys()))
    result = collections.OrderedDict(sorted(result.items(), reverse=True))
    #write to file
    with open(outputPath, 'w+') as outFile:
        invalidChars = set(string.punctuation)

        for val,key in result.items():
            #remove punctiations from list
            flag = True
            for punct in invalidChars:
                if punct in key:
                    flag = False 

            if flag:
                #remove prepositions
                tokens = nltk.word_tokenize(key.lower())
                prepCheck = nltk.pos_tag(tokens)
                prepCheckArr = prepCheck[0]
    
                if prepCheckArr[1] != "PRP":
                    #write remaining words as output
                    outFile.write(key.lower() + " " + str(val) + "\n")

    print("done!")

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

    print("Cleaning stop words for ham data...")
    custom_methods.write_without_stopwords(hamInputPath)

    print("Executing ham output files...")
    generate_output_file(outputPath, 'ham', hamInputPath)

    print("Calculating average TFIDF score list for ham data...")
    average_tfid_dictionary(hamInputPath)

    print("Executing ham output word sorting...")
    order_output_keyword_list_output(outputPath, 'ham')

    print("Cleaning stop words for phishing data...")
    custom_methods.write_without_stopwords(phishingInputPath)

    print("Executing phishing output files...")
    generate_output_file(outputPath, 'phishing', phishingInputPath)

    print("Calculating average TFIDF score list for phishing data...")
    average_tfid_dictionary(phishingInputPath)

    print("Executing phishing output word sorting...")
    order_output_keyword_list_output(outputPath, 'phishing')
    
    print("Getting diff of vectors...")
    get_diff_of_vectors(outputPath)
