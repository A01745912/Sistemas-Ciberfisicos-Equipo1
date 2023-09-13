#Codigo para poder desplegar mapa con la ubicación actual del rover.
from pymongo import MongoClient
from pymongo import DESCENDING  # Import DESCENDING from pymongo
import json
import customtkinter
import tkintermapview
#import paho.mqtt.client as mqttClient
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime, timedelta
from PIL import Image

# Create a MongoDB client
client2 = MongoClient('localhost', 27017)

# Access a specific database
db = client2['Datos']

# Access a specific collection
collection = db['prueba']

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

root = customtkinter.CTk()

root.geometry("700x650")

def subs():
    #marker_2.delete()
    
    # Retrieve the most recent document from the collection
    most_recent_document = collection.find_one({}, sort=[('_id', DESCENDING)])
    del most_recent_document['_id']
    coorx = most_recent_document['CoordenadaX']
    coory = most_recent_document['CoordenadaY']
    map_widget.set_position(coorx,coory) #CEM
    marker_2.set_position(coorx,coory)

    root.after(1000, subs)

map_widget = tkintermapview.TkinterMapView(root, width=800, height=600, corner_radius=0)
map_widget.place(relx=0.5, rely=0.5, anchor=customtkinter.CENTER)

#Set marker
marker_2 = map_widget.set_marker(19.597450907484646, -99.22712693520945, text="CEM")

#Set coordinates 
map_widget.set_position(19.597450907484646, -99.22712693520945) #CEM

#Set Address
#map_widget.set_address("Avenida Hidalgo 72, Estado de Mexico, Mexico")

#Set Zoom
map_widget.set_zoom(19)

root.after(1000, subs)

root.mainloop()

