#!/usr/bin/python3

import sys, os.path, struct, argparse, bz2, base64, zlib
from sys import argv

SNES_HEADER = 512
SRAM_SAVE = 65536

default_emubinary = "snezzi.gba"
default_database = "snezzi.dat"

anchor = b"SMEMMAP0"
iwramstart = b".IWRAMSTART"
iwramend = b".IWRAMEND"

def NOP(v):
	return 0x00000000

def LRAM(v):
	return (v & 0x0000FFFF) | 0x02000000

def HRAM(v):
	return (v & 0x0000FFFF) | 0x02010000

def LROM(v):
	return ((v & 0x00007FFF) + ((v >> 1) & ((romSize - 1) & ~0x7FFF))) + 0x08000000 + snesRomPosition

def HROM(v):
	return ((v & 0x0000FFFF) + (v & ((romSize - 1) & ~0xFFFF))) + 0x08000000 + snesRomPosition

def ROM(v):
	return(v & 0x000FFFFF) + 0x08000000 + snesRomPosition

def IO(v):
	return (v & 0x0000FFFF) | 0x80000000

def SRAM(v):
	return (v & 0x00001FFF) + 0x80006000

def SVEC(v):
	return (v & 0x000000FF) + 0x0203FF00

def _set(x,v):
	global memorymap
	result = (v(x * 0x2000) - (x * 0x2000)) & 0xFFFFFFFF
	memorymap += struct.pack("<I", int(result))

def _map(s,e,m0,m1,m2,m3,m4,m5,m6,m7):
	for i in range(s,e+1):
		x = i*8
		_set(x+0, m0)
		_set(x+1, m1)
		_set(x+2, m2)
		_set(x+3, m3)
		_set(x+4, m4)
		_set(x+5, m5)
		_set(x+6, m6)
		_set(x+7, m7)

def formmemorymap(loRom, romSize):
	global memorymap
	if loRom:
		# LoROM
		_map(0x00, 0x2f, LRAM,IO,  IO,  NOP, LROM,LROM,LROM,LROM)
		_map(0x30, 0x3f, LRAM,IO,  IO,  SRAM,LROM,LROM,LROM,LROM)
		_map(0x40, 0x6f, NOP, NOP, NOP, NOP, LROM,LROM,LROM,LROM)
		_map(0x70, 0x7d, SRAM,SRAM,SRAM,SRAM,LROM,LROM,LROM,LROM)
		_map(0x7e, 0x7e, LRAM,LRAM,LRAM,LRAM,LRAM,LRAM,LRAM,LRAM)
		_map(0x7f, 0x7f, HRAM,HRAM,HRAM,HRAM,HRAM,HRAM,HRAM,HRAM)

		_map(0x80, 0xaf, LRAM,IO,  IO,  NOP, LROM,LROM,LROM,LROM)
		_map(0xb0, 0xbf, LRAM,IO,  IO,  SRAM,LROM,LROM,LROM,LROM)
		_map(0xc0, 0xff, LROM,LROM,LROM,LROM,LROM,LROM,LROM,LROM)

	else:
		# HiROM
		_map(0x00, 0x2f, LRAM,IO,  IO,  NOP, HROM,HROM,HROM,HROM)
		_map(0x30, 0x3f, LRAM,IO,  IO,  SRAM,HROM,HROM,HROM,HROM)
		_map(0x40, 0x6f, HROM,HROM,HROM,HROM,HROM,HROM,HROM,HROM)
		_map(0x70, 0x7d, SRAM,SRAM,SRAM,SRAM,HROM,HROM,HROM,HROM)
		_map(0x7e, 0x7e, LRAM,LRAM,LRAM,LRAM,LRAM,LRAM,LRAM,LRAM)
		_map(0x7f, 0x7f, HRAM,HRAM,HRAM,HRAM,HRAM,HRAM,HRAM,HRAM)

		_map(0x80, 0xaf, LRAM,IO,  IO,  NOP, HROM,HROM,HROM,HROM)
		_map(0xb0, 0xbf, LRAM,IO,  IO,  SRAM,HROM,HROM,HROM,HROM)
		_map(0xc0, 0xff, HROM,HROM,HROM,HROM,HROM,HROM,HROM,HROM)
	
	memorymap += struct.pack("<2I", sramSizeBytes - 1, 0x8000000 + snesRomPosition)


def checksum(input):
    s = 0
    for i in range(0,len(input)-1):
        s += int(byte[i:i+2],16)


def readfile(name):
	with open(name, "rb") as fh:
		contents = fh.read()
	return contents

def writefile(name, contents):
	with open(name, "wb") as fh:
		fh.write(contents)

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
		description="This script will assemble the Snezziboy emulator and a single SNES ROM into a Gameboy Advance ROM image. If supplied with multiple ROM files it will create multiple compilations. It is recommended to type the script name, then drag and drop multiple ROM files onto the shell window, then add any additional arguments as needed. A dat file database is required.",
		epilog="coded by patters in 2022"
	)

	parser.add_argument(
		dest = 'romfile',
		help = ".sfc/.smc ROM image to add to compilation. Drag and drop multiple files onto your shell window.",
		type = argparse.FileType('rb'),
		nargs = '+'
	)
	parser.add_argument(
		'-e', 
		dest = 'emubinary',
		help = "Snezziboy binary, defaults to " + localpath + default_emubinary,
		type = argparse.FileType('rb'),
		default = localpath + default_emubinary
	)
	parser.add_argument(
		'-db', 
		dest = 'database',
		help = "Database file which stores speed hacks for many games, defaults to " + localpath + default_database + ". SNESAdvance SuperDAT file is also supported.",
		type = str,
		default = localpath + default_database
	)
	parser.add_argument(
		'-c',
		help = "clean brackets from ROM titles",
		action = 'store_true'
	)
	parser.add_argument(
		'-v',
		help = "verbose ouput, to mimic the original snezzi.exe build tool",
		action = 'store_true'
	)

	# don't use FileType('wb') here because it writes a zero-byte file even if it doesn't parse the arguments correctly
	parser.add_argument(
		'-o',
		dest = 'outputfile',
		help = "defaults to the ROM name with a .gba extension, may be overridden only when a single romfile is provided",
		type = str
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
		'-strip',
		help = "strip headered ROMs (.smc) and export as headerless (.sfc)",
		action = 'store_true'
	)
	args = parser.parse_args()

	emubinary = args.emubinary.read()

	for item in args.romfile:

		db_match = "  "

		romfilename = os.path.split(item.name)[1]
		romtype = os.path.splitext(romfilename)[1]
		romtitle = os.path.splitext(romfilename)[0]

		if romtype.lower() == ".sfc" or romtype.lower() == ".smc":

			rom = item.read()
			romSize = len(rom)
			if romSize%1024 == SNES_HEADER:
				# rom header is present, it needs to be removed to checksum only the rom data
				romdata = rom[SNES_HEADER:]
				romSize -= 512
				if args.v:
					print("Header      : Yes")
				if args.strip:
					if not os.path.exists(romtitle + ".sfc"):
						writefile(romtitle + ".sfc", romdata)
			else:
				romdata = rom
				if args.v:
					print("Header      : No")

			crcstr = hex(zlib.crc32(romdata))
			crcstr = str(crcstr)[2:].upper()

			emulator = bytearray(emubinary)
			emuSize = len(emulator)
			emuSize = int((emuSize + 4096) / 4096) * 4096

			if args.v:
				print("ROM Size    :", int(romSize*8/(1024*1024)), "megabits")
				print("CRC Checksum:", crcstr)
				print("Emu Core    :", int(emuSize/1024), "KB")

			# find all anchor positions
			anchorfound = emulator.find(anchor)
			iwramstartfound = emulator.find(iwramstart)
			iwramendfound = emulator.find(iwramend)

			snesRomPosition = int(emuSize/65536) * 65536
			if emuSize%65536!=0:
				snesRomPosition += 65536
			
			if args.v:
				print("SMEMMAP     :", str(hex(anchorfound)) )
				print("SNES ROM    :", str(hex(snesRomPosition)) )

				if iwramendfound - iwramstartfound <= (32 * 1024 - 512):
					print( "IWRAM Size  :", iwramendfound - iwramstartfound, "out of", (32*1024-512), "bytes")
				else:
					print( "IWRAM size  :", iwramendfound - iwramstartfound, "bytes (Invalid)")

			# check HiRom/LoROM by checking for matching SNES ROM header checksum and checksum complement 16bit values
			# the header occupies the last 64 bytes of the first page of ROM data ending at 0x7FFF for LoRom / 0xFFFF for HiROM
			# https://en.m.wikibooks.org/wiki/Super_NES_Programming/SNES_memory_map
			# https://sneslab.net/wiki/SNES_ROM_Header
			loROM = 1
			romCheckSum = struct.unpack("<H", romdata[0xFFDC:0xFFDE])[0]
			romInvCheckSum = struct.unpack("<H", romdata[0xFFDE:0xFFE0])[0]
			if (romCheckSum ^ romInvCheckSum) & 0xFFFF == 0xFFFF: # checksum XOR checksum complement
				loROM = 0
			else:
				romCheckSum = struct.unpack("<h", romdata[0x7FDC:0x7FDE])[0]
				romInvCheckSum = struct.unpack("<h", romdata[0x7FDE:0x7FE0])[0]
				if (romCheckSum ^ romInvCheckSum) & 0xFFFF == 0xFFFF: # checksum XOR checksum complement
					loROM = 1

			if args.v:
				if loROM:
					print("Memory Map  : LoROM")
				else:
					print("Memory Map  : HiROM")

			# obtain SRAM size from the SNES header
			if loROM:
				sramSize = romdata[0x7FD8]
			else:
				sramSize = romdata[0xFFD8]
			if sramSize:
				sramSizeBytes = (0x400 << sramSize)
			else:
				sramSizeBytes = 1

			if args.c:
				romtitle = romtitle.split(" [")[0] # strip the square bracket parts of the name
				romtitle = romtitle.split(" (")[0] # strip the bracket parts of the name

			if args.v:
				print("SRAM Size   :", int(sramSizeBytes/1024), "KB")
				print("Game        :", romtitle)

			# do the necessary patching
			with open(args.database, "r", encoding='latin-1') as fh:
				lines = fh.readlines()
				for record in lines:
					# SNESAdvance SuperDAT
					# CRC32|title|flags1|flags2|autoscroll1|autoscroll2|scale|offset|patches

					# snezziboy.dat
					# CRC32|title|patches

					if crcstr in record:
						db_match = "db"
						recorddata = record.split("|")

						#in either dat type, patches are the last record
						if len(recorddata) > 8 or len(recorddata) == 3:
							if args.v:
								print("Patch       :")
							patches = recorddata[len(recorddata) - 1].split(",")
							romarray = bytearray(romdata)
							for patch in patches:
								patch = patch.split("\n")[0] # remove any trailing newline char
								address = int(patch.split("=")[0],16)
								payload = patch.split("=")[1]
								payloadbytes = bytes.fromhex(payload)
								romarray[address:address+int(len(payloadbytes))] = payloadbytes
								if args.v:
									print(hex(address), "=", payload)
							rom = romarray

			# form memory map and write it to the emulator core
			memorymap = b""
			formmemorymap(loROM,romSize)
			emulator[anchorfound+8:anchorfound+8+len(memorymap)] = memorymap
			
			# pad to snesRomPosition and add romdata
			emulator += b"\0" * (snesRomPosition - len(emulator)) + rom

			if args.v:
				print()
			else:
				print(db_match, romtitle)

			if args.outputfile and len(args.romfile) == 1:
				outputfile = args.outputfile
			else:
				outputfile = romtitle + ".gba"

			writefile(outputfile, emulator)

			if args.pat:
				# EZ-Flash IV fw2.x GSS patcher metadata to force 64KB SRAM saves - for PATCH folder on SD card
				patchname = os.path.splitext(outputfile)[0] + ".pat"
				patchdata = b'QlpoOTFBWSZTWRbvmZEAAAT44fyAgIAAEUAAAACIAAQAAAQESaAAVEIaaGRoxBKeqQD1GTJoks40324rSIskHSFhIywXzTCaqwSzf4exCBTgBk/i7kinChIC3fMyIA=='
				writefile(patchname, bz2.decompress(base64.b64decode(patchdata)))

			if args.sav:
				# EZ-Flash IV fw1.x blank save - for SAVER folder on SD card
				savename = os.path.splitext(outputfile)[0] + ".sav"
				saveempty = b"\xff" * SRAM_SAVE
				if not os.path.exists(savename): # careful not to overwrite an existing save
					writefile(savename, saveempty)

		else:
			raise Exception(f'unsupported filetype for compilation - {romfilename}')

	if args.v:
		print("press L+R+Start for the emulator menu")
		print("press L+R+Select+Up to cycle BG Priority Sets")
		print("press L+R+Select+Down to cycle Forced BG Modes")



