import os, sys

""" 
Renames the filenames within the same directory to be Unix friendly
(1) Changes spaces to hyphens
(2) Makes lowercase (not a Unix requirement, just looks better ;)

Usage:
python rename.py
"""

def rename_mails(mailType):
    inputPath =  os.getcwd() + "/preprocessed_input_data/" + mailType + "/"
    outputPath = os.getcwd() + "/data/input/" + mailType + "/"

    filenames = os.listdir(inputPath)

    i = 1
    for filename in filenames:
        newName = outputPath + str(i) + ".eml"
        os.rename(outputPath + filename, newName)
        i = i +1


"""------------------------"""
#Program Execution
"""------------------------"""
if __name__ == '__main__':
    
    print("Renaming ham mails...")

    mailType = "ham"
    rename_mails(mailType)

    print("Ham mails are renamed!")

    time.sleep(1)

    print("Renaming spam mails")

    mailType = "phishing"
    rename_mails(mailType)

    print("Phishing mails are renamed!")