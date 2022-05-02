#!/bin/bash

for file in *.gb ; do ./goomba_compile.py "${file}" -o "${file%.gb}.gba" -e goomba_with_all_borders_and_palettes.gba -pat ; done

