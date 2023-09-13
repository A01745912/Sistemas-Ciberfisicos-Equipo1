import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Point
from geometry_msgs.msg import Twist
import json

class jsonros(Node):
    def __init__(self):
        super().__init__('pub_json')
        #self.publisher = self.create_publisher(Point, 'data_rover', 10)
        self.publisher = self.create_publisher(Twist, 'cmd_vel', 10)
        self.timer_period = 1
        self.dato = Twist()
        self.timer = self.create_timer(self.timer_period, self.motion)
        self.json_file = 'data.json'

    def motion(self):
        with open(self.json_file, 'r') as json_file:
            jsonD = json.load(json_file)
        self.dato.linear.x = float(jsonD['PosicionX']) #La funcion get toma el valor de key
        self.dato.angular.z = float(jsonD['PosicionY'])
        #self.dato.z = 0.0

        self.publisher.publish(self.dato)
        self.get_logger().info(f'Publicando dato JSON en ROS')

def main(args=None):
    # initialize the ROS communication
    rclpy.init(args=args)
    # declare the node constructor
    talker = jsonros()      
    # pause the program execution, waits for a request to kill the node (ctrl+c)
    rclpy.spin(talker)
    # Explicity destroy the node
    talker.destroy_node()
    # shutdown the ROS communication
    rclpy.shutdown()

if __name__ == '__main__':
    main()
