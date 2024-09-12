# Introduction
This format was designed back in 1998 for the Odyssey Globe and is MIDI-like in how it works.

The actual sequence data barely changed (if it did at all) over the years it was used, the final major use being on the Leapster 2 in 2008.

# Sequence header structure (LeapPad)
The original LeapPad version of the format is super basic. The header only contains 6 track pointers - nothing else.

If a track doesn't exist, the pointer is just set to 0. The pointers are big endian 16-Bit integers.

# Sequence header structure (Leapster)
The files always start with 0x0200 followed up by the track count as a little endian 16-Bit integer.
After that is a pointer and an ID for each track, all being 16-Bit values. The pointers are little endian while the IDs are big endian. 

The IDs don't appear to do anything noteworthy (you can blank them all out with zero consequences), but they might determine the original track order or what order the tracks were initially converted in.

# Track structure (in other words, the command list)
Durations are variable width. If the first byte of a duration is 0x80, use the following byte as the true duration. Anything past this (it can go beyond the range of 0x80-0x8F) takes the first byte of the duration minus 0x80 and appends the resulting byte to the start of the next byte for the true duration.

Examples:
- 95 0F is actually a duration of 0x150F
- 80 AF is actually a duration of 0xAF

Program changes are only variable width if 0xC0 appears in place of the instrument ID! All this does is tell the sequencer to grab sounds from the cartridge instead of the BaseROM/BIOS.

Loop end and track end have a data byte, but it's always zero

Notes have a duration which can be put into a note off event in the converted MIDI to end the note after the specified amount of time. 

There is no "note on" or "note off" events in this format.

Commands 0x81-0x84 aren't needed in conversions, as they're exclusively used by the sound driver because of the limited hardware.

They don't do anything worthwhile!

| Command name | Command byte | Command data | Command is variable width |
| ------------------------- | :----------: | :---------------: | --------------------: |
| Note | 00-7F | Duration | Yes, up to 3 bytes long |
| PitchShift Required. | 81 | None | No, 1 byte |
| PitchShift not Required. | 82 | None | No, 1 byte |
| Reserve voice | 83 | None | No, 1 byte |
| Release voice | 84 | None | No, 1 byte |
| Set volume | 88 | Volume | No, 2 bytes only |
| Program change | 89 | Mode, Program | Yes, up to 3 bytes long |
| Pitch bend | 8A | Bend, Duration | Yes, up to 4 bytes long |
| Loop Start | 8E | Loop Count | No, 2 bytes only |
| Loop End | 8F | Unused (always 00) | No, 2 bytes only |
| Track End | FF | Unused (always 00) | No, 2 bytes only |

# Extra information relating to converting this format
When converting this format, be sure to follow this order of operations when handling the notes, as the note duration will be messed up if you don't:

- Create a note on event with a duration of 0
- Create a note off event after the note on event with the note's duration value

To handle the volume command, just store it in a variable and use it as every note's velocity until another volume command is hit.
