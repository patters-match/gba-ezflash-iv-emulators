# HVCA exit code for EZ-Flash IV / 3in1 / Omega
# by patters in 2023, tidied by TechieSaru
# 
# https://gbatemp.net/threads/multi-platform-builder-scripts-for-gba-emulators.611219/post-10138443

add  r0, pc, #0x2c
ldm  r0, {r1 - r9, sp}
strh r7, [r1]
strh r8, [r2]
strh r7, [r3]
strh r8, [r4]
strh r9, [r5]
strh r8, [r6]
mov  r0, #0
strb r0, [sp, #0xfa]
mov  r0, #0xfc
swi  #0x10000
swi  #0
.word 0x09FE0000
.word 0x08000000
.word 0x08020000
.word 0x08040000
.word 0x09880000
.word 0x09FC0000
.word 0x0000D200
.word 0x00001500
.word 0x00008000
.word 0x03007F00
