import rclpy
from rusty_msgs.msg import GPSmsg
from rclpy.node import Node
import numpy as np
import matplotlib.pyplot as plt

class KalmanFilter():
    def __init__(self, state_space, measurement, dt, control=0):
        self.X = np.zeros((state_space, 1))  # State vector (initial) (4x1)
        self.P = np.eye(state_space)  # Covariance Matrix

        # State transition Matrix
        self.A = np.eye(state_space)
        for i in range(state_space // 2):
            self.A[i, i + state_space // 2] = dt

        # Control matrix
        self.B = np.zeros((state_space, control))

        # Measurement Matrix (H)
        self.H = np.zeros((measurement, state_space))
        for i in range(measurement):
            self.H[i, i] = 1

        # Process Noise covariance (Q)
        self.Q = np.diag([0.01, 0.01, 0.01, 0.01])

        # Measurement noise covariance (R)
        self.R = np.eye(measurement) * 0.005

        # Identity matrix
        self.I = np.eye(state_space)

    def predict(self, U=np.zeros((1, 1))):
        # Finding State and covariance (predicted)
        self.X = np.dot(self.A, self.X)
        self.P = np.dot(np.dot(self.A, self.P), self.A.T) + self.Q

        return self.X

    def update(self, Z):
        # Calculate kalman gain (K_k)
        Y = Z - np.dot(self.H, self.X)
        S = np.dot(np.dot(self.H, self.P), self.H.T) + self.R
        K = np.dot(np.dot(self.P, self.H.T), np.linalg.inv(S))

        self.X = self.X + np.dot(K, Y)
        self.P = np.dot(self.I - np.dot(K, self.H), self.P)

        return self.X


class GPSRectifier(Node):
    def __init__(self):
        super().__init__('gps_rectifier')
        
       
        self.subscription = self.create_subscription(GPSmsg, 'gps_data', self.gps_callback, 10)

        self.pub = self.create_publisher(GPSmsg, 'updated_state', 10)

        self.filtered_pub = self.create_publisher(GPSmsg, 'kalman_filtered_data', 10)

       
        self.kalman = KalmanFilter(4, 2, 0.1)

    
        self.unfiltered_easting = []
        self.unfiltered_northing = []
        self.filtered_easting = []
        self.filtered_northing = []

    def gps_callback(self, msg):
      
        latitude = msg.latitude
        longitude = msg.longitude
        altitude = msg.altitude
        utm_easting = msg.utm_easting
        utm_northing = msg.utm_northing
        zone = msg.zone

       
        self.unfiltered_easting.append(utm_easting)
        self.unfiltered_northing.append(utm_northing)

       
        measurement = np.array([[utm_easting], [utm_northing]])
        self.get_logger().info(f"Received Measurement: {measurement}")

       
        self.kalman.predict()
        X = self.kalman.update(measurement)
        self.get_logger().info(f"Updated State from Kalman Filter: {X}")

       
        kalman_msg = GPSmsg()
        kalman_msg.latitude = latitude
        kalman_msg.longitude = longitude
        kalman_msg.altitude = altitude
        kalman_msg.utm_easting = float(X[0])
        kalman_msg.utm_northing = float(X[1])
        kalman_msg.zone = zone

        
        self.filtered_easting.append(float(X[0]))
        self.filtered_northing.append(float(X[1]))

        self.filtered_pub.publish(kalman_msg)
        self.get_logger().info('Published Kalman Filtered GPS data.')

       
        if len(self.unfiltered_easting) % 10 == 0: 
            self.plot_data()

    def plot_data(self):
        plt.figure(figsize=(10, 5))

        # Plot UTM easting
        plt.subplot(1, 2, 1)
        plt.plot(self.unfiltered_easting, label='Unfiltered UTM Easting', color='blue')
        plt.plot(self.filtered_easting, label='Kalman Filtered UTM Easting', color='red')
        plt.title('UTM Easting')
        plt.xlabel('time')
        plt.ylabel('Easting (m)')
        plt.legend()
        plt.grid()

        # Plot UTM northing
        plt.subplot(1, 2, 2)
        plt.plot(self.unfiltered_northing, label='Unfiltered UTM Northing', color='blue')
        plt.plot(self.filtered_northing, label='Kalman Filtered UTM Northing', color='red')
        plt.title('UTM Northing')
        plt.xlabel('time')
        plt.ylabel('Northing (m)')
        plt.legend()
        plt.grid()

        plt.tight_layout()
        plt.show()

def main():
    rclpy.init()
    gps_rectifier = GPSRectifier()
    rclpy.spin(gps_rectifier)
    gps_rectifier.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
