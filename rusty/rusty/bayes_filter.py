#!/usr/bin/python3
import rclpy
from std_msgs.msg import Float64MultiArray
from sensor_msgs.msg import LaserScan, Odometry
from geometry_msgs.msg import Pose
from tf_transformations import euler_from_quaternion
from rusty_msgs.msg import Bayes
import numpy as np
from Robotics_concepts.Localization import BayesFilter  
from rclpy import Node

class Localization(Node):
    def __init__(self):
        super().__init__('bayes_filter_node')

        
        self.laser_measurement = self.create_subscription(LaserScan, '/scan', self.scanner, 10)
        self.odom_measurement = self.create_subscription(Odometry, '/odom', self.odom_callback, 10)

       
        self.posterior_publisher = self.create_publisher(Bayes, '/filter', 10)

        self.timer = self.create_timer(1, self.bayes_pub)

        # Initial sensor and motion measurements
        self.scan_measurement = 0.0
        self.control_motion = 0.0

       
        self.state_space = np.linspace(-5, 5, 100) 
        self.prior_belief = np.ones_like(self.state_space) / len(self.state_space) 

        # Create an instance of the BayesFilter class
        self.bayes_filter = BayesFilter(
            state_space=self.state_space,
            control_motion=self.control_motion,
            motion_noise=0.1,  # Example noise
            sensor_measurement=self.scan_measurement,
            measurement_noise=0.1  # Example noise
        )

        self.get_logger().info("BAYES FILTER ON RUSTY INITIALIZED")

    def scanner(self, scan_data):
        
        self.scan_measurement = np.min(scan_data.ranges)
        self.bayes_filter.sensor_measurement = self.scan_measurement
        self.get_logger().info(f"LASER SCAN RECEIVED: {self.scan_measurement}")

    def odom_callback(self, odom_data):
        
        pose = odom_data.pose.pose
        quaternion = pose.orientation
        eul_to_q = [quaternion.x, quaternion.y, quaternion.z, quaternion.w]
        roll, pitch, yaw = euler_from_quaternion(eul_to_q)

        self.control_motion = yaw  # Using yaw as the control input
        self.bayes_filter.control_motion = self.control_motion
        self.get_logger().info(f"ODOMETRY UPDATE: Position ({pose.position.x}, {pose.position.y}), Yaw: {yaw}")

    def bayes_pub(self):
        """Method to publish the updated belief using the Bayes filter."""
       
        new_belief = self.bayes_filter.bayes_filter(self.prior_belief)
        self.prior_belief = new_belief

        
        bayes_msg = Bayes()
        bayes_msg.belief = Float64MultiArray(data=new_belief.tolist())
        self.posterior_publisher.publish(bayes_msg)

        self.get_logger().info("Published updated belief.")

def main(args=None):
    rclpy.init(args=args)
    node = Localization()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
