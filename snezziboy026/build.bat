for %%f in (*.sfc *.smc) do @snezziboy_compile.py "%%f" -o "%%~nf.gba" -pat %*
