# TS4/TS8 File Format (Nintendo DS, LeapFrog Didj)

**Note:** All offsets are in hex and the format is little endian.

# Description

TS4 and TS8 store 8x8 tiles which get constructed into 16x16 blocks. Each block is referenced by an LYR file to construct a map or an image. Depending on the version of the format (Nintendo DS or LeapFrog Didj), color palettes may or may not be stored as the first 0x200 bytes of the file.

# Format breakdown

| Offset  | Description | Data Type/length |
|---------|-----------------------------------------------------------------------|------------------|
| 0-1FF   | Palette (skip this if you're looking at the DS version!) | BGR555 palette, 256 colors (0x200) |
| 200     | Unknown (version number?) | 16-Bit short |
| 202     | Index Table entry count | 16-Bit short |
| 204     | Total tile count | 32-Bit integer |
| Info    | The tile index table starts here. Use the index table entry count here. | Total tile count |
| -       | Read 4 entries until you hit the end of the length of the index table.  | 2 16-bit values, first one is the tile index, second one is unknown. There's 4 tiles per entry. |
| -       | The tile data should start right after reading the entries             | 4BPP (reverse order)/8BPP indexed tile data (depending on the file type) |
