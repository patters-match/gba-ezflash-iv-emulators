#!/usr/bin/python3

import sys, os.path, struct, argparse, bz2, base64
from sys import argv

EMUID = int(0x1A53454E) # "NES",0x1A - probably unintentional
EMU_HEADER = 60
SRAM_SAVE = 65536 # not 8KB as advertised in readme.txt

default_outputfile = "pceadv-compilation.gba"
default_emubinary = "pceadvance.gba"
default_cdrombios = "bios.bin"
header_struct_format = "<31sc5I12s" # https://docs.python.org/3/library/struct.html

# ROM header
#
# from gba.h in the PCEAdvance source code, flags deduced by testing with the Win32 builder
# 
#typedef struct {
#	char name[32] null terminated;
#	u32 filesize;
#	u32 flags;
#		Bit 0: 0=Full CPU, 1=50% CPU throttle (1 in decimal)
#		Bit 1: 0=CPU Speedhacks enabled, 1=Disable CPU Speedhacks (2 in decimal)
#		Bit 2: 0=JP rom, 1=USA rom (4 in decimal)
#		Bit 5: 0=spritefollow, 1=addressfollow (32 in decimal)
#	u32 address/sprite to follow;
#	u32 identifier;
#	char unknown[12];
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
		description="This script will assemble the PCEAdvance emulator, PC Engine/Turbografx-16 .pce ROM images, and .iso CD-ROM data tracks into a Gameboy Advance ROM image. It is recommended to type the script name, then drag and drop multiple ROM files onto the shell window, then add any additional arguments as needed.",
		epilog="coded by patters in 2022"
	)

	parser.add_argument(
		dest = 'romfile',
		help = ".pce or .iso image to add to compilation. Drag and drop multiple files onto your shell window. Note that PCEAdvance supports only one CD-ROM game per compilation.",
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
		'-b',
		dest = 'cdrombios',
		help = "CD-ROM / Super CD-ROM BIOS rom image, defaults to " + localpath + default_cdrombios,
		type = str,
		default = localpath + default_cdrombios
	)
	parser.add_argument(
		'-e',
		dest = 'emubinary',
		help = "PCEAdvance binary, defaults to " + localpath + default_emubinary,
		type = argparse.FileType('rb'),
		default = localpath + default_emubinary
	)
	parser.add_argument(
		'-t',
		dest = 'tcdfile',
		help = "CD-ROM track index file, needed for games with multiple data tracks, defaults to <iso_name>.tcd",
		type = argparse.FileType('rb'),
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
		help = "for EZ-Flash IV firmware 1.x - create a blank 8KB .sav file for the compilation, store in the SAVER folder, not needed for firmware 2.x which creates its own blank saves",
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

	iso_count = 0

	for item in args.romfile:

		flags = 0
		follow = 0 # sprite or address follow for 'Unscaled (Auto)' display mode

		romfilename = os.path.split(item.name)[1]
		romtitle = os.path.splitext(romfilename)[0]
		romtype = os.path.splitext(romfilename)[1]

		# HuCard
		if romtype.lower() == ".pce":
			rom = item.read()
			rom = rom + b"\0" * ((4 - (len(rom)%4))%4)

			# USA ROMs need this specific flag - remember, most will need to be decrypted first using PCEToy
			if "(U)" in romtitle or "(USA)" in romtitle:
				flags = set_bit (flags, 2)

			# sprite follow settings for display mode: Unscaled (Auto)
			if "1943" in romtitle:
				follow = 9
			if "aero blasters" in romtitle.lower():
				follow = 6
			if "atomic robokid special" in romtitle.lower():
				follow = 0
			if "devil crash" in romtitle.lower():
				follow = 11
			if "devil's crush" in romtitle.lower():
				follow = 11
			if "kyuukyoku tiger" in romtitle.lower():
				follow = 3
			if "legendary axe" in romtitle.lower():
				follow = 14
			if "raiden" in romtitle.lower():
				follow = 5

			if args.c:
				romtitle = romtitle.split(" [")[0] # strip the square bracket parts of the name
				romtitle = romtitle.split(" (")[0] # strip the bracket parts of the name

			romtitle = romtitle[:31]

			# unsure why 16 bytes are added to len(rom), but the original builder does this, despite that it pads the roms a lot more than 16b
			# however, you can't add more than one rom to the compilation unless this is done
			romheader = struct.pack(header_struct_format, romtitle.encode('ascii'), b"\0", len(rom)+16, flags, follow, 0, EMUID, b"@           ")

			compilation = compilation + romheader + rom

		# CD-ROM
		elif romtype.lower() == ".iso":
			# only a single CD-ROM image is supported per compilation
			if iso_count == 0:
				# first data track ISO needs a CD-ROM BIOS + optional TCD tracklist first
				cdbios = readfile(args.cdrombios)
				cdbios = cdbios + b"\0" * ((4 - (len(cdbios)%4))%4)
				cdtitle = romtitle
	
				if args.c:
					romtitle = romtitle.split(" [")[0] # strip the square bracket parts of the name
					romtitle = romtitle.split(" (")[0] # strip the bracket parts of the name

				romtitle = romtitle[:31]

				# use the ISO name for the cdbios entry in the rom list
				cdromheader = struct.pack(header_struct_format, romtitle.encode('ascii'), b"\0", len(cdbios)+16, flags, follow, 0, EMUID, b"@           ")
				compilation = compilation + cdromheader + cdbios

				if args.tcdfile:
					tracklist = args.tcdfile.read()
				elif os.path.exists(romtitle + ".tcd"):
					tracklist = readfile(romtitle + ".tcd")
				else:
					tracklist = b""

				cdrom = tracklist

			# append data track (any subsequent tracks are simply concatenated - a TCD file is required for multiple data tracks)
			cdrom = cdrom + item.read()
			iso_count = iso_count + 1
			if iso_count == 2 and tracklist == b"":
				print("Error: multiple ISO data tracks require a TCD tracklist, either named to match the first ISO, or defined via -t")
				print("       Note that PCEAdvance supports only a single CD-ROM game per compilation")
				sys.exit(1)

		else:
			print("Error: unsupported filetype for compilation -", romfilename)
			sys.exit(1)

		print (romtitle)

	# finished iterating rom list, append any CD-ROM data
	if iso_count:
		compilation = compilation + cdrom

		# Super CD-ROM compilations cannot be larger than 16384-192KB or they won't fit into PSRAM
		if "SCD" in cdtitle and len(compilation) > 16192 * 1024:
			compilation = compilation[:16191 * 1024]
			print("Warning: this Super CD-ROM compilation had to be truncated to fit within the 16192KB of remaining PSRAM - so YMMV")

		# Arcade Card compilations cannot be larger than 14336-192KB or they won't fit into PSRAM
		elif "ACD" in cdtitle and len(compilation) > 14144 * 1024:
			compilation = compilation[:14143 * 1024]
			print("Warning: this Arcade Card CD-ROM compilation had to be truncated to fit within the 14144KB of remaining PSRAM - so YMMV")

		# CD-ROM compilations cannot be larger than 16384KB or they won't fit into PSRAM
		elif len(compilation) > 16384 * 1024:
			compilation = compilation[:16383 * 1024]
			print("Warning: this CD-ROM compilation had to be truncated to fit within the 16MB of PSRAM - so YMMV")
			print("         build this one with a CD-ROM BIOS, rather than a Super CD-ROM BIOS")
			print("         or you will lose an additional 192KB of PSRAM")

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
