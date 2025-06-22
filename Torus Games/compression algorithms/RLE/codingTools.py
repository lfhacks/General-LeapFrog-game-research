import struct
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import os
import time
import zlib

class fileTools:
    """
    A class to handle various operations involving files
    """
    def ext(filepath):
        """
        Returns the extension from the input filename
        """
        return os.path.splitext(filepath)[1][1:]
    def name(path):
        """
        Returns the input filename without a path
        """
        return os.path.basename(path)
    def nameNoExt(path):
        """
        Returns the filename with no extension
        """
        return os.path.splitext(os.path.basename(path))[0]
    def size(path):
        """
        Returns the size of the file referenced by the path
        """
        return os.path.getsize(path)
    def folder(path):
        """
        Returns the folder with no file attached
        """
        return os.path.dirname(path)
    def compress(data):
        """
        Compresses data (loaded as bytes) with ZLIB
        """
        return zlib.compress(data)
    def decompress(data):
        """
        Decompresses ZLIB-compressed data
        """
        return zlib.decompress(data)
    def scanForBytes(path, string):
        """
        Reads an entire file into memory and checks it for a byte string
        
        Returns: True or False, string offset if found
        Format: scanForBytes(file path, byte string)
        """
        with open(path, 'rb') as file:
            content = file.read()
            offset = content.find(string)
            return string in content, offset
    def scanForAllBytes(path, byte_string):
        """
        Reads an entire file into memory and checks it for all occurrences of a byte string.
        
        Returns: List of offsets where the string is found.
        Format: scanForAllBytes(file path, byte string)
        """
        with open(path, 'rb') as file:
            content = file.read()
            offsets = []
            index = content.find(byte_string)
            
            while index != -1:
                offsets.append(index)
                index = content.find(byte_string, index + 1)  # Continue searching after the last occurrence
            
            return offsets if offsets else None  # Returns None if no matches are found

    def scanForBytesUpTo(path, string, end):
        """
        Reads part of a file (from the beginning) into memory and checks
        it for a byte string.
        
        Returns: True or False, string offset if found
        Format: scanForBytesUpTo(file path, byte string, read length)
        """
        with open(path, 'rb') as file:
            content = file.read(end)
            offset = content.find(string)
            return string in content, offset
    def scanForBytesInRange(path, string, start, end):
        """
        Reads part of a file (from the specified start offset to the specified end offset)
        into memory and checks it for a byte string.
        
        Returns: True or False, string offset if found
        Format: scanForBytesInRange(file path, byte string, start offset, end offset)
        """
        with open(path, 'rb') as file:
            file.seek(start)
            content = file.read(end-start)
            offset = content.find(string)
            return string in content, offset
    def getZeroTerminatedString(file, offset):
        """
        Gets any zero-terminated string at any given offset
        """
        string = ""
        scan = b''
        with open(file, "rb") as fileWithString:
            fileWithString.seek(offset)
            while scan != b'\x00':
                scan = fileWithString.read(1)
                if scan != b'\x00':
                    string = string+scan.decode("UTF-8")
        return string
    
class dialogs:
    """
    You can quickly open a dialog with this class
    """
    def file():
        """
        Opens a file dialog and returns a single file path after you select it
        """
        root = tk.Tk()
        root.withdraw()
        file = filedialog.askopenfilename()
        root.destroy()
        return file
    
    def files():
        """
        Opens a file dialog and returns a list of file paths after you select them
        """
        root = tk.Tk()
        root.withdraw()
        files = filedialog.askopenfilenames()
        root.destroy()
        return files
    
    def folder():
        """
        Opens a file dialog and returns the path after you select a folder
        """
        root = tk.Tk()
        root.withdraw()
        folder = filedialog.askdirectory()
        root.destroy()
        return folder
    
    def listedFolder():
        """
        Opens a file dialog and returns the path contents after you select a folder
        """
        root = tk.Tk()
        root.withdraw()
        folder = filedialog.askdirectory()
        root.destroy()
        return os.listdir(folder)
    
    def yesno(windowName, message):
        """Creates a yes or no prompt for the user to interact with

           format: yesno(windowName, message)
        """
        root = tk.Tk()
        root.withdraw()
        result = messagebox.askyesno(windowName, message)
        if result:
            return True
        else:
            return False

class encode:
    """
    Has functions for encoding strings
    """
    def utf8(data):
        return data.encode("UTF-8")
    
    def utf16(data):
        return data.encode("UTF-16")
    
    def utf32(data):
        return data.encode("UTF-32")
    
    def ascii(data):
        return data.encode("ASCII")

class decode:
    """
    Has functions for decoding strings
    """
    def utf8(data):
        return data.decode("UTF-8")
    
    def utf16(data):
        return data.decode("UTF-16")
    
    def utf32(data):
        return data.decode("UTF-32")
    
    def ascii(data):
        return data.decode("ASCII")

class LE_pack:
    """
    Has functions for packing a single value
    """
    def byte(value):
        return struct.pack("<b", value)
    
    def ubyte(value):
        return struct.pack("<B", value)
    
    def short(value):
        return struct.pack("<h", value)
    
    def ushort(value):
        return struct.pack("<H", value)
    
    def int(value):
        return struct.pack("<i", value)
    
    def uint(value):
        return struct.pack("<I", value)
    
    def long(value):
        return struct.pack("<q", value)
    
    def ulong(value):
        return struct.pack("<Q", value)
    
    def float(value):
        return struct.pack("<f", value)
    
    def double(value):
        return struct.pack("<d", value)

class LE_multipack:
    """
    Has functions for packing multiple values at once
    """
    def byte(values):
        return struct.pack("<{}b".format(len(values)), *values)
    
    def ubyte(values):
        return struct.pack("<{}B".format(len(values)), *values)
    
    def short(values):
        return struct.pack("<{}h".format(len(values)), *values)
    
    def ushort(values):
        return struct.pack("<{}H".format(len(values)), *values)
    
    def int(values):
        return struct.pack("<{}i".format(len(values)), *values)
    
    def uint(values):
        return struct.pack("<{}I".format(len(values)), *values)
    
    def long(values):
        return struct.pack("<{}q".format(len(values)), *values)
    
    def ulong(values):
        return struct.pack("<{}Q".format(len(values)), *values)
    
    def float(values):
        return struct.pack("<{}f".format(len(values)), *values)
    
    def double(values):
        return struct.pack("<{}d".format(len(values)), *values)

class LE_unpack:
    """
    Has functions for unpacking a single value
    """
    def byte(data):
        return struct.unpack("<b", data)[0]
    
    def ubyte(data):
        return struct.unpack("<B", data)[0]

    def short(data):
        return struct.unpack("<h", data)[0]
    
    def ushort(data):
        return struct.unpack("<H", data)[0]

    def s24(data):
        return int.from_bytes(data, byteorder='little', signed=True)
           
    def u24(data):
        return int.from_bytes(data, byteorder='little', signed=False)
    
    def int(data):
        return struct.unpack("<i", data)[0]
    
    def uint(data):
        return struct.unpack("<I", data)[0]

    def long(data):
        return struct.unpack("<q", data)[0]
    
    def ulong(data):
        return struct.unpack("<Q", data)[0]
    
    def float(data):
        return struct.unpack("<f", data)[0]
    
    def double(data):
        return struct.unpack("<d", data)[0]

class LE_multiunpack:
    """
    Has functions for unpacking multiple values at once
    """
    def byte(data):
        count = len(data)
        return struct.unpack("<{}b".format(count), data)
    
    def ubyte(data):
        count = len(data)
        return struct.unpack("<{}B".format(count), data)

    def short(data):
        count = len(data) // 2
        return struct.unpack("<{}h".format(count), data)
    
    def ushort(data):
        count = len(data) // 2
        return struct.unpack("<{}H".format(count), data)
    
    def int(data):
        count = len(data) // 4
        return struct.unpack("<{}i".format(count), data)
    
    def uint(data):
        count = len(data) // 4
        return struct.unpack("<{}I".format(count), data)

    def long(data):
        count = len(data) // 8
        return struct.unpack("<{}q".format(count), data)
    
    def ulong(data):
        count = len(data) // 8
        return struct.unpack("<{}Q".format(count), data)
    
    def float(data):
        count = len(data) // 4
        return struct.unpack("<{}f".format(count), data)
    
    def double(data):
        count = len(data) // 8
        return struct.unpack("<{}d".format(count), data)
    
class BE_pack:
    """
    Has functions for packing a single value
    """
    def byte(value):
        return struct.pack(">b", value)
    
    def ubyte(value):
        return struct.pack(">B", value)
    
    def short(value):
        return struct.pack(">h", value)
    
    def ushort(value):
        return struct.pack(">H", value)
    
    def int(value):
        return struct.pack(">i", value)
    
    def uint(value):
        return struct.pack(">I", value)
    
    def long(value):
        return struct.pack(">q", value)
    
    def ulong(value):
        return struct.pack(">Q", value)
    
    def float(value):
        return struct.pack(">f", value)
    
    def double(value):
        return struct.pack(">d", value)

class BE_multipack:
    """
    Has functions for packing multiple values at once
    """
    def byte(values):
        return struct.pack(">{}b".format(len(values)), *values)
    
    def ubyte(values):
        return struct.pack(">{}B".format(len(values)), *values)
    
    def short(values):
        return struct.pack(">{}h".format(len(values)), *values)
    
    def ushort(values):
        return struct.pack(">{}H".format(len(values)), *values)
    
    def int(values):
        return struct.pack(">{}i".format(len(values)), *values)
    
    def uint(values):
        return struct.pack(">{}I".format(len(values)), *values)
    
    def long(values):
        return struct.pack(">{}q".format(len(values)), *values)
    
    def ulong(values):
        return struct.pack(">{}Q".format(len(values)), *values)
    
    def float(values):
        return struct.pack(">{}f".format(len(values)), *values)
    
    def double(values):
        return struct.pack(">{}d".format(len(values)), *values)

class BE_unpack:
    """
    Has functions for unpacking a single value
    """
    def byte(data):
        return struct.unpack(">b", data)[0]
    
    def ubyte(data):
        return struct.unpack(">B", data)[0]

    def short(data):
        return struct.unpack(">h", data)[0]
    
    def ushort(data):
        return struct.unpack(">H", data)[0]

    def s24(data):
        return int.from_bytes(data, byteorder='big', signed=True)
           
    def u24(data):
        return int.from_bytes(data, byteorder='big', signed=False)
    
    def int(data):
        return struct.unpack(">i", data)[0]
    
    def uint(data):
        return struct.unpack(">I", data)[0]

    def long(data):
        return struct.unpack(">q", data)[0]
    
    def ulong(data):
        return struct.unpack(">Q", data)[0]
    
    def float(data):
        return struct.unpack(">f", data)[0]
    
    def double(data):
        return struct.unpack(">d", data)[0]

class BE_multiunpack:
    """
    Has functions for unpacking multiple values at once
    """
    def byte(data):
        count = len(data)
        return struct.unpack(">{}b".format(count), data)
    
    def ubyte(data):
        count = len(data)
        return struct.unpack(">{}B".format(count), data)

    def short(data):
        count = len(data) // 2
        return struct.unpack(">{}h".format(count), data)
    
    def ushort(data):
        count = len(data) // 2
        return struct.unpack(">{}H".format(count), data)
    
    def int(data):
        count = len(data) // 4
        return struct.unpack(">{}i".format(count), data)
    
    def uint(data):
        count = len(data) // 4
        return struct.unpack(">{}I".format(count), data)

    def long(data):
        count = len(data) // 8
        return struct.unpack(">{}q".format(count), data)
    
    def ulong(data):
        count = len(data) // 8
        return struct.unpack(">{}Q".format(count), data)
    
    def float(data):
        count = len(data) // 4
        return struct.unpack(">{}f".format(count), data)
    
    def double(data):
        count = len(data) // 8
        return struct.unpack(">{}d".format(count), data)

class magic:
    def checkHeader(path, magicBytes):
        """
        Checks a file's header for "magic bytes" to see if they match the input byte string
        """
        length = len(magicBytes)
        with open(path, "rb") as file:
            magic = file.read(length)
            if magic == magicBytes:
                return True
            else:
                return False
    def checkOffset(path, magicBytes, offset):
        """
        Checks a file for "magic bytes" at a specified offset to see if they match the input byte string
        """
        length = len(magicBytes)
        with open(path, "rb") as file:
            magic = file.read(length)
            if magic == magicBytes:
                return True
            else:
                return False

class BE_BitReader:
    def __init__(self, file, offset=0):
        """Initialize BitReader with a file object opened in binary mode ('rb')
        Args:
            file: File object opened in binary mode
            offset (int): Starting byte offset in the file
        """
        self.file = file
        self.bitBuffer = 0
        self.bitsInBuffer = 0
        if offset > 0:
            self.file.seek(offset)
    
    def read(self, num_bits):
        """Read specified number of bits from the file
        
        Args:
            num_bits (int): Number of bits to read
            
        Returns:
            int: Value read from the bits
        """
        while self.bitsInBuffer < num_bits:
            byte = self.file.read(1)
            if not byte:
                raise EOFError("Reached end of file while reading bits")
            self.bitBuffer = (self.bitBuffer << 8) | int.from_bytes(byte, 'big')
            self.bitsInBuffer += 8
            
        value = (self.bitBuffer >> (self.bitsInBuffer - num_bits)) & ((1 << num_bits) - 1)
        self.bitsInBuffer -= num_bits
        return value
    
    def align(self):
        """Align the bit reader to the next byte boundary by discarding remaining bits"""
        self.bitBuffer = 0
        self.bitsInBuffer = 0
    
    def seek(self, offset):
        """Seek to a specific byte offset in the file
        
        Args:
            offset (int): Byte offset to seek to
        """
        self.file.seek(offset)
        self.bitBuffer = 0
        self.bitsInBuffer = 0
    
    def tell(self):
        """Get current position in the file
        
        Returns:
            tuple: (byte_offset, bits_into_byte)
            - byte_offset is the offset of the last byte read
            - bits_into_byte is how many bits we've read into the current byte
        """
        byte_pos = self.file.tell()
        
        if self.bitsInBuffer > 0:
            complete_bytes = self.bitsInBuffer // 8
            byte_pos -= complete_bytes
            bits_into_byte = 8 - (self.bitsInBuffer % 8)
            if bits_into_byte == 8:
                bits_into_byte = 0
        else:
            bits_into_byte = 0
            
        return (byte_pos, bits_into_byte)

class LE_BitReader:
    def __init__(self, file, chunk_size=1, offset=0):
        """Initialize BitReaderLE with a file object opened in binary mode ('rb')
        
        Args:
            file: File object opened in binary mode
            chunk_size (int): Number of bytes to read at once for each data chunk
            offset (int): Starting byte offset in the file
        """
        self.file = file
        self.chunk_size = chunk_size
        self.bitBuffer = 0
        self.bitsInBuffer = 0
        if offset > 0:
            self.file.seek(offset)
    
    def read(self, num_bits):
        """Read specified number of bits from the file in little endian order
        
        Args:
            num_bits (int): Number of bits to read
            
        Returns:
            int: Value read from the bits
        """
        while self.bitsInBuffer < num_bits:
            bytes_needed = max(self.chunk_size, (num_bits - self.bitsInBuffer + 7) // 8)
            chunk = self.file.read(bytes_needed)
            if not chunk:
                raise EOFError("Reached end of file while reading bits")
                
            # Process bytes in little endian order
            value = int.from_bytes(chunk, 'little')
            self.bitBuffer |= value << self.bitsInBuffer
            self.bitsInBuffer += len(chunk) * 8
            
        # Extract the requested bits
        value = self.bitBuffer & ((1 << num_bits) - 1)
        self.bitBuffer >>= num_bits
        self.bitsInBuffer -= num_bits
        return value
    
    def align(self):
        """Align the bit reader to the next byte boundary by discarding remaining bits"""
        remaining_bits = self.bitsInBuffer % 8
        if remaining_bits:
            self.bitBuffer >>= remaining_bits
            self.bitsInBuffer -= remaining_bits
    
    def seek(self, offset):
        """Seek to a specific byte offset in the file
        
        Args:
            offset (int): Byte offset to seek to
        """
        self.file.seek(offset)
        self.bitBuffer = 0
        self.bitsInBuffer = 0
    
    def tell(self):
        """Get current position in the file
        
        Returns:
            tuple: (byte_offset, bits_into_byte)
            - byte_offset is the offset of the last byte read
            - bits_into_byte is how many bits we've read into the current byte
        """
        byte_pos = self.file.tell()
        
        if self.bitsInBuffer > 0:
            complete_bytes = self.bitsInBuffer // 8
            byte_pos -= complete_bytes
            bits_into_byte = self.bitsInBuffer % 8
        else:
            bits_into_byte = 0
            
        return (byte_pos, bits_into_byte)

class imageData:
    def maxValueForBits(bits): #Used later on in the color functions
        maxValue = (1 << bits) - 1
        return maxValue
    def indexedLinear(bits, file, offset, order, x, y):
        """Reads indexed pixel data of the specified bit width from a file
        
        Format: indexed(bits, file, offset, order, x, y)
        bits defines how many bits there is per pixel
        file defines the file path
        offset defines the start offset in the file
        order defines the pixel order (0 is linear, 1 is reverse order)
        x is the width, y is the height
        
        Returns: A list of integers used to assign colors from a palette to each pixel
        """
        #These might be common mistakes. Fix them automatically for the user.
        if x == 0:
            x = 1
        if y == 0: 
            y = 1
        
        convertedPixels = []
        with open(file, "rb") as pixels:
            pixels.seek(offset)
            pixelReader = BitReader(pixels)
            for vertical in range(y):
                for horizontal in range(x//2):  # Divide by 2 since we're reading pairs
                    if order == 0:  #Linear order (1, 2)
                        pixel1 = pixelReader.read(bits)
                        pixel2 = pixelReader.read(bits)
                        convertedPixels.extend([pixel1, pixel2])
                    elif order == 1:#Reverse order (2, 1)
                        pixel2 = pixelReader.read(bits)
                        pixel1 = pixelReader.read(bits)
                        convertedPixels.extend([pixel1, pixel2])
        return convertedPixels

    def indexedLinearFrame(bits, file, offset, order, x, y, frame):
        """Reads indexed pixel data of the specified bit width from a file (and gets the specified frame or tile)
        
        Format: indexed(bits, file, offset, order, x, y)
        bits defines how many bits there is per pixel
        file defines the file path
        offset defines the start offset in the file
        order defines the pixel order (0 is linear, 1 is reverse order)
        x is the width, y is the height
        frame is the frame number you want parsed
        
        Returns: A list of integers used to assign colors from a palette to each pixel
        """
        #These might be common mistakes. Fix them automatically for the user.
        if x == 0:
            x = 1
        if y == 0: 
            y = 1
        
        convertedPixels = []
        with open(file, "rb") as pixels:
            pixels.seek(offset)
            pixelReader = BitReader(pixels)
            for frames in range(frame): #Skip forward (frame) number of frames
                for vertical in range(y):
                    for horizontal in range(x//2):  # Divide by 2 since we're reading pairs
                        pixelReader.read(bits)
                        pixelReader.read(bits)
            for vertical in range(y):
                for horizontal in range(x//2):  # Divide by 2 since we're reading pairs
                    if order == 0:  #Linear order (1, 2)
                        pixel1 = pixelReader.read(bits)
                        pixel2 = pixelReader.read(bits)
                        convertedPixels.extend([pixel1, pixel2])
                    elif order == 1:#Reverse order (2, 1)
                        pixel2 = pixelReader.read(bits)
                        pixel1 = pixelReader.read(bits)
                        convertedPixels.extend([pixel1, pixel2])
        return convertedPixels

    def bgr555(file, offset, alphaMode, x, y):
        """Reads a BGR555/5551 palette from a file at the specified offset
        
           Format: bgr555(file, offset, alphaMode)
           file defines the file path
           offset defines the start offset in the file
           alphaMode defines if there is or isn't an alpha channel - 1 for True, 0 for False
           x is the width, y is the height
           
           Returns: A list of integers used to assign colors from a palette
           For color palettes, X should be the color count and Y should be 1
        """
        #These might be common mistakes. Fix them automatically for the user.
        if x == 0:
            x = 1
        if y == 0: 
            y = 1
        if alphaMode > 1:
            alphaMode = 1
        
        convertedPixels = []
        with open(file, "rb") as pixels:
            pixels.seek(offset)
            pixelReader = BitReader(pixels)
            for vertical in range(y):
                for horizontal in range(x):
                    blue = pixelReader.read(5)
                    green = pixelReader.read(5)
                    red = pixelReader.read(5)
                    alpha = pixelReader.read(1)
                    
                    blue = (blue * 255) // 31
                    green = (green * 255) // 31
                    red = (red * 255) // 31
                    alpha = alpha * 255
                    
                    if alphaMode == 0:
                        convertedPixels.append((red, green, blue))
                    elif alphaMode == 1:
                        convertedPixels.append((red, green, blue, alpha))
        return convertedPixels
    
    def bgr555LE(file, offset, alphaMode, x, y):
        """Reads a BGR555/5551 palette from a file at the specified offset in little endian byte order
        
           Format: bgr555_little_endian(file, offset, alphaMode)
           file defines the file path
           offset defines the start offset in the file
           alphaMode defines if there is or isn't an alpha channel - 1 for True, 0 for False
           x is the width, y is the height
           
           Returns: A list of integers used to assign colors from a palette
           For color palettes, X should be the color count and Y should be 1
        """
        #These might be common mistakes. Fix them automatically for the user.
        if x == 0:
            x = 1
        if y == 0: 
            y = 1
        if alphaMode > 1:
            alphaMode = 1
        
        convertedPixels = []
        with open(file, "rb") as pixels:
            pixels.seek(offset)
            # Use 2-byte chunks since BGR555 uses 16 bits per pixel
            pixelReader = BitReaderLE(pixels, chunk_size=2)
            
            for vertical in range(y):
                for horizontal in range(x):
                    # In little endian, the order is reversed at the byte level
                    # but we still read the bits in the same order within each 16-bit word
                    red = pixelReader.read(5)
                    green = pixelReader.read(5)
                    blue = pixelReader.read(5)
                    alpha = pixelReader.read(1)
                    
                    blue = (blue * 255) // 31
                    green = (green * 255) // 31
                    red = (red * 255) // 31
                    alpha = alpha * 255
                    
                    if alphaMode == 0:
                        convertedPixels.append((red, green, blue))
                    elif alphaMode == 1:
                        convertedPixels.append((red, green, blue, alpha))
        return convertedPixels

    def rgb555LE(file, offset, alphaMode, x, y):
        """Reads a BGR555/5551 palette from a file at the specified offset in little endian byte order
        
           Format: bgr555_little_endian(file, offset, alphaMode)
           file defines the file path
           offset defines the start offset in the file
           alphaMode defines if there is or isn't an alpha channel - 1 for True, 0 for False
           x is the width, y is the height
           
           Returns: A list of integers used to assign colors from a palette
           For color palettes, X should be the color count and Y should be 1
        """
        #These might be common mistakes. Fix them automatically for the user.
        if x == 0:
            x = 1
        if y == 0: 
            y = 1
        if alphaMode > 1:
            alphaMode = 1
        
        convertedPixels = []
        with open(file, "rb") as pixels:
            pixels.seek(offset)
            # Use 2-byte chunks since BGR555 uses 16 bits per pixel
            pixelReader = BitReaderLE(pixels, chunk_size=2)
            
            for vertical in range(y):
                for horizontal in range(x):
                    # In little endian, the order is reversed at the byte level
                    # but we still read the bits in the same order within each 16-bit word
                    red = pixelReader.read(5)
                    green = pixelReader.read(5)
                    blue = pixelReader.read(5)
                    alpha = pixelReader.read(1)
                    
                    blue = (blue * 255) // 31
                    green = (green * 255) // 31
                    red = (red * 255) // 31
                    alpha = alpha * 255
                    
                    if alphaMode == 0:
                        convertedPixels.append((blue, green, red))
                    elif alphaMode == 1:
                        convertedPixels.append((blue, green, red, alpha))
        return convertedPixels
    
    def rgb555(file, offset, alphaMode, x, y):
        """Reads an RGB555/5551 palette from a file at the specified offset
        
           Format: rgb555(file, offset, alphaMode)
           file defines the file path
           offset defines the start offset in the file
           alphaMode defines if there is or isn't an alpha channel - 1 for True, 0 for False
           x is the width, y is the height
           
           Returns: A list of integers used to assign colors from a palette
           For color palettes, X should be the color count and Y should be 1
        """
        #These might be common mistakes. Fix them automatically for the user.
        if x == 0:
            x = 1
        if y == 0: 
            y = 1
        if alphaMode > 1:
            alphaMode = 1
        
        convertedPixels = []
        with open(file, "rb") as pixels:
            pixels.seek(offset)
            pixelReader = BitReader(pixels)
            for vertical in range(y):
                for horizontal in range(x):
                    red = pixelReader.read(5)
                    green = pixelReader.read(5)
                    blue = pixelReader.read(5)
                    alpha = pixelReader.read(1)
                    
                    red = (red * 255) // 31
                    green = (green * 255) // 31
                    blue = (blue * 255) // 31
                    alpha = alpha * 255
                    
                    if alphaMode == 0:
                        convertedPixels.append((red, green, blue))
                    elif alphaMode == 1:
                        convertedPixels.append((red, green, blue, alpha))
        return convertedPixels

    def customWidthsAndOrder(file, offset, alphaMode, x, y, channelBits, channelOrder, littleEndian=True):
        """Reads a color palette from a file at the specified offset with custom bit widths and channel order
        
           Parameters:
           file: str - defines the file path
           offset: int - defines the start offset in the file
           alphaMode: int - defines if there is or isn't an alpha channel - 1 for True, 0 for False
           x: int - the width (for palettes, this is the color count)
           y: int - the height (for palettes, this should be 1)
           channelBits: list[int] - list of 4 integers defining bit widths for [R,G,B,A]
           channelOrder: list[int] - list of 4 integers defining channel order using [0=R,1=G,2=B,3=A]
           littleEndian: bool - determines which bit reader to use (default: True for little endian)
           
           Returns: A list of tuples containing color values (RGB or RGBA)
           
           Example usage:
           # For BGR format:
           colors = customWidthsAndOrder(file, 0, 1, 16, 1, [5,5,5,1], [2,1,0,3])
           # For RGB format:
           colors = customWidthsAndOrder(file, 0, 1, 16, 1, [5,5,5,1], [0,1,2,3])
        """
        # Input validation
        if x == 0:
            x = 1
        if y == 0: 
            y = 1
        if alphaMode > 1:
            alphaMode = 1
        
        if len(channelBits) != 4 or len(channelOrder) != 4:
            raise ValueError("channelBits and channelOrder must each contain exactly 4 values")
        if not all(0 <= order <= 3 for order in channelOrder):
            raise ValueError("channelOrder values must be between 0 and 3")
        if len(set(channelOrder)) != 4:
            raise ValueError("channelOrder must contain unique values")
        
        # Calculate total bits per pixel to determine chunk size
        total_bits = sum(channelBits)
        chunk_size = (total_bits + 7) // 8  # Round up to nearest byte
        
        convertedPixels = []
        with open(file, "rb") as pixels:
            pixels.seek(offset)
            # Choose the appropriate bit reader based on endianness
            ReaderClass = LE_BitReader if littleEndian else BE_BitReader
            pixelReader = ReaderClass(pixels, chunk_size=chunk_size)
            
            for vertical in range(y):
                for horizontal in range(x):
                    # Initialize color values
                    color_values = [0, 0, 0, 0]  # [R,G,B,A]
                    
                    # Read each channel in the specified order
                    for position, channel_type in enumerate(channelOrder):
                        bits = channelBits[channel_type]
                        if bits > 0:  # Only read if bits > 0
                            value = pixelReader.read(bits)
                            if channel_type == 3: #TEMPORARY FIX, DON'T KEEP!
                                value-=imageData.maxValueForBits(4)
                                if value < 0:
                                    value = value * -1
                            if bits > 0:  # Convert to 8-bit color value
                                value = (value * 255) // imageData.maxValueForBits(bits)
                            color_values[channel_type] = value
                    
                    # Create the final color tuple
                    if alphaMode == 0:
                        convertedPixels.append(tuple(color_values[:3]))  # RGB
                    else:
                        convertedPixels.append(tuple(color_values))  # RGBA
                        
            return convertedPixels
                        
        return convertedPixels
    def readBgr555Palette(file, offset, numColors): #For cases where the palette is little endian
        palette = []
        with open(file, "rb") as f:
            f.seek(offset)
            for i in range(numColors):
                bgr555 = struct.unpack('<H', f.read(2))[0]
                b = (bgr555 & 0x1F) << 3
                g = ((bgr555 >> 5) & 0x1F) << 3
                r = ((bgr555 >> 10) & 0x1F) << 3
                palette.append((r, g, b))
        return palette

    def generateTGA(width, height, pixels):
        """
        Generate TGA file data in memory
        
        Parameters:
        width (int): Image width
        height (int): Image height
        pixels (list): List of RGB or RGBA tuples containing color data
        
        Returns:
        bytearray: Complete TGA file data
        """
        # Validate input
        if len(pixels) != width * height:
            raise ValueError(f"Pixel count {len(pixels)} doesn't match dimensions {width}x{height}")
        
        # Check if we have alpha channel
        has_alpha = len(pixels[0]) == 4
        
        # Initialize TGA header (18 bytes)
        header = bytearray([
            0,      # ID length
            0,      # No color map
            2,      # Uncompressed true-color
            0, 0,   # Color map first entry
            0,      # Color map length LSB
            0,      # Color map length MSB
            0,      # Color map entry size
            0, 0,   # X origin
            0, 0,   # Y origin
            width & 0xFF, (width >> 8) & 0xFF,    # Width LSB, MSB
            height & 0xFF, (height >> 8) & 0xFF,   # Height LSB, MSB
            32 if has_alpha else 24,   # Bits per pixel
            0x28 if has_alpha else 0x20    # Image descriptor (0x20 = normal, 0x28 = normal + 8-bit alpha)
        ])
        
        # Create pixel data
        image_data = bytearray()
        for pixel in pixels:
            # TGA uses BGRA/BGR order
            if has_alpha:
                r, g, b, a = pixel
                image_data.extend([b, g, r, a])
            else:
                r, g, b = pixel
                image_data.extend([b, g, r])
        
        # Optional TGA footer (26 bytes)
        # Convert string to bytes using ord()
        signature = "TRUEVISION-XFILE."
        footer = bytearray([
            0, 0, 0, 0,    # Extension area offset
            0, 0, 0, 0,    # Developer directory offset
        ])
        footer.extend(ord(c) for c in signature)
        footer.append(0)  # Null terminator
        
        # Combine all parts
        tga_data = header + image_data + footer
        
        return tga_data
    
    #TO-DO: Implement a color sorting function so people can define a custom color order for palettes
    #Palette decoders should be designed to be reused to decode non-indexed (RGB/BGR/RGBA/BGRA) image data.

class offsetConverter:
    def RAMOffsetToBinaryOffset(RAMOffset, ROMBaseOffset):
        """Takes an offset (from a pointer table) and subtracts the ROM base offset from it
           to get the true offset in the binary file.
           Used for reversing binaries compiled for cartridge-based systems"""
        return RAMOffset-ROMBaseOffset
    def relativeOffsetToOffset(relativeOffset, baseOffset):
        """Takes an offset (from a pointer table) and adds it to a base offset for the true offset in a file
           Used for reversing a ton of formats
           (LeapPad ROMs being an example of this) and files embedded within other files"""
        return relativeOffset+baseOffset
    def wordToInt(wordAlignedOffset):
        """Takes a word-aligned offset and multiplies it by 2.
           Used for reversing VTech V.Smile games."""
        return wordAlignedOffset*2
    def intToWord(intAlignedOffset):
        """Takes a 32-Bit Integer-aligned offset and integer divides it by 2.
           Used for reversing VTech V.Smile games."""
        return intAlignedOffset//2

class riff:
    """Very basic RIFF-related functions for decoding RIFF files"""
    def parseRIFFChunk(file):
        magic = decode.utf8(file.read(4))
        length = unpack.uint(file.read(4))
        Format = decode.utf8(file.read(4))
        return magic, length, Format
    def parseChunk(file):
        fourCC = decode.utf8(file.read(4))
        length = unpack.uint(file.read(4))
        return fourCC, length
    def parseRIFFChunkAndReadData(file):
        magic = decode.utf8(file.read(4))
        length = unpack.uint(file.read(4))
        Format = decode.utf8(file.read(4))
        data = file.read(length-4)
        return magic, length, Format, data
    def parseChunkAndReadData(file):
        fourCC = decode.utf8(file.read(4))
        length = unpack.uint(file.read(4))
        data = file.read(length)
        return fourCC, length, data

class gameboy:
    def bankNumberToOffset(number):
        return number*0x4000






class MidiFileHandler:
    """
    A streamlined wrapper class for MIDI file functionality using Mido.
    Mido is only imported when this class is instantiated,
    making it optional for the overall library.
    """
    
    def __init__(self):
        """Initialize the MidiFileHandler and import Mido."""
        try:
            import mido
            self.mido = mido
        except ImportError:
            raise ImportError(
                "Mido is required for MIDI functionality. "
                "Please install it using 'pip install mido'."
            )
    
    def create_midi_file(self, ticks_per_beat=480):
        """
        Create a new MIDI file.
        
        Args:
            ticks_per_beat (int, optional): Resolution of the MIDI file. Defaults to 480.
        
        Returns:
            tuple: (MidiFile object, MidiTrack object)
        """
        midi_file = self.mido.MidiFile(ticks_per_beat=ticks_per_beat)
        track = self.mido.MidiTrack()
        midi_file.tracks.append(track)
        return midi_file, track
    
    def create_multi_track_midi_file(self, num_tracks=1, ticks_per_beat=480):
        """
        Create a new MIDI file with multiple tracks.
        
        Args:
            num_tracks (int, optional): Number of tracks to create. Defaults to 1.
            ticks_per_beat (int, optional): Resolution of the MIDI file. Defaults to 480.
        
        Returns:
            tuple: (MidiFile object, list of MidiTrack objects)
        """
        midi_file = self.mido.MidiFile(ticks_per_beat=ticks_per_beat)
        tracks = []
        
        for _ in range(num_tracks):
            track = self.mido.MidiTrack()
            midi_file.tracks.append(track)
            tracks.append(track)
            
        return midi_file, tracks

    def create_pitch_bend_message(self, value, channel=0, time=0):
        """
        Create a pitch bend message.
        
        Args:
            value (int): Pitch bend value (-8192 to 8191)
            channel (int, optional): MIDI channel (0-15). Defaults to 0.
            time (int, optional): Time in ticks since the last message. Defaults to 0.
        
        Returns:
            Message: Mido Message object
        """
        # Ensure the value is within the valid range
        if value < -8192 or value > 8191:
            print(f"Warning: Pitch bend value {value} out of range (-8192 to 8191). Clamping.")
            value = max(-8192, min(8191, value))
            
        return self.mido.Message('pitchwheel', pitch=value, channel=channel, time=time)
    
    def add_track(self, midi_file):
        """
        Add a new track to an existing MIDI file.
        
        Args:
            midi_file: Mido MidiFile object
        
        Returns:
            MidiTrack: The newly created track
        """
        track = self.mido.MidiTrack()
        midi_file.tracks.append(track)
        return track
    
    def save_midi_file(self, midi_file, filename='output.mid'):
        """
        Save a MIDI file to disk.
        
        Args:
            midi_file: Mido MidiFile object
            filename (str, optional): Output filename. Defaults to 'output.mid'.
            
        Returns:
            bool: True if successfully saved, False otherwise.
        """
        try:
            midi_file.save(filename)
            return True
        except Exception as e:
            print(f"Error saving MIDI file: {e}")
            return False

    def combine_midi_files(self, midi_files, output_filename='combined.mid', assign_channels=True):
        """
        Combine multiple MIDI files into a single multi-track MIDI file,
        avoiding the drum channel (9) when assigning channels.
        
        Args:
            midi_files (list): List of MIDI file paths or Mido MidiFile objects
            output_filename (str, optional): Output filename. Defaults to 'combined.mid'.
            assign_channels (bool, optional): Whether to assign unique channels to each track.
                                              Defaults to True.
            
        Returns:
            bool: True if successfully combined and saved, False otherwise.
        """
        try:
            # Create a new MIDI file with the same ticks_per_beat as the first input file
            first_file = midi_files[0]
            if isinstance(first_file, str):
                first_file = self.load_midi_file(first_file)
            
            if not first_file:
                print("Error: Could not load the first MIDI file")
                return False
                
            combined_file = self.mido.MidiFile(ticks_per_beat=first_file.ticks_per_beat)
            
            # Track the next available channel, skipping the drum channel (9)
            next_channel = 0
            
            # Process each input MIDI file
            for file_index, midi_file in enumerate(midi_files):
                # Load the file if it's a string (file path)
                if isinstance(midi_file, str):
                    midi_file = self.load_midi_file(midi_file)
                    
                if not midi_file:
                    print(f"Warning: Skipping file at index {file_index} - could not load")
                    continue
                    
                # Add each track from the current file to the combined file
                for track_index, track in enumerate(midi_file.tracks):
                    new_track = self.mido.MidiTrack()
                    combined_file.tracks.append(new_track)
                    
                    # Determine channel for this track
                    channel_map = {}
                    if assign_channels:
                        # Find all channels used in this track
                        used_channels = set()
                        for msg in track:
                            if hasattr(msg, 'channel'):
                                used_channels.add(msg.channel)
                        
                        # Map each original channel to a new unique channel
                        for original_channel in used_channels:
                            # If the original channel is the drum channel (9), keep it as is
                            if original_channel == 9:
                                channel_map[original_channel] = 9
                                continue
                                
                            # Skip the drum channel (9) when assigning new channels
                            if next_channel == 9:
                                next_channel = 10
                                
                            # Skip if we've run out of channels
                            if next_channel > 15:
                                print(f"Warning: Out of MIDI channels. Some tracks may use the same channel.")
                                channel_map[original_channel] = original_channel
                            else:
                                channel_map[original_channel] = next_channel
                                next_channel += 1
                    
                    # Add track name
                    track_name = f"File {file_index+1} - Track {track_index+1}"
                    original_name = None
                    
                    # Extract metadata and channel messages first
                    meta_messages = []
                    for msg in track:
                        if msg.type == 'track_name':
                            original_name = msg.name
                        if msg.is_meta:
                            meta_messages.append(msg.copy())
                    
                    if original_name:
                        track_name += f" ({original_name})"
                    
                    self.add_track_name(new_track, track_name, time=0)
                    
                    # Add important meta messages first (tempo, key signature, etc.)
                    for msg in meta_messages:
                        if msg.type in ['set_tempo', 'key_signature', 'time_signature']:
                            if msg.type != 'track_name':  # Skip original track name
                                new_track.append(msg.copy())
                    
                    # Now add all non-meta messages with channel reassignment
                    for msg in track:
                        if not msg.is_meta:
                            new_msg = msg.copy()
                            if hasattr(new_msg, 'channel') and assign_channels:
                                if new_msg.channel in channel_map:
                                    new_msg.channel = channel_map[new_msg.channel]
                            new_track.append(new_msg)
                    
                    # Add any remaining meta messages
                    for msg in meta_messages:
                        if msg.type not in ['set_tempo', 'key_signature', 'time_signature', 'track_name']:
                            new_track.append(msg.copy())
            
            # Save the combined file
            return self.save_midi_file(combined_file, output_filename)
            
        except Exception as e:
            print(f"Error combining MIDI files: {e}")
            return False
    
    def load_midi_file(self, filename):
        """
        Load a MIDI file from disk.
        
        Args:
            filename (str): Path to MIDI file
            
        Returns:
            MidiFile object or None if loading failed
        """
        try:
            return self.mido.MidiFile(filename)
        except Exception as e:
            print(f"Error loading MIDI file: {e}")
            return None
    
    def create_note_on_message(self, note, velocity=64, channel=0, time=0):
        """
        Create a note-on message.
        
        Args:
            note (int): MIDI note number (0-127)
            velocity (int, optional): Note velocity (0-127). Defaults to 64.
            channel (int, optional): MIDI channel (0-15). Defaults to 0.
            time (int, optional): Time in ticks since the last message. Defaults to 0.
        
        Returns:
            Message: Mido Message object
        """
        return self.mido.Message('note_on', note=note, velocity=velocity, 
                               channel=channel, time=time)
    
    def create_note_off_message(self, note, velocity=0, channel=0, time=0):
        """
        Create a note-off message.
        
        Args:
            note (int): MIDI note number (0-127)
            velocity (int, optional): Release velocity (0-127). Defaults to 0.
            channel (int, optional): MIDI channel (0-15). Defaults to 0.
            time (int, optional): Time in ticks since the last message. Defaults to 0.
        
        Returns:
            Message: Mido Message object
        """
        return self.mido.Message('note_off', note=note, velocity=velocity, 
                                channel=channel, time=time)
    
    def create_program_change_message(self, program, channel=0, time=0):
        """
        Create a program change message.
        
        Args:
            program (int): Program number (0-127)
            channel (int, optional): MIDI channel (0-15). Defaults to 0.
            time (int, optional): Time in ticks since the last message. Defaults to 0.
        
        Returns:
            Message: Mido Message object
        """
        return self.mido.Message('program_change', program=program, 
                                channel=channel, time=time)
    
    def create_control_change_message(self, control, value, channel=0, time=0):
        """
        Create a control change message.
        
        Args:
            control (int): Control number (0-127)
            value (int): Control value (0-127)
            channel (int, optional): MIDI channel (0-15). Defaults to 0.
            time (int, optional): Time in ticks since the last message. Defaults to 0.
        
        Returns:
            Message: Mido Message object
        """
        return self.mido.Message('control_change', control=control, value=value, 
                                channel=channel, time=time)
    
    def set_pitch_bend_range(self, track, semitones=2, cents=0, channel=0, time=0):
        """
        Set the pitch bend range for a MIDI channel using RPN (Registered Parameter Number) messages.
        
        Args:
            track: Mido MidiTrack object
            semitones (int, optional): Number of semitones for the pitch bend range (1-24). Defaults to 2.
            cents (int, optional): Additional cents (0-100). Defaults to 0.
            channel (int, optional): MIDI channel (0-15). Defaults to 0.
            time (int, optional): Time in ticks since the last message. Defaults to 0.
        """
        # Validate inputs
        if semitones < 1 or semitones > 24:
            print(f"Warning: Pitch bend range of {semitones} semitones might not be supported by all devices.")
        
        if cents < 0 or cents > 100:
            print(f"Warning: Cents value {cents} out of range (0-100). Clamping.")
            cents = max(0, min(100, cents))
        
        # Convert cents to LSB value (0-127)
        cents_msb = min(127, int(cents * 127 / 100))
        
        # 1. Select RPN parameter for pitch bend range (0,0)
        track.append(self.create_control_change_message(control=101, value=0, channel=channel, time=time))
        track.append(self.create_control_change_message(control=100, value=0, channel=channel, time=0))
        
        # 2. Set the parameter value (semitones)
        track.append(self.create_control_change_message(control=6, value=semitones, channel=channel, time=0))
        
        # 3. Set the fine adjustment (cents)
        #track.append(self.create_control_change_message(control=38, value=cents_msb, channel=channel, time=0))
        
        # 4. Deselect RPN (127,127)
        track.append(self.create_control_change_message(control=101, value=127, channel=channel, time=0))
        track.append(self.create_control_change_message(control=100, value=127, channel=channel, time=0))
    
    def add_tempo_change(self, track, tempo, time=0):
        """
        Add a tempo change message to a track.
        
        Args:
            track: Mido MidiTrack object
            tempo (int): Tempo in microseconds per beat
            time (int, optional): Time in ticks since the last message. Defaults to 0.
        """
        track.append(self.mido.MetaMessage('set_tempo', tempo=tempo, time=time))
    
    def add_time_signature(self, track, numerator=4, denominator=4, time=0):
        """
        Add a time signature message to a track.
        
        Args:
            track: Mido MidiTrack object
            numerator (int, optional): Numerator of time signature. Defaults to 4.
            denominator (int, optional): Denominator of time signature (power of 2). Defaults to 4.
            time (int, optional): Time in ticks since the last message. Defaults to 0.
        """
        # For denominator, convert to power of 2 (e.g., 4 becomes 2, 8 becomes 3)
        from math import log2
        clocks_per_click = 24
        notated_32nd_notes_per_beat = 8
        
        track.append(self.mido.MetaMessage('time_signature', 
                                          numerator=numerator,
                                          denominator=int(log2(denominator)),
                                          clocks_per_click=clocks_per_click,
                                          notated_32nd_notes_per_beat=notated_32nd_notes_per_beat,
                                          time=time))
    
    def add_key_signature(self, track, key='C', time=0):
        """
        Add a key signature message to a track.
        
        Args:
            track: Mido MidiTrack object
            key (str, optional): Key name (e.g., 'C', 'F#m'). Defaults to 'C'.
            time (int, optional): Time in ticks since the last message. Defaults to 0.
        """
        # Map of key names to (key signature, major/minor) pairs
        key_map = {
            'C': (0, 0), 'Am': (0, 1),
            'G': (1, 0), 'Em': (1, 1),
            'D': (2, 0), 'Bm': (2, 1),
            'A': (3, 0), 'F#m': (3, 1),
            'E': (4, 0), 'C#m': (4, 1),
            'B': (5, 0), 'G#m': (5, 1),
            'F#': (6, 0), 'D#m': (6, 1),
            'C#': (7, 0), 'A#m': (7, 1),
            'F': (-1, 0), 'Dm': (-1, 1),
            'Bb': (-2, 0), 'Gm': (-2, 1),
            'Eb': (-3, 0), 'Cm': (-3, 1),
            'Ab': (-4, 0), 'Fm': (-4, 1),
            'Db': (-5, 0), 'Bbm': (-5, 1),
            'Gb': (-6, 0), 'Ebm': (-6, 1),
            'Cb': (-7, 0), 'Abm': (-7, 1),
        }
        
        if key in key_map:
            key_sig, mode = key_map[key]
            track.append(self.mido.MetaMessage('key_signature', 
                                              key=key_sig, 
                                              mode=mode, 
                                              time=time))
        else:
            print(f"Warning: Unknown key signature '{key}'. Using C major.")
            track.append(self.mido.MetaMessage('key_signature', 
                                              key=0, 
                                              mode=0, 
                                              time=time))
    
    def add_track_name(self, track, name, time=0):
        """
        Add a track name message to a track.
        
        Args:
            track: Mido MidiTrack object
            name (str): Name of the track
            time (int, optional): Time in ticks since the last message. Defaults to 0.
        """
        track.append(self.mido.MetaMessage('track_name', name=name, time=time))
    
    def add_text_event(self, track, text, time=0):
        """
        Add a text event message to a track.
        
        Args:
            track: Mido MidiTrack object
            text (str): Text to add
            time (int, optional): Time in ticks since the last message. Defaults to 0.
        """
        track.append(self.mido.MetaMessage('text', text=text, time=time))
    
    def add_lyrics(self, track, text, time=0):
        """
        Add lyrics to a track.
        
        Args:
            track: Mido MidiTrack object
            text (str): Lyric text
            time (int, optional): Time in ticks since the last message. Defaults to 0.
        """
        track.append(self.mido.MetaMessage('lyrics', text=text, time=time))
    
    def add_instrument_name(self, track, name, time=0):
        """
        Add an instrument name to a track.
        
        Args:
            track: Mido MidiTrack object
            name (str): Name of the instrument
            time (int, optional): Time in ticks since the last message. Defaults to 0.
        """
        track.append(self.mido.MetaMessage('instrument_name', name=name, time=time))
    
    def add_note(self, track, note, duration, velocity=64, channel=0, time=0):
        """
        Add a note (note_on followed by note_off) to a track.
        
        Args:
            track: Mido MidiTrack object
            note (int): MIDI note number (0-127)
            duration (int): Duration of the note in ticks
            velocity (int, optional): Note velocity (0-127). Defaults to 64.
            channel (int, optional): MIDI channel (0-15). Defaults to 0.
            time (int, optional): Time in ticks since the last message. Defaults to 0.
        """
        track.append(self.create_note_on_message(note, velocity, channel, time))
        track.append(self.create_note_off_message(note, 0, channel, duration))
    
    def add_chord(self, track, notes, duration, velocity=64, channel=0, time=0):
        """
        Add a chord (multiple simultaneous notes) to a track.
        
        Args:
            track: Mido MidiTrack object
            notes (list): List of MIDI note numbers (0-127)
            duration (int): Duration of the chord in ticks
            velocity (int, optional): Note velocity (0-127). Defaults to 64.
            channel (int, optional): MIDI channel (0-15). Defaults to 0.
            time (int, optional): Time in ticks since the last message. Defaults to 0.
        """
        # Add note_on messages for all notes in the chord
        for i, note in enumerate(notes):
            # First note has the specified time, others are simultaneous (time=0)
            current_time = time if i == 0 else 0
            track.append(self.create_note_on_message(note, velocity, channel, current_time))
        
        # Add note_off messages for all notes
        for i, note in enumerate(notes):
            # First note_off has the full duration, others are simultaneous
            current_time = duration if i == 0 else 0
            track.append(self.create_note_off_message(note, 0, channel, current_time))
    
    def add_end_of_track(self, track, time=0):
        """
        Add an end-of-track message.
        
        Args:
            track: Mido MidiTrack object
            time (int, optional): Time in ticks since the last message. Defaults to 0.
        """
        track.append(self.mido.MetaMessage('end_of_track', time=time))
    
    def bpm_to_tempo(self, bpm):
        """
        Convert beats per minute to tempo in microseconds per beat.
        
        Args:
            bpm (float): Beats per minute
            
        Returns:
            int: Tempo in microseconds per beat
        """
        return int(60000000 / bpm)
    
    def seconds_to_ticks(self, seconds, ticks_per_beat, tempo):
        """
        Convert seconds to ticks.
        
        Args:
            seconds (float): Time in seconds
            ticks_per_beat (int): Resolution of the MIDI file
            tempo (int): Tempo in microseconds per beat
            
        Returns:
            int: Time in ticks
        """
        beats_per_second = 1000000 / tempo
        beats = seconds * beats_per_second
        return int(beats * ticks_per_beat)
