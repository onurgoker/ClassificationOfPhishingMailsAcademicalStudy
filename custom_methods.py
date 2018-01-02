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