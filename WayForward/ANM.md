# ANM File Format

**Note:** All offsets are in hex and the format is little endian.
**Another note:** This format is different to the Nintendo DS version of the format. 

Palettes are stored in the ANM file itself.

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
| 210    | Tile alignment and hitbox table offset (needs documentation!) | 32-Bit integer |
| 214    | Start of current sprite (add the sprite data start offset to this!)| 32-Bit integer |
| 218    | Size of the current sprite in bytes | 32-Bit integer |
