This aims to document the sprite format used in most of the handheld titles made by Torus Games.

LeapFrog game list:
- Cars (shadows, a few menu graphics)
- Cars: Supercharged (shadows, a few menu graphics)
- NASCAR (shadows, a few menu graphics, some track objects)
- Sonic X (every sprite)
- Go, Diego, Go! Animal Rescuer (every sprite)

GBA game list:
- Backyard Football
- Backyard Football 2006
- Backyard Sports Football 2007
- Cabela's Big Game Hunter 2005 Adventures
- Curious George
- Dead to Rights
- Doom II
- Duke Nukem Advance
- Fantastic 4
- Fantastic 4: Flame On
- Gumby vs. the Astrobots
- Ice Nine
- Minority Report: Everybody Runs
- Pitfall: the Lost Expedition
- Rapala Pro Fishing
- Shrek Smash n' Crash Racing
- Sportsmans Pack Cabela's Big Game Hunter + Rapala Pro Fishing
- The Invincible Iron Man

DS game list:
- Shrek Smash n' Crash Racing

Maybe more? Their DS library still needs to be checked.

Some sprites still come out broken with this documentation, so it's unfinished!

Remaining issues with this documentation:
- Earlier GBA titles (Space Invaders, Planet of the Apes) are different in how they work and need to be documented too
- Some sprites have a single chunk misplaced
- Some sprites use the wrong palettes
- Some sprites load the wrong tiles entirely

Sprite container header format:
| Address                        | Variable Name        | Data Type                         | Description                       |
|--------------------------------|----------------------|-----------------------------------|-----------------------------------|
| 0x0                            | Magic number         | Section signature, 32-Bit         | b'\x03\x00\x01\x00' or b'\x04\x00\x01\x00' |
| 0x4                            | Entry count          | 16-Bit little endian integer      | The number of sprite offsets               |
| 0x6                            | Palette table offset | 16-Bit little endian integer      | Where the palette table starts             |
| 0x8                            | Tile data start      | 16-Bit little endian integer      | Where the tile data starts                 |
| 0xA                            | Unknown              | 16-Bit                            | Unknown                                    |
| Loop the next entry            |                      |                                   |                                            |
| 0xC                            | Sprite offset        | 32-Bit little endian integer      | Points to a sprite                         |

Palette table format:
| Address                        | Variable Name        | Data Type                         | Description                       |
|--------------------------------|----------------------|-----------------------------------|-----------------------------------|
| 0x0                            | Palette count        | 32-Bit little endian integer      | How many color palettes there are |
|                                |                      |                                   | There's 16 colors per palette     |
| 0x4                            | Palette data         | BGR555 palette                    | There should be {palette count}   |
|                                |                      |                                   | entries.                          |

Tile data format (early) (Fantastic 4, Pitfall):
| Address                        | Variable Name        | Data Type                         | Description                       |
|--------------------------------|----------------------|-----------------------------------|-----------------------------------|
| 0-0xC                          | Unknown              |                                   | I have no idea what these are for |
| 0xC                            | Tile data            | 4BPP GBA format tiles             | The tile data                     |

Tile data format (later) (Sonic X, Diego, Shrek...):
| Address                        | Variable Name        | Data Type                         | Description                       |
|--------------------------------|----------------------|-----------------------------------|-----------------------------------|
| 0-0x8                          | Unknown              |                                   | I have no idea what these are for |
| 0x8                            | Tile data            | 4BPP GBA format tiles             | The tile data                     |

Sprite (all offsets are relative to the sprite start offset!):
| Address                        | Variable Name          | Data Type                         | Description                         |
|--------------------------------|------------------------|-----------------------------------|-------------------------------------|
| 0x0                            | Animation count        | 16-Bit little endian integer      | The animation count                 |
| 0x2                            | Base palette ID offset | 16-Bit little endian integer      | Pointer to this sprite's palette ID |
| 0x4                            | Padding                | 32-Bit                            | Padding bytes? Always 0.            |
| Loop the next entry            |                        |                                   |                                     |
| 0x8                            | Animation offset       | 32-Bit little endian integer      | Animation offsets                   |

Animation (all offsets are relative to the animation start offset!):
| Address                        | Variable Name        | Data Type                         | Description                       |
|--------------------------------|----------------------|-----------------------------------|-----------------------------------|
| 0x0                            | Frame count          | 8-Bit integer                     | The number of frames              |
| 0x1                            | Unknown              | 8-Bit                             | Unknown                           |
| 0x2                            | Playback speed       | 16-Bit little endian integer      | Usage is unknown                  |
| Loop the next entries          |                      |                                   |                                   |
| 0x4                            | Frame offset         | 32-Bit little endian integer      | Offset for this frame             |
| 0x8                            | Padding              | 16-Bit                            | Padding                           |

Frame:
| Address                        | Variable Name        | Data Type                         | Description                       |
|--------------------------------|----------------------|-----------------------------------|-----------------------------------|
| 0x0                            | Chunk count          | 16-Bit little endian integer      | How many chunks are in this frame |
| 0x2                            | Unknown              | 32-Bit                            | Unknown                           |
| 0x6                            | Align X              | 8-Bit integer                     | X alignment value - subtract it   |
| 0x7                            | Align Y              | 8-Bit integer                     | Y alignment value - subtract it   |
| 0x8                            | X size?              | 8-Bit integer                     | X size in tiles?                  |
| 0x9                            | Y size?              | 8-Bit integer                     | Y size in tiles?                  |
| 0xA                            | Unknown              | 16-Bit                            | Unknown                           |

Chunk:
| Address                        | Variable Name        | Data Type                         | Description                       |
|--------------------------------|----------------------|-----------------------------------|-----------------------------------|
| 0x0                            | Align X              | 8-Bit integer                     | X alignment value - add it        |
| 0x1                            | Align Y              | 8-Bit integer                     | Y alignment value - add it        |
| 0x2                            | Shape                | 8-Bit                             | Chunk shape/size value            |
| 0x3                            | Additional palette ID| 8-Bit integer                     | Add this to the base palette ID   |
| 0x4                            | Next chunk offset    | 8-Bit integer                     | Relative to current chunk start   |
| 0x5                            | Unknown              | 8-Bit                             | Unknown                           |
| Loop the next entry            |                      |                                   | Using the size, loop the next part|
| 0x6                            | Tile IDs             | 16-Bit                            | The IDs of this chunk's tiles     |

Examples:





<img width="160" height="160" alt="frame_160_000_000" src="https://github.com/user-attachments/assets/fac9153e-5a1b-4f4d-b104-942020f67774" />

<img width="160" height="160" alt="frame_162_000_000" src="https://github.com/user-attachments/assets/7bc50b5a-d4bd-43fb-a096-1d8580065304" />

<img width="180" height="70" alt="SonicX" src="https://github.com/user-attachments/assets/40b06428-6e4a-4818-898b-18f7444aee61" />
