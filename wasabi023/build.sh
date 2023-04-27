#!/bin/bash

for file in *.sv ; do ./wasabi_compile.py "${file}" -o "${file%.*}.gba" -pat "$@" ; done
