# Author Onur GOKER
# Created in 31/12/2017

import os, re, string, node, nltk, math, sys
from email import message_from_file
from nltk import word_tokenize
from nltk.corpus import stopwords

attachmentPath = "./attachments"
emailPath = "mails/phishing/"
mailCount = 300

"""""------------------------"""
# Node class
"""------------------------"""""

class Node(object):
    
    def __init__(self, data=None, next_node=None):
        self.data = data
        self.next_node = next_node

    def get_data(self):
        return self.data

    def get_next(self):
        return self.next_node

    def set_next(self, new_next):
        self.next_node = new_next

    def removeNode(self,value):
        prev = None
        curr = self.head
        while curr:
            if curr.getData() == value:
                if prev:
                    prev.setNextNode(curr.getNextNode())
                else:
                    self.head = curr.getNextNode()
                return True
                    
            prev = curr
            curr = curr.getNextNode()
            
        return False

"""------------------------"""
# Linked List class
"""------------------------"""

class LinkedList(object):
    def __init__(self, head=None):
        self.head = head

    def __iter__(self):
        # Remember, self is our UnorderedList.
        # In order to get to the first Node, we must do
        current = self.head
        # and then, until we have reached the end:
        while current is not None:
            yield current
            # in order to get from one Node to the next one:
            current = current.get_next()

    def insert(self, data):
        new_node = Node(data)
        new_node.set_next(self.head)
        self.head = new_node

    def size(self):
        current = self.head
        count = 0
        while current:
            count = count + 1
            current = current.get_next()
        return count

    def search(self, data):
        count = 0
        current = self.head
        found = False
        while current and found is False:
            if current.get_data() == data:
                count = count + 1
            else:
                current = current.get_next()
        if current is None:
             return 0
        
        return count

    def delete(self, data):
        current = self.head
        previous = None
        found = False
        while current and found is False:
            if current.get_data() == data:
                found = True
            else:
                previous = current
                current = current.get_next()
        if current is None:
            raise ValueError("Data not in list")
        if previous is None:
            self.head = current.get_next()
        else:
            previous.set_next(current.get_next())

    def printList(self):
        temp = self.head
        while(temp):
            print (temp.data + " \n"),
            temp = temp.next_node

    def removeDuplicates(self):
        current = self.head
        next_next = ""

        if current is None:
            return
    
        while current.get_next() is not None:
            if current.get_data() == current.get_next().get_data():
                next_next = current.get_next().get_next()
                removeNode(current.get_next())
                current.get_next().setData(next_next) 
            else:
                current = current.get_next()

"""------------------------"""
#Functions
"""------------------------"""
def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext

def isLineEmpty(line):
    return len(line.strip()) == 0

def mail_exists (f):
    """Checks whether eml file exists or not."""
    return os.path.exists(os.path.join("./", f))

def file_exists (f):
    """Checks whether extracted file was extracted before."""
    return os.path.exists(os.path.join(attachmentPath, f))

def extract (msgfile, key):
    """Extracts all data from e-mail, including From, To, etc., and returns it as a dictionary.
    msgfile -- A file-like readable object
    key     -- Some ID string for that particular Message. Can be a file name or anything.
    Returns dict()
    Keys: from, to, subject, date, text, html, parts[, files]
    Key files will be present only when message contained binary files.
    For more see __doc__ for pullout() and caption() functions.
    """
    m = message_from_file(msgfile)
    #Subject = caption(m)
    Text, Html, Files, Parts = pullout(m, key)
    Text = Text.strip(); Html = Html.strip()
    msg = Text
    return msg

def caption (origin):
    """Extracts: To, From, Subject and Date from email.Message() or mailbox.Message()
    origin -- Message() object
    Returns tuple(From, To, Subject, Date)
    If message doesn't contain one/more of them, the empty strings will be returned.
    """

    if origin.has_key("subject"): Subject = origin["subject"].strip()
    return Subject

def save_file (fn, cont):
    """Saves cont to a file fn"""
    file = open(os.path.join(attachmentPath, fn), "w")
    file.write(cont)
    file.close()

def pullout (m, key):
    """Extracts content from an e-mail message.
    This works for multipart and nested multipart messages too.
    m   -- email.Message() or mailbox.Message()
    key -- Initial message ID (some string)
    Returns tuple(Text, Html, Files, Parts)
    Text  -- All text from all parts.
    Html  -- All HTMLs from all parts
    Files -- Dictionary mapping extracted file to message ID it belongs to.
    Parts -- Number of parts in original message.
    """
    Html = ""
    Text = ""
    Files = {}
    Parts = 0
    if not m.is_multipart():
        if m.get_filename(): # It's an attachment
            fn = m.get_filename()
            cfn = construct_name(key, fn)
            Files[fn] = (cfn, None)
            if file_exists(cfn): return Text, Html, Files, 1
            save_file(cfn, m.get_payload(decode=True))
            return Text, Html, Files, 1
        # Not an attachment!
        # See where this belongs. Text, Html or some other data:
        cp = m.get_content_type()
        if cp=="text/plain": Text += m.get_payload(decode=True)
        elif cp=="text/html": Html += m.get_payload(decode=True)
        else:
            # Something else!
            # Extract a message ID and a file name if there is one:
            # This is some packed file and name is contained in content-type header
            # instead of content-disposition header explicitly
            cp = m.get("content-type")
            try: id = disgra(m.get("content-id"))
            except: id = None
            # Find file name:
            o = cp.find("name=")
            if o==-1: return Text, Html, Files, 1
            ox = cp.find(";", o)
            if ox==-1: ox = None
            o += 5; fn = cp[o:ox]
            fn = disqo(fn)
            cfn = construct_name(key, fn)
            Files[fn] = (cfn, id)
            if file_exists(cfn): return Text, Html, Files, 1
            save_file(cfn, m.get_payload(decode=True))
        return Text, Html, Files, 1
    # This IS a multipart message.
    # So, we iterate over it and call pullout() recursively for each part.
    y = 0
    while 1:
        # If we cannot get the payload, it means we hit the end:
        try:
            pl = m.get_payload(y)
        except: break
        # pl is a new Message object which goes back to pullout
        t, h, f, p = pullout(pl, key)
        Text += t; Html += h; Files.update(f); Parts += p
        y += 1
    return Text, Html, Files, Parts

def construct_name (id, fn):
    """Constructs a file name out of messages ID and packed file name"""
    id = id.split(".")
    id = id[0]+id[1]
    return id+"."+fn

def disqo (s):
    """Removes double or single quotations."""
    s = s.strip()
    if s.startswith("'") and s.endswith("'"): return s[1:-1]
    if s.startswith('"') and s.endswith('"'): return s[1:-1]
    return s

def disgra (s):
    """Removes < and > from HTML-like tag or e-mail address or e-mail ID."""
    s = s.strip()
    if s.startswith("<") and s.endswith(">"): return s[1:-1]
    return s



"""------------------------"""
#Program Execution
"""------------------------"""

if __name__ == '__main__':
    stopWords = set(stopwords.words('english'))
    numbers = ["0","1","2","3","4","5","6","7","8","9"]
    word_document = ""

    #return and count all words
    for i in range(1,mailCount+1):
        fileName = emailPath + str(i) + ".eml" 

        if(mail_exists(fileName)):
            fileOpen = open(fileName) #file open
            fileRead = fileOpen.read()
            fileRead = cleanhtml(fileRead)
            wordList = word_tokenize(fileRead) #tokenize

            for word in wordList:
                word = word.strip()
                if word not in stopWords and not isLineEmpty(word) and word not in numbers and word is not None:
                    word = re.sub('[^A-Za-z0-9]+', '', word)
                    word_document = word_document + " " + word

            fileOpen.close()