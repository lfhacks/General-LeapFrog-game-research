This is a breakdown of the Leapster RIB format. This also gets used on the LeapReader, Tag, Tag Jr. and Fly Pentop Computer.

All variables are little endian!

# Chorus RIB Table structure

| Offset (Hex) | Variable Name                | Data Size | Description                                      |
|--------------|------------------------------|-----------|----------------------------------------------------------|
| 0x100        | signature                    | 0x18      | ROM signature (terminated by 00, 00 is included  |
| 0x118        | ChorusRIBTableMinorVersion   | 0x01      | Minor version of the Chorus RIB Table            |
| 0x119        | ChorusRIBTableMajorVersion   | 0x01      | Major version of the Chorus RIB Table            |
| 0x11A        | ribCount                     | 0x02      | Number of RIB entries                            |
| 0x11C        | deviceStartAddress           | 0x04      | Start address of the device (subtract from all pointers!)|
| 0x120        | deviceEndAddress             | 0x04      | End address of the device                        |
| 0x124        | pFullChecksum                | 0x04      | Full checksum pointer                            |
| 0x128        | pSparseChecksum              | 0x04      | Sparse checksum pointer                          |
| 0x12C        | pBootSafeFcnTable            | 0x04      | Boot safe function table pointer (always zero?)  |
| 0x130        | reserved                     | 0x04      | Reserved                                         |
| 0x134        | reserved                     | 0x04      | Reserved                                         |
| 0x138        | reserved                     | 0x04      | Reserved                                         |
| 0x13C        | reserved                     | 0x04      | Reserved                                         |
| 0x140        | ribTable                     | 0x04      | Start address of the RIB table                   |

# RIB Table structure

| Address                        | Variable Name        | Data Size | Description                       |
|--------------------------------|----------------------|-----------|--------------------------------------------|
| ribTable+0x00                  | signature            | 0x04      | RIB signature                     |
| ribTable+0x04                  | RIBMinorVersion      | 0x01      | Minor version of the RIB          |
| ribTable+0x05                  | RIBMajorVersion      | 0x01      | Major version of the RIB          |
| ribTable+0x06                  | resourceGroupCount   | 0x02      | Number of resource groups         |
| ribTable+0x08                  | reserved             | 0x04      | Reserved                          |
| ribTable+0x0C                  | reserved             | 0x04      | Reserved                          |
| ribTable+0x10                  | reserved             | 0x04      | Reserved                          |
| ribTable+0x14                  | reserved             | 0x04      | Reserved                          |
| ribTable+0x18                  | reserved             | 0x04      | Reserved                          |
| ribTable+0x1C                  | reserved             | 0x04      | Reserved                          |

Repeat the next part however many times resourceGroupCount specifies
| Address                        | Variable Name        | Data Size | Description                       |
|--------------------------------|----------------------|-----------|--------------------------------------------|
| ribTable+0x20                  | RIB_Group_ID         | 0x02      | RIB Group ID                      |
| ribTable+0x22                  | count                | 0x02      | Number of entries in this table   |
| ribTable+0x24                  | offset               | 0x04      | Start offset of the table         |


# RIB group IDs (to-do)


# Index Table structures (to-do)

