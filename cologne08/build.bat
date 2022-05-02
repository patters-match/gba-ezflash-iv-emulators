for %%f in (*.col *.rom) do @cologne_compile.py "%%f" -o "%%~nf.gba" -pat
