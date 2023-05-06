@for %%f in (*.sna *.z80) do @zxadvance_compile.py "%%f" -o "%%~nf.gba" -pat %*
