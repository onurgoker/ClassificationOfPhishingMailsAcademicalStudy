from nltk.corpus import stopwords
from string import punctuation
import re, os, email, sys, xml, time

"""------------------------"""
# Functions
"""------------------------"""


def cleanhtml(raw_html):
    cleanr = "</?[^\W].{0,10}?>"
    return re.sub(cleanr, '', raw_html)


def isLineEmpty(line):
    return len(line.strip()) == 0


def mail_exists(f):
    """Checks whether eml file exists or not."""
    return os.path.exists(os.path.join("./", f))


def word_count(string):
    my_string = string.lower().split()
    my_dict = {}
    for item in my_string:
        if item in my_dict:
            my_dict[item] += 1
        else:
            my_dict[item] = 1

def get_mail_body(fileRead):
    b = email.message_from_string(fileRead)
    body = ""

    if b.is_multipart():
        for part in b.walk():
            ctype = part.get_content_type()
            cdispo = str(part.get('Content-Disposition'))

            # skip any text/plain (txt) attachments
            if ctype == 'text/plain' and 'attachment' not in cdispo:
                body = part.get_payload(decode=False)  # decode
                break
    # not multipart - i.e. plain text, no attachments, keeping fingers crossed
    else:
        body = b.get_payload(decode=False)

    return body


def get_mail_title(fileRead):
    msg = email.message_from_string(fileRead)

    return msg['subject']


def remove_tags(text):
    TAG_RE = re.compile(r'<[^>]+>')
    return TAG_RE.sub('', text)

def remove_nonascii(text):
    ans = ""
    text.lower()
    for x in text:
        if (ord(x) >= 97 or ord(x) <= 122) and (ord(x) < 48 or ord(x) > 57) and ord(x) < 128:
            ans += x
    return ans


def remove_stopwords(text):
    stops = stopwords.words("english")
    text = ' '.join([word for word in text.split() if word not in stops])
    return text


def write_without_stopwords(inputPath):
    print("Starting job: Stopword Removal")
    time.sleep(2)
    mailCount = len(os.listdir(inputPath))
    
    for i in range(1, mailCount):
        print("File: " + str(i))
        inputFileName = inputPath + str(i) + ".eml"

        if(mail_exists(inputFileName)):
            readFile = open(inputFileName, 'r')
            text = str(readFile.read())
            read = remove_stopwords(text)

            writeFile = open(inputFileName, "w+")
            writeFile.write(read)  # write without stopwords
            writeFile.close()

    print("Finishing job: Stopword Removal")


