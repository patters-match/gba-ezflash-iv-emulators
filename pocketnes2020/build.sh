#!/bin/bash

for file in *.nes ; do ./pocketnes_compile.py "${file}" -o "${file%.nes}.gba" -pat ; done

