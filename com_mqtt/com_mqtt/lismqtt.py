import rclpy
import numpy as np
# import the ROS2 python libraries
from rclpy.node import Node
#from std_msgs.msg import String
from custom_msgs.msg import Sensores
from rclpy.qos import ReliabilityPolicy, QoSProfile
# importamos librerias MQTT
import paho.mqtt.client as mqttClient
import time
import json

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
    print("Archivo JSON recibido y guardado")
    print("Mensaje - {}:{}".format(message.topic, message.payload))

class ListenerMQTT(Node):

    def __init__(self):
        # call the class constructor
        super().__init__('lismqtt')
        # create the publisher object
        #self.publisher= self.create_publisher(Sensores, 'data_mqtt', 10)
        # define the timer period for 0.5 seconds
        self.timer_period = 0.5
        # define the variable to save the received info
        self.dato = Sensores()

        self.timer = self.create_timer(self.timer_period, self.motion)

        self.Connected = False  #variable para verificar el estado de la conexión
        self.broker_address="10.48.60.51"#10.48.60.66 dir de rasp "10.48.60.51" #dirección del Broker profe
        self.port= 1883 #puerto por defecto de MQTT
        self.tag = "/Robot1"  #tag, etiqueta o tópico
        #self.tag2 = "/Equipo1/Humedad"  #tag, etiqueta o tópico
        #self.tag3 = "/Equipo1/Bateria"  #tag, etiqueta o tópico

        self.client1=mqttClient.Client("cliente")
        self.client1.on_connect=on_connect
        self.client1.on_message=on_message #===> Duda
        self.client1.connect(self.broker_address,self.port)
        self.client1.loop_start()

    #def odom_callback(self,msg):
        #self.dato = msg
       

    def motion(self):
        
        #self.publisher.publish(self.dato)
        # print the data
        
        self.client1.subscribe(self.tag)
        #self.get_logger().info('Mensaje: "%s"' % self.dato)
        try:
            time.sleep(0.5)
        except KeyboardInterrupt:
            print("Recepción de mensajes detenida por el usuario")
            self.client1.disconnect()
            self.client1.loop_stop()
         
def main(args=None):
    # initialize the ROS communication
    rclpy.init(args=args)
    # declare the node constructor
    listener = ListenerMQTT()    
    # pause the program execution, waits for a request to kill the node (ctrl+c)
    rclpy.spin(listener)
    # Explicity destroy the node
    listener.destroy_node()
    # shutdown the ROS communication
    rclpy.shutdown()

if __name__ == '__main__':
    main()
