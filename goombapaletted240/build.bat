for %%f in (*.gb) do @goomba_compile.py "%%f" -o "%%~nf.gba" -e goomba_with_all_borders_and_palettes.gba -pat
