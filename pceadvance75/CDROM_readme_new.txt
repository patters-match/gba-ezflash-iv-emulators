Using CD-ROMs with PCEAdvance:                           (updated by patters)
--------------------------------------------------------------------------------
Compilations built with the legacy Win32 builder included with PCEAdvance 7.5
cannot have CD-ROM data appended correctly. This builder mistakenly pads the
preceding ROM data which breaks CD support. Use the new Python 3 builder
instead. You can read the builder's full help text using the -h option.

To be able to use PC Engine / TurboGrafx16 CD-ROM games you have to have a
CD-ROM System ROM in your build. The builder will add this automatically, it
defaults to importing the file bios.bin but this can be overridden using the
-b option (BIOS). To use CD-ROM support from Pogoshell just make a compilation
with only a CD-ROM System ROM and use it as the plugin for .iso and .pce files.

Most CD-ROM games have their data stored in CD track 2, and have a very similar
sized second copy of that data as the final CD track. All other tracks are
usually audio. PCEAdvance cannot play the audio so usually it only needs a
game's track 2 data in .iso format. This can be extracted from a typical
.bin/.cue disc image using a tool such as Isobuster for Windows, or using
'bchunk' on macOS or Linux. Add .iso files using the builder in the same way as
you would add a regular .pce file.

Some games do have multiple data tracks (excluding the last duplicate of track
2), for instance Macross 2036, and in this case they will need a .tcd track
index file. Some are included with PCEAdvance, along with details of the
specification. If you need to make new ones, the Table of Contents (TOC) LBA
values can be taken directly from https://www.necstasy.net and converted to
hex. If the Python 3 builder finds a .tcd file with the same name as the .iso
file it will be added automatically. The track index can also be manually
specified using the -t option.

Owing to the way PCEAdvance organises the CD-ROM data you are limited to a
single CD game in each build, but it can co-exist with other ROMs and it can
be added in any order in the list using the Python 3 builder.

Note that PSRAM on the EZ-Flash flashcarts is limited to 16MB. Unfortunately
PSRAM cannot be addressed if the emulator is run from NOR flash (32MB). This
means that both the PCEAdvance compilation and its additional RAM requirement
must fit within that 16MB. Oversized compilations can be truncated by the
builder using the -trim option, losing some game data in the process. For this
reason you should label your ISO filenames with the required system type:
(CD) for CD-ROM, (SCD) for Super CD-ROM, or (ACD) for Arcade CD-ROM.
You can determine this by consulting the lists published at
https://www.necstasy.net. Akumajou Dracula X: Chi no Rondo (20.8MB) is one
such title. Although the trimmed game does apparently work, it would not be
playable to completion on EZ-Flash.


CD-ROM games tested so far:
--------------------------------------------------------------------------------
Addams Family (U): Ok, fullscreen images flicker.
Cosmic Fantasy 2 (U): Intro & game ok, can't fit whole game though.
Download 2 (J): Ok
Exile (U): Crashes if you hit the Ants.
Final Zone II (U): Ok.
Gain Ground: Too big.
Golden Axe: Ok, need to skip intro.
HellFire S: Ok, screen too wide though.
Jyuohki (J)/(Altered Beast): Ok
Macross 2036 (J): Ok
MineSweeper (J): Ok.
Monster Lair: Ok.
Rayxanber II (U): Ok.
Red Alert (J): Ok
Rainbow Islands (J): Very slow
Road Spirits: Ok
Space Fantasy Zone (J/U): Ok
Splash Lake (U): Ok
Spriggan (J): Ok, stops after 3rd level?
Super Darius: Ok. What is different from the Hucard version? A bigger logo?
Valis II (U): Ok.
Valis III (U): Works,I've only got the first data track so the intro is corrupt.
Valis IV (J): Same as Valis III.
Ys Book 1&2 (U): Ok
Ys 3: Wanderers From Ys (U): Too big too fit on a flashcart.
Zero Wing (J): Ok


Super CD-ROM games tested so far (SuperCard / EZ-Flash builds only):
--------------------------------------------------------------------------------
Conan: Intro Ok
Cotton - Fantastic Night Dream (U): Ok
Double Dragon 2: Ok
Dracula X (J): Ok
Forgotten Worlds (J): Ok
Gate of Thunder (J): Ok
Genocide (J): Ok
Gradius 2 (J): Ok
Image Fight 2 (U): Ok
Loom (U): Flickering graphics.
Lords Of Thunder: Ok
Nexzr: Ok
Rayxanber III (J): Ok
Riot Zone: Ok
R-Type Complete CD (J): Ok
Shadow of the Beast (U): Ok, some flicker in intro.


Arcade CD-ROM games tested so far (SuperCard / EZ-Flash builds only):
-------------------------------------------------------------------------------
None confirmed working with EZ-Flash at least. Most data tracks are way too
large. The only realistic contenders are:

Mad Stalker (J) (5.1MB): Hangs at loading screen
Ginga Fukei Densetsu Sapphire (J) (15.6MB): Hangs at white screen
World Heroes 2 (J) (17.7MB): Hangs at black screen
