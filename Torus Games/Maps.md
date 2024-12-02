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

Below is a few examples of assembled blocks:

![block_0](https://github.com/user-attachments/assets/bfe7bc8e-f958-4fcc-85d2-9912bb882641)

![block_175](https://github.com/user-attachments/assets/3c04c5cb-0708-4530-8b6d-11b7b59fc9d0) ![block_176](https://github.com/user-attachments/assets/6bff3a1f-f342-4105-ae7b-540d2e0267ea) ![block_177](https://github.com/user-attachments/assets/a698f2b5-3fc0-4852-a8d2-3e60d0e4ecf8)



## Background map
The format here is almost identical, but it uses the constructed blocks to assemble a map. The flip bits are still here, but the palette values aren't.

| Address                        | Variable Name        |
|--------------------------------|----------------------|
| 0x0                    | Block index  |
| Info                   | Repeat for X*Y blocks |

Below is a few examples of assembled maps:

![output](https://github.com/user-attachments/assets/9f523fcd-5fc8-431d-b75a-93c3a853d166)

![output](https://github.com/user-attachments/assets/8916dec0-00e3-4e78-9961-9c363e1673e1)
