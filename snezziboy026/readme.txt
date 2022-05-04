Snezziboy User Guide
-----------------------------------------------------------

Contents

1. Licensing
2. About Snezziboy
3. File Manifest
4. How to use
5. Configuration Menu
6. Patch Data
7. Credits


1. Licensing
~~~~~~~~~~~~~~~~~~~~~

The Snezziboy Emulator ("Program") is:

Copyright (C) 2006 bubble2k

This program is free software; you can redistribute it and/or 
modify it under the terms of the GNU General Public License as 
published by the Free Software Foundation; either version 2 of 
the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, 
but WITHOUT ANY WARRANTY; without even the implied warranty of 
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the 
GNU General Public License for more details.

You should have received a copy of the GNU General Public 
License along with this program; if not, write to the Free 
Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, 
MA 02111-1307 USA


2. About Snezziboy
~~~~~~~~~~~~~~~~~~~~~

Snezziboy was inspired by the development of the SNES Emulator developed for
the Gameboy Advance system, commonly known as SNES Advance. Much credit must
be given to the authors of the SNES Advance emulator, FluBBa and Loopy, 
Without their daring effort in making the first emulator for the SNES on the
gameboy in the first place, it is unlikely that Snezziboy would have ever
existed. 

Snezziboy was also born out of a challenge that I wanted to take on to 
develop on an handheld, or an embedded system. The challenges were basic but
very huge for an emulator:
  - Small memory footprint
  - Slow speed

The general rule of thumb is that for any emulator to work with decent, the
machine that emulates the other should run about say, 10-20 times faster.
THe SNES was a 2.58MHz machine, while the Gameboy Advance was a 16.78 MHz
machine; only about 8 times faster in clock speed. Fortunately, the 
graphical capabilities, as FluBBa and Loopy had discovered, of the Gameboy
Advance were very similar to the SNES, therefore allowing an emulator to
exploity the Gameboy Advance hardware to accelerate the graphics processing.

The emulator is far from complete as of 12 May 2006, but it is already 
running some games at fairly decent speed, even though it is not running them 
at full. 

As at 28 May 2006, the following games are known to be working fairly well:
 - Castlevania X
 - Super Castlevania 4 (no mode 7 graphics yet)
 - Gradius 3
 - Megaman X
 - Megaman 7
 - Darius Twin
 - Super Mario World (some garbled/missing graphics)
 - SUper Mario All-Stars (Super Mario Bro, The Lost Worlds)
 - Kirby's Avalanche (some garbled graphics)
 - Tetris Attack

This emulator will be made open source, and by doing so, I hope to invite
competent developers to further enhance the project, and if possible help in
identifying and fixing bugs.


3. File Manifest
~~~~~~~~~~~~~~~~~~~~~

The following three files must be in the same folder:

   snezzi.dat       Patch data file in text format.
                    The file format of this file is exactly the same as
                    that of the superdat for SNES Advance.

   snezzi.gba       Emulation core for the Snezziboy.

   snezzi.exe       Builder to construct the .gba file for an SNES ROM
                    (Each SNES ROM will have exactly 1 gba file).


4. How to Use
~~~~~~~~~~~~~~~~~~~~~

1. Copy the SNES ROM file (.smc / .fig / .swc, etc) into the same folder
   as the snezzi.exe.

2. In the command line in a DOS box, issue the following command:
       snezzi SNESGAME.SMC 

   (Alternatively, in Windows Explorer, drag the SNESGAME.SMC file onto
   the snezzi.exe file)

3. An output file SNESGAME.SMC.gba will be created in the same folder as 
   the SNES ROM file.

4. Copy the SNESGAME.SMC.gba file into your flash cartridge as described
   in your flash cartridge manual, load it up into gameboy and run it.

   (For Supercard users, please run the .gba file through the Supercard
   patcher before playing. I recommend turning all options off except 
   "Compress").

5. During the game, use (L+R+start) to access the configuration menu.


6. Configuration Menu
~~~~~~~~~~~~~~~~~~~~~

The configuration menu has the following options:

   a. BG0         The priority of the first background layer.
                  P0 - front-most
                  P1 - behind P0
                  P2 - behind P1
                  P3 - rear-most

   b. BG1         The priority of the second background layer. 
                  (options are the same as BG0)

   c. BG2         The priority of the second background layer. 
                  (options are the same as BG0)

   d. BG3         The priority of the second background layer. 
                  (options are the same as BG0)

   e. CTRL        This indicates the CTRL key that can be used
                  to input the additional SNES X/Y keys. When used
                  in combination with the GBA A/B keys, we can input
                  the full X/Y/A/B keys into the game.

                  START  - use the start button as the CTRL key
                  SELECT - use the start button as the CTRL key
                  L      - use the start button as the CTRL key
                  R      - use the start button as the CTRL key

                  If you are still confused, think of it as a 
                  "SHIFT" key that allows you to shift button A 
                  to button X, for example.

   f. BUTTON A    This indicates the key(-combination) to you should
                  press in order to input the SNES button A.

                  A      - the GBA A button
                  B      - the GBA B button
                  CTRL A - the GBA A button + the CTRL key above
                  CTRL B - the GBA B button + the CTRL key above

   g. BUTTON B    (same as button A)

   h. BUTTON X    (same as button A)

   i. BUTTON Y    (same as button A)

   j. BACKDROP    This allows the SNES game to display a backdrop 
                  color. Not all games like this option, and may 
                  exhibit flickers in the background, due to the
                  difference in the way the SNES and the GBA 
                  handles backdrop colors in hardware.

                  YES    - yes, show backdrop color
                  NO     - no, do not show backdrop color

                  So far only Super Mario World is known to 
                  produce the effect as intended with the backdrop
                  set to YES.

    k. BG ENABLE  This allows the VRAM allocation for graphics to
                  switch between two algorithms when backgrounds
                  are enabled / disabled.
                  FAST  - Fast, but no refresh of tiles. May cause
                          certain graphical glitches.
                  SMART - (Slightly) Smarter, but slow since it
                          refreshes everytime the game 
                          enables/disabless the BG.

    l. BG FORCED MODE
                  Forces the game to display the graphics in the
                  specific SNES mode. This may be needed by certain
                  games that switch between two modes in the same 
                  frame; but Snezziboy chooses to display only
                  one of them.
                  
                  Set to AUTO to use one of whatever the game 
                  specifies for a frame.

    m. HDMA ENABLE 
                  Set to YES to allow the game to emulate HDMA. This
                  may cause games to slowdown on the GBA whenever it 
                  uses HDMA, but some games must require HDMA before 
                  its backgrounds are properly viewable. 
                  Set to NO to disable all HDMA emulation. 
                  

    y. RETURN TO GAME
                  Returns to the game. Pressing start in the 
                  configuration screen also returns you to the game

    z. RESET GAME
                  Does a "hard reset" on the emulator and returns
                  the game to the start. 
    

6. Patch Data
~~~~~~~~~~~~~~~~~~~~~

The Patch Data file (snezzi.dat) contains a list of SNES ROMs and patch
values either to bypass copy protection locks, or for speed hacks.

The format of the Patch Data is exactly the same as SNES Advance's 
superdat, but not all fields defined are used by Snezziboy. Each field
is delimited by a pipe symbol, that is, '|' and the semantics of the
fields that the Snezziboy Builder understands are:

   Field #1  : CRC32 Checksum of the SNES ROM
   Field #2  : Game name
   Last Field: Patch information

The rest of the fields between Field #2 and the Last Field are ignored
entirely.

The patch information takes the following format:
   Address1=Byte1Byte2Byte3Byte4...,Address2=Byte1Byte2....,

For example, the following patch information
   1C7=428A,1080=EAEAEA
tells Snezziboy to:
   patch the SNES ROM at 1C7, 1C8 with the bytes 42 and 8A.
   patch the SNES ROM at 1080, 1081, 1082 with the bytes EA, EA, EA

If the checksum of your SNES ROM does not match that in the patch data
file, the Snezziboy Builder will not patch it. 


7. Credits
~~~~~~~~~~~~~~~~~~~~~

Flubba, Loopy		For their bold attempt in SNES emulation on the GBA.
anomie			For the SNES documentation on IO registers and timings.
ZSNES Team		For their ZSNES emulator
Snes9x Team		For their Snes9x emulator
