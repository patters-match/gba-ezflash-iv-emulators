#!/usr/bin/python3

import sys, bz2, base64
from sys import argv

LINE = 100

def readfile(name):
	with open(name, "rb") as fh:
		contents = fh.read()
	return contents

data = readfile(argv[1])
compressed = bz2.compress(data)
string = base64.b64encode(compressed)
for x in range(0, len(string), LINE):
	if x == 0:
		print ("\t ",string[x:x+LINE], "\\")
	elif len(string) - x > LINE:
		print ("\t+",string[x:x+LINE], "\\")
	else:
		print ("\t+",string[x:len(string)])
