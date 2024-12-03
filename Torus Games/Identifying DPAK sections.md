# Identifying DPAK sections using their headers
Below is a list of checks you can do to identify what each section is:

| Section type | What to check for |
| Audio (GBA-exclusive) | "MUSC" |
| Sprites (compressed) | "SPRT" |
| Sprites (uncompressed, V3) | 03000100 |
| Sprites (uncompressed, V4) | 04000100 |
| Maps (normal, compressed, V3) | skip the first 4 bytes and check for 03000100 |
| Maps (normal, compressed, V4) | skip the first 4 bytes and check for 04000100 |
| Maps (racing games) | "MDE7" |
| Stage layouts/object names | 01000000 |
