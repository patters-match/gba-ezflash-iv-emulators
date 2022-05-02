#!/usr/bin/python

import os, sys, struct
from sys import argv
from stat import *

#typedef struct {
#        char name[32];
#        u32 filesize;
#        u32 flags;
#        u32 spritefollow;
#        u32 reserved;
#} romheader;

emptysave = "\xff" * 65536

def readfile(name):
	try:
		fd = open(name, "rb")
		contents = fd.read()
		fd.close()
	except IOError:
		print "Error reading", name
		sys.exit(1)
	return contents

def writefile(name, contents):
	try:
		fd = open(name, "wb")
		fd.write(contents)
		fd.close()
	except IOError:
		print "Error writing", name
		sys.exit(1)

if __name__ == "__main__":
	if len(argv) != 4:
		print "Usage: %s pocketnes.gba rom romtitle"
		sys.exit(0)
	pocketnes = readfile(argv[1])
	rom = readfile(argv[2])
	rom = rom + "\0" * (len(rom)%4)
	romheader = struct.pack("31scIIII", argv[3], "\0", len(rom), 0, 0, 0)
	outputfilename = os.path.splitext(argv[2])[0] + ".gba"	
	outputsavename = os.path.splitext(argv[2])[0] + ".sav"
	writefile(outputfilename, pocketnes + romheader + rom)
	writefile(outputsavename, emptysave)
