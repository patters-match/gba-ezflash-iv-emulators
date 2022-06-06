#!/usr/bin/python3

import sys, os.path, struct, argparse, bz2, base64
from sys import argv

EMU_ID = int(0x1A534D53) # "SMS",0x1A
EMU_HEADER = 64
SRAM_SAVE = 65536

default_outputfile = "smsadv-compilation.gba"
default_emubinary = "smsadvance.gba"
header_struct_format = "<8I31sc" # https://docs.python.org/3/library/struct.html

# ROM header
#
# from gba.h in the SMSAdvance source code and Formats.txt in the binary distribution
# 
#typedef struct {
#	u32 identifier;
#	u32 filesize;
#	u32 flags;
#		Bit 0: 0=NTSC, 1=PAL (1 in decimal)
#		Bit 1: 0=USA/EUR, 1=JP (2 in decimal)
#		Bit 2: 0=SMS/SG rom, 1=GG rom (4 in decimal)
#		Bit 3: 0=SMS, 1=SMS2 (8 in decimal) https://www.smspower.org/forums/16872-SMS1VsSMS2
#		Bit 4: reserved for CPU speedhacks
#		Bit 5: 0=spritefollow, 1=addressfollow (32 in decimal)
#	u32 spritefollow;
#   u32 0=Game ROM, 1=GG/SMS BIOS;
#	u32 reserved[3];
#	char name[32] null terminated;
#} romheader;

#def readfile(name):
#	with open(name, "rb") as fh:
#		contents = fh.read()
#	return contents

def writefile(name, contents):
	with open(name, "wb") as fh:
		fh.write(contents)
		if name == default_outputfile:
			print("...wrote", name)	

#def get_bit(value, n):
#    return ((value >> n & 1) != 0)

def set_bit(value, n):
    return value | (1 << n)

def clear_bit(value, n):
    return value & ~(1 << n)


if __name__ == "__main__":

	if os.path.dirname(argv[0]) and os.path.dirname(argv[0]) != ".":
		localpath = os.path.dirname(argv[0]) + os.path.sep
	else:
		localpath = ""

	parser = argparse.ArgumentParser(
		description="This script will assemble the SMSAdvance emulator and Master System/Game Gear/SG-1000 ROMs into a Gameboy Advance ROM image. It is recommended to type the script name, then drag and drop multiple ROM files onto the shell window, then add any additional arguments as needed.",
		epilog="coded by patters in 2022"
	)

	parser.add_argument(
		dest = 'romfile',
		help = ".sms/.gg/.sg ROM image to add to compilation. Drag and drop multiple files onto your shell window.",
		type = argparse.FileType('rb'),
		nargs = '*' # it's possible to build a compilation with only a BIOS ROM
	)
	parser.add_argument(
		'-s',
		dest = 'splashscreen',
		help = "76800 byte raw 240x160 15bit splashscreen image",
		type = argparse.FileType('rb')
	)
	parser.add_argument(
		'-b',
		dest = 'bios',
		help = "optional BIOS rom image(s). Since both a Master System and a Game Gear BIOS can be added, use this argument after specifying the game ROMs",
		type = argparse.FileType('rb'),
		nargs = '+' #it's possible to build a compilation with both a GG and an SMS BIOS
	)
	parser.add_argument(
		'-bb',
		help = "allow boot to BIOS-integrated games, via an '-- Empty --' romlist entry. Requires BIOS to be enabled in the SMSAdvance options, and System must be changed from Auto to Master System since it cannot be autodetected when there is no ROM",
		action = 'store_true'
	)
	parser.add_argument(
		'-e', 
		dest = 'emubinary',
		help = "SMSAdvance binary, defaults to " + localpath + default_emubinary,
		type = argparse.FileType('rb'),
		default = localpath + default_emubinary
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

	if args.splashscreen:
		compilation = compilation + args.splashscreen.read()

	if args.bios:
		for item in args.bios:
			biosflag = 1
			flags = 0
			follow = 0 # sprite or address follow for 'Unscaled (Auto)' display mode
			bios = item.read()
			bios = bios + b"\0" * ((4 - (len(bios)%4))%4)
			biosfilename = os.path.split(item.name)[1]
			biosname = os.path.splitext(biosfilename)[0]
			biostype = os.path.splitext(biosfilename)[1]
			if "(J)" in biosname or "(Japan)" in biosname or "(JP)" in biosname:
				flags = set_bit (flags, 1)
			if biostype.lower() == ".gg" or ".gg.bin" in biosfilename.lower(): # using .bin for BIOS roms stops them being added in batch jobs
				flags = set_bit (flags, 2) # GG roms need this flag
			biosheader = struct.pack(header_struct_format, EMU_ID, len(bios), flags, follow, biosflag, 0, 0, 0, biosfilename[:31].encode('ascii'), b"\0")
			compilation = compilation + biosheader + bios

		if args.bb:
			biosflag = 0
			flags = 0
			follow = 0 # sprite or address follow for 'Unscaled (Auto)' display mode
			empty = b"\xff" * 16384
			emptyname = "-- Empty --"
			emptyheader = struct.pack(header_struct_format, EMU_ID, len(empty), flags, follow, biosflag, 0, 0, 0, emptyname.encode('ascii'), b"\0")
			compilation = compilation + emptyheader + empty

	for item in args.romfile:

		biosflag = 0
		flags = 0
		follow = 0 # sprite or address follow for Unscaled (Auto) display mode

		romfilename = os.path.split(item.name)[1]
		romtype = os.path.splitext(romfilename)[1]
		romtitle = os.path.splitext(romfilename)[0]

		# Game Gear
		if romtype.lower() == ".gg":
			flags = set_bit (flags, 2) # GG roms need this flag
			if "castle of illusion" in romtitle.lower():
				flags = clear_bit (flags, 2) # with one exception - this GG game is technically an SMS rom
			# set JP region for JP-only titles
			# e.g. to convert Power Strike II to GG Aleste II, rename the rom to "GG Aleste II (J).gg", build, and you will get the JP title screen
			if "(J)" in romtitle or "(Japan)" in romtitle or "(JP)" in romtitle:
				flags = set_bit (flags, 1)

		# Master System
		elif romtype.lower() == ".sms":
			if "(E)" in romtitle or "(Europe)" in romtitle or "(EUR)" in romtitle:
				flags = set_bit (flags, 0) # set PAL timing for EUR-only titles
			if "(J)" in romtitle or "(Japan)" in romtitle or "(JP)" in romtitle:
				flags = set_bit (flags, 1) # set JP region for JP-only titles
			# Some Master System titles make use of the enhanced SMSv2 VDP https://www.smspower.org/forums/16872-SMS1VsSMS2
			if "cosmic spacehead" in romtype.lower():
				flags = set_bit (flags, 3)
			if "excellent dizzy collection" in romtype.lower():
				flags = set_bit (flags, 3)
			if "fantastic dizzy" in romtype.lower():
				flags = set_bit (flags, 3)
			if "micro machines" in romtype.lower():
				flags = set_bit (flags, 3)
			# Some titles also use double height sprites, which are buggy on SMSv1 https://nicole.express/2021/i-am-the-mark-iii.html
			if "earthworm jim" in romtype.lower():
				flags = set_bit (flags, 3)

		# SG-1000
		elif romtype.lower() == ".sg":
			# no special cases
			flags = 0

		else:
			print("Error: unsupported filetype for compilation -", romfilename)
			sys.exit(1)

		if args.c:
			romtitle = romtitle.split(" [")[0] # strip the square bracket parts of the name
			romtitle = romtitle.split(" (")[0] # strip the bracket parts of the name

		if args.m:
			if os.path.getsize(item.name) <= 196608:
				romtitle = "* " + romtitle[:29]
			else:
				romtitle = "  " + romtitle[:29]
		else:
			romtitle = romtitle[:31]


		rom = item.read()
		rom = rom + b"\0" * ((4 - (len(rom)%4))%4)
		romheader = struct.pack(header_struct_format, EMU_ID, len(rom), flags, follow, biosflag, 0, 0, 0, romtitle.encode('ascii'), b"\0")
		compilation = compilation + romheader + rom

		print (romtitle)

	if args.bios or args.romfile:
		writefile(args.outputfile, compilation)
	else:
		parser.print_usage()

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
