from codingTools import *
syn = dialogs.file()
#A quick and simple LeapFrog SYN decoder for testing and research purposes
def decodeSYN(syn, offsets, system): #Pass the already partially parsed SYN to this function
    midis = []
    index = 0
    for offset in offsets:
        volume = 0x64
        midi = MidiFileHandler()
        midiFile, track = midi.create_midi_file()
        midi.add_track_name(track, f'{system} test {index}')
        midi.add_tempo_change(track, midi.bpm_to_tempo(32))
        syn.seek(offset)
        decoder = BE_BitReader(syn)
        while True:
            data = decoder.read(8) #Read 8 bits (1 byte)
            if data in range(0, 0x7F):
                variableWidthBit = decoder.read(1)
                if variableWidthBit == 0:
                    duration = decoder.read(7)
                    #print(f'Note = {data}, duration = {duration}')
                    if data != 0:
                        midi.add_note(track, data, duration, volume)
                    else:
                        track.append(midi.create_note_off_message(data, volume, time=duration))
                    
                else:
                    duration = decoder.read(15)
                    if data != 0:
                        midi.add_note(track, data, duration, volume)
                    else:
                        track.append(midi.create_note_off_message(data, volume, time=duration))
                    #print(f'Note = {data}, duration = {duration}')
            elif data == 0x88:
                volume = decoder.read(8) #Volume
                #print(f'Volume = {volume}')
            elif data == 0x89:
                data = decoder.read(8)
                if data == 0xC0:
                    instrument = decoder.read(8)
                    #print(f'Program change - cartridge instrument {instrument}')
                    track.append(midi.create_program_change_message(instrument))
                else:
                    #print(f'Program change - BaseROM instrument {data}')
                    track.append(midi.create_program_change_message(data))
            elif data == 0x8A:
                bend = decoder.read(8)
                variableWidthBit = decoder.read(1)
                if variableWidthBit == 0:
                    duration = decoder.read(7)
                    track.append(midi.create_pitch_bend_message(bend, time=duration))
                    #print(f'Pitch bend = {bend}, duration = {duration}')
                else:
                    duration = decoder.read(15)
                    track.append(midi.create_pitch_bend_message(bend, time=duration))
                    #print(f'Pitch bend = {bend}, duration = {duration}')
            elif data == 0x8E:
                loops = decoder.read(8)
            elif data == 0x8F:
                padding = decoder.read(8)
            elif data == 0xFF:
                break
        midi.save_midi_file(midiFile, f'TEST_MIDI_{index:02}.mid')
        midis.append(f'TEST_MIDI_{index:02}.mid')
        index+=1
    midi.combine_midi_files(midis, "Combined test.mid")

with open(syn, "rb") as f: #Decode the header and parse the SYN file. trackOffsets stores offsets, system is used in the track name, f is the file.
    trackOffsets = []
    headCheck = f.read(2)
    if headCheck != b'\x02\x00': #LeapPad SYN
        f.seek(0)
        trackOffsets = BE_multiunpack.ushort(f.read(12))
        system = "LeapPad"
    else: #Leapster SYN
        trackCount = LE_unpack.ushort(f.read(2))
        for track in range(trackCount):
            offset = LE_unpack.ushort(f.read(2))
            ID = BE_unpack.ushort(f.read(2))
            trackOffsets.append(offset)
        system = "Leapster"
    decodeSYN(f, trackOffsets, system)
