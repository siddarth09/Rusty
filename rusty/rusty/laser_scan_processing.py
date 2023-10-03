import rclpy 
from sensor_msgs.msg import LaserScan
from rclpy import Node 
import math 

class Scanner(Node):
    def __init__(self, topicName = "/scan"):
        super().__init__("scanner")
        self.laser_sub=self.create_subscription(LaserScan,topicName,self.laser_cb)
        self.angle_min=0.0
        self.angle_max=math.degrees(1.57)
        self.range_of_value=list()
        self.range_min=0.0
        self.range_max=12.0
        
    def laser_cb(self,msg):
        self.angle_max=msg.angle_max
        self.angle_min=msg.angle_min
        for i in range(len(msg.range)):
            self.range_of_value[i]=msg.range[i]
            
