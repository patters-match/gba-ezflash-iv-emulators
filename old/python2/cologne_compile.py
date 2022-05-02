#!/usr/bin/python

import os, sys, struct
from sys import argv
from stat import *

EMUID=0x1A4C4F43

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
	if len(argv) != 5:
		print "Usage: %s cologne.gba bios rom romtitle"
		sys.exit(0)
	cologne = readfile(argv[1])
	bios = readfile(argv[2])
	bios = bios + "\0" * (len(bios)%4)
	biosheader = struct.pack("2Ih2bIb3b3I31sc", EMUID, len(bios), 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, argv[2], "\0")
	rom = readfile(argv[3])
	rom = rom + "\0" * (len(rom)%4)
	romheader = struct.pack("8I31sc", EMUID, len(rom), 0, 0, 0, 0, 0, 0, argv[3], "\0")
	outputfilename = os.path.splitext(argv[3])[0] + ".gba"	
	writefile(outputfilename, cologne + biosheader + bios + romheader + rom)
