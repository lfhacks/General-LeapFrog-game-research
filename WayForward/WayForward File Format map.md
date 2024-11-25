# What does what here exactly?
The following table should list every single file type and what it's used for:

| Format | Description                                                           | Additional info |
|--------|-----------------------------------------------------------------------|-----------------|
| ANM    | These store sprites and animations, but can be both 4BPP and 8BPP     | - | 
| AN4    | These store sprites and animations, but are always 4BPP               | - |
| AN8    | These store sprites and animations, but are always 8BPP               | - |
| LYR    | These use TS4/TS8 files to construct a map or an image                | There's a file table that gets stored in the game executable. Use that for the TS8 filenames it references. |
| SCN    | These store "scenery"/object placement data                           | - |
| TS4    | These store 4BPP tiles that get constructed into 16x16 blocks         | - |
| TS8    | These store 8BPP tiles that get constructed into 16x16 blocks         | - |
