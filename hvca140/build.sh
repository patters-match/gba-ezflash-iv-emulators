#!/bin/bash

# Place disksys.rom in the same folder as this script

for file in add/*.fds add/*.nes ; do
	out="${file/ \(*}" # strip brackets from name
	if [ -e "${file%.*}.cfg" ]; then
		./hvca_compile.py "${file}" "${file%.*}.cfg" -x "bin/flash_ez4_ezo.sub" -o "${out%.*}.gba" -pat
	else
		./hvca_compile.py "${file}" -x "bin/flash_ez4_ezo.sub" -o "${out%.*}.gba" -pat
	fi
done
