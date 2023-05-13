.text
.arm

@mov r0,#0x100
add r3,pc,#1
bx r3
@mov r4,#0x02000000
@0:
@ldr r1,[r3],#4
@str r1,[r4],#4
@subs r0,r0,#4
@bne 0b
@mov r0,#0x02000000
@add r0,r0,#29
@bx r0

.thumb
reset_code:
mov r0,#0x20
lsl r3,r0,#22 @#0x8000000 r3
lsl r0,r0,#12 @#0x0020000
add r4,r3,r0  @#0x8020000 r4
add r5,r4,r0  @#0x8040000 r5
lsl r1,r0,#8  @#0x2000000
add r2,r3,r1  @#0xa000000
lsr r1,r3,#4  @#0x0800000
sub r6,r2,r1  @#0x9800000
lsr r1,r1,#4  @#0x0080000
add r6,r6,r1  @#0x9880000 r6
sub r2,r2,r0  @#0x9fe0000 r2
sub r7,r2,r0  @#0x9fc0000 r7

mov r0,#210
lsl r0,r0,#8  @0xd200 r0
mov r1,#21
lsl r1,r1,#8  @0x1500 r1

strh r0,[r2]
strh r1,[r3]
strh r0,[r4]
strh r1,[r5]

lsr r0,r3,#12 @#0x0008000 r0

strh r0,[r6]
strh r1,[r7]

lsl r1,r0,#11 @#0x4000000
sub r1,r1,#8  @#0x3FFFFFA
mov r0,#0xfc  @#252 r0
str r0,[r1] @#0x3FFFFFA (mirror of #0x3007FFA
swi 0x01
swi 0x00
reset_end:
