SMSAdvance V2.5
--------------------------------------------------------------------------------
This is a SEGA Master System & Game Gear emulator for the GBA.
You can also play SG-1000 games on it.

Features:
 Most things you'd expect from an SMS emulator.
 Except these...

Missing:
 Correct sprite collision and overflow.
 Speech samples.
 YM2413 emulation.
 EEPROM save for the few GG games that use it.
 Screen mode 3 (not really used).

Check your roms!
http://www.smspower.org/maxim/smschecker/
--------------------------------------------------------------------------------
How to use:
--------------------------------------------------------------------------------
Run SMSAdvance.exe to add roms to the emulator.
Do no overwrite the original .gba file!

When the emulator starts, use Up/Down to select game, then use
B or A to start the game selected.
Press L+R to open the menu, A to choose, B (or L+R again) to cancel.

--------------------------------------------------------------------------------
Menu:
--------------------------------------------------------------------------------
Controller:
	Autofire: Select if you want autofire.
	Controller: 2P control player 2, Link is used to linkup 2 GBAs.
	Swap A/B: Swap which GBA button is mapped to which SMS/GG button.
	Use R as Start: Map the GBA R button to the GG Start button.
	Use Select as Reset: Map the GBA SELECT button to the SMS Reset button.

Display:
	Display: Here you can select if you want scaled or unscaled screenmode.
		Unscaled mode:  L & R buttons scroll the screen up and down.
		Scaled modes:  Press L+SELECT to adjust the background.
	Scaling: Here you can select if you want flicker or barebones lineskip.
	Gamma: Lets you change the gamma ("brightness").
	GG Border: Lets you change between black, bordercolor and none.
	Lock toprows: For unscaled screenmode.
		Some games use this automaticly, Double Dragon, OutRun etc.
		but you can also choose to force it.
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
	Autoload state: Toggle Savestate autoloading.
		Automagicaly load the savestate associated with the selected game.
	Fake spritecollision: Some games require this, Pit Fighter doesn't like it.
	Region: Change the region of the SMS and video standard.
	Use BIOS: If you have added a BIOS you can select if you want to use it.
	Machine: Here you can select the hardware, Auto should work for most games.

Help:
	Some dumb info about the game...

Link Transfer:
	Lets you transfer small games to other GBAs, also see the advanced topic.

Go Multiboot:
	You can use the Go Multiboot feature to force the game to run in multiboot
	mode. Useful if you want to boot someone else up and eject the cartridge.
	Do not eject cartridges from a GameBoy Player as it will just reset.

Save Manager:
	Quick savestate: Creates a savestate/overwrites the current if one exists.
		You can also use R+SELECT as a shortcut.
	Quick loadstate: Load a savestate associated with the current game.
		You can also use R+START as a shortcut.
	Savestate: Select if you want to overwrite an old state or create a new.
	Loadstate: Select which state you want to load.
	Save SRAM: Save the SRAM for the current game.
		It's automaticly loaded when starting a game and saved when entering
		the menu after it is created the first time.
	Manage savememory: Lets you erase SRAM (for now).

Sleep: Put the GBA into sleepmode.
	START+SELECT wakes up from sleep mode (activated from this menu or from
	5/10/30	minutes of inactivity).

Restart: Lets you select a new game.

Exit: Let's you exit the emulator back to Pogo or the FA/F2A menu.

--------------------------------------------------------------------------------

	
Make sure your flashing software allocates 64kByte/512kbit SRAM for SMSAdvance.

--------------------------------------------------------------------------------
Advanced:
--------------------------------------------------------------------------------
EWRAM speed: this changes the waitstate on EWRAM between 2 and 1, this
can probably damage your GBA and definitly uses more power,
around 10% speedgain. Use at your own risk!

Link transfer:  Send a SMS game to another GBA.  The other GBA must be in
  multiboot receive mode (no cartridge inserted, powered on and waiting with
  the "GAME BOY" logo displayed). Only one game can be sent at a time, and
  only if it's small enough to send (approx. 128kB or less). A game can only
  be sent to 1 (one) Gameboy at a time, disconnect all other gameboys during
  transfer.

Use an original Nintendo cable!

Pogoshell:
Copy smsadvance.gba to the plugin folder (or compress it to mbz before you copy
 it) then rename it to smsadvance.bin and add this line to the pogo.cfg file:
sms 1 smsadvance.bin 2
or
sms 1 smsadvance.mbz 2


--------------------------------------------------------------------------------
Credits:
--------------------------------------------------------------------------------
Huge thanks to Loopy for the incredible PocketNES and the builder, without it
this emu would probably never have been made.

Thanks to:
Dwedit for maintaining the GBAMP version of SMSAdvance.
Reesy for help with the Z80 emu core.
Some MAME people + Maxim for the SN76496 info.
Charles MacDonald (http://cgfm2.emuviews.com/) for VDP info.
Omar Cornut (http://www.smspower.org/) for help with various SMS stuff.
Vinpire for the splashscreen.
The crew at PocketHeaven for their support.
Check out the SMSAdvance forum there.
http://boards.pocketheaven.com/viewforum.php?f=40

-------------------------------
Fredrik Olsson
FluBBa@passagen.se
http://www.gbaretro.com/
http://hem.passagen.se/flubba/gba.html
-------------------------------

