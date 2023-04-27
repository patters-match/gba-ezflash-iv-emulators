#!/bin/bash

for file in *.rom ; do ./msxadvance_compile.py "${file}" -o "${file%.rom}.gba" -pat "$@" ; done

