import ctypes
from ctypes.wintypes import LPCSTR, UINT
import os
import tkinter as tk
from tkinter import filedialog

#I'm starting to think this isn't actually the format value... It's probably a configuration value instead.
formats = [5, 0x20, 0x21, 0x22, 0x23, 0x24, 0x25, 0x26, 0x27, 0x28, 0x29, 0x2A, 0x2B, 0x2C, 0x2D, 0x2E, 0x2F,       #S720
           ]
#First time configuration. If the algorithms folder isn't defined in algodir.txt yet, make the user select the algorithm folder.
if not os.path.isfile(os.path.join(os.getcwd(), "algodir.txt")):
    with open("algodir.txt", "w+") as algos:
        algorithms = filedialog.askdirectory()
        algos.write(algorithms)
else:
    with open("algodir.txt", "r") as algos:
        algorithms = algos.readline().strip()
        print(algorithms)

root = tk.Tk()
root.withdraw()
files = filedialog.askopenfilenames()
root.destroy()

if os.path.exists(os.getcwd()+"/WAVs/") == False:
    os.makedirs(os.getcwd()+"/WAVs/") #This is where files get saved to

def s720(dll, file, rate):
    s720dll = ctypes.WinDLL(dll)
    decproto = ctypes.WINFUNCTYPE(ctypes.c_uint, LPCSTR, LPCSTR, UINT, UINT)
    decparamflags = ((1, 'infile'), (1, 'outfile'), (1, 'samplerate', rate), (1, 'unknown', 0))
    decfunc = decproto(('s4872_dec', s720dll), decparamflags)
    outfile = os.getcwd()+"/WAVs/" + os.path.splitext(os.path.basename(file))[0] + '.wav'
    decfunc(infile=LPCSTR(file.encode('ascii')), outfile=LPCSTR(outfile.encode('ascii')))
    print(outfile)

for file in files:
    with open(file, "rb") as f:
        f.seek(4)
        data = f.read(1)[0]
        if data in formats:
            rate = 11025
            s720(f'{algorithms}/S4872.DLL', file, rate)
        else:
            print(hex(data))
        
