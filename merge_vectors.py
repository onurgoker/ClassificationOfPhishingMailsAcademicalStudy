import os

def merge_vectors(mailCount):
    print("Merging ham and phishing vectors...")
    arr = []
    hamMailPath = "output_vectors_" + str(mailCount) + "_ham.csv"
    phishingMailPath = "output_vectors_" + str(mailCount) + "_phishing.csv"

    with open(hamMailPath, "r") as ins:
        for line in ins:
            arr.append(line)


    with open(phishingMailPath, "r") as ins:
        for line in ins:
            arr.append(line)

    fileOpen = open("output_vectors_mixed_" + str(mailCount) + ".csv", "w+")

    for line in arr:
        fileOpen.write(line)

    print("Deleting ham and phishing vectors...")
    
    os.remove(hamMailPath)
    os.remove(phishingMailPath)