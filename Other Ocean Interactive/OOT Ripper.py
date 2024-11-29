import struct
from PIL import Image
from enum import Enum

"""
class ImageFormat(Enum):
    RGBA5551 = 0
    RGBA4444 = 1
    RGB565 = 2
"""
    
filename = (input("What is the name of your file (leave out the .oot extension): "))

with open((filename + ".oot"), "rb") as file:
    unknown1 = struct.unpack("<I", file.read(4))
    crop_width, crop_height, width, height = struct.unpack("<4I", file.read(16))
    print("The image has a data size of " + str(width) + "x" + str(height) + " with a true size of " + str(crop_width) + "x" + str(crop_height))
    unknown2, unknown3, unknown4, unknown5 = struct.unpack("<4I", file.read(16))
    bytelayout, unknown6, unknown7, unknown8, unknown9, unknown10, unknown11 = struct.unpack("<7I", file.read(28))
    imagedata = file.read()
    if height == 0:
        # override for handling certain heightless files from Ni Hao, Kai-lan and potentially Tinker 
        print("Warning: Height is blank - assuming 256px")
        height = 256
    if bytelayout == 1:
        print("RGBA4444")
        rawimage = Image.frombytes("RGBA", (width, height), imagedata, "raw", "RGBA;4B")
        # quick hack to get around PIL's lack of little-endian RGBA4 support
        rawimage = Image.merge('RGBA', rawimage.split()[::-1])
        image_crop = rawimage.crop((0, 0, crop_width, crop_height))
        image_crop.save((filename + ".png"))
        image_crop.show()
    elif bytelayout == 0:
        raise ValueError("RGBA5551 file detected - please convert manually")
        rawimage = Image.frombytes("RGBA", (width, height), imagedata, "raw", "BGRA;15") # note - expects big endian. UDIs tend to be little-endian.
        image_crop = rawimage.crop((0, 0, crop_width, crop_height))
        image_crop.save((filename + "_test.png"))
        image_crop.show()
    elif bytelayout == 2:
        print("RGB565")
        rawimage = Image.frombytes("RGB", (width, height), imagedata, "raw", "BGR;16")
        image_crop = rawimage.crop((0, 0, crop_width, crop_height))
        image_crop.save((filename + ".png"))
        image_crop.show()
    elif bytelayout == 7:
        rawimage = Image.frombytes("L", (width, height), imagedata, "raw", "L")
        image_crop = rawimage.crop((0, 0, crop_width, crop_height))
        image_crop.save((filename + ".png"))
        image_crop.show()
    else:
        print("\033[1;33mDebug: This texture is stored in unimplemented format " + str(bytelayout) + ". Please paste this message into a new issue on GitHub and include a zip file of your affected samples.\033[1;37m")
