#!/bin/bash

for file in *.pce *.iso ; do ./pceadvance_compile.py "${file}" -o "${file%.*}.gba" -pat "$@" ; done
