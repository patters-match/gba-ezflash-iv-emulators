#!/bin/bash

for file in *.ngp ; do ./ngpadvance_compile.py "${file}" -o "${file%.ngp}.gba" -pat ; done

