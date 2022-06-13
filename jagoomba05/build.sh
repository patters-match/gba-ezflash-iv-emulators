#!/bin/bash

for file in *.gb *.gbc ; do ./goomba_compile.py "${file}" -o "${file%.*}.gba" -pat ; done

