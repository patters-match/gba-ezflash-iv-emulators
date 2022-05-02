for %%f in (*.gb *.gbc) do @goomba_compile.py "%%f" -o "%%~nf.gba" -pat
