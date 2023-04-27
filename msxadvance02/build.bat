for %%f in (*.rom) do @msxadvance_compile.py "%%f" -o "%%~nf.gba" -pat %*
