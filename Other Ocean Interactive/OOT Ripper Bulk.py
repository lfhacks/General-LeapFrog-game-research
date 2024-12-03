import struct
from PIL import Image
from pathlib import Path
import time

filelist = list(Path('.').glob('*.oot'))

def rgba5551_to_argb1555(rgba_data):
    argb_data = bytearray(len(rgba_data))  # Same length since it's still 16 bits per pixel
    for i in range(0, len(rgba_data), 2):
        # Extract the 16-bit pixel value
        pixel = (rgba_data[i] << 8) | rgba_data[i + 1]
        
        # Extract the RGBA components
        r = (pixel >> 11) & 0x1F  # Red: bits 15:11
        g = (pixel >> 6) & 0x1F  # Green: bits 10:6
        b = (pixel >> 1) & 0x1F  # Blue: bits 5:1
        a = pixel & 0x1        # Alpha: bit 0
        
        # Reassemble in ARGB1555 order
        argb_pixel = (a << 15) | (r << 10) | (g << 5) | b
        
        # Store the ARGB1555 pixel value
        argb_data[i] = argb_pixel >> 8
        argb_data[i + 1] = argb_pixel & 0xFF
    
    return argb_data

for files in filelist:
    with open(files, "rb") as file:
        print(files)
        unknown1 = struct.unpack("<I", file.read(4))
        crop_width, crop_height, width, height = struct.unpack("<4I", file.read(16))
        print("The image has a data size of " + str(width) + "x" + str(height) + " with a true size of " + str(crop_width) + "x" + str(crop_height))
        unknown2, unknown3, unknown4, unknown5 = struct.unpack("<4I", file.read(16))
        bytelayout, unknown6, unknown7, unknown8, unknown9, unknown10, unknown11 = struct.unpack("<7I", file.read(28))
        imagedata = file.read()
        if height == 0:
            # override for handling certain heightless files from Ni Hao, Kai-lan and potentially Tinker Bell
            print("Warning: Height is blank - assuming 256px")
            height = 256
        if bytelayout == 1:
            print("RGBA4444")
            rawimage = Image.frombytes("RGBA", (width, height), imagedata, "raw", "RGBA;4B")
            # quick hack to get around PIL's lack of little-endian RGBA4 support
            rawimage = Image.merge('RGBA', rawimage.split()[::-1])
            image_crop = rawimage.crop((0, 0, crop_width, crop_height))
            image_crop.save(files.with_suffix('.png'))
        elif bytelayout == 0:
            print("RGBA5551")
            imagedata_swapped = rgba5551_to_argb1555(imagedata)
            rawimage = Image.frombytes("RGBA", (width, height), imagedata_swapped, "raw", "BGRA;15") # note - expects big endian.
            image_crop = rawimage.crop((0, 0, crop_width, crop_height))
            image_crop.save(files.with_suffix('.png'))
        elif bytelayout == 2:
            print("RGB565")
            rawimage = Image.frombytes("RGB", (width, height), imagedata, "raw", "BGR;16")
            image_crop = rawimage.crop((0, 0, crop_width, crop_height))
            image_crop.save(files.with_suffix('.png'))
        elif bytelayout == 6:
            print("1-bit")
            rawimage = Image.frombytes("1", (width, height), imagedata, "raw", "1;IR")
            image_crop = rawimage.crop((0, 0, crop_width, crop_height))
            image_crop.save(files.with_suffix('.png'))
        elif bytelayout == 7:
            print("A8")
            rawimage = Image.frombytes("L", (width, height), imagedata, "raw", "L")
            image_crop = rawimage.crop((0, 0, crop_width, crop_height))
            image_crop.save(files.with_suffix('.png'))
        else:
            print("\033[1;33mDebug: This texture is stored in unimplemented format " + str(bytelayout) + ". Please paste this message into a new issue on GitHub and include a zip file of your affected samples.\033[1;0m")
