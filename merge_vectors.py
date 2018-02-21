import os, errno

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

    mailName = str(mailCount)

    if mailName.count("0") == 3:
        mailName = mailName.replace("000","k")
    elif mailName.count("0") == 4:
        mailName = mailName.replace("0000","0k")

    directory = "output/vector/w2v/"

    if not os.path.exists(directory):
        os.makedirs(directory)

    fileOpen = open(directory + "v" + mailName + ".txt", 'w+')

    for line in arr:
        fileOpen.write(line)

    print("Deleting ham and phishing vectors...")
    
    os.remove(hamMailPath)
    os.remove(phishingMailPath)