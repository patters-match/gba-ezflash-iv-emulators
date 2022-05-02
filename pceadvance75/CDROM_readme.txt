Using CD-ROM with PCEAdvance:
--------------------------------------------------------------------------------
To be able to use PC-Engine/TurboGrafx16 CD-ROM games you have to have
a CD-ROM System rom in your build.
Use the normal builder to add any normal games that you want but also add a
CD-ROM System rom to the compilation. After that also add the datatracks from
the CD and optionaly a .tcd file ("cue" file) to the compilation, this is
easiest done from a command prompt or in a batch file:
copy /b pcebuild.gba+cdgame.tcd+cdgame.iso pcecdbuild.gba

The .tcd files are not needed for all games, but the games that have several
datatracks require it (not the ones that have a second copy of the first
datatrack on the last datatrack), I will try to make .tcd files for all games
that are requested. You can only have 1 CD game in each build right now
and you start it by choosing the CD-ROM System and then pushing start.

To use it from Pogoshell just make a build with only the CD-ROM System rom
and use it as the plugin for iso files (and pce files).

CD-Rom games I've tested so far:
--------------------------------------------------------------------------------
Addams Family (U): Ok, fullscreen images flicker.
Cosmic Fantasy 2 (U): Intro & game ok, can't fit whole game though.
Download 2 (J): Ok
Exile (U): Crashes if you hit the Ants.
Final Zone II (U): Ok, need to skip intro.
Gain Ground: Too big.
Golden Axe: Ok, need to skip intro.
HellFire S: Ok, screen too wide though.
Jyuohki (J)/(Altered Beast): Ok
Macross 2036 (J): Ok
MineSweeper (J): Ok.
Monster Lair: Ok.
Rayxanber II (U): Palette issues on first Boss, corrupt "Game Over" screen.
Red Alert (J): Ok
Road Spirits: Ok
Space Fantasy Zone (J/U): Ok
Splash Lake (U): Ok
Spriggan (J): Ok, stops after 3rd level?
Super Darius: Ok. What is different from the Hucard version? A bigger logo?
Valis II (U): Ok, need to skip intro.
Valis III (U): Works,I've only got the first data track so the intro is corrupt.
Valis IV (J): Same as Valis III.
Ys Book 1&2 (U): Ok
Ys 3: Wanderers From Ys (U): Too big too fit on a flashcart.

Super CD-Rom games I've tested so far:
--------------------------------------------------------------------------------
Conan: Intro Ok
Cotton - Fantastic Night Dream (U): Ok
Double Dragon 2: Ok
Dracula X (J): Ok
Forgotten Worlds (J): Ok
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


