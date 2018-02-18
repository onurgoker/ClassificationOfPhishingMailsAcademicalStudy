import os, sys, time
import rename
from shutil import copyfile

def rename_mails(mailType):
    inputPath =  os.getcwd() + "/preprocessed_input_data/" + mailType + "/"
    outputPath = os.getcwd() + "/data/input/" + mailType + "/"

    filenames = os.listdir(inputPath)
    i = 1

    for filename in filenames:
        newName = outputPath + str(i) + ".txt"
        copyfile(inputPath + filename, newName)
        i = i +1

"""------------------------"""
#Program Execution
"""------------------------"""
if __name__ == '__main__':
    
    print("Renaming ham mails...")

    mailType = "ham"
    rename.rename_mails(mailType)

    print("Ham mails are renamed!")

    time.sleep(1)

    print("Renaming spam mails")

    mailType = "phishing"
    rename.rename_mails(mailType)

    print("Phishing mails are renamed!")