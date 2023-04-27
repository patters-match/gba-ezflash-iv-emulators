#!/usr/bin/python3

# Place disksys.rom in the same folder as this script

import os
import glob
import subprocess
import sys

file_list = glob.glob(os.path.join('add', '*.fds')) + glob.glob(os.path.join('add', '*.nes'))

for file_path in file_list:
    file_name, file_ext = os.path.splitext(os.path.basename(file_path))
    out_name = file_name.split(' (', 1)[0]

    cfg_path = os.path.join('add', '{}.cfg'.format(file_name))
    output_path = os.path.join('add', '{}.gba'.format(out_name))

    if os.path.exists(cfg_path):
        subprocess.call([sys.executable, 'hvca_compile.py', file_path, cfg_path, '-x', os.path.join('bin', 'flash_ez4_ezo.sub'), '-o', output_path, '-c', '-pat'])
    else:
        subprocess.call([sys.executable, 'hvca_compile.py', file_path, '-x', os.path.join('bin', 'flash_ez4_ezo.sub'), '-o', output_path, '-c', '-pat'])
