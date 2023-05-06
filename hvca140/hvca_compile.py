#!/usr/bin/python3

import sys, os.path, struct, argparse, bz2, base64, glob
from sys import argv

EMU_ID = int(0x04174170)
EMU_END_MARKER = int(0x41700417)
EMU_HEADER = 44
SRAM_SAVE = 65536

default_outputfile = "hvca-compilation.gba"
default_emubinpath = "bin"
default_bios = "disksys.rom" # must be 8KB
default_palette = "hvca.pal"
header_struct_format = "<I31sx3sxI" # https://docs.python.org/3/library/struct.html

# hvcamkfs file header
#
# very similar to the Famicom Advance builder https://github.com/kik/fca/blob/master/fca/src/tool/fca-mkfs.c
# HVCA is based on Famicom Advance
# 
#struct file_header {
#  long magic;
#  char name[32]; # null terminated
#  char ext[4]; # null terminated
#  long length;
#};

def readfile(name):
	with open(name, "rb") as fh:
		contents = fh.read()
	return contents

def writefile(name, contents):
	with open(name, "wb") as fh:
		fh.write(contents)
		if name == default_outputfile:
			print("...wrote", name)	

def appendfile(file, verbose):
	global compilation
	filename = os.path.split(file.name)[1]
	name = os.path.splitext(filename)[0]
	name = name[:31]
	ext = os.path.splitext(filename)[1].strip(".")
	ext = ext[:3]
	if ext.lower() == "nes" or ext.lower() == "fds" or ext.lower() == "nsf" or ext.lower() == "cfg":
		if args.c:
			name = name.split(" [")[0] # strip the square bracket parts of the name
			name = name.split(" (")[0] # strip the bracket parts of the name
	contents = file.read()
	if ext.lower() == "nes" and contents[:4] != b'NES\x1a':
		raise Exception('NES ROMs must be headered')
	if ext.lower() == "fds" and contents[:4] != b'FDS\x1a':
		# reconstruct missing FDS header which HVCA requires
		num_disk_sides = int(len(contents)/65500).to_bytes(1, byteorder='little')
		contents = b'FDS\x1a' + num_disk_sides + b"\0" * 11 + contents
	size = len(contents)
	contents += b"\0" * ((4 - (len(contents)%4))%4) # 4 byte alignment
	fileheader = struct.pack(header_struct_format, EMU_ID, name.encode('ascii'), ext.encode('ascii'), size)
	compilation += fileheader + contents
	if verbose:
		print('{:<32}{}'.format(name,ext))


#def get_bit(value, n):
#    return ((value >> n & 1) != 0)

#def set_bit(value, n):
#    return value | (1 << n)

#def clear_bit(value, n):
#    return value & ~(1 << n)


if __name__ == "__main__":

	if os.path.dirname(argv[0]) and os.path.dirname(argv[0]) != ".":
		localpath = os.path.dirname(argv[0]) + os.path.sep
	else:
		localpath = ""

	parser = argparse.ArgumentParser(
		description="This script will assemble the HVCA emulator and NES/FDS/NSF ROMs into a Gameboy Advance ROM image. It is recommended to type the script name, then drag and drop multiple ROM files onto the shell window, then add any additional arguments as needed.",
		epilog="coded by patters in 2023"
	)

	parser.add_argument(
		dest = 'romfile',
		help = ".nes/.fds/.nsf/.cfg files to add to the compilation. Drag and drop multiple files onto your shell window. A .cfg filename must match the filename of the game it targets.",
		type = argparse.FileType('rb'),
		nargs = '+'
	)
	parser.add_argument(
		'-e', 
		dest = 'emubinpath',
		help = "HVCA binaries folder, defaults to " + localpath + default_emubinpath,
		type = str,
		default = localpath + default_emubinpath
	)
	parser.add_argument(
		'-b',
		dest = 'bios',
		help = "BIOS rom image needed for FDS support, defaults to " + localpath + default_bios,
		type = argparse.FileType('rb'),
		default = localpath + default_bios
	)
	parser.add_argument(
		'-p',
		dest = 'palette',
		help = "optional palette file",
		type = argparse.FileType('rb'),
	)
	parser.add_argument(
		'-x',
		dest = 'exitsub',
		help = "flashcart-specific .sub exit subroutine",
		type = argparse.FileType('rb'),
	)
	parser.add_argument(
		'-v',
		help = "verbose ouput, similar to the original hvcamkfs.exe build tool",
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
		'-c',
		help = "clean brackets from ROM titles",
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

	compilation = readfile(args.emubinpath + os.path.sep + "base.bin")
	if args.v:
		print('{:<32}{}'.format("base","bin"))

	searchpath = args.emubinpath + os.path.sep + "font*.raw"
	for fontfile in sorted(glob.glob(searchpath)):
		with open(fontfile, "rb") as fonthandle:
			appendfile(fonthandle, args.v)

	searchpath = args.emubinpath + os.path.sep + "mapr" + os.path.sep + "*.bin"
	for maprfile in sorted(glob.glob(searchpath)):
		with open(maprfile, "rb") as maprhandle:
			appendfile(maprhandle, args.v)

	if args.exitsub:
		appendfile(args.exitsub, args.v)

	if args.palette:
		appendfile(args.palette, args.v)

	fdsfiles, nesfiles, nsffiles, cfgfiles =([], [], [], [])

	for item in args.romfile:
		romfilename = os.path.split(item.name)[1]
		romtitle = os.path.splitext(romfilename)[0]
		romtype = os.path.splitext(romfilename)[1]
		if romtype.lower() == ".fds":
			fdsfiles.append(item)
		elif romtype.lower() == ".nes":
			nesfiles.append(item)
		elif romtype.lower() == ".nsf":
			nsffiles.append(item)
		elif romtype.lower() == ".cfg":
			cfgfiles.append(item)
		else:
			raise Exception(f'unsupported filetype for compilation - {romfilename}')

	if fdsfiles:
		appendfile(args.bios, args.v)

	for item in fdsfiles:
		appendfile(item, True)
	for item in nesfiles:
		appendfile(item, True)
	for item in nsffiles:
		appendfile(item, True)
	for item in cfgfiles:
		appendfile(item, True)

	# this does not appear to be needed, but it's here for consistency with merge.bat's use of the hvcamkfs -c option:
	#  -c   Add END-MAGIC-NUM (FCA compatible)
	compilation += EMU_END_MARKER.to_bytes(4, byteorder='little') + b"\0" * (EMU_HEADER - 4)

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
