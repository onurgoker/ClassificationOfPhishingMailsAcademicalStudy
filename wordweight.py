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

if __name__ == '__main__':
    #clean stop words
    custom_methods.write_without_stopwords(hamInputPath, outputPath)
    custom_methods.write_without_stopwords(phishingInputPath, outputPath)
