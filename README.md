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

