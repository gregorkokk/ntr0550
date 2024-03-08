import SH1106
import config
import traceback
import time
import paho.mqtt.client as paho
from PIL import Image, ImageDraw, ImageFont

what_to_send = "grex siin"


for i in range (1,16):
    if i < 10:
        paho_client = "client-00" + str(i)
        client_subscribe = "class/iot0" + str(i)
    else:
        paho_client = "client-0" + str(i)
        client_subscribe = "class/iot" + str(i)

print(paho_client)
print(client_subscribe)

try:
    disp = SH1106.SH1106()
    disp.Init()
    disp.clear()
    # Create blank image for drawing.
    image1 = Image.new('1', (disp.width, disp.height), "WHITE")
    draw = ImageDraw.Draw(image1)
    font = ImageFont.truetype('Font.ttf', 20)
    font10 = ImageFont.truetype('Font.ttf', 13)

except IOError as e:
    print(e)

broker="10.8.0.1"

# Define callback
def on_message(client, userdata, message):
    global disp, draw, font10, image1
    print(f"sending data to: {paho_client}")
    draw.text((0, 0), what_to_send, font = font10, fill = 0)
    disp.ShowImage(disp.getbuffer(image1))
    print(f"received message =  {what_to_send}")
    time.sleep(5)
    disp.clear()

client = paho.Client(paho_client)

# Bind function to callback
client.on_message = on_message

# Set username and password
client.username_pw_set(username = "iot_module", password = "parool")

print("connecting to broker ", broker)
client.connect(broker)   # connect
client.loop_start()      # start loop to process received messages
client.loop_start()      # start loop to process received messages
client.subscribe(client_subscribe) #subscribe
time.sleep(2)


# loop until exit with CTRL + C
try:
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    print("exiting")
    client.disconnect() # disconnect
    client.loop_stop()  # stop loop

except Exception as e:
    print("An error occurred:", e)
    traceback.print_exc()

    # Disconnect and stop the loop to prevent further issues
    client.disconnect()
    client.loop_stop()

    # Sleep for a short while before retrying
    time.sleep(5)
