This is a breakdown of the Leapster RIB format. This also gets used on the LeapReader, Tag, Tag Jr. and Fly Pentop Computer.

All variables are little endian!

# Chorus RIB Table structure

| Offset (Hex) | Variable Name                | Data Size | Description                                      |
|--------------|------------------------------|-----------|----------------------------------------------------------|
| 0x100        | signature                    | 0x18      | "Copyright LeapFrog" signature (terminated by 00, 00 is included)  |
| 0x118        | ChorusRIBTableMinorVersion   | Byte      | Minor version of the Chorus RIB Table            |
| 0x119        | ChorusRIBTableMajorVersion   | Byte      | Major version of the Chorus RIB Table            |
| 0x11A        | ribCount                     | 16-Bit Integer      | Number of RIB entries                            |
| 0x11C        | deviceStartAddress           | 32-Bit Integer      | Start address of the device (subtract from all pointers!)|
| 0x120        | deviceEndAddress             | 32-Bit Integer      | End address of the device                        |
| 0x124        | pFullChecksum                | 32-Bit Integer      | Full checksum pointer                            |
| 0x128        | pSparseChecksum              | 32-Bit Integer      | Sparse checksum pointer                          |
| 0x12C        | pBootSafeFcnTable            | 32-Bit Integer      | Boot safe function table pointer (always zero?)  |
| 0x130        | reserved                     | 0x04      | Reserved                                         |
| 0x134        | reserved                     | 0x04      | Reserved                                         |
| 0x138        | reserved                     | 0x04      | Reserved                                         |
| 0x13C        | reserved                     | 0x04      | Reserved                                         |
| 0x140        | ribTable                     | 32-Bit Integer      | Start address of the RIB table                   |

# RIB Table structure

| Address                        | Variable Name        | Data Size | Description                       |
|--------------------------------|----------------------|-----------|--------------------------------------------|
| ribTable+0x00                  | signature            | 0x04      | RIB signature                     |
| ribTable+0x04                  | RIBMinorVersion      | Byte      | Minor version of the RIB          |
| ribTable+0x05                  | RIBMajorVersion      | Byte      | Major version of the RIB          |
| ribTable+0x06                  | resourceGroupCount   | 16-Bit Integer      | Number of resource groups         |
| ribTable+0x08                  | reserved             | 0x04      | Reserved                          |
| ribTable+0x0C                  | reserved             | 0x04      | Reserved                          |
| ribTable+0x10                  | reserved             | 0x04      | Reserved                          |
| ribTable+0x14                  | reserved             | 0x04      | Reserved                          |
| ribTable+0x18                  | reserved             | 0x04      | Reserved                          |
| ribTable+0x1C                  | reserved             | 0x04      | Reserved                          |

Repeat the next part however many times resourceGroupCount specifies
| Address                        | Variable Name        | Data Size | Description                                |
|--------------------------------|----------------------|-----------|--------------------------------------------|
| ribTable+0x20                  | RIB_Group_ID         | 16-Bit Integer      | RIB Group ID                               |
| ribTable+0x22                  | count                | 16-Bit Integer      | Number of entries in this group table      |
| ribTable+0x24                  | offset               | 32-Bit Integer      | Start offset of the table                  |


# RIB group IDs
These are little endian values that get read as shorts by the Leapster.
| ID                        | Name              | Description                                               |
|---------------------------|-------------------|-----------------------------------------------------------|
| 0x1000                    | Boot              | Might control where execution starts?                     |
| 0x1001                    | Modules           | Libraries used by the current program are referenced here |
| 0x1002                    | Unknown           | No documentation exists for this one.                     |
| 0x1003                    | Product Info      | The game title, ID, build date and other info             |
| 0x1004                    | Unknown           | No documentation exists for this one.                     |
| 0x1005                    | Group             | What this does is unknown. Group is the actual name here. |
| 0x1006                    | Asset             | Where all common assets are stored (SFX, music, instruments...) |
| 0x1007-0x1008             | Unknown           | No documentation exists for these ones.                   |
| 0x1009                    | System Apps       | What this actually does is unknown                        |
| 0x100A-0x100B             | Unknown           | No documentation exists for these ones.                   |
| 0x100C                    | Leapster Datasets | Stores datasets used for educational stuff (unknown format) |
| 0x100D                    | C-Style Datasets  | Stores datasets used for educational stuff (compiled?) |
| 0x100E-0x1FFF             | Unknown           | No documentation exists for these ones.                   |
| 0x2000                    | Leapster Apps     | What this actually does is unknown                        |
| 0x2001-0x3000             | Unknown           | No documentation exists for these ones.                   |
| 0x3001                    | Group (2)         | Like the previous one named "Group", what this is for is unknown. |
| 0x3002-0xFFFF             | Unknown           | No documentation exists for these ones.                   |


# Group structure
| Address                                | Variable Name        | Data Type                         | Description                       |
|-----------------------|----------------------|-----------------------------------|-------------------------------------------|
| groupTableOffset+0x00 | dataID               | 16-Bit Integer      | Data identifier                           |
| groupTableOffset+0x02 | groupMinorVersion    | Byte                | Minor version of the current table index  |
| groupTableOffset+0x03 | groupMajorVersion    | Byte                | Major version of the current table index  |
| groupTableOffset+0x04 | dataOrDataOffset     | 32-Bit Integer      | Can either be an offset or 4 bytes of data (like the part number in hex) |


# Index Table structures (to-do)

