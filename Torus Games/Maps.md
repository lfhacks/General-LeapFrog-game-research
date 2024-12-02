# Torus Games map format
How these are scaled is currently unknown! That information is stored separately from the map data itself.

## Block map
Block maps construct 32x32 blocks out of 4 8x8 tiles each. Below is how a single block would be formatted:

| Address                        | Variable Name        |
|--------------------------------|----------------------|
| 0x0    | Tile 1 index |
| 0x2    | Tile 2 index |
| 0x4    | Tile 3 index |
| 0x6    | Tile 4 index |

The first 6 bits of the tile index value also control the color palette and flip. Below is the structure of one:

PPPPVHIIIIIIIIII

P is the palette index, V is vertical, H is horizontal, I is the tile index.

## Background map
The format here is almost identical, but it uses the constructed blocks to assemble a map. The flip bits are still here, but the palette values aren't.

| Address                        | Variable Name        |
|--------------------------------|----------------------|
| 0x0                    | Block index  |
| Info                   | Repeat for X*Y blocks |
