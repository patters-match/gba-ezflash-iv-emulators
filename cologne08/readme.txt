Cologne V0.8
--------------------------------------------------------------------------------
This is a Coleco Vision emulator for the GBA.
It was just a quick and dirty hack from SMSAdvance.

Features:
 A lot of games can actually be played.

Missing:
 Several different controllers.
 Not all keys are mapped to the GBA.
 Correct sprite collision and overflow.
 Screen modes 1 & 3.

Bugs:
 Some games freze/crash.

--------------------------------------------------------------------------------
How to use:
--------------------------------------------------------------------------------
!!! You must supply a BIOS to be able to run games !!!
Run Cologne.exe to add roms to the emulator.
Use the Bios tick box to add a BIOS.
Do no overwrite the original .gba file!

When the emulator starts, use Up/Down to select game, then use
B or A to start the game selected.
Press L+R to open the menu, A to choose, B (or L+R again) to cancel.
Press R+Start to show the virtual Coleco Joystick, press R+Start to leave.

--------------------------------------------------------------------------------
Menu:
--------------------------------------------------------------------------------
Controller:
	Autofire: Select if you want autofire.
	Controller: 2P control player 2.
	Swap A/B: Swap which GBA button is mapped to which Coleco fire button.
	Map L to: Lets you map the L button to any Coleco keypad button.
	Map R to: Lets you map the R button to any Coleco keypad button.
	Map Start to: Lets you map the Start button to any Coleco keypad button.
	Map Select to: Lets you map the Select button to any Coleco keypad button.

Display:
	Display: Here you can select if you want scaled or unscaled screenmode.
		Unscaled mode:  L & R buttons scroll the screen up and down.
		Scaled modes:  Press L+SELECT to adjust the background.
	Scaling: Here you can select if you want flicker or barebones lineskip.
	Gamma: Lets you change the gamma ("brightness").
	Perfect sprites: Uses a lot of cpu, only use when really necessary.
	Disable background: Turn on/off background rendering.
	Disable sprites: Turn on/off sprite rendering.

Other Settings:
	VSync: Switch between speed modes, can also be toggled with L+START.
		On: Will wait for the next vsync if needed, best for most games.
		Force: Can help with graphics in some games, often slow.
		Off: Can speed up some games if they don't allready use all cpu time.
		Slowmo: Good for beating that extra fast game.
	FPS_Meter: Toggle fps meter.
	Autosleep: Change the autosleep time, also see Sleep.
	EWRAM Speed: Use with caution!
	Fake spritecollision: Some games require this.
	TV Type: Change the video standard.

Help:
	Some dumb info...

Link Transfer:
	Lets you transfer small games to other GBAs, also see the advanced topic.

Go Multiboot:
	You can use the Go Multiboot feature to force the game to run in multiboot
	mode. Useful if you want to boot someone else up and eject the cartridge.
	Do not eject cartridges from a GameBoy Player.

Sleep: Put the GBA into sleepmode.
	START+SELECT wakes up from sleep mode (activated from this menu or from
	5/10/30	minutes of inactivity).

Restart: Lets you select a new game.

Exit: Let's you exit the emulator back to Pogo or the FA/F2A menu.

--------------------------------------------------------------------------------

--------------------------------------------------------------------------------
Advanced:
--------------------------------------------------------------------------------
EWRAM speed: this changes the waitstate on EWRAM between 2 and 1, this
can probably damage your GBA and definitly uses more power,
around 10% speedgain. Use at your own risk!

Link transfer:  Send a Coleco game to another GBA.  The other GBA must be in
  multiboot receive mode (no cartridge inserted, powered on and waiting with
  the "GAME BOY" logo displayed). Only one game can be sent at a time.
  A game can only be sent to 1 (one) Gameboy at a time, disconnect all other
  gameboys during transfer.

Use an original Nintendo cable!

Pogoshell:
Add an empty file and a BIOS.
Copy col.gba to the plugin folder (or compress it to mbz before you copy
 it) then rename it to cologne.bin and add this line to the pogo.cfg file:
col 1 cologne.bin 2
rom 1 cologne.bin 2
or
col 1 cologne.mbz 2
rom 1 cologne.mbz 2


--------------------------------------------------------------------------------
Credits:
--------------------------------------------------------------------------------
Huge thanks to Loopy for the incredible PocketNES and the builder, without it
this emu would probably never have been made.
Thanks to:
Reesy for help with the Z80 emu core.
Some MAME people + Maxim for the SN76496 info.
Sean Young for the TMS9918 info.
Charles MacDonald (http://cgfm2.emuviews.com/) for more VDP info.
Ghislain "cador" for the splashscreen.
rvchipie7 (?) for inspiration for the virtual joystick.

-------------------------------
Fredrik Olsson
FluBBa@passagen.se
http://hem.passagen.se/flubba/gba.html
http://www.gbaretro.com/
-------------------------------

