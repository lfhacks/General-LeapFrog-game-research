# Introduction
This guide is exclusively for the LeapPad 3 and onwards. DO NOT USE IT ON ANYTHING FROM BEFORE THE LF3000/NXP4330!

It can brick earlier devices due to them being more likely to suffer from memory corruption. They're also just far too slow for this.

List of bad devices for this guide:
- Crammer (doesn't run Linux)
- Leaptop, MyPals and anything similar (doesn't run Linux)
- Leapster 2 (doesn't run Linux)
- Didj (it's impossible here anyways, not enough RAM to run ffmpeg)
- Leapster Explorer
- LeapsterGS Explorer
- LeapBand (doesn't run Linux)
- LeapPad Explorer (all variants)
- LeapPad 2 Explorer (all variants)
- LeapPad Ultra (all variants)
- LeapPad Jr. (there's no way to properly hack this one currently and it lacks Wi-Fi capabilities)
- RockIt Twist (doesn't run Linux)
- LeapFrog Epic (works entirely differently to the other devices and doesn't run Linux)
- LeapPad Academy (works entirely differently to the other devices and doesn't run Linux)

List of devices that are okay for this guide (output quality will vary)
- LeapPad 3
- LeapPad Platinum
- LeapPad Ultimate
- LeapTV (not worth it due to this one having HDMI out though)

One more thing to note:

If this guide doesn't directly say to shut off your LeapPad, don't. Follow it carefully!

Mistakes could lock you out of modding your device or even worse, brick it.



# What you'll need
First, grab your phone and connect it to wi-fi. Enable the hotspot and connect your LeapPad 3 and your computer to it.

(This is needed to grab the IP! Both devices need to be on the same network!)

LeapPad Manager (to enable developer mode and send commands) and the LeapPad port of ffmpeg:

https://archive.org/download/leappad3capturesetup be sure to get all setup-related files from here that aren't linked to later.

A Linux machine or VM to stream your captures to (allows for longer recordings and smoother framerates)

FileZilla (So you can FTP to the LeapPad)


# Accessing the files on your LeapPad
First, you'll want to gain FTP access. This requires that you enable developer mode. 

Be sure to install the LoadDev app first in case anything goes wrong! It can disable developer mode.

Once developer mode is active, reboot the LeapPad 3 and connect to it again using LeapPad Manager

Send this command to the LeapPad:

/usr/sbin/vsftpd &

That will enable FTP and run it in the background to prevent LeapPad Manager from freezing as you run it

Now you can connect to the LeapPad using FileZilla:
- Enter the IP listed by your hotspot and enter "root" as the username
- Leave the password blank

The next step is optional, but if you do this repeatedly, it can be useful:

- Connect to the LeapPad using FileZilla if you aren't already connected
- Go to /etc/mdev/ and drag/drop cartridge.sh to a folder on your computer
- Open it with notepad
- add the /usr/sbin/vsftpd & command right at the start of the file

Now, every time you insert a cartridge, it'll enable FTP access. At that point, you'll only need to know the IP of your LeapPad!

# Gaining access to the terminal through Telnet
Get PuTTY here:

https://putty.org/

Now go to LeapPad Manager and run "/etc/init.d/telnetd restart" (do not put this in your cartridge script! It breaks something you'll need later if you do that.)

![image](https://gist.github.com/user-attachments/assets/d7f9cb90-abf5-4066-a1b4-446dfedf0a50)

Get your LeapPad's IP again and set up PuTTY like what's seen below (the IP seen there is an example, do not use that one):

![image](https://gist.github.com/user-attachments/assets/9167861b-6ac6-41a6-8909-9923549ca72c)

Once everything is set up, click "Open" and if everything was successful, a terminal should pop up. 

As a test, try typing "ls /" and hit enter. If you can type at all and there's a folder named "LF", it's working.

# Installing ffmpeg to the LeapPad
- Put the "ffmpeg" file into /usr/bin/ over FTP
- run "chmod +x /usr/bin/ffmpeg" over Telnet (this allows it to run)
- Put the libraries in a folder named "ffmp" on the root of the device over FTP
- run chmod +x on all of them over Telnet

# Using ffmpeg
First, you need to run "LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/ffmp" over Telnet. You have to do this every time you reboot the device!

Next, try running this:

ffmpeg -f fbdev -i /dev/fb1 -r 40 -vcodec mpeg2video -b 999k -f mpeg2video /LF/Bulk/TEST.mpg

If it works, press Q on the Telnet window when you want it to stop.

Now use FTP to copy the test video off of your device and try playing it with VLC.

# Where's the audio?
You'll need a 3.5mm AUX cable for this step:
- Connect one end to your computer's microphone port (this is required to get audio captures)
- Connect the other end to the headphone port on your LeapPad
- Open your preferred audio recording software (such as Audacity)
- Press record

Now the audio should be getting recorded. You'll have to know basic video editing to put the audio and video together.

# Setting up a VM so you can stream the ffmpeg output to the said VM
If you're already using a Linux machine, you can skip the VM setup.

- Get VirtualBox (be sure that all drivers are set to install!)
- Get a Ubuntu ISO and set up your VM for the first time
- Close the VM after the setup process is done
- Go to Settings > Network and set the Attached to option to Bridged Adapter
- Click the bar on the Name field and select the device your machine uses for Wi-Fi

# Streaming the file data over to your Linux machine/VM
This can be done with a simple change to the command:

On the Linux machine/VM (in the terminal):

nc -l -p 19000 > "/home/(username)/Documents/TEST.mpg"

On the LeapFrog device (over Telnet):

ffmpeg -f fbdev -i /dev/fb1 -r 40 -vcodec mpeg2video -b 999k -f mpeg2video tcp://(Linux machine or VM IP):19000



Of course, to use it, you'll need to get your computer's IP. Do the following:

- Open your terminal if you haven't already
- Run "ip addr show"
- Look for lines with "inet" at the start. The first one that isn't in the LOOPBACK section is most likely your IP.
- Run the Linux machine/VM part of the capture command
- Put the IP in place of the (Linux machine of VM IP) part of the command on your LeapFrog device

Example (change out the username and IP for your own if you want these to work!):

On the Linux machine/VM in the terminal:

nc -l -p 19000 > "/home/FunnyUsername/Documents/TEST.mpg"

On the LeapFrog device over Telnet:

ffmpeg -f fbdev -i /dev/fb1 -r 40 -vcodec mpeg2video -b 999k -f mpeg2video tcp://0.0.0.0:19000

# Getting files off of your VM
There's several ways to do this, but a quick way to do it is this:

- cd to the directory your files are in
- Run "python3 -m http.server 8000" in the terminal
- Go to http://(your VM's IP):8000 in your internet browser of choice
- Press CTRL+C in the terminal to end this once you're done 

# Alternative method for setting up ffmpeg permanently
- Be sure that you have both your LeapPad and your computer connected to the same network and can view the LeapPad's IP for later
- Open LeapPad Manager
- Connect to your LeapPad 3/Platinum/Ultimate

### Just a warning for the next section:
This makes it so Telnet is always on and running as root without a password. This is very insecure.

Now send the following commands:

- echo /etc/init.d/vsftpd start >> /etc/init.d/rcS
- echo /etc/init.d/telnetd start >> /etc/init.d/rcS
- mkdir -p /usr/local/lib

Reboot the system with LeapPad Manager (LeapPad > Reboot system)

Connect to the LeapPad over FTP using the IP you got earlier and "root" as the username and transfer the FFMPEG files to the following locations:

- /usr/bin/ (ffmpeg)
- /usr/local/lib/ (libraries)

Connect to the LeapPad using Telnet and send the following command:

chmod +x /usr/bin/ffmpeg

Now reboot it and ffmpeg should work without having to load the libraries manually. It might require you to reboot the LeapPad several times before it starts working.

# Credits
SparXalt for the alternative setup that allows you to keep this stuff working permanently

https://github.com/SparXalt
