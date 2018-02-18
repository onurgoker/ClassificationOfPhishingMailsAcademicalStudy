def merge_vectors(mailCount):
    arr = []

    with open("output_vectors_" + str(mailCount) + "_ham.csv", "r") as ins:
        for line in ins:
            arr.append(line)


    with open("output_vectors_" + str(mailCount) + "_phishing.csv", "r") as ins:
        for line in ins:
            arr.append(line)

    fileOpen = open("output_vectors_mixed_" + str(mailCount) + ".csv", "w+")

    for line in arr:
        print(line)
        fileOpen.write(line)
