# WayForward Leapster sprite transparency RLE decompression info
This is a very simple algorithm. The color pixel data is uncompressed, but the transparent pixels are.

It's designed with storing graphics in RAM shortly before drawing them to the screen in mind (so already drawn visuals can be reused).

## Format
Each chunk starts with a 16-bit value. We can decode it like this:

- Read 1 byte for the transparent pixel count
- Read 1 byte for the literal (already uncompressed pixel) count

Now do the following:

- Run a loop that appends (transparent pixel count) repeated copies of 0x00 0xF0 to the data
- Run a loop that reads the following 16-Bit BGRA4444 (or RGBA4444?) pixel color values out of the data

That's literally all there is to this algorithm.
