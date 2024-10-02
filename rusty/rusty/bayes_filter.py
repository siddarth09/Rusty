#! /usr/bin/python3
import rclpy 
from std_msgs.msg import Float64MultiArray
from Robotics_concepts.Localization import Bayes_filter
from rclpy import Node 
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Pose
from tf_transformations import euler_from_quaternion
from rusty_msgs.msg import Bayes
import numpy as np

class localization(Node):
    def __init__(self):
        super.__init__('bayes_filter_node')
        self.laser_measurement=self.create_subscription(LaserScan,'/scan',10,self.scanner)
        self.odom_measurement=self.create_subscription(Odometry,'/odom',10,self.odom_callback)
        
        self.posterior_publisher=self.create_publisher(Bayes,'/filter',10)
        self.timer=self.create_timer(1,self.bayes_pub)
        
        self.scan_measurement=0.0
        self.control_motion=0.0
        
        self.get_logger().info("BAYES FILTER ON RUSTY INITIALIZED")
        
    def scanner(self,scan_data):
        self.scan_measurement=np.min(scan_data.ranges)
        self.get_logger().info(f"LASER INITIALIZED = {self.scan_measurement}")
        
    def odom_callback(self,odom_data):
        pose=odom_data.pose.pose
        quaternion=pose.orientation
        eul_to_q= [quaternion.x,quaternion.y,quaternion.z,quaternion.w]
        roll,pitch,yaw=euler_from_quaternion(eul_to_q)
        
        self.control_motion=yaw
        self.get_logger().info(f"Odometry Update: Position ({pose.position.x}, {pose.position.y}), Yaw: {yaw}")
        
        
    def bayes_pub(self):
        
        
    