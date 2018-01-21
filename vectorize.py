
import os
path = 'data/input/ham/'
arr = os.listdir(path)

# read dict.txt to d
d = {}
with open("data/output/dict.txt") as f:
    for line in f:
       (key, val) = line.split()
       d[key.lower()] = round(float(val),3)

# sort dictionary by weight
import operator
sorted_x = sorted(d.items(), key=operator.itemgetter(1))
# take the first 100
v = sorted_x[0:101]


# read a file and split into 'words'
import string 
vecfile = open('vectors.txt', 'a')
for f in arr:
	try:
		file = open(path + f, 'r')
		words = list(file.read().lower().split())
		words = [word.strip(string.punctuation) for word in words]
	except UnicodeDecodeError:
		continue

	vecfile.write('%s ' % f)
	# create vector with weights multiplied by the occurrence count in the words list
	for w in v:
	    vecfile.write('%s ' % str(round(w[1]*words.count(w[0]),3)))
	vecfile.write('ham\n')
