# TS8 File Format (Nintendo DS, LeapFrog Didj)

**Note:** All offsets are in hex and the format is little endian.

Palettes are stored in the TS8 file itself. These files store tiles used to construct maps and should always be 8 bits per pixel.

Skip the palette part and this documentation should also work for the Nintendo DS version of the format.

| Offset  | Description | Data Type/length |
|---------|-----------------------------------------------------------------------|------------------|
| 0-1FF   | Palette (skip this if you're looking at the DS version!) | BGR555 palette, 256 colors (0x200) |
| 200     | Unknown | 16-Bit short |
| 202     | Unknown | 16-Bit short |
| 204     | Total tile count | 32-Bit integer |
| 208-213 | Unused | - |
| Info    | The tile index table starts here. Use the tile count from before here. | Total tile count |
| -       | Read (Total tile count) number of entries, each entry being a 32-Bit integer    | - |
| -       | The tile data should start right after reading the entries             | 8BPP indexed tile data |
