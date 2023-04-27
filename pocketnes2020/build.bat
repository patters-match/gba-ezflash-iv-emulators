@for %%f in (*.nes) do @pocketnes_compile.py "%%f" -o "%%~nf.gba" -pat %*
