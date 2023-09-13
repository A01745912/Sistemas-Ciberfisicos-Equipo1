import rclpy
import numpy as np
import random
import paho.mqtt.client as mqttClient
import json
import time
import cv2
import base64
# import the ROS2 python libraries
from rclpy.node import Node
#from std_msgs.msg import String
from custom_msgs.msg import Sensores
from rclpy.qos import ReliabilityPolicy, QoSProfile

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

class Listener(Node):

    def __init__(self):
        # call the class constructor
        super().__init__('cammqtt')
        # create the publisher object
        #self.subscriber = self.create_subscription(Sensores, 'data_cam', self.odom_callback, QoSProfile(depth=10, reliability=ReliabilityPolicy.RELIABLE	))

        # define the timer period for 0.5 seconds
        self.timer_period = 0.1
        # define the variable to save the received info
        
        self.cap = cv2.VideoCapture(0)
        
        self.Connected = False  #variable para verificar el estado de la conexión
        self.broker_address= "10.48.60.51"#10.48.60.66 dir de rasp "10.48.60.51" #dirección del Broker profe
        self.port= 1883 #puerto por defecto de MQTT
        self.tag1 = "/Equipo1/Camara"  #tag, etiqueta o tópico
        #self.tag2 = "/Equipo1/Humedad"  #tag, etiqueta o tópico
        #self.tag3 = "/Equipo1/CO2"  #tag, etiqueta o tópico

        self.client = mqttClient.Client() #instanciación
        self.client.on_connect = on_connect #agregando la función
        self.client.connect(self.broker_address, self.port)
        self.client.loop_start() #inicia la instancia

        self.timer = self.create_timer(self.timer_period, self.motion)
        
    
    def __del__(self):
        self.cap.release()
       
    def motion(self):
        # print the data
        try:
            ret, frame = self.cap.read()
            encoded_image = base64.b64encode(cv2.imencode('.jpg', frame)[1]).decode('utf-8')
            #val1=json.dumps({"Video": encoded_image})
            self.get_logger().info('Mensaje enviado')
            self.client.publish(self.tag1,encoded_image,qos=0)

                #time.sleep(2)
        except KeyboardInterrupt: #cuando presionas Ctrl +C
            print("Envío de datos detenido por el usuario")
            self.client.disconnect()
            self.client.loop_stop()
        #self.get_logger().info('Mensaje: "%s"' % self.dato)
           
def main(args=None):
    # initialize the ROS communication
    rclpy.init(args=args)
    # declare the node constructor
    listener = Listener()      
    # pause the program execution, waits for a request to kill the node (ctrl+c)
    rclpy.spin(listener)
    # Explicity destroy the node
    listener.destroy_node()
    # shutdown the ROS communication
    rclpy.shutdown()

if __name__ == '__main__':
    main()


