import re,os

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

def word_count(string):
    my_string = string.lower().split()
    my_dict = {}
    for item in my_string:
        if item in my_dict:
            my_dict[item] += 1
        else:
            my_dict[item] = 1
    print(my_dict)