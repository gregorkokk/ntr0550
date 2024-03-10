import traceback
import time
import paho.mqtt.client as paho
from PIL import Image, ImageDraw, ImageFont
import SH1106  

class MQTTClient:
    def __init__(self, client_id, subscribe_topic, broker, username, password, draw, disp):
        self.client_id = client_id #ID of MQTT client
        self.subscribe_topic = subscribe_topic #topic, client subscribes
        self.broker = broker #address of the MQTT broker
        self.username = username #username
        self.password = password #password
        self.client = paho.Client(client_id) # MQTT client object creater using the paho library
        self.client.on_connect = self.on_connect 
        self.client.on_message = self.on_message
        self.draw = draw #drawing on the display
        self.disp = disp #opject representing the display

    def connect(self):
        self.client.username_pw_set(self.username, self.password)
        self.client.connect(self.broker)
        self.client.loop_start()
        self.client.subscribe(self.subscribe_topic)

    def on_connect(self, client, userdata, flags, rc):
        print(f"Connected to MQTT broker {i} with result code: {rc}")

    def on_message(self, client, userdata, message):
        pass

    def send_message(self, topic, message, device_id):
        self.client.publish(topic, message)
        self.disp.ShowImage(self.disp.getbuffer(image1))
    
    def __str__(self):
        return f"client ID: {self.client_id}, subscribe topic: {self.subscribe_topic}, message: {message_to_send}"

    def disconnect(self):
        self.client.disconnect()
        self.client.loop_stop()

try:
    # display
    disp = SH1106.SH1106()
    disp.Init()
    disp.clear()
    image1 = Image.new('1', (disp.width, disp.height), "WHITE")
    draw = ImageDraw.Draw(image1)
    font10 = ImageFont.truetype('Font.ttf', 13)

    # MQTT
    broker = "10.8.0.1"
    username = "iot_module"
    password = "parool"

    clients = []

    for i in range(0, 16):
        if i < 10:
            client_id = f"client-00{i}"
            subscribe_topic = f"class/iot0{i}"
        else:
            client_id = f"client-0{i}"
            subscribe_topic = f"class/iot{i}"

        try:
            client = MQTTClient(client_id, subscribe_topic, broker, username, password, draw, disp)
            client.connect()
            clients.append(client)

        except Exception as e:
            print(f"An error occurred for client {client_id}: {e}")
            traceback.print_exc()
            time.sleep(5)

    message_to_send = "grex tervitab"

    for i, client in enumerate(clients, 1):
        client.send_message("common/topic", message_to_send, f"client-00{i}")

    for client in clients:
       print(client)

    # Loop until exit with CTRL + C
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    print("Exiting")
    for client in clients:
        client.disconnect()

except IOError as e:
    print(f"Error initializing display: {e}")

finally:
    disp.clear()

