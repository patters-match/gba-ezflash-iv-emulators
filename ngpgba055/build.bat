@for %%f in (*.ngp *.ngc) do @ngpgba_compile.py "%%f" -o "%%~nf.gba" -pat %*
