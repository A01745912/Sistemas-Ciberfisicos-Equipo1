import rclpy
import random
import numpy as np
# import the ROS2 python libraries
from rclpy.node import Node
#from std_msgs.msg import String
from custom_msgs.msg import Sensores

class Talker(Node):

    def __init__(self):
        # Here you have the class constructor
        # call the class constructor
        super().__init__('nodo_talker')
        # create the publisher object
        self.publisher= self.create_publisher(Sensores, 'data', 10)
        self.msg = Sensores()
        # define the timer period for 0.5 seconds
        self.timer_period = 0.5
        self.timer = self.create_timer(self.timer_period, self.motion)

    def motion(self):
        # print the data
        self.msg.coordenada.x = round(random.uniform(19.597,19.598),4)
        self.msg.coordenada.y = round(random.uniform(-99.227,-99.228),4)
        self.msg.coordenada.z = 0.0
        
        self.msg.posicion.position.x = 1.0
        self.msg.posicion.position.y = 1.0
        self.msg.posicion.position.z = 1.0
        self.msg.posicion.orientation.x = 1.0
        self.msg.posicion.orientation.y = 1.0
        self.msg.posicion.orientation.z = 1.0
        self.msg.posicion.orientation.w = 1.0
        
        self.msg.camara = round(random.uniform(50,100),1)
        
        self.msg.vel.linear.x = round(random.uniform(0,10),2)
        self.msg.vel.linear.y = 2.0
        self.msg.vel.linear.z = 2.0
        self.msg.vel.angular.x = 2.0
        self.msg.vel.angular.y = 2.0
        self.msg.vel.angular.z = round(random.uniform(-1,1),3)

        self.msg.conexion = True
        self.msg.bateria = round(random.uniform(0,1),1)
        self.msg.temperatura = round(random.uniform(25,35),2)
        self.msg.humedad = random.randint(40,80)
        
        self.msg.brazo.position.x = 3.0
        self.msg.brazo.position.y = 3.0
        self.msg.brazo.position.z = 3.0
        self.msg.brazo.orientation.x = 3.0
        self.msg.brazo.orientation.y = 3.0
        self.msg.brazo.orientation.z = 3.0
        self.msg.brazo.orientation.w = 3.0
        
        self.msg.status = "Hola Mundo"
        self.publisher.publish(self.msg)
        self.get_logger().info('Mensaje pub')
        
           
def main(args=None):
    # initialize the ROS communication
    rclpy.init(args=args)
    # declare the node constructor
    talker = Talker()      
    # pause the program execution, waits for a request to kill the node (ctrl+c)
    rclpy.spin(talker)
    # Explicity destroy the node
    talker.destroy_node()
    # shutdown the ROS communication
    rclpy.shutdown()

if __name__ == '__main__':
    main()


