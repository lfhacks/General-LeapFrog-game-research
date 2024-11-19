# ANM File Format

**Note:** All offsets are in hex and the format is little endian.

**Another note:** This format is different to the Nintendo DS version of the format. 

Palettes are stored in the ANM file itself. The sprite data is 8 bits per pixel (and tiled, each tile is 8 pixels wide and 8 pixels tall).

| Offset | Description | Data Type |
|--------|-----------------------------------------------------------------------|------------------|
| 0-1FF  | Palette (BGR555 format) | - |
| 200    | Unknown | 16-Bit short |
| 202    | Unknown | 16-Bit short |
| 204    | Unknown | 16-Bit short |
| 206    | Total frame count | 16-Bit short |
| 208    | Sprite data start offset | 32-Bit integer |
| 20C    | Size of all sprite data from the start offset | 32-Bit integer |
| (Info) | Repeat the following for however many frames there are in the file | - |
| 210    | Tile alignment and hitbox table offset | 32-Bit integer |
| 214    | Start of current sprite (add the sprite data start offset to this!)| 32-Bit integer |
| 218    | Size of the current sprite in bytes | 32-Bit integer |


The info starting after this point is a work in progress!

| Offset | Description | Data Type |
|--------|-----------------------------------------------------------------------|------------------|
| (start of tile alignment/hitbox table)  | Main hitbox | 32 bytes (structure not yet known) |
| (start of tile alignment/hitbox table)+32  | Chunk count (for this example, it's 2) | 16-Bit short |
| (start of tile alignment/hitbox table)+34  | Chunk 1 X position | 16-Bit short |
| (start of tile alignment/hitbox table)+36  | Chunk 2 X position | 16-Bit short |
| (start of tile alignment/hitbox table)+38  | Chunk 1 Y position | 16-Bit short |
| (start of tile alignment/hitbox table)+40  | Chunk 2 Y position | 16-Bit short |
| (start of tile alignment/hitbox table)+32  | Chunk 1 offset (Check below for the format!) | 16-Bit short |
| (start of tile alignment/hitbox table)+32  | Chunk 2 offset (Check below for the format!) | 16-Bit short |

The offsets are formatted like this (these are the individual bits of the offset value):

| Bits | Description |
|--------|-----------------------------------------------------------------------|
| 0 | How many bits per pixel this sprite is (0 = 4, 1 = 8) | 
| 1 | Unused |
| 2-3 | X size (tiles) (0 is 1) |
| 4-5 | Y size (tiles) (0 is 1) |
| 6-13 | Starting tile index (from start of current sprite offset) | 
| 14-15 | Unused |
