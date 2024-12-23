import tkinter as tk #Used to kill the extra tkinter window
from tkinter import filedialog
import os
import tarfile
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
root = tk.Tk()#Create a root window
root.withdraw()#Hide the root window
files = filedialog.askopenfilenames()
root.destroy()#Destroy the root window

class LF3Decryptor:
    def __init__(self):
        self.file_in = ""
        self.cache_folder = r"decrypted"
        self.has_decrypted = False

        if not os.path.exists(self.cache_folder):
            os.makedirs(self.cache_folder)

    def init_ctr(self, key, iv):
        cipher = Cipher(algorithms.AES(key), modes.CTR(iv), backend=default_backend())
        return cipher

    def decrypt_ctr(self, cipher, data):
        decryptor = cipher.decryptor()
        return decryptor.update(data) + decryptor.finalize()

    def lf3_decrypt(self, file_input):
        self.file_in = file_input
        print(f"Decrypting {self.file_in}...")

        key = b'\x44\xee\x33\x41\x4a\x56\x48\xe1\x5e\x1c\x7e\x15\x85\xb1\x07\x38'
        iv = bytearray(16)

        cipher = self.init_ctr(key, iv)

        try:
            with open(self.file_in, 'rb') as file_stream1:
                file_stream1.seek(0)
                num_array1 = file_stream1.read(16)
                cipher = self.init_ctr(key, num_array1)
                num_array2 = file_stream1.read()
                
                buffer = self.decrypt_ctr(cipher, num_array2)

                decrypted_tar_path = os.path.join(self.cache_folder, os.path.splitext(os.path.basename(self.file_in))[0] + ".tar.bz")
                
                with open(decrypted_tar_path, 'wb') as file_stream2:
                    file_stream2.write(buffer)

                if os.path.exists(decrypted_tar_path):
                    print(f"Your LF3 has been successfully decrypted.")

        except FileNotFoundError:
            print(f"File not found: {self.file_in}")
        except Exception as e:
            print(f"An error occurred: {e}")
            print("Decryption Failed")


if __name__ == "__main__":
    lf3_decryptor = LF3Decryptor()
    if os.path.exists("decrypted") == False: #Check if the folder exists already. If not, make it.
        os.mkdir("decrypted")
        
    for file in files: #Do a loop that goes through every selected file, allowing for multiple files to be selected at once
        if os.path.isfile(file):
            lf3_decryptor.lf3_decrypt(file)
