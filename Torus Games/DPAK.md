This container format is used in almost every Torus Games release on the GBA, Leapster and Didj. 

It stores sprites, maps, level layouts and palette data. The said data can also be compressed (and the compression format names are sort of known), but the actual algorithms used are unknown.

Here's a list of LeapFrog games that used it:
- Cars
- Cars Supercharged
- Counting on Zero
- Didji Racing: Tiki Tropics
- Go, Diego, Go! Animal Rescuer
- NASCAR
- Sonic X

For the Didj game, it's stored in an elf file. Said elf file even has the DPAK section names.

| Address                        | Variable Name        | Data Type                         | Description                       |
|--------------------------------|----------------------|-----------------------------------|-----------------------------------|
| offset+0x00                    | identifier           | 4 Bytes                           | Identifier                        |
| offset+0x04                    | entries              | Little Endian 16-Bit Integer      | Number of entries                 |
| offset+0x06                    | torus                | (10 bytes)                        | "Torus" signature                 |
| (Info)                         | Repeat the rest for however many entries there are
| offset+0x10                    | Chunk Type           | Little Endian 32-Bit Integer      | Chunk type                        |
| offset+0x14                    | Chunk Offset         | Little Endian 32-Bit Integer      | Data offset                       |
| offset+0x18                    | Chunk Size           | Little Endian 32-Bit Integer      | Data size                         |
| offset+0x1C                    | nothing              | 4 Bytes                           | Reserved                          |

# Compressed files
If a file is compressed, it starts with the following bytes:
- "ZB" (LZB section)
- "ZW" (LZW section)
