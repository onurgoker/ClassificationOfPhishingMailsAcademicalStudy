import re,os,email,sys,xml

"""------------------------"""
#Functions
"""------------------------"""
def cleanhtml(raw_html):
    cleanr = "</?[^\W].{0,10}?>"
    return re.sub(cleanr, '', raw_html)

def isLineEmpty(line):
    return len(line.strip()) == 0

def mail_exists (f):
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
    print(my_dict)

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