import SH1106
import time
import config
import traceback
import paho.mqtt.client as paho
from PIL import Image,ImageDraw,ImageFont

broker="10.8.0.1"

# Define callback
def on_message(client, userdata, message):
    time.sleep(1)
    try:
        disp = SH1106.SH1106()
        # Initialize library.
        disp.Init()
        # Clear display.
        disp.clear()
    
        # Create blank image for drawing.
        image1 = Image.new('1', (disp.width, disp.height), "WHITE")
        draw = ImageDraw.Draw(image1)
        font = ImageFont.truetype('Font.ttf', 20)
        font10 = ImageFont.truetype('Font.ttf',13)
 
        draw.line([(0,0),(127,0)], fill = 0)
        draw.line([(0,0),(0,63)], fill = 0)
        draw.line([(0,63),(127,63)], fill = 0)
        draw.line([(127,0),(127,63)], fill = 0)
        
        draw.text((30,0), str(message.payload.decode("utf-8")), font = font10, fill = 0)
    
        # image1=image1.rotate(180) 
        disp.ShowImage(disp.getbuffer(image1))
        time.sleep(2)
        
        Himage2 = Image.new('1', (disp.width, disp.height), 255)  # 255: clear the frame
        bmp = Image.open('pic.bmp')
        Himage2.paste(bmp, (0,5))
        # Himage2=Himage2.rotate(180) 	
        disp.ShowImage(disp.getbuffer(Himage2))

    except IOError as e:
        continue
    
    except KeyboardInterrupt:    
        print("ctrl + c:")
        disp.RPI.module_exit()
        exit()
        
    print("received message =",str(message.payload.decode("utf-8")))

for x in range(1, 16):
    if x < 10:
        client= paho.Client("client-00"+str(x))
    else:
        client= paho.Client("client-0"+str(x))
    # Bind function to callback
    client.on_message=on_message
    
    # Set username and password
    client.username_pw_set(username = "iot_module", password = "parool")
    
    print("connecting to broker ",broker)
    client.connect(broker)   # connect
    client.loop_start()      # start loop to process received messages
    print("subscribing ")
    if (x < 10):
        client.subscribe("class/iot0"+str(x))
    else:
        client.subscribe("class/iot"+str(x))
    time.sleep(2)
    
    try:
            while True:
                        time.sleep(5)
                        for num in range(1, 13):
                            padded_num = str(num).zfill(2)
                            client.publish("class/iot" + padded_num, "grex saadab parimat!")
                        break
    except KeyboardInterrupt:
        print("exiting")
        client.disconnect() #disconnect
        client.loop_stop() #stop loop
