	EXPORT doReset
;
; Visoly start-code; must be sent before any command
;
init_flashcart
	ldr		r0, =flash_constants
	ldmia	r0,{r2-r5}
	add		r0,r0,#16

;   WriteRepeat (0x987654, 0x5354, 1);
	ldr		r1,[r0]
	strh	r2,[r1]

;   WriteRepeat ( 0x12345, 0x1234, 500);
	ldr		r1,[r0,#4]
	mov		r12,#500
0
	strh	r3,[r1]
	subs	r12,r12,#1
	bne		%B0

;   WriteRepeat ( 0x12345, 0x5354, 1);
	ldr		r1,[r0,#4]
	strh	r2,[r1]
	
;   WriteRepeat ( 0x12345, 0x5678, 500);
	mov		r12,#500
1
	strh	r4,[r1]
	subs	r12,r12,#1
	bne		%B1

;   WriteRepeat (0x987654, 0x5354, 1);
	ldr		r1,[r0]
	strh	r2,[r1]

;   WriteRepeat ( 0x12345, 0x5354, 1);
	ldr		r1,[r0,#4]
	strh	r2,[r1]

;   WriteRepeat (0x765400, 0x5678, 1);
	ldr		r1,[r0,#12]
	strh	r4,[r1]

;   WriteRepeat ( 0x13450, 0x1234, 1);
	ldr		r1,[r0,#16]
	strh	r3,[r1]

;   WriteRepeat ( 0x12345, 0xabcd, 500);
	ldr		r1,[r0,#4]
	mov		r12,#500
2
	strh	r5,[r1]
	subs	r12,r12,#1
	bne		%B2

;   WriteRepeat (0x987654, 0x5354, 1);
	ldr		r1,[r0]
	strh	r2,[r1]

	bx		lr

; r0 = New rom start value
; 10 bits
; 9-3 = 16Mbit -> 256Kbit
; 2-0 = 128Mbit -> 32Mbit
; Only bits 3,1,0 allowed for older carts
set_rom_start
	ldr	r1,=0x096B592E
	strh	r0,[r1]
	bx		lr

; Restore cartstart & Softreset
doReset
	mov r1,#REG_BASE
	mov r0,#0
	strh r0,[r1,#REG_DM0CNT_H]	;stop all DMA
	strh r0,[r1,#REG_DM1CNT_H]
	strh r0,[r1,#REG_DM2CNT_H]
	strh r0,[r1,#REG_DM3CNT_H]
	add r1,r1,#0x200
	str r0,[r1,#8]		;interrupts off

	bl		init_flashcart
	mov		r0, #0
	ldr		r1,=0x3007ffa	;must be 0 before swi 0x00 is run, otherwise it tries to start from 0x02000000.
	strh		r0,[r1]
	bl		set_rom_start
	mov		r0, #8		;VRAM clear
	swi		0x010000
	swi		0x000000

flash_constants
        DCD   0x5354
        DCD   0x1234
        DCD   0x5678
        DCD   0xabcd

        DCD   (0x00987654 * 2) + 0x08000000
        DCD   (0x00012345 * 2) + 0x08000000
        DCD   (0x00007654 * 2) + 0x08000000
        DCD   (0x00765400 * 2) + 0x08000000
        DCD   (0x00013450 * 2) + 0x08000000

        END

