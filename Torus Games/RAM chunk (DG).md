# RAM chunk format

### Note:
This format is exclusive to the GBA version. I'm keeping this up for others who may find it useful, but it isn't relevant here.

The memory in every game developed by Torus is split up into sections. Each chunk is structured like this:

| Address                        | Variable Name         | Data Type                         | Description                       |
|--------------------------------|-----------------------|-----------------------------------|-----------------------------------|
| 0x00                    | Header magic + version       | 4 Bytes                           | Header magic                       |
| 0x04                    | RAM chunk size               | 32-Bit Integer      | How large this chunk is in RAM           |
| 0x08                    | Offset of previous RAM chunk | 32-Bit Offset       | Where the previous section of memory is in RAM  |
| Rest of data            | Data | Data | The rest of the data in this chunk |
