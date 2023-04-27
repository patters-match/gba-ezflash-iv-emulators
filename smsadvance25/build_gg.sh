#!/bin/bash

for file in *.gg ; do ./smsadvance_compile.py "${file}" -o "${file%.gg}.gba" -pat "$@" ; done
