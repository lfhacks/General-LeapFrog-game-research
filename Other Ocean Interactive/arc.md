Some Leapster Explorer and LeapPad Explorer games from Other Ocean Interactive have a data.arc file. It's a container with raw, headerless LZMA-compressed data. There's no stream end bytes either.

The dictionary size is 0x80000

lc is 3

lp is 0

pb is 2

Games that used this format (INCOMPLETE!):
- LeapSchool Reading


Header structure:
| Address                        | Variable Name        | Data Type                         | Description                       |
|--------------------------------|----------------------|-----------------------------------|-----------------------------------|
| 0x0                            | Uncompressed size    | 32-Bit little endian integer      | The uncompressed file table size  |
| 0x4                            | Compressed size      | 32-Bit little endian integer      | The compressed file table size    |
| 0x8                            | Compressed data start| Raw LZMA-compressed data          | The compressed file table data    |

File table structure (you need to decompress it first!):
| Address                        | Variable Name        | Data Type                         | Description                       |
|--------------------------------|----------------------|-----------------------------------|-----------------------------------|
| 0x0                            | First filename       | String                            | A zero-terminated string (the zero is included here) |
| End of name + 0                | File offset          | 32-Bit integer                    | (For data *after* the compressed file table) |
| Emd of name + 4                | Uncompressed size    | 32-Bit integer                    | Note: You need to get the compressed size using the next entry |

Files are also compressed, so they need to be decompressed as well.
