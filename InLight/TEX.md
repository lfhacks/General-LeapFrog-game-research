# InLight .TEX format

There seem to be two variations of .TEX files. One variant has a 16-byte header that goes before the compressed zlib stream, while the other variant seems to only consist of the zlib stream itself, and as such, the image header is compressed with the raw image data.

## Variant 1 (uncompressed header)

| Offset | Size | Description |
| ------ | ---- | ----------- |
| 0x00 | u32 | Unknown |
| 0x04 | u32 | Width |
| 0x08 | u32 | Height |
| 0x0c | u32 | Image size |

## Variant 2 (compressed header)

736 bytes long, ends with 0xDF repeated 8 times. Tends to be tiled (?)
### Variant 3 (`IL_TEXTR` magic)

| Offset | Size | Description |
| ------ | ---- | ----------- |
| 0x00 | u64 | Magic (`IL_TEXTR`) |
| 0x08 | u32 | Unknown (version?) |
| 0x0c | u32 | Byte layout (0 = RGBA8888, 1 = RGBA4444, 2 = RGBA5551) |
| 0x10 | u32 | Width |
| 0x14 | u32 | Height |
| 0x18 | u32 | Compressed image size |
| 0x1c | u32 | Unknown |
| 0x20 | u32 | Unknown |
