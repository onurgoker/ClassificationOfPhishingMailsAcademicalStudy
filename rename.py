import os, sys

""" 
Renames the filenames within the same directory to be Unix friendly
(1) Changes spaces to hyphens
(2) Makes lowercase (not a Unix requirement, just looks better ;)

Usage:
python rename.py
"""
mailType = "ham"
path =  os.getcwd() + "/data/input/" + mailType + "/"

filenames = os.listdir(path)

i = 1
for filename in filenames:
    newName = path + str(i) + ".eml"
    os.rename(path + filename, newName)
    i = i +1
