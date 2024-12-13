import struct
import tkinter as tk
from tkinter import filedialog
import mido
import os

root = tk.Tk()
root.withdraw()
files = filedialog.askopenfilenames()
root.destroy()
def convert_tempo(tempo_number):
    #print(tempo_number)
    tempo_number = int(tempo_number)
    if 1 <= tempo_number <= 0xFFF:
        midi_tempo = 600000000 // (tempo_number//2)
        return midi_tempo
    else:
        raise ValueError("Tempo number must be between 1 and 0xFFF")



def add_midi_message(message_type, channel, data1, data2, delta_time):
    global current_time
    if message_type == 'program_change':
        track.append(mido.Message('program_change', program=data1, channel=channel, time=delta_time))
    elif message_type == 'note_on':
        track.append(mido.Message('note_on', note=data1, velocity=data2, channel=channel, time=delta_time))
    elif message_type == 'note_off':
        track.append(mido.Message('note_off', note=data1, velocity=0, channel=channel, time=delta_time))

for file_path in files:
    mid = mido.MidiFile()
    track = mido.MidiTrack()
    mid.tracks.append(track)
    with open(file_path, "rb") as sun:
        prevnotes = []
        lastNote = 0
        while True:
            data = sun.read(2)
            if not data:
                break  # End of file
            if data[1] in range(0x27, 0x2F): #Set tempo
                tempo = data[0]
                if data[1] >= 0x27:
                    tempobytemain = f"{data[0]:02x}"
                    tempoconverted = int(f"{int(data[1] & 0x0F) - 7:01x}{tempobytemain}", 16)
                    tempo = tempoconverted
                    track.append(mido.MetaMessage('set_tempo', tempo=convert_tempo(tempo)))
            if data[1] in range(0, 16): #Program change
                channel = data[1]
                add_midi_message('program_change', channel, data[0], None, 0)
            if data[1] == 0x10: #Pitchwheel (and others?)
                bend = sun.read(2)
                #Left this in just in case anyone wants to try to figure it out
                #print(hex(data[1]), hex(data[0]), hex(bend[1]), hex(bend[0]))
                
            if data[1] == 0x40: #Beat count value (might be how long the notes are all held for?)
                var = 0 #The current channel
                for note in prevnotes:
                    add_midi_message('note_off', note[1], note[0], 0, data[0])
                    data = data.replace(struct.pack("<B", data[0]), b'\x00')
                if len(prevnotes) == 0: #I put this in to get around pitch bends for now.
                    add_midi_message('note_off', 0, 0, 0, data[0])
                prevnotes = [] #Clear the previous notes
                
            if data[1] in range(0x80, 0x8F): #Most likely note data. There can be multiple of these in a row, but they always eventually get followed up with a beat count value (the previous thing in this script)
                channel = int(str("0x"+str(hex(data[0]))[2]), 16) #The channel ID
                DT1 = str(hex(data[1]))[3]
                DT2 = str(hex(data[0]))[2]
                DT = int(f"0x{DT1}{DT2}", 16) #Unknown, is not duration like I thought it was though
                data2 = sun.read(2) #Should hold the pitch info. Byte 2 (1 in Python) is always 0x40.
                data3 = sun.read(2) #Should hold the volume info
                volume = data3[0]
                pitch = data2[0]
                note = pitch, channel
                prevnotes.append(note)
                lastNote = data2[0]
                add_midi_message('note_on', channel, data2[0], data3[0], 0)
    
    #Save our MIDI
    base, ext = os.path.splitext(file_path)
    output_path = f"{base}_converted.mid"
    mid.save(output_path)
    print(f"Conversion complete! MIDI file saved as {output_path}")
