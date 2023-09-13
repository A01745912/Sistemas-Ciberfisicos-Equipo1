from pymongo import MongoClient
from pymongo import DESCENDING  # Import DESCENDING from pymongo
import json
import customtkinter
import paho.mqtt.client as mqttClient
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime, timedelta
from PIL import Image
import subprocess

def on_connect(client, userdata, flags, rc):
    """Función que establece la conexión

    """
    if rc==0:
        print("Conectado al broker")
        global Connected
        Connected = True
    else:
        print("Falla en la conexión")
    return

Connected = False  #variable para verificar el estado de la conexión
broker_address= "10.48.60.51" #dirección del Broker
port= 1883 #puerto por defecto de MQTT
tag1 = "/Robot1"  #tag, etiqueta o tópico

client = mqttClient.Client() #instanciación
client.on_connect = on_connect #agregando la función
client.connect(broker_address, port)
client.loop_start() #inicia la instancia

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

def login():
    print("Test")

def subs():
    # Retrieve the most recent document from the collection
    most_recent_document = collection.find_one({}, sort=[('_id', DESCENDING)])
    del most_recent_document['_id']
    co2 = round(most_recent_document['CO2'],1)
    hum = most_recent_document['Humedad']
    tem = round(most_recent_document['Temperatura'],2)
    batery = round(most_recent_document['Bateria'],2)
    label1.configure(text=co2)
    label2.configure(text=hum)
    label3.configure(text=tem)
    bar.set(batery) #Agregar el nivel de bateria a la barra de progreso.
    #print("hola")
    pipeline = [
    {
        '$sort': {'_id': -1}
    },
    {
        '$limit': 5
    }
    ]
    result = list(collection.aggregate(pipeline))
    data = []
    for document in result:
        del document['_id']
        opcion = combobox_graf.get()
        if opcion == "Humedad":
            data.append(document['Humedad'])
            ax.set_ylim([35, 85])
        elif opcion == "Temperatura":
            data.append(document['Temperatura'])
            ax.set_ylim([10, 40])
        elif opcion == "CO2":
            data.append(document['CO2'])
            ax.set_ylim([0, 100])
        elif opcion == "Vel Lineal":
            data.append(document['VelLin'])
            ax.set_ylim([0, 15])
        elif opcion == "Vel Angular":
            data.append(document['VelAng'])
            ax.set_ylim([-1, 1])
            
        #print(document)
    #data = [1, 2, 3, 4, 5]
    data.reverse()
    ax.clear()
    ax.plot(data)
    ax.set_xlabel('X-axis')
    ax.set_ylabel('Y-axis')
    ax.set_title(combobox_graf.get())
    
    canvas.draw()
    root.after(2000, subs)

def msg():
    x = int(entry1.get())
    y = int(entry2.get())
    val1=json.dumps({"PosicionX": x,"PosicionY": y})
    print(tag1,val1)
    client.publish(tag1,val1,qos=0)
    root.after(2000, subs)

def mapas():
    # Execute the second script using subprocess
    subprocess.Popen(["python", "mapa.py"])
    root.after(2000, subs)

def video():
    # Execute the second script using subprocess
    subprocess.Popen(["python", "camaramqtt.py"])
    root.after(2000, subs)

my_image = customtkinter.CTkImage(light_image=Image.open("Interfaz/QLogo.png"),
                                  dark_image=Image.open("Interfaz/QLogo.png"),
                                  size=(70, 70))

image_label = customtkinter.CTkLabel(root, image=my_image, text="")
image_label.pack(padx=1, pady=1)

#Pestanias
tabView = customtkinter.CTkTabview(master=root)
tabView.pack(padx=10, pady=10, expand=True)

tabView.add("Datos")
tabView.add("Envio")
tabView.add("Graphs")
tabView.add("Maps")
tabView.add("Camera")

tabView.set("Datos")

#frame = customtkinter.CTkFrame(master=root)
#frame.pack(pady=20, padx=90, fill="both")#, expand=True)

#frame2 = customtkinter.CTkFrame(master=root)
#frame2.pack(pady=20, padx=130, fill="both")#, expand=True)

#Titulos de datos del robot
labelco2 = customtkinter.CTkLabel(master=tabView.tab("Datos"), text="CO2:")
labelco2.grid(row=0, column=0, pady=12, padx=10)

labelhum = customtkinter.CTkLabel(master=tabView.tab("Datos"), text="Humedad:")
labelhum.grid(row=1, column=0, pady=12, padx=10)

labeltem = customtkinter.CTkLabel(master=tabView.tab("Datos"), text="Temperatura:")
labeltem.grid(row=2, column=0, pady=12, padx=10)

labelbat = customtkinter.CTkLabel(master=tabView.tab("Datos"), text="Bateria:")
labelbat.grid(row=3, column=0, pady=12, padx=10)

#Labels con datos del robot
label1 = customtkinter.CTkLabel(master=tabView.tab("Datos"), text="")#, text_font=("Roboto", 24))
label1.grid(row=0, column=1, pady=12, padx=10)

label2 = customtkinter.CTkLabel(master=tabView.tab("Datos"), text="")
label2.grid(row=1, column=1, pady=12, padx=10)

label3 = customtkinter.CTkLabel(master=tabView.tab("Datos"), text="")
label3.grid(row=2, column=1, pady=12, padx=10)

#Barra de nivel de bateria
bar = customtkinter.CTkProgressBar(master=tabView.tab("Datos"),orientation="horizontal")
bar.grid(row=3, column=1,pady=10, padx=10)

#Entradas de datos para enviar al robot
entry1 = customtkinter.CTkEntry(master=tabView.tab("Envio"), placeholder_text="Coordenada en x")
entry1.pack(pady=12, padx=10)
entry2 = customtkinter.CTkEntry(master=tabView.tab("Envio"), placeholder_text="Coordenada en y")
entry2.pack(pady=12, padx=10)

#Mensaje de pestania mapas
labelmap = customtkinter.CTkLabel(master=tabView.tab("Maps"), text="Haga click para mostrar ubicacion")
labelmap.pack(pady=12, padx=10)

#Boton para mostrar mapa
button = customtkinter.CTkButton(master=tabView.tab("Maps"), text="Show", command=mapas)
button.pack(padx=12, pady=10)

#Mensaje de pestania camara
labelmap = customtkinter.CTkLabel(master=tabView.tab("Camera"), text="Haga click para mostrar video")
labelmap.pack(pady=12, padx=10)

#Boton para mostrar imagen
button = customtkinter.CTkButton(master=tabView.tab("Camera"), text="Show", command=video)
button.pack(padx=12, pady=10)

#Boton para graficar
#plot_button = customtkinter.CTkButton(master=tabView.tab("Graphs"), text="Plot Data", command=plot_draw)
#plot_button.pack()

#Opciones de graficas.
optionmenu = customtkinter.StringVar(value="")

combobox_graf = customtkinter.CTkComboBox(master=tabView.tab("Graphs"), values=["Humedad","Temperatura","CO2", "Vel Lineal", "Vel Angular"],variable=optionmenu)
combobox_graf.pack(pady=12, padx=10)

#Grafica de datos
fig, ax = plt.subplots()
canvas = FigureCanvasTkAgg(fig,master=tabView.tab("Graphs"))
canvas.get_tk_widget().pack()

#Boton para enviar datos por MQTT
button = customtkinter.CTkButton(master=tabView.tab("Envio"), text="Send", command=msg)
button.pack(padx=12, pady=10)
#frame2.grid_columnconfigure(0, weight=1)

root.after(500, subs)

root.mainloop()

# Close the connection
client2.close()