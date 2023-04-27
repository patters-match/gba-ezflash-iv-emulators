for %%f in (*.pce *.iso) do @pceadvance_compile.py "%%f" -o "%%~nf.gba" -pat %*
