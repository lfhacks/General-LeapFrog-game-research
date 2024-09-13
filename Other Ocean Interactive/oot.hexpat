#pragma author applecuckoo
#pragma description Other Ocean Interactive .oot (Other Ocean Texture?)

#pragma endian little

enum ByteLayout : u32 {
    RGBA5551,
    RGBA4444,
    RGB565
};

struct OOTHeader {
    // 64 bytes long. We don't know what the majority of this is.
    padding[4]; // could be a CRC or other checksum?
    u32 originalWidth;
    u32 originalHeight;
    u32 width;
    u32 height;
    padding[16];
    ByteLayout byteLayout;
    padding[24];
};

OOTHeader header @ 0x00;