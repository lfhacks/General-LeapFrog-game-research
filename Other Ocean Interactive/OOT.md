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

Some example decoded oot files:




<img width="56" height="52" alt="hamster2" src="https://github.com/user-attachments/assets/01126c64-e7ea-4b82-a7f7-83545d86b2a6" />
<img width="72" height="64" alt="hamster1" src="https://github.com/user-attachments/assets/357b00f2-a29d-47cc-8eec-8c92679fa056" />
<img width="320" height="240" alt="gig_smw" src="https://github.com/user-attachments/assets/e67aa090-1a48-4409-9691-c95462ac8262" />
