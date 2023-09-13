import paho.mqtt.client as mqttClient
import time
import json
import pymongo

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

def on_message(client,userdata,message):
    """Función que recibe los mensajes del broker
    
    """
    payload = message.payload.decode("utf-8")
    data = json.loads(payload)

    with open("data.json", "w") as file:
        json.dump(data, file, indent=4)
    print("Archivo JSON recibido y guardado.")
    
    resultado = collection.insert_one(data)
    print("ID del documento insertado:", resultado.inserted_id)

    print("Mensaje - {}:{}".format(message.topic, message.payload))
    return

# Establecer una conexión a la base de datos MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")

# Seleccionar una base de datos
db = client["Datos"]

# Seleccionar una colección
collection = db["prueba"]

Connected = False  #variable para verificar el estado de la conexión
broker_address="10.48.60.51"#"10.48.60.51" #dirección del Broker del profe "10.48.60.66" dir de la rasp
port= 1883 #puerto por defecto de MQTT
tag = "/Equipo1/#"  #tag, etiqueta o tópico

client1=mqttClient.Client()
client1.on_connect=on_connect
client1.on_message=on_message
client1.connect(broker_address,port)
client1.loop_start()

while Connected != True:
    time.sleep(0.1)
    client1.subscribe(tag)
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Recepción de mensajes detenida por el usuario")
        client1.disconnect()
        client1.loop_stop()