PCEAdvance V7.5

This is a PC-Engine/TurboGrafx-16 emulator for the GBA, it can also
emulate some of the CD-ROM games, and Super CD-ROM if you've got an EZ3 card.
It's mostly slow, crap sound, "Chikudenya Toubee (J)" doesn't even start.
All games are not perfect.

But there are actually games that are enjoyable:
1943 Kai (J) - Takes some time before it starts, but runs ok.
Aero Blasters (U) - ok speed. (spr 6)
After Burner II (J) - Cool game =)
Alien Crush (J) - Perfect?
Atomic Robokid Special (J) - Good speed. (spr 0)
Bomberman 93 - Perfect?
Darius (Alpha/Plus) - Very good speed.
Gomola Speed - Strange but funny game.
Hani in the Sky (J) - Good speed.
Image Fight (J) - Good speed.
Kyuukyoku Tiger (J) - Good Speed.
Mr. Heli - Screen to wide, otherwise ok.
Neutopia (U) - Seem ok, even save.
Ninja Warriors (J) - Good speed.
Operation Wolf (J) - Good speed.
Override (J) - Super speed if you turn off Timer IRQ.
Pacland (J) - Good speed.
R-Type - Good speed.
Rastan Saga II (J) - Good speed.
Super Star Soldier.
Tatsujin (J) - Good speed.
Tenseiryu Saint Dragon (J) - Good speed.

These are just suggestions, please try what ever game you like
(alot of US games doesn't work because they are encrypted,
use PCEToy to decrypt these before you use them.
Also remember to click "US rom" in the builder if you want them to work).
Don't use overdumps as these are evil on PC Engine.
Make sure your flashing software allocates 8kByte/64kbit SRAM for PCEAdvance.


How to use:
When the emulator starts use Up/Down to select game, then use
B or A to start the game selected.
Press L+R to open the menu, A to choose, B (or L+R again) to cancel.
HScroll: (Manual) Lets you scroll the screen with the L & R buttons.
Unscaled modes:  L & R buttons scroll the screen up and down.
Scaled modes:  Press L+SELECT to adjust the background.
Sound: Off, no sound.
       On, low quality low CPU usage.
       On(Mixer), better quality more cpu usage.

TimerIRQ: Some games use the TimerIRQ to play sounds and music,
by dissabling the timer you can make some games faster.
EWRAM speed: this changes the waitstate on EWRAM between 2 and 1, this
can probably damage your GBA and definitly uses more power, little to no
speedgain. Dont use!
Speed modes:  L+START switches between throttled/unthrottled/slomo mode.

Sleep:  START+SELECT wakes up from sleep mode (activated from menu or 5/10/30
minutes of inactivity)


Pogoshell:
To use as a Pogoshell plugin, first copy "pceadvance.gba" to the
plugin folder then rename it to "pce.bin".
To make it work with US roms the name of the rom must not contain (J) or (j).
In the same manner Japanese roms should preferably contain (J) or (j),
most Japanese roms seem to run on US hardware anyway though.


Multi player link play:  Go to the menu and change Controller: to read
  "Link2P"/"Link3P"/"Link4P", depending on how many Gameboys you will use.
  Once this is done on all GBAs, leave the menu on all slaves first, then
  the master, the game will restart and you can begin playing.
  If the link is lost (cable is pulled out, or a GBA is restarted),
  link must be re-initiated, this is done by a restart on the master and
  then selecting the appropriate link and leave the menu. The slaves doesn't
  have to do anything.
Use an original Nintendo cable!

--------------------------------------------------------------------------------
Advanced:
--------------------------------------------------------------------------------
SRAM:
The first 8kByte of the GBA sram is the pce sram, this can be exchanged between
other pce emus, I think you have to change MagicEngine's ini to old format.
Use a "CD-ROM System" rom to manage your pce sram's, press [SELECT] to access the
SRAM manager, the US version is encrypted, don't forget to decrypt it.

GameBoy Player:
To be able to check for the GameBoy Player one must display the GameBoy Player
logo, the easiest way to get it is by downloading it from my homepage.
Otherwise you can rip it from any other game that displays it (SMA4 &
Pokemon Pinball). There is no actuall use for it yet, but the check is there and
I would appreciate if people could test it on their GameBoy Players, it says in
the menu "PCEAdvance v7.3 on GBP".

CD Games in Pogoshell:
Make a PCEAdvance build with only a CD-ROM System rom, then copy the build to
the plugins folder of Pogoshell and rename it to pce.bin, next edit the config.
Add the following line to where the other plugins are in the config file.
iso 1 pce.bin 2
Now you should be able to just add PC-Engine iso files to Pogo and run them.

Credits:
Huge thanks to Loopy for the incredible PocketNES, without it this emu would
probably never have been made.
Big thanks to Hoe for the ROM-Builder.
Thanks to:
Zeograd for a lot of help with the debugging.
Charles MacDonald (http://cgfm2.emuviews.com) &
David Shadoff for a lot of the info.

-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
Big thanks to www.XGFlash2.com for support, go there for all your GBA/SP flash card needs.
-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

Don't forget to join the PCEAdvance forum at www.pocketheaven.com

-------------------------------
Fredrik Olsson
FluBBa@passagen.se
http://hem.passagen.se/flubba/gba.html
-------------------------------

Some things to consider regarding emulation:
PCE has 64kByte of VRAM which can be background and/or sprites,
GBA has 64kByte background and 32kByte sprite VRAM.
The PCE CPU runs at either 1.78MHz (like the NES) or at 7.2MHz (all
games seem to use the fast mode), the GBA CPU runs at 16MHz.
