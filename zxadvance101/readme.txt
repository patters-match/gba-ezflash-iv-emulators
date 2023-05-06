ZXAdvance 1.0.1a
================

  Created by [-TheHiVE-]
  Email: zxadvance@btinternet.com

About
=====
  
  ZXAdvance is ZX Spectrum emulator for the Gameboy Advance.
  It is written in 100% pure ARM ASM for maximum speed on real hardware.
  Although ZXAdvance is no longer in beta, this version does have _some_
  stability and emulation issues.
  I am actively working on correcting problems though, and please feel
  free to contact me about bugs, errors, or enhancement requests.

Requirements
============

  A Gameboy Advance, or emulator.
  A Flash Cart & Linker.
  A PC with a Windows operating system.
  Z80/SNA Snapshots.
  Pogoshell (optional).

  Sadly ZXAdvance does NOT work with multiboot cables, nor will it in the future.

Creating ZXAdvance binaries
===========================

  ZXAdvance Standalone
  --------------------
  Run ZXA.EXE and add ROMs to the list.
  Double click ROMs in the list to change the controls, or ROM name.
  Click the Create button to generate a standalone binary.
  Upload this to your GBA flash cart.

  Pogoshell (ZXA4Pogo)
  --------------------
  Run ZXA.EXE and DO NOT add any ROMs to the list.
  Click the Create button to generate a Pogoshell binary.
  You can optionally tell ZXA where Pogoshell resides on your PC, and ZXA
  will then automatically create the binary in the Pogoshell filesystem, and
  compile Pogoshell for you.

MENU OPTIONS
============

  General Control
  ---------------
  Use up/down to highlight the required menu option.
  Press A to select an option.
  Press B to return to the previous menu.

  Load ROM (NOT available in ZXA4Pogo)
  ------------------------------------
  This option is presented when you have injected ROMs into the native ZXA binary.
  Selecting it will present you with a list of injected ROMs.
  Use up/down to select the required ROM. Use left/right to view subsequent pages
  of ROMs (assuming you have injected more than 10).
  Press A to preview the ROM in the mini viewing window.
  Once previewed, if you wish to load the ROM press A again.

  Exit to Pogoshell (ONLY available in ZXA4Pogo)
  ----------------------------------------------
  Simply returns to the Pogoshell menu.

  Reset ROM
  ---------
  This is a quick way of reloading the currently selected ROM image.

  Reset Emulator
  --------------
  This will reset the entire emulator, and reload the initial ROM image.

  Save/Load Snapshot
  ------------------
  These options will allow you to save and restore upto two ROM states.
  Note that they are saved to the GBA internal memory, and as such will be lost
  when you power off, or reset the GBA.

  Save/Load SRAM
  --------------
  These options will allow you to save a single ROM state.
  As this state is saved to the SRAM on the flash cart, it will remain available
  even after powering off, or reseting the GBA.
  Note: ZXA uses the first SRAM slot.

  Video Modes
  -----------
  There are 5 standard video modes, and a customizable one.
  Select the one that is most appropriate to the ROM you are playing.
   - Full Screen:    Unscaled display.
   - Scale X:        The screen is scaled to fit horizontally.
   - Scale Y:        The screen is scaled to fit vertically.
   - Scale X & Y:    The screen is scaled to fit horizontally, and vertically.
   - Platform Genre: The top two thirds are unscaled. The bottom third is scaled to fit.
                     This mode is particularly suited to games akin to Manic Miner.
   - Custom:         You can set both the offset and the vertical and horizontal scaling
                     manually. Changes are saved in SRAM and may be recalled at any time.
                     Use up/down while pressing and holding A to change the settings.


  Video Effects
  -------------
  There are two simple video effects available.
   - Black & White:  Uses a monochrome palette to render the video.
   - Fake Scanlines: Gives the impression of veiwing on a crap TV with scanlines visible.

  Brightness
  ----------
  Use to set the brightness (useful when using GBASP, GBA with afterburner/light etc.)
   - Normal:         Optimal setting for GBASP/GBA with Afterburner.
   - Bright:         For GBA's with exteral lighting solutions.
   - Dark:           Not much use, except when using on emulators.

  Audio
  -----
  Use this option to simply enable to disable audio.
  Optionally, just turn down the sound on your GBA ;)

  Emulation Settings
  ------------------
  Use these to tailor the emulator.
   - Frameskip:      Has four settings. Set to zero for no frameskipping.
                     Get to 1, 2, or 3 to skip that number of frames in 4.
   - R Register:     How the R Register is emulated.
                     It is optimally set to use the TStates, but you can override this
                     to force it to increment the R register instead.
   - Renderer:       Should fix some flickering games, but this is not currently working
   - Pause on Menu:  Select this if you do NOT want the ROMs to continue emulating when
                     you activate the menu.
   - Throttle:       Choose this to disable the audio synching.
                     This will allow some ROMs to run at an 'overclocked' speed.
                     Note that disabling throttling will most likely cause wierd audio
                     gliches.
   - Show Intro:     Select this to enable or disable the intro ROM.
   - Debugger:       Not available in the public build.
   - Disassembler:   Not available in the public build.

  Control Settings
  ----------------
  Use these to customize the control mechanics.
   - Redefine:       Select this will present you with a list of GBA key states, and their
                     bindings. Use up/down while pressing and holding A to change
                     the required key binding.
   - Quick Redefine: Provides a quick way of configuring either Kempston or Cursor bindings.
   - Virtual Keys:   Select this to display a 'virtual' keyboard.
                     When this is active, the normal key bindings will be unavailable.
                     You may select keys from the 'virtual' keyboard by pressing A.

  Cheats
  ------
  Use these options to enter 'pokes' or to apply trainers, etc.
   - Insert Poke:    Not available in the public build.
   - Cheat Database: Not available in the public build.

TO DO
=====

  These features will appear in the next build.
   - Preview Snapshot/SRAM (like the ROM menu preview).
   - Enable Poke support.
   - Enable Cheat database support.
   - Fix Renderer Interrupt Sequencing.
   - Fix CPU bugs (still some there, and some more I've introduced in this build).
   - Enable ZX80/Zx81 support (almost finished).
   - Add TAP/TZX support.

KNOWN PROBLEMS
==============

  These are what I know about. If there's more, please let me know.
   - No cheat support/poke support. I ran out of time (it's there but too buggy).
   - Renderer Interrupt sequencing does not work. I'll fix in the next release
   - SRAM is not saved if you don't close the menus and reopen before exiting to Pogoshell.
   - Some ROMs (Head Over Heels for example), cause the subsequent ROMs to fail too.
     I know why, and will fix in the next release.

HELP
====

  If you would like to assist me with this project, either by submitting bug reports,
  beta testing, additional coding, whatever, then please contact me.
  If you are working on a Z80 based emulator, and want some help or pointers, then again,
  please get in touch. I'm always pleased to assist.

COPYRIGHTS
==========

  ZXAdvance uses the Amstrad ZX Spectrum ROM image.
  You do _not_ need to provide this, it comes prepackaged with ZXAdvance.
  Amstrad allow free distribution of this ROM with non commercial emulators.
  (see http://www.worldofspectrum.org/permits/amstrad-roms.txt)

  ZXAdvance uses a hacked version of Jetset Willy in its intro.
  Mathew Smith the creator of this game has given the WOS permission to redistribute
  this game. 
  (see http://www.worldofspectrum.org/infoseekpub.cgi?regexp=matthew+smith)

  ZXAdvance is a copyrighted work.
  You may NOT sell or redistribute it for profit.
  You may NOT copy, or modify any of it's binary code.
  You may NOT redistribute this binary with commercial ROMs.
  You may ONLY redistribute the binary if accompanied with this UNMODIFIED Readme.txt file.

CONTACT
=======

  Download the latest versions of ZXAdvance from:
  http://zxadvance.gbaemu.com

  Email the author [-TheHiVE-] at:
  zxadvance@btinternet.com

  Contact the author occasionally on IRC at:
  EFNET #emuholic

THANKS
======

  Thanks to all the beta testers of 0.9.3.
  Thanks to Guyfawkes of emuholic/gbaemu/gp32emu for kindly hosting my site.
  Thanks to Costis, for the special VBA build ;)
  Thanks to everyone that has sent emails and PM's of support.

  ZXAdvance is for all those people, and fans of the ZX Spectrum everywhere!