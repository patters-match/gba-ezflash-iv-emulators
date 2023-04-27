#!/bin/bash

for file in *.col *.rom ; do ./cologne_compile.py "${file}" -o "${file%.*}.gba" -pat "$@" ; done
