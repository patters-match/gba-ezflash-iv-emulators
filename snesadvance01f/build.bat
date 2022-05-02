for %%f in (*.sfc *.smc) do @snesadvance_compile.py "%%f" -o "%%~nf.gba" -pat
