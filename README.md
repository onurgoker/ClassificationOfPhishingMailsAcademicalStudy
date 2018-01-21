# phishing

**parse email messages in ../data/input subdirectories (ham, spam, phishing, ...) and put the clean text messages in ../data/output (stop words and other junk cleaned)**

python parse.py -input data/input/ -output data/output/

**read all ham and spam emails in the directories -ham and -spam, calculate tf.idf average scores for each word in each batch and take the difference of scores and write to -output file in (word, weight) format.**

python wordweight.py -ham data/output/ham/ -phishing data/output/phishing/ -output data/output/dict.txt

**create word vectors with weights for each email file in -ham and -spam directories, and write the vectors to -output file in the format (???).**

python vectorize.py -ham data/output/ham/ -phishing data/output/spam/ -dict data/dict.txt -output data/vectors.txt

-----------
# phishing
Phishing e-mail parser

#execution
run program.py inputpath outputpath
e.g.: python program.py "mails/phishing/" "output.txt"

#parameters
open prm.py file and change the parameters as follow:

language: language for stopword removal
numbers: one digit strings to exclude from word list (0-9)
mailCount: number of mails to be processed (1-300)
