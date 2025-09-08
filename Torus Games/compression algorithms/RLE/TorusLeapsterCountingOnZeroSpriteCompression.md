# Torus Games sprite decompression info (Leapster) (Counting on Zero only! It was changed in future titles.)

## Description of the format
This format was designed specifically to be decompressed directly onto the frame buffer. Every command is to tell the renderer what to do next.

The following example screenshot from Counting on Zero requires the game to decompress 10 RLE-compressed sprites onto the frame buffer:

![0037](https://github.com/user-attachments/assets/f1419736-6730-4fc9-b678-1334445c1d4c)

## Command list
Each command takes up 3 bits and is stored like this in a nibble (C is for the command bits, X is the remaining bit)

CCCX

Note:

Replace l with | if you use this in code.

| Command value | Description          | Structure                                                                   |
|---------------|----------------------|-----------------------------------------------------------------------------|
| 0 to 3        | Horizontal movement  | Next nibble is a displacement value, calculate full displacement like this: |
| 0 to 3        | Horizontal movement  | displacement = (command << 4) l displacementNibble                          |
| 0 to 3        | Horizontal movement  | With the displacement calculated, add it to the current X position          |
| 0 to 3        | Horizontal movement  | on the screen (a frame buffer in the case of the Leapster)                  |
| 4             | Set palette index    | Next nibble is the index value                                              |
| 5             | Draw pixels          | Next nibble is part of the run length. Combine the least significant bit of |
| 5             | Draw pixels          | the command nibble with this value to get the full run length.              |
| 5             | Draw pixels          | Each pixel is drawn from left to right if the sprite isn't flipped.         |
| 5             | Draw pixels          | The palette index from earlier also gets combined with this value, making   |
| 5             | Draw pixels          | an 8-Bit pixel. (basically, 4-Bit color index + palette index * 0x10)       |
| 6             | Move to next row     | Resets X position to the left edge of the sprite, adds 1 to y position      |
| 7             | Reset to left edge   | Resets the X position to the left edge of the sprite                        |
