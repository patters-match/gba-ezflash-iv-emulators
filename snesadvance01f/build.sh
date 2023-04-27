#!/bin/bash

for file in *.sfc *.smc ; do ./snesadvance_compile.py "${file}" -o "${file%.*}.gba" -pat "$@" ; done

