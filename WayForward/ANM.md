# ANM File Format

**Note:** All offsets are in hex and the format is little endian.

Palettes are stored in the ANM file itself (Didj version only - skip that part if you're looking at the DS version). The sprite data is 8 bits per pixel (and tiled, each tile is 8 pixels wide and 8 pixels tall).

| Offset | Description | Data Type |
|--------|-----------------------------------------------------------------------|------------------|
| 0-1FF  | Palette (BGR555 format) (skip this if you're looking at the DS version!) | - |
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
| (start of tile alignment/hitbox table)+00  | Main hitbox | 32 bytes (structure not yet known, the values in here are all 16-Bit shorts) |
| (start of tile alignment/hitbox table)+20  | Chunk count (for this example, it's 2 - the X/Y/info value counts are determined by this value) | 16-Bit short |
| (start of tile alignment/hitbox table)+22  | Chunk 1 X position | 16-Bit short |
| (start of tile alignment/hitbox table)+24  | Chunk 2 X position | 16-Bit short |
| (start of tile alignment/hitbox table)+26  | Chunk 1 Y position | 16-Bit short |
| (start of tile alignment/hitbox table)+28  | Chunk 2 Y position | 16-Bit short |
| (start of tile alignment/hitbox table)+2A  | Chunk 1 info (Check below for the format!) | 16-Bit short |
| (start of tile alignment/hitbox table)+2C  | Chunk 2 info (Check below for the format!) | 16-Bit short |

The info variables are formatted like this (these are the individual bits of the info value):

| Bits | Description |
|--------|-----------------------------------------------------------------------|
| 0 | How many bits per pixel this sprite is (0 = 4, 1 = 8) | 
| 1 | Unused? |
| 2-3 | X size (tiles) (0 is 1) |
| 4-5 | Y size (tiles) (0 is 1) |
| 6-13 | Starting tile index (from start of current sprite offset) | 
| 14-15 | Unused? |

Here's an example (B is the bits per pixel value, _ is unused, X/Y are the size, S is the start index in tiles):

B_XXYYSSSSSSSS__

1001010000000000

With my current documentation, that'd be 8 bits per pixel, 2 tiles wide, 2 tiles tall and you'd start on tile index 0
