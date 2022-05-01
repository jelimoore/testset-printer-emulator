import serial
import subprocess
import os
from wand.image import Image
from wand.display import display
from datetime import datetime

BAUD_RATE = 115200
PORT = 'COM8'
# HP 8935 monitor color is about #fc9d03
FOREGROUND = '#fc9d03'
BACKGROUND = '#000000'

notifier = ToastNotifier()

def processPCL(dataIn):
    #don't process if too little data
    if (len(dataIn) > 10):
        print("Got good data")
        gpcl = subprocess.run(['gpcl6win64.exe', '-sDEVICE=png16m', '-r600', '-dDownScaleFactor=3', '-o' '-', '-'], capture_output=True, input=dataIn)
        #print(gpcl)
        with Image(blob=gpcl.stdout) as img:
            #print(img.size)
            # don't know what this is but i need it
            img.format = 'jpeg'
            # crop it
            img.crop(25, 125, width=1425, height=775)
            # color replace
            img.opaque_paint(target='#000000', fill=FOREGROUND, fuzz=5)
            img.opaque_paint(target='#ffffff', fill=BACKGROUND, fuzz=5)

            # save the image and open it in photo viewer
            imageName = 'capture-' + datetime.now().strftime('%H.%M.%S') + '.png'
            img.save(filename='PNG24:' + imageName)
            os.startfile(imageName)
        print("Processed image")
        return True
    else:
        return None

def waitForData():
    with serial.Serial(port=PORT, baudrate=BAUD_RATE, rtscts=True, timeout=4) as testset:
        rx_data = b''
        while True:
            while testset.in_waiting:
                curr_char = testset.read()
                #print("Read {}".format(curr_char))
                rx_data += curr_char
                #break if we get a newline + FF
                if (b'\r\n\r\x0c' in rx_data):
                    # send data off and then reset buffer
                    #print("Received data: {}".format(rx_data))
                    processPCL(rx_data)
                    rx_data = b''
        testset.close()

waitForData()