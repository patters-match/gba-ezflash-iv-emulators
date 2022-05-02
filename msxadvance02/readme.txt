MSXAdvance V0.4
--------------------------------------------------------------------------------
This is a MSX1 emulator for the GBA.
It was just a quick and dirty hack from Cologne.

Features:
 A lot of games can actually be played.

Missing:
 Not all keys are mapped to the GBA.
 Correct sprite collision and overflow.
 Screen mode 3.
 Savestates.

Bugs:
 Screen mode 1 is not correct.
 The sound sucks.
 Probably a lot more.

--------------------------------------------------------------------------------
How to use:
--------------------------------------------------------------------------------
!!! You must supply a BIOS to be able to run games !!!
Run MSXAdvance.exe to add roms to the emulator.
Use the Bios tick box to add a BIOS.
A freely available Bios can be found at http://cbios.sourceforge.net/

When the emulator starts, use Up/Down to select game, then use
B or A to start the game selected.
Press L+R to open the menu, A to choose, B (or L+R again) to cancel.

Default in-game controlls:
	D-Pad:	Joystick.
	A & B:	Fire buttons.
	L:		0.
	R:		1.
	Start:	2.
	Select:	3.
	R+Start:Bring up Keyboard.

Controller->: Settings for controller
	Controller: 1P=Joystick1, 2P=Joystick2, Cursor=Keyboard cursor keys.
	Remapping: Use joypad to select key and press A to confirm.
Display->: Settings for the display
	Unscaled mode:  L & R buttons scroll the screen up and down.
	Scaling modes:
		Hard:   Every 6th scanline is skipped.
		Normal: Every 5th & 6th scanline is blended equally.
		Soft:   All lines are blended differently. !Experimental!
	Scaled modes:  Press L+SELECT to change which lines are skipped/blended.
Other->: Misc settings
	Speed modes:  L+START switches between throttled/unthrottled/slomo mode.
	Sleep:  START+SELECT wakes up from sleep mode (activated from menu or 5/10/30
		minutes of inactivity)


--------------------------------------------------------------------------------
Advanced:
--------------------------------------------------------------------------------
EWRAM speed: this changes the waitstate on EWRAM between 2 and 1, this
can probably damage your GBA and definitly uses more power,
around 10% speedgain. Use at your own risk!

Link transfer:  Send a MSX game to another GBA.  The other GBA must be in
  multiboot receive mode (no cartridge inserted, powered on and waiting with
  the "GAME BOY" logo displayed). Only one game can be sent at a time, and
  only if it's small enough to send (approx. 128kB or less). A game can only
  be sent to 1 (one) Gameboy at a time, disconnect all other gameboys during
  transfer.

Use an original Nintendo cable!

Pogoshell:
Add an empty file and a BIOS.
Copy msx.gba to the plugin folder then rename it to msxadvance.mb
(or compress it to .mbz)  and add this line to the pogo.cfg file:
rom 1 msxadvance.mb 2
or
rom 1 msxadvance.mbz 2


--------------------------------------------------------------------------------
Credits:
--------------------------------------------------------------------------------
Huge thanks to Loopy for the incredible PocketNES and the builder, without it
this emu would probably never have been made.
Thanks to:
Reesy for help with the Z80 emu core.
Some MAME people for the AY38910 info.
Sean Young for the TMS9918 info.
Charles MacDonald (http://cgfm2.emuviews.com/) for more VDP info.

-------------------------------
Fredrik Olsson
FluBBa@passagen.se
http://hem.passagen.se/flubba/gba.html
-------------------------------

