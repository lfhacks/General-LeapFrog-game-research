#pragma author applecuckoo
#pragma description LeapFrog Leapster RIB table - WIP!

import type.magic;
import std.string;

u32 LastOffset;
u32 deviceStartAddress_g;

enum RIBGroupType : u16 {
    Boot = 0x1000,
    Modules = 0x1001,
    ProductInfo = 0x1003,
    Group = 0x1005,
    AssetGroup = 0x1006,
    LeapsterSysApps = 0x1009,
    LeapsterDatasets = 0x100C,
    CStyleDatasets = 0x100D,
    LeapsterApps = 0x2000,
    Group2 = 0x3001
};

struct BootRIBGroup {
    u16 bootCount;
    u32 bootOffset;
};

struct ModRIBGroup {
    u16 modCount;
    u32 modOffset;
    LastOffset = $;
    $ = modOffset - deviceStartAddress_g;
    u32 test;
};

struct RIBGroup {
    RIBGroupType id;
    u16 count;
    u32 offset;
};

struct LeapFrogRIB {
    // start of LeapFrog RIB table
    type::Magic<"LEAP"> id;
    u8 LeapRIBMinorVersion;
    u8 LeapRIBMajorVersion;
    u16 resourceGroupCount;
    padding[24];
    RIBGroup ribGroups[resourceGroupCount];
};

struct ChorusRIB {
    type::Magic<"Copyright LeapFrog     \x00"> copyright;
    u8 ChorusRIBMinorVersion;
    u8 ChorusRIBMajorVersion;
    u16 ribCount;
    u32 deviceStartAddress;
    deviceStartAddress_g = deviceStartAddress;
    u32 deviceEndAddress;
    u32 pFullChecksum;
    u32 pSparseChecksum;
    u32 pBootSafeFcnTable;
    padding[16];
    u32 ribTable;
    
};

struct LeapsterROM {
    padding[0x100];
    ChorusRIB chorusRib;
    LeapFrogRIB lfRib @ chorusRib.ribTable - deviceStartAddress_g;
};

LeapsterROM rom @ 0x0;