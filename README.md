# EZ-Flash IV Exit-Patched Emulator Collection
This is a collection of emulators for the Gameboy Advance, SRAM-patched and exit-patched to function optimally with the EZ-Flash IV flashcart. Modern cross-platform compilation builder scripts are also included.

Emulator|Target System|Author(s)|1st Release
:-------|:------------|:--------|:---
[PocketNES 1-4-2020](https://github.com/Dwedit/PocketNES/releases)|Nintendo NES|Loopy, later FluBBa, Dwedit|Jan 2001?
[PCEAdvance 7.5](https://web.archive.org/web/20150430211123/http://www.ndsretro.com/gbadown.html)|NEC PC Engine / Super CD-ROM²|FluBBa|Apr 2003
[Goomba Paletted 2.40](http://goomba.webpersona.com)|Nintendo Gameboy|FluBBa|Oct 2003
[HVCA](https://www.gamebrew.org/wiki/HVCA_GBA)|Nintendo NES / Famicom Disk System|outside-agb?|Sep 2004
[Wasabi](https://github.com/FluBBaOfWard/WasabiGBA)|Watara Supervision|FluBBa|Nov 2004
[SNESAdvance 0.1f](https://web.archive.org/web/20080208234615/http://www.snesadvance.org/index.html)|Nintendo SNES|Loopy, FluBBa|Feb 2005
[SMSAdvance 2.5](https://web.archive.org/web/20150430211123/http://www.ndsretro.com/gbadown.html)|SEGA Master System / Game Gear / SG-1000|FluBBa|Jul 2005
[Cologne 0.8](https://web.archive.org/web/20150430211123/http://www.ndsretro.com/gbadown.html)|ColecoVision|FluBBa|Jan 2006
[Goomba Color 2019_5_4](https://www.dwedit.org/gba/goombacolor.php)|A Goomba fork to add Gameboy Color|FluBBa, Dwedit|Jan 2006
[MSXAdvance 0.2](https://github.com/patters-syno/msxadvance)|MSX-1 (*version 0.2 is most compatible*)|FluBBa|Mar 2006
[Murdoc 0.3](https://web.archive.org/web/20150430211123/http://www.ndsretro.com/gbadown.html)|Mr. Do! Arcade|Flubba|May 2006
[Snezziboy 0.26](https://sourceforge.net/projects/snezziboy/files/snezziboy%20%28binaries%2Bsource%29/v0.26/)|Nintendo SNES|bubble2k|May 2006
[NGPGBA 0.55](https://web.archive.org/web/20150430211123/http://www.ndsretro.com/gbadown.html)|SNK Neo Geo Pocket / NGP Color|Flubba|Jul 2008
[GhostsnGoblinsGBA 0.1](https://web.archive.org/web/20150430211123/http://www.ndsretro.com/gbadown.html)|Ghosts'n Goblins Arcade|Flubba|Apr 2009
[YieArKungFuGBA 0.1](https://web.archive.org/web/20150430211123/http://www.ndsretro.com/gbadown.html)|Yie Ar Kung-Fu Arcade|Flubba|Apr 2009
[Jagoomba 0.5](https://github.com/EvilJagaGenius/jagoombacolor/releases)|An enhanced Goomba Color fork|FluBBa, Dwedit, Jaga + various|Nov 2021

## Background
These emulators were originally designed to be used in a number of ways: 
1. assemble many game ROMs into a large ```.gba``` compilation and browse the games from a menu upon launch  
   - *slow to load into EZ-Flash PSRAM before execution, single 64KB SRAM save may constrain*  
2. as plugins for the Pogoshell file manager  
   - *only supports much older flashcart devices e.g. Flash2Advance*  
3. bundle each game ROM with its own copy of the emulator into a standalone ```.gba``` file  
   - *best for EZ-Flash IV - plenty of SD card storage, quick to load, can use save states since each game has its own 64KB of SRAM*  

## Purpose
This collection serves use case 3 above. In each emulator folder the build script will iterate through the ROMs in the current folder, building a ```.gba``` executable for each title. The build scripts invoke my own Python 3 [gba-emu-compilation-builders](https://github.com/patters-syno/gba-emu-compilation-builders) scripts, which may also serve use case 1 if required. Run the compile script with ```-h``` for more information.

Each emulator's Exit function in the L+R menu was typically intended for Pogoshell-era flashcarts. Where needed, this function has been manually patched so that Exit actually returns to the EZ-Flash IV menu.

## Usage
- Install Python 3 if not present
- ```git clone https://github.com/patters-syno/gba-ezflash-iv-emulators```
- Add games to the chosen emulator folder
- See notes on firmware versions below
- Run **build.bat** from a Command Prompt (Windows), or **build.sh** from a Terminal session (macOS / Linux)
- Copy the resulting ```.gba``` files to the EZ-Flash IV SD card

## EZ-Flash IV Versions
#### Firmware 2.x
- The build scripts will generate the required patch files to force 64KB SRAM saves for each executable, to be placed in the PATCH folder on the SD card.
- It is recommended that you disable the firmware's integrated GSS patcher (Global Soft-reset and Sleep) for the emulators. Add the following exclusions to the bottom of **KEYSET.CFG** at the root of your SD card:
  ```
  #GAMELIST TO SKIP GSS AUTOMATICALLY
  #EMULATORS
  COLG = 1   #Cologne
  GGAC = 1   #GhostsnGoblinsGBA
  GMBC = 1   #Goomba Color/Jagoomba
  GMBA = 1   #Goomba
  HVCA = 1   #HVCA
  MSXA = 1   #MSXAdvance
  MRDO = 1   #Murdoc
  NGPE = 1   #NGPGBA
  PCEA = 1   #PCEAdvance
  PNES = 1   #PocketNES
  SMSA = 1   #SMSAdvance
  SNAV = 1   #SNESAdvance
  SNZI = 1   #Snezziboy
  WSBI = 1   #Wasabi
  YIAC = 1   #YieArKungFuGBA
  ```
#### Firmware 1.x
- The ```.gba``` files produced by this collection are ready to be copied directly onto the SD card. Do not use the EZ4 Client to patch them.
- The emulators in this collection have all been header-patched to force 64KB SRAM saves, using cory1492's v2 patcher (EZ4-64-2). The 1.x firmware reads some metadata from the GBA ROM header to determine save size, and without this fix many homebrew binaries will default to 32KB.
- gbata7 was used to fix the GBA ROM header after these patches (emulators crash on some firmwares without this fix).
- You will need to edit **build.bat** (for Windows) and **build.sh** (for macOS and Linux) to change the compile script options from ```-pat``` to ```-sav``` so that the blank save files are generated for each executable, to be placed in the Saver folder on the SD card.

## Exit-Patching Method
Each of the emulators uses some variation of the **visoly.s** source file which was designed to exit back to early flash card menus or Pogoshell. Since they are not identical, it is not trivial to make a binary patcher. The following sample files are included to facilitate patching additional binaries:
File|Description
:---|:----------
ez4/reset_ez4.s|Code to reset into ez4 loader; copies itself into ewram before running
ez4/reset_ez4.bin|Binary to reset into ez4 loader
ez4/reset_ez4-2.s|Code to reset into ez4 loader; switches from arm to thumb and runs in-place
ez4/reset_ez4-2.bin|Binary to reset into ez4 loader
ez4/visoly.s|Code to reset, as used in many of FluBBa's emulators
ez4/visoly.bin|Binary to reset, as used in many of FluBBa's emulators

My own method for patching additional emulators was to check that their **visoly.s** was indeed mostly consistent with the versions in other emulator source code. Then I used a hex editor to compare exit-patched emulator binaries with their unpatched originals so I could determine the initial state of the replaced section (usually **visoly.bin**).

I found that by progressively trimming both ends of this sequence, I was able to successfully locate the equivalent section in the new binary, even if there were sometimes minor differences. Then it was a case of selecting the most appropriately sized variant of the *reset_ez4* binary code to overwrite (usually **reset_ez4.bin**).

--------
## Emulator Tips
#### Cologne
- Find the BIOS rom with the no-delay patch to speed up the boot time: "ColecoVision BIOS (1982) (No Title Delay Hack)"
- R+Start to bring up the virtual controller keypad
#### MSXAdvance
- The BIOS you need is "MSX System v1.0 + MSX BASIC (1983)(Microsoft)[MSX.ROM]"
- R+Start to bring up the virtual keyboard
- Early [compatibility list](https://web.archive.org/web/20070612060046/http://boards.pocketheaven.com/viewtopic.php?t=3768)
- Versions 0.3 and 0.4 [significantly broke compatibility](https://gbatemp.net/threads/msxadvance-compatibility-many-games-in-gamelist-txt-dont-work.609615/)
#### PCEAdvance
- Audio tends to work pretty well in mixer mode, but you do need to restart the emulator after enabling it
- [CD-ROM ISO extracting info](https://github.com/patters-syno/pceadvance#pc-engine-cd-rom-support), and [this forum thread](https://gbatemp.net/threads/pceadvance-cd-rom-support-howto-required.610542/)
- [CD-ROM² / Super CD-ROM² / Arcade CD-ROM² titles lists, and TOCs](https://www.necstasy.net/)
- [Speedhacks howto](https://web.archive.org/web/20060508083011/http://boards.pocketheaven.com/viewtopic.php?t=27)
- EZ-Flash IV & EZ-Flash 3in1 PSRAM is now enabled for Super CD-ROM² support and, in theory, Arcade CD-ROM²
- CD-ROM ISOs should include 'CD', 'SCD', or 'ACD' in their filenames to indicate their type
#### SMSAdvance
- BIOS booting (effectively a blank 16KB ROM image) requires the system type to be hard set to Master System, assuming Master System BIOS games, because without a ROM the emulator cannot guess which system BIOS (SMS or GG) should be loaded
- "Lock toprows" is an option for Full Screen display mode useful for certain Master System games, such as Outrun, which can keeps the score/speedometer on screen despite cropping the image to the GBA resolution
#### SNESAdvance
- Start+Select+A+B for the emulator menu
- Select+Up/Down to change screen offset
- [List of best functioning games](https://web.archive.org/web/20050305113636/http://ygodm.tonsite.biz/snesadv/snesadv_gamelist.html)
#### Snezziboy
- L+R+Start for the emulator menu
- L+R+Select+Up to cycle BG Priority Sets
- L+R+Select+Down to cycle Forced BG Modes
- [Wiki page](https://web.archive.org/web/20090503124323/http://wiki.pocketheaven.com/Snezziboy)
- [Compatibility list](https://web.archive.org/web/20090508192702/http://wiki.pocketheaven.com/Snezziboy_Compatibility_List)
#### YieArKungFuGBA
- The emulator menu is broken unless you build a compilation with both ROM variants
#### HVCA
- Hold L+R in the menu to exit back to the flashcart menu
