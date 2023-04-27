#!/bin/bash

for file in *.ngp *.ngc ; do ./ngpadvance_compile.py "${file}" -o "${file%.*}.gba" -pat ; done

