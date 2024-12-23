import ctypes
from ctypes.wintypes import LPCSTR, UINT
import os
import tkinter as tk
from tkinter import filedialog
formats = [0x07,             #A1600 (11025Hz)
           0x09,             #A1600 (8000Hz)
           0x20, 0x80, 0xC0, #A1800
           0x27, 0x2F,       #S720
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

def a16(dll, file, rate):
    a1600dll = ctypes.WinDLL(dll)
    decproto = ctypes.WINFUNCTYPE(ctypes.c_uint, LPCSTR, LPCSTR, ctypes.POINTER(UINT), UINT, UINT, UINT)
    decparamflags = ((1, 'infile'), (1, 'outfile'), (2, 'fp'), (1, 'unk1', 8000), (1, 'Sample_Rate', rate), (1,'unk2', 0))
    decfunc = decproto(('a1600_dec', a1600dll), decparamflags)
    outfile = os.getcwd()+"/WAVs/" + os.path.splitext(os.path.basename(file))[0] + '.wav'
    decfunc(infile=LPCSTR(file.encode('ascii')), outfile=LPCSTR(outfile.encode('ascii')))
    print(outfile)
    
def a18(dll, file):
    a1800dll = ctypes.WinDLL(dll)
    decproto = ctypes.WINFUNCTYPE(ctypes.c_uint, LPCSTR, LPCSTR, ctypes.POINTER(UINT), UINT, UINT)
    decparamflags = ((1, 'infile'), (1, 'outfile'), (2, 'fp'), (1, 'unk1', 16000), (1,'unk2', 0))
    decfunc = decproto(('dec', a1800dll), decparamflags)
    outfile = os.getcwd()+"/WAVs/" + os.path.splitext(os.path.basename(file))[0] + '.wav'
    decfunc(infile=LPCSTR(file.encode('ascii')), outfile=LPCSTR(outfile.encode('ascii')))
    print(outfile)

for file in files:
    with open(file, "rb") as f:
        f.seek(4)
        data = f.read(1)[0]
        if data == formats[0]:
            rate = 11025
            a16(f'{algorithms}/A1600.DLL', file, rate)
        elif data == formats[1]:
            rate = 8000
            a16(f'{algorithms}/A1600.DLL', file, rate)
        elif data == formats[2] or data == formats[3] or data == formats[4]:
            a18(f'{algorithms}/A1800.DLL', file)
        else:
            print(hex(data))
        
