#!/usr/bin/python

import os, sys, struct
from sys import argv
from stat import *

SMSID=0x1A534D53

#typedef struct {
#        u32 identifier;
#        u32 filesize;
#        u32 flags;
#        u32 spritefollow;
#        u32 reserved[4];
#        char name[32];
#} romheader;

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
		print "Usage: %s smsadvance.gba rom romtitle"
		sys.exit(0)
	smsadvance = readfile(argv[1])
	rom = readfile(argv[2])
	rom = rom + "\0" * (len(rom)%4)
	romheader = struct.pack("8I31sc", SMSID, len(rom), 0, 0, 0, 0, 0, 0, argv[3], "\0")
	outputfilename = os.path.splitext(argv[2])[0] + ".gba"	
	writefile(outputfilename, smsadvance + romheader + rom)
