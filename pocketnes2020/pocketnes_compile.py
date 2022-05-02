#!/usr/bin/python3

import sys, os.path, struct, argparse, bz2, base64, zlib
from sys import argv

EMU_HEADER = 48
NES_HEADER = 16
SRAM_SAVE = 65536

default_outputfile = "pocketnes-compilation.gba"
default_emubinary = "pocketnes.gba"
default_database = "pnesmmw.mdb"
header_struct_format = "<31sc4I" # https://docs.python.org/3/library/struct.html

# ROM header
#
# from gba.h in the PocketNES source code and FORMATS.txt in the binary distribution, and testing with the Win32 builder
#
#typedef struct {
#	char name[32] null terminated;
#	u32 filesize;
#	u32 flags;
#		Bit 0: 1=Enable PPU speed hack (1 in decimal);
#		Bit 1: 1=Disable CPU Speedhacks (2 in decimal);
#		Bit 2: 1=Use PAL timing (4 in decimal);
#		Bit 5: 0=spritefollow, 1=addressfollow (32 in decimal);
#	u32 address/sprite to follow;
#	u32 reserved;
#} romheader;

def readfile(name):
	with open(name, "rb") as fh:
		contents = fh.read()
	return contents

def writefile(name, contents):
	with open(name, "wb") as fh:
		fh.write(contents)
		if name == default_outputfile:
			print("...wrote", name)	

#def get_bit(value, n):
#    return ((value >> n & 1) != 0)

def set_bit(value, n):
    return value | (1 << n)

#def clear_bit(value, n):
#    return value & ~(1 << n)


if __name__ == "__main__":

	if os.path.dirname(argv[0]) and os.path.dirname(argv[0]) != ".":
		localpath = os.path.dirname(argv[0]) + os.path.sep
	else:
		localpath = ""

	parser = argparse.ArgumentParser(
		description="This script will assemble the PocketNES emulator and NES ROMs into a Gameboy Advance ROM image. It is recommended to type the script name, then drag and drop multiple ROM files onto the shell window, then add any additional arguments as needed.",
		epilog="coded by patters in 2022"
	)

	parser.add_argument(
		dest = 'romfile',
		help = ".nes ROM image to add to compilation. Drag and drop multiple files onto your shell window.",
		type = argparse.FileType('rb'),
		nargs = '+'
	)
	parser.add_argument(
		'-s',
		dest = 'splashscreen',
		help = "76800 byte raw 240x160 15bit splashscreen image",
		type = argparse.FileType('rb')
	)
	parser.add_argument(
		'-e', 
		dest = 'emubinary',
		help = "PocketNES binary, defaults to " + localpath + default_emubinary,
		type = argparse.FileType('rb'),
		default = localpath + default_emubinary
	)
	parser.add_argument(
		'-db', 
		dest = 'database',
		help = "PocketNES Menu Maker Database file which stores optimal flags and sprite follow settings for many games, defaults to " + localpath + default_database,
		type = str,
		default = localpath + default_database
	)
	parser.add_argument(
		'-dbn',
		help = "use game titles from PocketNES Menu Maker database",
		action = 'store_true'
	)	
	parser.add_argument(
		'-m',
		help = "mark small ROMs suitable for link transfer",
		action = 'store_true'
	)
	parser.add_argument(
		'-c',
		help = "clean brackets from ROM titles",
		action = 'store_true'
	)

	# don't use FileType('wb') here because it writes a zero-byte file even if it doesn't parse the arguments correctly
	parser.add_argument(
		'-o',
		dest = 'outputfile',
		help = "compilation output filename, defaults to " + default_outputfile,
		type = str,
		default = default_outputfile
	)
	parser.add_argument(
		'-sav',
		help = "for EZ-Flash IV firmware 1.x - create a blank 64KB .sav file for the compilation, store in the SAVER folder, not needed for firmware 2.x which creates its own blank saves",
		action = 'store_true'
	)
	parser.add_argument(
		'-pat',
		help = "for EZ-Flash IV firmware 2.x - create a .pat file for the compilation to force 64KB SRAM saves, store in the PATCH folder",
		action = 'store_true'
	)
	args = parser.parse_args()


	compilation = args.emubinary.read()

	# ensure the first ROM's data is 256 byte aligned (after headers) for optimal performance
	# https://github.com/Dwedit/PocketNES/issues/5
	compilation = compilation + b"\0" * ((256 - ((len(compilation) + EMU_HEADER + NES_HEADER)%256))%256) 

	if args.splashscreen:
		compilation = compilation + args.splashscreen.read()

	for item in args.romfile:

		flags = 0
		follow = 0 # sprite or address follow for Unscaled (Auto) display mode
		db_match = "  "

		romfilename = os.path.split(item.name)[1]
		romtype = os.path.splitext(romfilename)[1]
		romtitle = os.path.splitext(romfilename)[0]

		if romtype.lower() == ".nes":

			rom = item.read()

			if os.path.exists(args.database):
				# use PocketNES Menu Maker database metadata for the roms, if the database is present

				if rom[0:4] == b'NES\x1a':
					# rom header is present, it needs to be removed to checksum only the rom data
					romdata = rom[NES_HEADER:]
				else:
					romdata = rom
				crcstr = hex(zlib.crc32(romdata))
				crcstr = str(crcstr)[2:]

				with open(args.database) as fh:
					lines = fh.readlines()
					for record in lines:
						if crcstr in record:
							db_match = "db"
							recorddata = record.split("|")
							if args.dbn:
								romtitle = recorddata[1]
							if len(recorddata) > 2:
								if recorddata[2] != "\n":
									flagrecord = recorddata[2]
									if " " in flagrecord:
										flagrecord = flagrecord.split(" ")[0] # remove trailing comments
									if flagrecord:
										flags = int(flagrecord)
							if len(recorddata) > 3:
								if recorddata[3] != "\n":
									followrecord = recorddata[3]
									if " " in followrecord:
										followrecord = followrecord.split(" ")[0] # remove trailing comments
									if followrecord:
										follow = int(followrecord)

			else:
				if "(E)" in romtitle or "(Europe)" in romtitle or "(EUR)" in romtitle:
					flags = set_bit (flags, 2) # set PAL timing for EUR-only titles

			if args.m:
				if os.path.getsize(item.name) <= 196608:
					romtitle = "* " + romtitle
				else:
					romtitle = "  " + romtitle

			if args.c:
				romtitle = romtitle.split(" [")[0] # strip the square bracket parts of the name
				romtitle = romtitle.split(" (")[0] # strip the bracket parts of the name

			romtitle = romtitle[:31]

		else:
			print("Error: unsupported filetype for compilation -", romfilename)
			sys.exit(1)

		# align rom data (after headers) on 256 byte boundaries for optimal performance
		# https://github.com/Dwedit/PocketNES/issues/5
		# https://en.wikipedia.org/wiki/Data_structure_alignment
		rom = rom + b"\0" * ((256 - ((len(rom) + EMU_HEADER)%256))%256)

		romheader = struct.pack(header_struct_format, romtitle.encode('ascii'), b"\0", len(rom), flags, follow, 0)
		compilation = compilation + romheader + rom

		print (db_match, romtitle)

	writefile(args.outputfile, compilation)

	if args.pat:
		# EZ-Flash IV fw2.x GSS patcher metadata to force 64KB SRAM saves - for PATCH folder on SD card
		patchname = os.path.splitext(args.outputfile)[0] + ".pat"
		patchdata = b'QlpoOTFBWSZTWRbvmZEAAAT44fyAgIAAEUAAAACIAAQAAAQESaAAVEIaaGRoxBKeqQD1GTJoks40324rSIskHSFhIywXzTCaqwSzf4exCBTgBk/i7kinChIC3fMyIA=='
		writefile(patchname, bz2.decompress(base64.b64decode(patchdata)))

	if args.sav:
		# EZ-Flash IV fw1.x blank save - for SAVER folder on SD card
		savename = os.path.splitext(args.outputfile)[0] + ".sav"
		saveempty = b"\xff" * SRAM_SAVE
		if not os.path.exists(savename): # careful not to overwrite an existing save
			writefile(savename, saveempty)
