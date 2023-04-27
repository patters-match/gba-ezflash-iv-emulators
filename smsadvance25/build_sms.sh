#!/bin/bash

for file in *.sms ; do ./smsadvance_compile.py "${file}" -o "${file%.sms}.gba" -pat  "$@"; done
