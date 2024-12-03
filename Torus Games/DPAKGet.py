#The Torus Games functions (combined into one script for the sake of simplification)
import struct
from PIL import Image
import math
import os
import tkinter as tk #Used to kill the extra tkinter window
from tkinter import filedialog

root = tk.Tk()#Create a root window
root.withdraw()#Hide the root window
file = filedialog.askopenfilename()
ROMName = os.path.basename(file).split(".")[0]
root.destroy()#Destroy the root window

def DPAKExtract(file, offset):
    files = []
    chunks = []
    #These 3 variables are used to save the entire DPAK alongside the split sections
    headerPostTorus = b''#Holds the header data from after the "Torus" string
    dataChunks = b''     #Where the data chunks go
    completeDPAK = b''   #Where everything gets combined to
    with open(file, "rb") as rom:
        rom.seek(offset)
        identifier = rom.read(4)
        entries = rom.read(2)
        torus = rom.read(0xA)
        for entry in range(struct.unpack("<H", entries)[0]):
            chunkType = struct.unpack("<I", rom.read(4))[0]
            dataOffset = struct.unpack("<I", rom.read(4))[0]+offset
            dataSize = struct.unpack("<I", rom.read(4))[0]
            nothing = rom.read(4)
            headerPostTorus += struct.pack("<III", chunkType, dataOffset-offset, dataSize)+nothing
            currentOffset = rom.tell()
            rom.seek(dataOffset)
            data = rom.read(dataSize)
            dataChunks += data
            files.append(data)
            chunks.append(chunkType)
            rom.seek(currentOffset)
    fullData = [identifier, entries, torus, headerPostTorus, dataChunks]
    
    for data in fullData:
        completeDPAK += data
    return files, chunks, completeDPAK

def readbgr555(file, offset, height):
    with open(file, 'rb') as f:
        f.seek(offset)
        paletteData = f.read(16*(height*2))
        print(f"Total palettes: {16*(height)}")
    return paletteData

def bgr555toRGB(color):
    b = (color & 0b0111110000000000) >> 7
    g = (color & 0b0000001111100000) >> 2
    r = (color & 0b0000000000011111) << 3
    return (r, g, b)

def paletteToImage(paletteData, width, height):
    img = Image.new('RGB', (width, height))
    pixels = img.load()
    for i in range(min(height*16, width * height)):
        color = struct.unpack('<H', paletteData[i*2:i*2+2])[0]
        rgb = bgr555toRGB(color)
        x = i % width
        y = i // width
        pixels[x, y] = rgb
    return img

def paletteConverter(file, offset, width, height):
    paletteData = readbgr555(file, offset, height)
    img = paletteToImage(paletteData, width, height)
    return img

def getPalette(file):
    with open(file, "rb") as f:
        f.seek(4)
        spriteCount = struct.unpack("<H", f.read(2))[0]
        paletteOffset = struct.unpack("<H", f.read(2))[0]
        spriteOffset = struct.unpack("<H", f.read(2))[0]
        width = 16
        f.seek(paletteOffset)
        height = struct.unpack("<I", f.read(4))[0]
        paletteOffset = paletteOffset+4
        image = paletteConverter(file, paletteOffset, width, height)
        return image

def checkForByteString(path, string):
    with open(path, 'rb') as file:
        content = file.read()
        offset = content.find(string)
        return string in content, offset
    
DPAKCheck = checkForByteString(file, b'DPAK')

if DPAKCheck[0]: #Torus DPAK found (contains sprites, maps and level data for games from Torus)
    print(f"Torus Games DPAK found at offset {hex(DPAKCheck[1])}!")
    torusOut = [os.getcwd()+f"/Split_ROMs/{ROMName}/Torus/",
                os.getcwd()+f"/Split_ROMs/{ROMName}/Torus/split/"]
    for outputPath in torusOut:
        if os.path.exists(outputPath) == False:
            os.makedirs(outputPath)
    DPAKOffset = DPAKCheck[1]
    files, chunkIDs, fullDPAK = DPAKExtract(file, DPAKOffset)
    index = 0
    with open(torusOut[0]+"Torus Data Package.DPAK", "w+b") as out:
        out.write(fullDPAK)
    for file in files:
        try:
            with open(torusOut[1]+f"DPAK_Identifier_{chunkIDs[index]}_Index_{index}.bin", "w+b") as out:
                out.write(file)
                if file[0:4] == b'\x01\x00\x00\x00':
                    print(f"Stage layouts are stored in DPAK_Identifier_{chunkIDs[index]}_Index_{index}.bin")
                if file[0:4] == b'\x04\x00\x01\x00':
                    print(f"Sprites are stored in DPAK_Identifier_{chunkIDs[index]}_Index_{index}.bin")
                    image = getPalette(torusOut[1]+f"DPAK_Identifier_{chunkIDs[index]}_Index_{index}.bin")
                    image.save(torusOut[1]+f"palette.png")
                if file[0:4] == b'SPRT':
                    print(f"LZB/LZW-compressed sprites are stored in DPAK_Identifier_{chunkIDs[index]}_Index_{index}.bin")
                if file[0:4] == b'MDE7':
                    print(f"(Likely LZB/LZW-compressed) race tracks are stored in DPAK_Identifier_{chunkIDs[index]}_Index_{index}.bin")
                if file[0:4] == b'MUSC':
                    print(f"Music and sound effects are stored in DPAK_Identifier_{chunkIDs[index]}_Index_{index}.bin")
        except:
            pass #In case another DPAK with that exact index and ID assigned to a section exists
        index+=1
