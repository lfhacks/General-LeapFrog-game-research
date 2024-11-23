import struct
from PIL import Image

filename = (input("What is the name of your file (leave out the .oot extension): "))

with open((filename + ".oot"), "rb") as file:
    unknown1 = struct.unpack("<I", file.read(4))
    crop_width, crop_height, width, height = struct.unpack("<4I", file.read(16))
    print("The image has a data size of " + str(width) + "x" + str(height) + " with a true size of " + str(crop_width) + "x" + str(crop_height))
    unknown2, unknown3, unknown4, unknown5 = struct.unpack("<4I", file.read(16))
    bytelayout, unknown6, unknown7, unknown8, unknown9, unknown10, unknown11 = struct.unpack("<7I", file.read(28))
    imagedata = file.read()
    if bytelayout == 1:
        print("RGBA4444")
        rawimage = Image.frombytes("RGBA", (width, height), imagedata, "raw", "RGBA;4B")
        # quick hack to get around PIL's lack of little-endian RGBA4 support
        rawimage = Image.merge('RGBA', rawimage.split()[::-1])
        image_crop = rawimage.crop((0, 0, crop_width, crop_height))
        image_crop.save((filename + ".png"))
        image_crop.show()
    if bytelayout == 0:
        raise ValueError("RGBA5551 file detected - please convert manually")
        rawimage = Image.frombytes("RGBA", (width, height), imagedata, "raw", "BGRA;15") # note - expects big endian. UDIs tend to be little-endian.
        image_crop = rawimage.crop((0, 0, crop_width, crop_height))
        image_crop.save((filename + "_test.png"))
        image_crop.show()
    if bytelayout == 2:
        print("RGB565")
        rawimage = Image.frombytes("RGB", (width, height), imagedata, "raw", "BGR;16")
        image_crop = rawimage.crop((0, 0, crop_width, crop_height))
        image_crop.save((filename + ".png"))
        image_crop.show()
