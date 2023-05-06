#!/bin/bash

for file in *.sna *.z80 ; do ./zxadvance_compile.py "${file}" -o "${file%.*}.gba" -pat "$@" ; done
