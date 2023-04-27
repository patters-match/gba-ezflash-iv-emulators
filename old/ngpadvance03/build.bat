for %%f in (*.ngp *.ngc) do @ngpadvance_compile.py "%%f" -o "%%~nf.gba" -pat
