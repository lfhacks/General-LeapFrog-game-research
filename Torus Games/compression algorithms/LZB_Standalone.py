#Torus Games LZB decompressor
def LE_Integer(data):
    value = 0
    index = 0
    for byte in data:
        value |= (byte << (8 * index))
        index+=1
    return value

class LZBDecompressor:
    def __init__(self):
        self.lzbTable = [
                 0, 1, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4, 4,
                 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5,
                 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6,
                 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6,
                 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7,
                 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7,
                 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7,
                 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7,
                 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8,
                 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8,
                 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8,
                 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8,
                 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8,
                 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8,
                 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8,
                 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8
                 ]
        
        self.lzbBitStreamOffset = 0  #Where the decompressor is in the bit stream (in bytes)
        self.bitOffset = 1           #Where the decompressor is in a byte
        self.compressedData = None   #The data the decompressor will decompress

    def getBitLzb(self): #Gets a single bit from the bit stream
        self.bitOffset -= 1
        if self.bitOffset == 0:
            self.lzbBitStreamOffset += 1
            self.bitOffset = 8
        
        currentByte = self.compressedData[self.lzbBitStreamOffset]
        bit = (currentByte >> (self.bitOffset - 1)) & 0x1
        return bit

    def TSE_UnpackLzb(self, compressedData):
        #Check the signature
        signature = compressedData[0:2]
        if signature != b'ZB':
            return None

        #If the signature is valid, read the rest of the header
        uncompressedSize = LE_Integer(compressedData[2:5])

        #Relative to the start of the header
        bitstreamOffset = LE_Integer(compressedData[5:8])
        
        outputBuffer = bytearray(uncompressedSize)
        
        self.compressedData = compressedData
        self.lzbBitStreamOffset = bitstreamOffset
        
        currentWritePosition = 0
        
        literalsOffset = 8
        
        if currentWritePosition >= uncompressedSize:
            return outputBuffer
        
        #This is where the magic happens
        while currentWritePosition < uncompressedSize:
            controlBit = self.getBitLzb()
            
            if controlBit == 0: #The bit was 0, so get literal data
                #Decode the length
                literalLength = 1
                while True:
                    if self.getBitLzb() != 0:
                        break
                    literalLength = (literalLength << 1) | self.getBitLzb()
                
                outputBuffer[currentWritePosition:currentWritePosition + literalLength] = compressedData[literalsOffset:literalsOffset + literalLength]
                
                literalsOffset += literalLength
                currentWritePosition += literalLength
                
            else: #The bit was 1, so get previously decompressed data
                currentIndex = currentWritePosition
                
                if currentIndex < 0xFF:
                    requiredBits = self.lzbTable[currentIndex]
                elif currentIndex < 0x10000:
                    requiredBits = self.lzbTable[currentIndex >> 8] + 8
                else:
                    requiredBits = self.lzbTable[currentIndex >> 16] + 16

                #Decode the offset
                offset = 0
                bitsToRead = requiredBits
                while bitsToRead > 0:
                    offset = (offset << 1) | self.getBitLzb()
                    bitsToRead -= 1

                #Decode the length
                previousDataLength = 1
                while True:
                    if self.getBitLzb() != 0:
                        break
                    previousDataLength = (previousDataLength << 1) | self.getBitLzb()
                previousDataLength += 1
                
                if previousDataLength > 0:
                    previousDataSourcePosition = offset
                    
                    if currentWritePosition + previousDataLength > uncompressedSize:
                        previousDataLength = uncompressedSize - currentWritePosition
                    
                    for i in range(previousDataLength):
                        outputBuffer[currentWritePosition] = outputBuffer[previousDataSourcePosition]
                        currentWritePosition += 1
                        previousDataSourcePosition += 1
        
        return outputBuffer
