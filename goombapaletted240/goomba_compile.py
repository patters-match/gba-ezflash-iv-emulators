#!/usr/bin/python3

import sys, os.path, struct, argparse, bz2, base64
from sys import argv

SRAM_SAVE = 65536

default_outputfile = "goomba-compilation.gba"
default_emubinary = "jagoombacolor.gba"

# no emulator-specific headers are used, Goomba will parse ROM headers in concatenated data
# use this script for Goomba, Goomba Color, and Jagoomba

#def readfile(name):
#	with open(name, "rb") as fh:
#		contents = fh.read()
#	return contents

def writefile(name, contents):
	with open(name, "wb") as fh:
		fh.write(contents)
		if name == default_outputfile:
			print("...wrote", name)	

if __name__ == "__main__":

	if os.path.dirname(argv[0]) and os.path.dirname(argv[0]) != ".":
		localpath = os.path.dirname(argv[0]) + os.path.sep
	else:
		localpath = ""

	parser = argparse.ArgumentParser(
		description="This script will assemble the Goomba/Goomba Color/Jagoomba emulator and Gameboy/Gameboy Color ROMs into a Gameboy Advance ROM image. It is recommended to type the script name, then drag and drop multiple ROM files onto the shell window, then add any additional arguments as needed.",
		epilog="coded by patters in 2022"
	)

	parser.add_argument(
		dest = 'romfile',
		help = ".gb/.gbc ROM image to add to compilation. Drag and drop multiple files onto your shell window.",
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
		help = "Goomba binary, defaults to " + localpath + default_emubinary,
		type = argparse.FileType('rb'),
		default = localpath + default_emubinary
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
		'-f',
		help = "use filenames to replace the ROM header game titles (these vary between 11, 15, and 16 chars)",
		action = 'store_true'
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
		compilation += args.splashscreen.read()

	for item in args.romfile:
		romfilename = os.path.split(item.name)[1]
		romtitle = os.path.splitext(romfilename)[0]
		romtype = os.path.splitext(romfilename)[1]

		if romtype.lower() == ".gb" or romtype.lower() == ".gbc":
			rom = item.read()

			# determine whether this ROM has an 11, 15, or 16 byte title
			# https://gbdev.gg8.se/wiki/articles/The_Cartridge_Header
			# https://github.com/EvilJagaGenius/jagoombacolor/blob/eade75121d7c2568b812867de854e6cdcd527271/src/main.c#L651
			nogameid = False
			if rom[323] == 128 or rom[323] == 192: # GBC game
				for romchar in range(319,324):
					if rom[romchar] == 0: # can't be a GAME_ID
						nogameid = True
						break
				if nogameid:
					titlelength = 15
				else:
					titlelength = 11
			else:
				titlelength = 16

			# existing ROM title
			outputtitle = rom[308:308+titlelength].decode('ascii')

			if args.f:
				outputtitle = romtitle[:titlelength]
				pad = b""
				if len(outputtitle) == 15:
					# if we overwrite all 15 bytes, the last 4 will be interpreted as a GAME_ID by the emulator
					outputtitle = romtitle[:titlelength-1]
					pad = b"\0"
				outputtitle = outputtitle.split(" [")[0] # strip the square bracket parts of the name (not many chars available)
				outputtitle = outputtitle.split(" (")[0] # strip the bracket parts of the name (not many chars available)
				outputtitlebytes = outputtitle.encode('ascii') + pad
				headername = struct.pack(str(titlelength) + "s",outputtitlebytes)
				romarray = bytearray(rom)
				romarray[308:308+titlelength] = headername
				rom = romarray

			compilation += rom
			print('{:<17}{}'.format(outputtitle.rstrip("\x00"),romtype.strip(".")))
		else:
			raise Exception(f'unsupported filetype for compilation - {romfilename}')

	# on EZ-Flash IV, random data in PSRAM after Goomba compilation may be interpreted as GB roms without 264 null bytes of padding
	# which can result in duplicate game list entries
	# https://www.dwedit.org/dwedit_board/viewtopic.php?id=643
	compilation += b"\0" * 264

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
