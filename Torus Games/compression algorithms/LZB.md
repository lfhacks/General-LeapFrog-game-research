# Torus Games LZB file format documentation
This is incomplete (and will probably stay that way for a while). Expect missing information.

Every file starts with "ZB". This is checked with the following code:
```asm
Unpack_GetType: ; Get the compression type for the file we're accessing
    ldb_s      r1,[r0]      ; Load a byte from the offset in r0 into r1 (first half of magic number)
    ldb_s      r12,[r0,0x1] ; Load a byte from the offset in r0 + 1 into r12 (second half of magic number)
    asl_s      r12,r12,0x8  ; Shift r12 left by 8 bits
    or_s       r1,r1,r12    ; Combine r1 and r12 to make a 16-Bit value, store the result in r1

    ; Each of these lines checks if r1 contains the magic numbers for known formats
    breq       r1,0x425a,LZB
    breq       r1,0x5444,DT
    breq       r1,0x575a,LZW

    ; This only runs if the bytes didn't match what was expected by the previous branch if equal instructions
    mov_s      r0,0x0 ; Set the mode to 0 (uncompressed)
    b_s        ReturnFromFunction ; Return from this function
                                              
    LZB:  
        mov_s      r0,0x2 ; Set the mode to 2 (LZB compression)
        b_s        ReturnFromFunction ; Return from this function
    DT:
        mov_s      r0,0x3 ; Set the mode to 3 (delete, frees up memory)
        b_s        ReturnFromFunction ; Return from this function
    LZW:
        mov_s      r0,0x1 ; Set the mode to 1 (LZW compression, unused)
        ; This is assembly code, so branching to the return label right before it isn't needed

    ReturnFromFunction:
        j_s        blink ; Return to where this function was called from
```

After this is the decompressed size and the instruction block offset, both of which are 24-Bit values.

The literal data (raw bytes used by the commands in the instruction block) always starts at offset 0x8.
