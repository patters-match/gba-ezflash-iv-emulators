# EZ-Flash IV Exit-Patched Emulator Collection
This is a collection of emulators for the Gameboy Avdance, SRAM- and exit-patched to function optimally with the EZ-Flash IV flashcart.

Emulator|Target System|Author(s)|Released
:-------|:------------|:--------|:---
[PocketNES 1-4-2020](https://github.com/Dwedit/PocketNES/releases)|Nintendo NES|Loopy, later FluBBa, Dwedit|Jan 2001?
[PCEAdvance 7.5](https://web.archive.org/web/20150430211123/http://www.ndsretro.com/gbadown.html)|NEC PC Engine|FluBBa|Apr 2003
[Goomba Paletted 2.40](http://goomba.webpersona.com)|Nintendo Gameboy|FluBBa|Oct 2003
[SNESAdvance 0.1f](https://web.archive.org/web/20080208234615/http://www.snesadvance.org/index.html)|Nintendo SNES|Loopy, FluBBa|Feb 2005
[SMSAdvance 2.5](https://web.archive.org/web/20150430211123/http://www.ndsretro.com/gbadown.html)|SEGA Master System, Game Gear, SG-1000|FluBBa|Jul 2005
[Cologne 0.8](https://web.archive.org/web/20150430211123/http://www.ndsretro.com/gbadown.html)|ColecoVision|FluBBa|Jan 2006
[Goomba Color 2019_5_4](https://www.dwedit.org/gba/goombacolor.php)|a Goomba fork to add Gameboy Color|Dwedit|Jan 2006
[MSXAdvance 0.2](https://web.archive.org/web/20150430211123/http://www.ndsretro.com/gbadown.html)|MSX-1 (*version 0.2 is most compatible*)|FluBBa|Mar 2006
[NGPAdvance 0.3](https://web.archive.org/web/20150430211123/http://www.ndsretro.com/gbadown.html)|SNK Neo Geo Pocket / NGP Color|Flubba|Jul 2008
[Jagoomba 0.4a](https://github.com/EvilJagaGenius/jagoombacolor/releases)|enhanced Goomba Color fork|Jaga|Nov 2021

## Purpose
These emulators were originally designed to be used in a number of ways. You could:
1. assemble many ROMs into a large compilation and browse the games from a menu upon launch
2. use the emulator as a plugin for the Pogoshell file manager, which supported older flashcart devices e.g. Flash2Advance
3. bundle each ROM with its own copy of the emulator

The EZ-Flash flashcart copies ```.gba``` files to its interal PSRAM before execution which can be quite slow for large emulator compilations. Since the whole compilation must share the 64KB SRAM save this can get quite contended, particularly for those emulators which support save states.

On an EZ-Flash IV device the SD card means storage is cheap, so option 3 is the optimal choice. This allows fast loading of games and, provided the exit menu function works, easy navigation to the next one without having to power cycle the GBA.

Where needed, these emulator binaries have been manually exit-patched so that the L+R Exit menu option returns to the EZ-Flash IV menu. To be very clear, the exit patch does *not* enable L+Up+A+B at any time. Nor does it attempt to apply a Start+Select+A+B reset patch. It is meant solely to allow the emulator Exit menu option to function correctly.

## Usage
This compilation leverages my Python 3 [gba-emu-compilation-builders](https://github.com/patters-syno/gba-emu-compilation-builders), invoked by **build.bat** (for Windows) and **build.sh** (for macOS and Linux) to iterate through the ROMs in the current folder building a ```.gba``` executable for each.

## EZ-Flash Versions
#### Firmware 1.x
- Don't use the EZ Flash client to patch the resulting compilations. A major point of this collection is to avoid having to constantly patch.
- The emulators in this collection have all been header-patched to force 64KB SRAM saves, using cory1492's v2 patcher (EZ4-64-2). The 1.x firmware reads some metadata from the GBA ROM header to determine save size, and without this fix many homebrew binaries will default to 32KB.
- gbata7 was used to fix the GBA ROM header after these patches (emulators crashed on some firmwares without this fix).
- You will need to edit build.bat (for Windows) and build.sh (for macOS and Linux) to change the compile script options from ```-pat``` to ```-sav``` so that the blank save files are generated for each executable
#### Firmware 2.x
- The build scripts will generate the required patch files to force 64KB SRAM saves for each executable, to be placed in the PATCH folder on the SD card.
- It is recommended that you disable GSS (Global Softreset and Sleep Patch). Change this line in KEYSET.CFG at the root of your SD card:
  ```DISABLE_GSS = 1``` (From 0 to 1)
  Or if you prefer to keep GSS, here is a list of exclusions to add (Add the following to the bottom of the file):
  ```
  #GAMELIST TO SKIP GSS AUTOMATICALLY
  #EMULATORS
  COLG = 1   #Cologne
  GMBC = 1   #Goomba Color/Jagoomba
  GMBA = 1   #Goomba
  MSXA = 1   #MSXAdvance
  NGPA = 1   #NGPAdvance
  PCEA = 1   #PCEAdvance
  PNES = 1   #PocketNES
  SMSA = 1   #SMSAdvance
  SNAV = 1   #SNESAdvance
  ```

## Included Files
* Updated emulators, SRAM and exit-patched in the following folders:

cologne08/               Cologne v0.8
goombapaletted240/       Goomba Paletted v2.40 (Kuwanger's Fork)
jagoomba0.4a/            Jagoomba fork of Goomba Color 2019_5_4 with support for additional games
msxadvance02/            MSXAdvance v0.2 (this is by far the most compatible and stable version, despite 0.3 & 0.4)
                         open source BIOS replacement (cbios021.bin), newer versions not working
ngpadvance03/            NGPAdvance v0.3
pceadvance75/            PCEAdvance v7.5 with CD-ROM support
                         PCEAdvance v7.5 EZ3 version with Super CD-ROM support (apparently not working on EZ4)
pocketnes2020/           PocketNES 1-4-2020 (Dwedit's Fork)
                         PocketNES Menu Maker database (pnesmmw.mdb)
smsadvance250/           SMSAdvance v2.5
snesadvance01f/          SNESAdvance 0.1f (this emulator has no exit option to patch)
                         SNESAdvance 0.1f Secret of Mana font fix version, with save to skip crash issue
                         SuperDAT (snesadvance.dat)
                         snesadvance.dat from Snes9x4D (snesadvance2.dat) with metadata for additional titles
old/                     Goomba Color 2019_5_4, menu date updated (incorrect in official release)
                         Goomba Color 2014_12_14
                         MSXAdvance v0.1
                         MSXAdvance v0.3 (significantly worse compatibility than 0.2)
                         MSXAdvance v0.4 (significantly worse compatibility than 0.2)
                         PocketNES 7-1-2013 (Dwedit's Fork)
                         PocketNES v9.98

* Builder scripts (in the emulator folders)

cologne_compile.py       python 3 program to create a .gba file from cologne, a Coleco bios, and Coleco ROM
goomba_compile.py        python 3 program to create a .gba file from jagoomba/goomba/goombacolor and a GB/GBC ROM
msxadvance_compile.py    python 3 program to create a .gba file from msxadvance, an MSX1 bios, and MSX ROM
ngpadvance_compile.py    python 3 program to create a .gba file from ngpadvance, and a Neo Geo Pocket ROM
pceadvance_compile.py    python 3 program to create a .gba file from pceadvance, and a PC Engine ROM/ISO
pocketnes_compile.py     python 3 program to create a .gba file from pocketnes and an NES ROM
smsadvance_compile.py    python 3 program to create a .gba file from smsadvance and a SMS/GG/SG-1000 ROM
snesadvance_compile.py   python 3 program to create a .gba file from snesadvance and a SMC/SFC ROM
build.bat                batch script to create a .gba file for each ROM in the folder (for Windows)
build.sh                 bash script to create a .gba file for each ROM in the folder (for macOS and Linux)
old/python2/             old python2 compile scripts

* Example source and compiled binary code for the EZ Flash IV reset (exit) function

ez4/reset_ez4.bin        Binary to reset into ez4 loader
ez4/reset_ez4.s          Code to reset into ez4 loader; copies itself into ewram before running
ez4/reset_ez4-2.bin      Binary to reset into ez4 loader
ez4/reset_ez4-2.s        Code to reset into ez4 loader; switches from arm to thumb and runs in-place
ez4/visoly.s             Visoly.s, ripped from an older version of pocketnes
ez4/EZ Flash IV help.txt Release notes for the EZ Flash IV firmware 2.xx - useful to keep on the SD card as a
                         reminder of the various EZ Flash IV button combos
ez4/emupatch.pat         Pre-made patcher metadata file to force 64KB SRAM saves (for EZ-Flash 4 firmware 2.xx)
                         A copy to be placed in /PATCH/ for each .gba file (the compile scripts create these)

* Tools folder includes the original Windows-only menu makers and tools used for patching emulators for saving
tools/
binary_encode.py         script to bzip2 compress and then base64 encode binary data for inclusion in other scripts
CologneBin.zip           Cologne Menu Maker
EZ4-64-2.zip             cory1492's v2 EZ-IV SRAM 64k Patcher
gbata7a-en.zip           GBA Tool Advance (used to fix headers/ commonly used to remove ROM intros)
goombafront.zip          Goomba/Goomba Color Menu Maker
MSXAdvanceBin.zip        MSXAdvance Menu Maker
NGPAdvanceBin.zip        NGPAdvance Menu Maker
PCEAdvanceBin.zip        PCEAdvance Menu Maker
pnesmmw12a.zip           PocketNES Menu Maker
SMSAdvanceBin.zip        SMSAdvance Menu Maker
SNESAdvanceBin.zip       SNESAdvance Menu Maker


More about visoly.s and exit patching
-------------------------------------

Between each of the various emulators, every one uses some variation of the visoly.s file.  Because they're not
identical, it's not trivially possible to make a search/replace binary patcher. Instead, the visoly.s is included
for those adventurous enough to arm disassemble one of the emulators and compare against the visoly.s to figure
out where init_flashcart is.  This is where the exit code is patched at.


Emulator tips
-------------

Cologne     - find the BIOS ROM with the no-delay patch to speed up the boot time: "ColecoVision BIOS (1982) (No
              Title Delay Hack)"
            - R+Start to bring up the virtual controller keypad
MSXAdvance  - the BIOS you need is "MSX System v1.0 + MSX BASIC (1983)(Microsoft)[MSX.ROM]"
            - R+Start to bring up the virtual keyboard
            - the emulator does not auto-select the correct mappper. You often need to change this (typically to
              Konami5) in Other Settings and restart the emulator for it to take effect
            - see https://web.archive.org/web/20070612060046/http://boards.pocketheaven.com/viewtopic.php?t=3768
                  https://gbatemp.net/threads/msxadvance-compatibility-many-games-in-gamelist-txt-dont-work.609615/
PCEAdvance  - audio tends to work pretty well in mixer mode, but you do need to restart the emulator after
              enabling it
            - For CD-ROM ISO tips see here:
              https://gbatemp.net/threads/pceadvance-cd-rom-support-howto-required.610542/
            - CD-ROM / Super CD-ROM titles list here:
              https://gamicus.fandom.com/wiki/List_of_PC-Engine_CD-ROM²_video_games
SMSAdvance  - BIOS booting (effectively a blank 16KB ROM image) requires the system type to be hard set to Master
              System, assuming Master System BIOS games, because without a ROM the emulator cannot guess which
              system BIOS (SMS or GG) should be loaded
SNESAdvance - Start+Select+A+B for the emulator menu
            - Select+Up/Down to change screen offset
            - see https://web.archive.org/web/20050305113636/http://ygodm.tonsite.biz/snesadv/snesadv_gamelist.html
