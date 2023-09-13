#Codigo para mostrar imagen en custom tkinter

import base64
import cv2 as cv
import numpy as np
import paho.mqtt.client as mqtt
import customtkinter
from PIL import Image
from PIL import Image, ImageTk

MQTT_BROKER = "10.48.60.51"
MQTT_RECEIVE = "/Equipo1/Camara"

frame = np.zeros((240, 320, 3), np.uint8)


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(MQTT_RECEIVE)


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    global frame
    # Decoding the message
    img = base64.b64decode(msg.payload)
    # converting into numpy array from buffer
    npimg = np.frombuffer(img, dtype=np.uint8)
    # Decode to Original Frame
    frame = cv.imdecode(npimg, 1)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_BROKER)

# Starting thread which will receive the frames
client.loop_start()

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

root = customtkinter.CTk()

root.geometry("400x350")

image_label = customtkinter.CTkLabel(root,text="")
image_label.pack()

while True:
# Convert the OpenCV BGR image to RGB
    rgb_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)

    # Convert the RGB frame to a PIL Image
    pil_image = Image.fromarray(rgb_frame)

    # Convert the PIL Image to a PhotoImage for CTKImage
    ctk_image = ImageTk.PhotoImage(image=pil_image)
    image_label.configure(image=ctk_image)
    image_label.image = ctk_image
    #cv.imshow("Stream", frame)
    #if cv.waitKey(1) & 0xFF == ord('q'):
    #    break

    root.update()

# Stop the Thread
client.loop_stop()