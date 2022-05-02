#!/bin/bash

for file in *.sg ; do ./smsadvance_compile.py "${file}" -o "${file%.sg}.gba" -pat ; done
