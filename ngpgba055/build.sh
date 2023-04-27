#!/bin/bash

for file in *.ngp *.ngc ; do ./ngpgba_compile.py "${file}" -o "${file%.*}.gba" -pat "$@" ; done

