for %%f in (*.sv) do @wasabi_compile.py "%%f" -o "%%~nf.gba" -pat %*
