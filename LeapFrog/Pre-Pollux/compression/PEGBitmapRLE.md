# PEG Bitmap RLE decompression info
This format is actually a direct copy of TGA RLE compression. I'll still describe it below, but you can probably already find open source code samples that can decode it.

Because decompressing a PEG Bitmap requires information from the header (specifically the width and the height because there's no compressed length or terminator value), this is the structure:

| Value name              | Bit width      |
|-------------------------|----------------|
| Unknown                 | 8-Bit          |
| Bits per pixel          | 8-Bit          |
| Width                   | 16-Bit         |
| Height                  | 16-Bit         |
| Unknown                 | 32-Bit         |
| Padding                 | 16-Bit         |
| Pixel data start offset | 32-Bit pointer |

Every chunk starts with a command byte. The count can be obtained from it with the following code:

(command & 0x7F) + 1

If the highest bit is 1, the decompressor is in repeat mode (read a single pixel and repeat it count number of times)

If the highest bit is 0, the decompressor is in literal mode (read pixels count number of times)
