# Getting screenshots (LeapFrog Explorer only!)

## Which devices should I use this on?
Preferrably, any LeapFrog Explorer device that lacks Wi-Fi connectivity that isn't the LeapPad Jr (screenshots do not need the extra power those devices have):

- Leapster(GS) Explorer
- LeapPad 1 and 2

The Didj *WILL NOT* work! Do not use a Didj for this guide. 

Even if you could install fbgrab, the devices it uses for rendering (layers) are incompatible with fbgrab (which is for frame buffers).

## Getting what you need to do this
First, you need to obtain the required tools:

Get [LeapPad Manager](https://archive.org/download/leappad3capturesetup/LeapPad_Manager.rar) (for the setup process)

Get [LoadDev](https://archive.org/download/leappad3capturesetup/LoadDev.tar) (to disable developer mode)

Get [fbgrab](https://archive.org/download/leappad3capturesetup/fbgrab.zip) (for screenshots)

Get [FileZilla](https://filezilla-project.org/download.php?show_all=1) (for FTP)

Get [PuTTY](https://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html) (for telnet/sending commands)

## The setup process
Unpack LeapPad Manager in any location (it can go anywhere, the install location doesn't matter)

Install LoadDev onto your LeapFrog Explorer device with LeapPad Manager, then reboot and check if it shows up.

If it does, continue with the next steps.

**Note:** Skipping the previous step isn't recommended, as doing so could render your LeapFrog Explorer device inaccessible to LeapPad Manager after enabling developer mode.



Ok, now that it's installed, you can enable developer mode with LeapPad Manager. Follow this guide to gain FTP access:

https://web.archive.org/web/20210507031605/https://spiffyhacks.com/thread-215.html

If you don't understand the filezilla setup part:

Enter "root" as the username and leave the password field blank. Use the IP LeapPad Manager tells you to.



For Telnet, you just need the IP. Make sure your PuTTY window looks like this before connecting:

![image](https://github.com/user-attachments/assets/acd9eb0a-e81d-4f09-9a21-68dc3bbc8418)



## Copying the files over
Copy fbgrab (without the libraries) into /usr/bin on the LeapFrog Explorer device, then run "chmod +x /usr/bin/fbgrab" on it with LeapPad Manager

Copy the libraries into /usr/lib

Reboot the LeapFrog Explorer device



## Using fbgrab
Open PuTTY and connect to your LeapFrog Explorer device.

Enter this command to test it:

fbgrab -a -d /dev/fb1 /LF/Bulk/test4.png

If it worked, try changing the output filename and opening a game. This will not work for FMVs/pre-rendered videos.

Example:

fbgrab -a -d /dev/fb1 /LF/Bulk/NFLRush.png

![NFLRush](https://github.com/user-attachments/assets/6968f66e-b34d-4d47-b3d9-e689c99882e0)
