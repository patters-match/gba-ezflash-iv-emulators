  YieArGBA V0.1
--------------------------------------------------------------------------------
This is a Yie Ar KUNG-FU - Arcade emulator for the GBA.
Everything seem to work except flipscreen and speech.
You should still be able to enjoy the game though. =)

--------------------------------------------------------------------------------
How to use:
--------------------------------------------------------------------------------
First unzip yiear.zip (and yiear2.zip if you want) into the
same folder as the emulator.* Then run one of the .bat files to compile the
roms and the emulator.

When the emulator starts, use Up/Down to select game, then use
B or A to start the game selected.
Press L+R to open the menu, A to choose, B (or L+R again) to cancel.

Controller: 2P is only used to start a 2 player game.
Unscaled mode:  L & R buttons scroll the screen up and down.
Scaled modes:  Press R+SELECT to adjust the background.
Speed modes:  R+START switches between throttled/unthrottled/slomo mode.

Sleep:  START+SELECT wakes up from sleep mode (activated from menu or 5/10/30
minutes of inactivity)

Make sure your flashing software allocates 8kByte/64kbit SRAM for SonSonGBA.

*filenames are taken from MAME 130
--------------------------------------------------------------------------------
Advanced:
--------------------------------------------------------------------------------
EWRAM speed: this changes the waitstate on EWRAM between 2 and 1, this
can probably damage your GBA and definitly uses more power,
around 10% speedgain. Use at your own risk!

Link transfer*:  Send SonSon to another GBA.  The other GBA must be in
  multiboot receive mode (no cartridge inserted, powered on and waiting with
  the "GAME BOY" logo displayed).  Only one game can be sent at a time. A game
  can only be sent to 1 (one) Gameboy at a time, disconnect all other gameboys
  during transfer.

Use an original Nintendo cable!

Pogoshell*:
You can use the "build_pogoyiear.bat" to compile only
the roms and use the emulator as a plugin in Pogo.
Copy the plugin (or compress it to mbz before you copy it) then add this line to
the pogo.cfg file:
yie 1 YieAr.gba 2
or
yie 1 YieAr.mbz 2

* Link and Pogo are untested, probably doesn't work.
--------------------------------------------------------------------------------
Credits:
--------------------------------------------------------------------------------
Huge thanks to Loopy for the incredible PocketNES, without it this emu would
probably never have been made.
Thanks to:
Enrique Sanchez, for the MAME driver.


-------------------------------
Fredrik Olsson
FluBBa@passagen.se
www.ndsretro.com / www.gbaretro.com
-------------------------------

