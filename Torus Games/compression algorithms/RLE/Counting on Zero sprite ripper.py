from codingTools import *

def decompressSprite(inputFilename, offset, version, maxWidth=512, maxHeight=512, maxBytes=381920, XAdjust=0, YAdjust=0): #Adjustment values need bug fixing. Too lazy to do that for now, but I might do it later.
    with open(inputFilename, "rb") as tseRLE:
        tseRLE.seek(offset)
        RLEReader = BE_BitReader(tseRLE)
    
        #Initialize canvas
        canvas = [[0 for X in range(maxWidth)] for Y in range(maxHeight)]
        
        #State variables
        nibbleIndex = 0 #The script originally read in nibbles. I switched over to a bit reader to simplify it.
        xPos = 0+XAdjust
        yPos = 0+YAdjust
        startX = 0+XAdjust
        maxXUsed = 0
        maxYUsed = 0
        paletteIndex = 0
        
        if version == 0: #Counting on Zero for the Leapster L-MAX
            while nibbleIndex < (maxWidth*maxHeight) * 2 and yPos < maxHeight:
                #Read 3 bits for the command
                command = RLEReader.read(3)
                    
                    
                nibbleIndex += 1
                
                if command <= 3: #Horizontal movement
                    #Read remaining chunk of displacement value and combine with the command value
                    displacement = (command << 5)| RLEReader.read(5) 
                    nibbleIndex += 1
                    
                    xPos += displacement
                    
                elif command == 4: #Set palette index
                    RLEReader.read(1) #For alignment purposes, read 1 bit
                    paletteIndex = RLEReader.read(4) << 4 #Bit shift it early for the 8BPP conversion process
                    nibbleIndex += 1
                    
                elif command == 5: #Draw pixels
                    #Read run length nibble
                    runLength = RLEReader.read(5)
                    nibbleIndex += 1
                    
                    #Draw the run of pixels
                    for i in range(runLength):
                        #Read pixel data
                        pixelData = RLEReader.read(4)
                        nibbleIndex += 1
                        #Combine the palette index with the pixel's color index to convert from 4bpp over to 8bpp
                        pixelValue = paletteIndex | pixelData
                        
                        #Plot pixel if within bounds
                        if xPos + i < maxWidth and yPos < maxHeight:
                            canvas[yPos][xPos + i] = pixelValue
                            maxXUsed = max(maxXUsed, xPos + i + 1)
                            maxYUsed = max(maxYUsed, yPos + 1)
                    
                    xPos += runLength
                    
                elif command == 6: #Next row
                    RLEReader.read(1) #For alignment purposes, read 1 bit
                    yPos += 1
                    xPos = startX  #Reset to left edge
                    
                elif command == 7: #Reset to left edge
                    RLEReader.read(1) #For alignment purposes, read 1 bit
                    xPos = startX
                
                #Safety check
                if nibbleIndex > maxBytes * 2:
                    break
        #Do not use the code below! It's currently completely broken.
##        elif version == 1: #Cars, Cars Supercharged, NASCAR, Didji Racing: Tiki Tropics
##            while nibbleIndex < (maxWidth*maxHeight) * 2 and yPos < maxHeight:
##                #Read 3 bits for the command
##                command = RLEReader.read(3)
##                    
##                nibbleIndex += 1
##
##                if command == 0 or command == 1:  #Skip pixels
##                    count = RLEReader.read(5)
##                    nibbleIndex += 1
##
##                    skipAmount = (count | command << 5) + 1
##                    xPos += skipAmount
##                    
##                elif command == 2 or command == 3:  #Draw pixel run
##                    #Read count variable
##                    count = RLEReader.read(5)
##                    nibbleIndex += 1
##                    
##                    runLength = (count | (command << 5)) + 1
##
##                    for i in range(runLength):
##                        #Read color index nibble
##                        colorIndexNibble = RLEReader.read(4)
##                        nibbleIndex += 1
##                        
##                        #Combine the palette index with pixel color index to convert over to 8BPP
##                        indexValue = paletteIndex | colorIndexNibble
##                        
##                        #Plot pixel if within bounds
##                        currentX = xPos + i
##                        if currentX < maxWidth and yPos < maxHeight:
##                            canvas[yPos][currentX] = indexValue
##                            maxXUsed = max(maxXUsed, currentX + 1)
##                            maxYUsed = max(maxYUsed, yPos + 1)
##                    
##                    xPos += runLength
##                    
##                elif command == 4:  #Change palette bank
##                    RLEReader.read(1) #For alignment purposes
##                    #Read palette bank value
##                    bank = RLEReader.read(4)
##                    nibbleIndex += 1
##                    
##                    #Set the palette index
##                    paletteIndex = bank << 4
##                    
##                elif command == 5:  #Fill with single color index
##                    #Read the fill length
##                    fillLength = (RLEReader.read(5)) + 4
##                    nibbleIndex += 1
##                    
##                    #Read the color index nibble
##                    colorIndexNibble = RLEReader.read(4)
##                    nibbleIndex += 1
##                    
##                    #Repeatedly draw a single color to the canvas
##                    pixelValue = paletteIndex | colorIndexNibble #Convert color index to 8bpp
##                    for i in range(fillLength):
##                        currentX = xPos + i
##                        if currentX < maxWidth and yPos < maxHeight:
##                            canvas[yPos][currentX] = pixelValue
##                            if colorIndexNibble != 0:
##                                maxXUsed = max(maxXUsed, currentX + 1)
##                            maxYUsed = max(maxYUsed, yPos + 1)
##                    
##                    xPos += fillLength
##                    
##                elif command == 6:  #Next row
##                    RLEReader.read(1) #Align the bit reader
##                    yPos += 1
##                    xPos = startX  #Reset to left edge
##                    
##                elif command == 7:  #Reset X position
##                    RLEReader.read(1) #Align the bit reader
##                    xPos = startX
##
##                #Safety check
##                if nibbleIndex > maxBytes * 2:
##                    break
        #Convert canvas to color index data
        pixels = bytearray()
        for y in range(maxHeight):
            for x in range(maxWidth):
                pixels.append(canvas[y][x] & 0xFF)
        
    return pixels, maxWidth, maxHeight

def DPAKExtract(file, offset): #Excuse any potential ugliness in this code, it's old. This is used if the user attempts to run this script on a ROM instead of a DPAK container.
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
        for entry in range(LE_unpack.ushort(entries)):
            chunkType = LE_unpack.uint(rom.read(4))
            dataOffset = LE_unpack.uint(rom.read(4))+offset
            dataSize = LE_unpack.uint(rom.read(4))
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

def checkForByteString(path, string):
    with open(path, 'rb') as file:
        content = file.read()
        offset = content.find(string)
        return string in content, offset

def checkForEmbeddedDPAK(file):
    DPAKCheck = checkForByteString(file, b'DPAK')

    if DPAKCheck[0]: #Torus DPAK found (contains sprites, maps and level data for games from Torus)
        print(f"Torus Games DPAK found at offset {hex(DPAKCheck[1])}!")
        DPAKOffset = DPAKCheck[1]
        files, chunkIDs, fullDPAK = DPAKExtract(file, DPAKOffset)
        index = 0
        with open("PackedAssets.DPAK", "w+b") as out:
            out.write(fullDPAK)
        return "PackedAssets.DPAK"

def readSPRTSectionHeader(DPAK, baseOffset): #Header is unchanged between formats, so this should be reusable
    DPAK.seek(baseOffset)
    
    signature = DPAK.read(4)
    SPRTVersion = DPAK.read(4)
    fileCount = LE_unpack.uint(DPAK.read(4))
    
    if signature != b'SPRT': #End on invalid SPRT sections
        return False, 0
    
    return SPRTVersion, fileCount

def readSpriteHeader(DPAK, spriteFileOffset):
    DPAK.seek(spriteFileOffset) #Now we have to go to the sprite file itself

    unknownHeaderValues = DPAK.read(4) #The games never access these (at least going off of MAME's watchpoints never being set off). Skipping...
    
    paletteTableOffset = LE_unpack.uint(DPAK.read(4))+spriteFileOffset
    frameTableOffset = LE_unpack.uint(DPAK.read(4))+spriteFileOffset

    #After this point is a frame index table (and it's actually used by the games too) - maybe a future version of the script could output GIF files?
    #A proper frame count could also be obtained from reading it.

    return paletteTableOffset, frameTableOffset

def extractFrames(DPAK, spriteFileOffset, frameTableOffset, colors, version):
    currentSpriteOutputDirectory = f'{os.getcwd()}/CONVERTEDSPRITES/{spriteFileOffset:010}/'
    lowestSpriteOffset = 0 #Used to brute force the frame counts - there isn't a proper frame count variable in the header sadly
    
    DPAK.seek(frameTableOffset)
    for frame in range(256): #Brute force for now - will fix eventually.
        if version == 0: #Counting on Zero
            spriteWidth, spriteHeight, spriteAlignX, spriteAlignY = DPAK.read(4)
        else: #Cars, Cars Supercharged, NASCAR, Didji Racing: Tiki Tropics
            spriteWidth, spriteHeight, spriteAlignX, spriteAlignY = DPAK.read(4)
            
            spriteWidth*=8  #They changed the resolution calculation from pixels to tiles
            spriteHeight*=8 #They changed the resolution calculation from pixels to tiles

        unknownOffsetVariable = DPAK.read(4) #The purpose of this is unknown for now. It's almost always going to right before the sprite data though.
        spriteDataOffset = LE_unpack.uint(DPAK.read(4))+spriteFileOffset

        if spriteDataOffset > lowestSpriteOffset: #Avoid going backwards if possible - the brute force method we're doing leads to lots of extra broken sprites without this
            lowestSpriteOffset = spriteDataOffset
            
            pixelIndices, maxXUsed, maxYUsed = decompressSprite(file, spriteDataOffset, version, spriteWidth, spriteHeight, 9999999)

            
            pixels = []
            for pixel in range(maxXUsed*(spriteHeight)):
                if pixelIndices[pixel] != 0: #Colored pixel
                    pixels.append(colors[pixelIndices[pixel]])
                else: #Transparent pixel
                    pixels.append((0, 0, 0, 0))

            if not os.path.exists(currentSpriteOutputDirectory):
                os.makedirs(currentSpriteOutputDirectory)
            
            TGA = imageData.generateTGA(maxXUsed, spriteHeight, pixels)
            with open(f'{currentSpriteOutputDirectory}/Sprite_{frame:04}.tga', "w+b") as outSprite:
                outSprite.write(TGA)
            
            

def readSPRTSection(file, SPRTSectionBaseOffset, version):
    #Just setting up a bunch of variables early here...
    doesThisPaletteHaveAlpha = 1 #Alpha is another term for transparency. This format doesn't have transparency in the color data.
    paletteCount = 16            #Used in place of the image resolution values in the custom widths and order function
    channelBitWidths = [4,4,4,4] #How many bits there are in each color of the palette
    channelOrder = [2,1,0,3]     #The color order (Blue, Green, Red, Alpha in this case)

    
    #This is where the actual code starts
    with open(file, "rb") as DPAK:
        SPRTVersion, fileCount = readSPRTSectionHeader(DPAK, SPRTSectionBaseOffset) #Moved because it's easier to keep the code organized this way

        if SPRTVersion == False: #Not a valid SPRT section. End decoding here.
            return False

        for spriteIndex in range(fileCount):
            spriteFileOffset = LE_unpack.uint(DPAK.read(4))+SPRTSectionBaseOffset

            nextSPRTSectionTableEntry = DPAK.tell() #Save current offset so we can seek to the next entry after parsing the sprites

            paletteTableOffset, frameTableOffset = readSpriteHeader(DPAK, spriteFileOffset)

            colors = imageData.customWidthsAndOrder(file, paletteTableOffset, doesThisPaletteHaveAlpha, paletteCount, paletteCount, channelBitWidths, channelOrder)
            try:
                extractFrames(DPAK, spriteFileOffset, frameTableOffset, colors, version)
            except:
                "The bit reader went beyond the target range..."
            DPAK.seek(nextSPRTSectionTableEntry)
            
isSPRT = True #By default, set this to true

def readDPAKAndRipSprites(file):
    with open(file, "rb") as DPAK: #I already have all of the code for this disassembled and commented, so this is the easy part
        magic = DPAK.read(4) #"DPAK"
        if magic != b'DPAK': #Don't kill the script yet, check if the input is a ROM
            file = checkForEmbeddedDPAK(file)
            return file
            
        fileCount = LE_unpack.ushort(DPAK.read(2))
        signature = DPAK.read(10) #"Torus" + 5 bytes of padding
        for DPAKFileIndex in range(fileCount):
            fileType = LE_unpack.uint(DPAK.read(4))   #Defines what type of file this is (we're looking for 0x2 in this case)
            fileOffset = LE_unpack.uint(DPAK.read(4)) #Officially referred to as just "file"
            fileSize = LE_unpack.uint(DPAK.read(4))   #Unfortunately, this value is inaccurate. All files are larger than this value.
            fileFlags = LE_unpack.uint(DPAK.read(4))  #Always 0, was likely used in earlier GBA games
            if fileType == 2:
                isSPRT = readSPRTSection(file, fileOffset, 0)
                mode = 1
            elif fileType == 3 and isSPRT == False:
                isSPRT = readSPRTSection(file, fileOffset, 1)

file = dialogs.file()

file = readDPAKAndRipSprites(file)

if file != None:
    result = readDPAKAndRipSprites(file)
    if result != None:
        print("This file is incompatible with the script and can't be used.")
