NGPAdvance V0.3
--------------------------------------------------------------------------------
This is a SNK NeoGeo Pocket Color emulator for the GBA.

Features:
	Can play most games.

Missing:
	Lots of stuff.

--------------------------------------------------------------------------------
How to use:
--------------------------------------------------------------------------------
Run NGPAdvance.exe to add roms to the emulator, you can also add a real bios.
Do no overwrite the original .gba file!

When the emulator starts, use Up/Down to select game, then use
B or A to start the game selected.
Press L+R to open the menu, A to choose, B (or L+R again) to cancel.

On the NeoGeo Pocket button A is to the left and button B is to the right,
I've mapped this so the left button (A) from the NeoGeo Pocket is the left button
on the GBA (B), you can switch this in the menu.
--------------------------------------------------------------------------------
Menu:
--------------------------------------------------------------------------------
Controller:
	Autofire: Select if you want autofire.
	Controller: 2P control player 2, Link is used to linkup 2 GBAs.
	Swap A/B: Swap which GBA button is mapped to which NGP button.

Display:
	Gamma: Lets you change the gamma ("brightness").
	Border: doesn't work yet.
	Palette: Choose which palette to use for mono games.
	Disable foreground: Turn on/off foreground rendering.
	Disable background: Turn on/off background rendering.
	Disable sprites: Turn on/off sprite rendering.

Other Settings:
	VSync: Switch between speed modes, can also be toggled with L+START.
		On: Will wait for the next vsync if needed, best for most games.
		Force: Can help with graphics in some games, often slow.
		Off: Can speed up some games if they don't allready use all cpu time.
		Slowmo: Good for beating that extra fast game.
	FPS-Meter: Toggle fps meter.
	Autosleep: Change the autosleep time, also see Sleep.
	EWRAM Speed: Use with caution!
	Machine: NeoGeoPocketColor should work for most games.
	Language: Switch language settings for the NeoGeo Pocket.
	Speedhacks: Turn on/off speedhacks.
	Z80: Turn the emulation of the Z80 on/off.
	Change batteries: Change batteries in the NGP.
	Change sub battery: Change the clock battery in the NGP.
	Use BIOS: doesn't work yet.
	CPU speed: Set the CPU speed of the NeoGeo Pocket,
		this doesn't lock the cpu speed, the games can still change it.

Help:
	Some dumb info...

Save Manager:
	Save SRAM: Save the SRAM for the current game (it's automaticly loaded).
	Manage savememory: Lets you erase SRAM (for now).

Sleep: Put the GBA into sleepmode.
	START+SELECT wakes up from sleep mode (activated from this menu or from
	5/10/30	minutes of inactivity).

Restart: Lets you select a new game.

Exit: Let's you exit the emulator back to Pogo or the FA/F2A menu.

--------------------------------------------------------------------------------

	
Make sure your flashing software allocates 64kByte/512kbit SRAM for NGPAdvance.

--------------------------------------------------------------------------------
Advanced:
--------------------------------------------------------------------------------
EWRAM speed: this changes the waitstate on EWRAM between 2 and 1, this
can probably damage your GBA and definitly uses more power,
around 10% speedgain. Use at your own risk!


Pogoshell:
Copy ngpadvance.gba to the plugin folder (or compress it to mbz before you copy
 it) then rename it to ngpadvance.bin and add this line to the pogo.cfg file:
ngp 1 ngpadvance.bin 2
or
ngp 1 ngpadvance.mbz 2


--------------------------------------------------------------------------------
Credits:
--------------------------------------------------------------------------------
Huge thanks to Loopy for the incredible PocketNES and the builder, without it
this emu would probably never have been made.

Thanks to:
The crew at PocketHeaven for their support.
All the people involved in developing other NGP emulators.
Flavor for some ideas on NGP emulation and support.

-------------------------------
Fredrik Olsson
FluBBa@passagen.se
http://hem.passagen.se/flubba/gba.html
http://www.gbaretro.com/
-------------------------------

