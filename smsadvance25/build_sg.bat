@for %%f in (*.sg) do @smsadvance_compile.py "%%f" -o "%%~nf.gba" -pat %*
