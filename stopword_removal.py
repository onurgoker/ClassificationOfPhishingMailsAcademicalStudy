def write_without_stopwords(inputPath, outputPath):
    mailCount = len(os.listdir(inputPath))

    for i in range(1,mailCount+1):
        inputFileName = inputPath + str(i) + ".eml" 

        if(custom_methods.mail_exists(inputFileName)):
            readFile    = open(inputFileName, 'r')
            text        = str(readFile.read())
            read        = custom_methods.remove_stopwords(text)

            writeFile = open(inputFileName, "w+")
            writeFile.write(read) #write without stopwords
            writeFile.close()