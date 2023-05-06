#!/usr/bin/python3

import sys, os.path, struct, argparse, bz2, base64, zlib
from sys import argv

EMU_ID = int(0x1A4C4F43) # "COL",0x1A - probably unintentional since Formats.txt incorrectly states it should be "MSX",0x1A
EMU_HEADER = 64
SRAM_SAVE = 65536

default_outputfile = "msxadv-compilation.gba"
default_emubinary = "msxadva.gba"
default_bios = "bios.bin" # recommended to use 'MSX System v1.0 + MSX BASIC (1983)(Microsoft)[MSX.ROM]'
header_struct_format = "<8I31sx" # https://docs.python.org/3/library/struct.html

# ROM header
#
# from gba.h in the MSXAdvance source code and Formats.txt in the binary distribution, and testing with the Win32 builder
#
#typedef struct {
#	u32 identifier;
#	u32 filesize;
#	u32 flags;
#		Bit 0: 0=NTSC, 1=PAL (1 in decimal)
#		Bit 4: reserved for CPU speedhacks (16 in decimal)
#		Bit 5: 0=spritefollow, 1=addressfollow (32 in decimal)
#	u32 spritefollow;
#	u32 bios; 0=Game ROM, 1=MSX1 BIOS ROM
#	u32 mapper; 0=undefined, 1=Konami4, 2=Konami5, 3=ASCII8k, 4=ASCII16k, 5=RTYPE
#	u32 reserved[2];
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

#def clear_bit(value, n):
#    return value & ~(1 << n)

def detectmapper(romdata):
	size = len(romdata)
	crcval = zlib.crc32(romdata)
	
	#R-Type, various versions
	if crcval == 0xa884911c or crcval == 0x5b14c736 or crcval == 0x827919e4 or crcval == 0x71e94fce:
		return 'RTYPE'
	if crcval == 0x2a019191:
		return 'ASCII8K'
	if crcval == 0xa3a51fbb:
		return 'ASCII16K'
	if crcval == 0x952bfaa4:
		return 'KONAMI5'	
	#not sure if the versions that don't use the RTYPE mapper are fully playable, but they seem to run ok

	if size < 0x10000:
		if (size <= 0x4000) and (romdata[0] == b'A') and (romdata[1] == b'B'):
			initAddr = struct.unpack("<H", romdata[2:4])[0]
			textAddr = struct.unpack("<H", romdata[8:10])[0]
			if (textAddr & 0xC000) == 0x8000:
				if (initAddr == 0) or (((initAddr & 0xC000) == 0x8000) and (romdata[initAddr & (size - 1)] == 0xC9)):
					#return 'ROM_PAGE2'
					return 'KONAMI4'

		# not correct for Konami-DAC, but does this really need
		# to be correct for _every_ rom?
		#return 'ROM_MIRRORED'
		return 'KONAMI4'

	elif size == 0x10000 and (not ((romdata[0] == b'A')) and (romdata[1] == b'B')):
		# 64 kB ROMs can be plain or memory mapped...
		# check here for plain, if not, try the auto detection
		#(thanks for the hint, hap)
		#return 'ROM_MIRRORED'
		return 'KONAMI4'
	else:
		#  GameCartridges do their bankswitching by using the Z80
		#  instruction ld(nn),a in the middle of program code. The
		#  address nn depends upon the GameCartridge mappertype used.
		#  To guess which mapper it is, we will look how much writes
		#  with this instruction to the mapper-registers-addresses
		#  occur.

		typeGuess = {
			'KONAMI4' : 0,
			'KONAMI5' : 0,
			'ASCII8K'  : 0,
			'ASCII16K' : 0,
		}
		for i in range(0,size - 3):
			if romdata[i] == 0x32:
				value = struct.unpack("<H", romdata[i + 1:i + 3])[0]
				if value == 0x5000 or value == 0x9000 or value == 0xb000:
					typeGuess['KONAMI5'] += 1
				elif value == 0x4000 or value == 0x8000 or value == 0xa000:
					typeGuess['KONAMI4'] += 1
				elif value == 0x6800 or value == 0x7800:
					typeGuess['ASCII8K'] += 1
				elif value == 0x6000:
					typeGuess['KONAMI4'] += 1
					typeGuess['ASCII8K'] += 1
					typeGuess['ASCII16K'] += 1
				elif value == 0x7000:
					typeGuess['KONAMI5'] += 1
					typeGuess['ASCII8K'] += 1
					typeGuess['ASCII16K'] += 1
				elif value == 0x77ff:
					typeGuess['ASCII16K'] += 1

		if typeGuess['ASCII8K']:
			typeGuess['ASCII8K'] -= 1 # -1 -> max_int

		type = max(typeGuess, key=typeGuess.get)

		if type == 'ASCII16K' and typeGuess['KONAMI4'] == typeGuess['ASCII16K']:
			type = 'KONAMI4'
		return type


if __name__ == "__main__":

	if os.path.dirname(argv[0]) and os.path.dirname(argv[0]) != ".":
		localpath = os.path.dirname(argv[0]) + os.path.sep
	else:
		localpath = ""

	parser = argparse.ArgumentParser(
		description="This script will assemble the MSXAdvance emulator, a BIOS and MSX1 ROMs into a Gameboy Advance ROM image. It is recommended to type the script name, then drag and drop multiple ROM files onto the shell window, then add any additional arguments as needed.",
		epilog="coded by patters in 2022"
	)

	parser.add_argument(
		dest = 'romfile',
		help = ".rom image to add to compilation. Drag and drop multiple files onto your shell window.",
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
		help = "mandatory BIOS rom image, defaults to " + localpath + default_bios,
		type = argparse.FileType('rb'),
		default = localpath + default_bios
	)
	parser.add_argument(
		'-bb',
		help = "allow boot to the BIOS only, via an '-- Empty --' romlist entry",
		action = 'store_true'
	)
	parser.add_argument(
		'-e', 
		dest = 'emubinary',
		help = "MSXAdvance binary, defaults to " + localpath + default_emubinary,
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
	parser.add_argument(
		'-nomap',
		help = "disable automatic selection of ROM mapper type",
		action = 'store_true'
	)
	args = parser.parse_args()


	compilation = args.emubinary.read()

	if args.splashscreen:
		compilation = compilation + args.splashscreen.read()

	biosflag = 1
	flags = 0
	mapper = 0
	follow = 0 # sprite or address follow for 'Unscaled (Auto)' display mode
	bios = args.bios.read()
	bios += b"\0" * ((4 - (len(bios)%4))%4)
	biosfilename = os.path.split(args.bios.name)[1]
	biosheader = struct.pack(header_struct_format, EMU_ID, len(bios), flags, follow, biosflag, mapper, 0, 0, biosfilename[:31].encode('ascii'))
	compilation += biosheader + bios

	if args.bb:
		biosflag = 0
		flags = 0
		mapper = 0
		follow = 0 # sprite or address follow for 'Unscaled (Auto)' display mode
		empty = b"\xff" * 16384
		emptyname = "-- Empty --"
		emptyheader = struct.pack(header_struct_format, EMU_ID, len(empty), flags, follow, biosflag, mapper, 0, 0, emptyname.encode('ascii'))
		compilation += emptyheader + empty

	for item in args.romfile:

		biosflag = 0
		flags = 0
		follow = 0 # sprite or address follow for Unscaled (Auto) display mode
		mapper = 0
		mappername = ""

		romfilename = os.path.split(item.name)[1]
		romtype = os.path.splitext(romfilename)[1]
		romtitle = os.path.splitext(romfilename)[0]
		rom = item.read()
		rom += b"\0" * ((4 - (len(rom)%4))%4)

		if romtype.lower() == ".rom":

			if "(E)" in romtitle or "(Europe)" in romtitle or "(EUR)" in romtitle:
				flags = set_bit (flags, 0) # set PAL timing for EUR-only titles

			if not args.nomap:
				mappername = detectmapper(rom)
				if mappername == 'KONAMI4': mapper = 1
				elif mappername == 'KONAMI5': mapper = 2
				elif mappername == 'ASCII8K': mapper = 3
				elif mappername == 'ASCII16K': mapper = 4
				elif mappername == 'RTYPE': mapper = 5

		else:
			raise Exception(f'unsupported filetype for compilation - {romfilename}')

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

		romheader = struct.pack(header_struct_format, EMU_ID, len(rom), flags, follow, biosflag, mapper, 0, 0, romtitle.encode('ascii'))
		compilation += romheader + rom

		print(romtitle.ljust(32), mappername)

	if not args.romfile:
		print("No ROMs specified, writing emulator and BIOS only")
	writefile(args.outputfile, compilation)

	if not args.romfile:
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
