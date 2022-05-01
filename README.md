# testset-printer-emulator

A replacement for the old HP BTS software for 8935 series communications service monitors. Theoretically this will work with any HP (and likely other) test set with a print feature, but it only has been tried on an 8935. 

## Instructions

Download ghostPCL from https://www.ghostscript.com/releases/gpcldnld.html and put `gpcl6dll64.dll` and `gpcl6win64.exe` in the current directory.

Download and install Imagemagick from https://imagemagick.org/script/download.php#windows. Check Install Headers and Development Files.

Install pyserial and Wand via pip.

On your test set, set the printer type to Deskjet (others may work but have no been tested) and port to Serial 9 (for the 8935). A quick note on baud rate - the maximum speed the 8935 will go without flow control is 19,200bps. Many cheaper USB-serial interfaces or null modem cables do not pin out the flow control wires. At 19,200 it will take approximately 12 seconds for the image to get transmitted to your computer. If you reach the maximum speed of 115,200 you will need to enable RTS/CTS flow control on the test set and have a serial adapter capable of hardware flow control. I have found the Sabrent FTDI-based adapter to work well, as well as StarTech null modem cables. These seem to pass RTS/CTS just fine. At 115,200 your time to print is down to only about 2-3 seconds - so it is well worth it to get a higher quality cable.

Run the `pcltopng.py` file. When you hit Print on the test set, it will transmit the image to your computer, and when it's done processing, it will automatically open with your default application for viewing images. Images are stored with a simple timestamp appended to the file name.

Tweak the Background and Foreground settings in the heading of the file to change the hue shift. By default, the color correction is set to make the resulting image look like an 8935's monitor. If you would like no color correction, set foreground to #000000 and background to #ffffff, which is the default black and white (essentially setting it to no color correction).