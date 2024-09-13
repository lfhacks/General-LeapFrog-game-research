# Other Ocean Interactive .oot (Other Ocean Texture?)

64 byte header (all values are little endian):

| Offset | Size | Description |
| ------ | ---- | ----------- |
| 0x00 | u32 | Unknown (id/checksum?) |
| 0x04 | u32 | Original width (crop to this width) |
| 0x08 | u32 | Original height (crop to this height) |
| 0x0c | u32 | Width (actual width of the image data) |
| 0x10 | u32 | Height (actual height of the image data) |
| 0x14 | u32 | Unknown |
| 0x18 | u32 | Unknown |
| 0x1c | u32 | Unknown |
| 0x20 | u32 | Unknown |
| 0x24 | u32 | Byte layout for each pixel, RGBA5551 = 0x00, RGBA4444 = 0x01, RGB565 = 0x02 |
| 0x28 | u32 | Unknown |
| 0x2c | u32 | Unknown |
| 0x30 | u32 | Unknown |
| 0x34 | u32 | Unknown |
| 0x38 | u32 | Unknown |
| 0x3c | u32 | Unknown |

The rest is the raw pixel data.
