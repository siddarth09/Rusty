import numpy as np
import matplotlib.pyplot as plt

import rclpy 
from rclpy.node import Node 
from rusty_msgs.msg import VnHundred
from rusty_msgs.msg import GPSmsg

import numpy as np

class ExtendedKF():
    def __init__(self, state_dim, measurement_dim, control_dim, dt):
        self.X = np.zeros((state_dim, 1))  # State vector (px, py, vx, vy)
        self.P = np.eye(state_dim)  # Covariance matrix
        self.Q = np.eye(state_dim) * 0.1  # Process noise covariance
        self.R = np.eye(measurement_dim) * 0.5  # Measurement noise covariance
        self.I = np.eye(state_dim)  # Identity matrix
        self.dt = dt  # Time step

    def g(self, X, U):
        # Motion model: state transition with control input
        px, py, vx, vy = X.flatten()
        ax, ay = U.flatten()  # Control input (acceleration in x and y)
        
        # State prediction with velocity and acceleration
        return np.array([[px + vx * self.dt],
                         [py + vy * self.dt],
                         [vx + ax * self.dt],
                         [vy + ay * self.dt]])

    def h(self, X):
        # Measurement model: only position is measured
        px, py = X[0, 0], X[1, 0]
        return np.array([[px],
                         [py]])

    def jacobian_G(self):
        # Jacobian of the motion model (g) with respect to the state
        return np.array([[1, 0, self.dt, 0],
                         [0, 1, 0, self.dt],
                         [0, 0, 1, 0],
                         [0, 0, 0, 1]])

    def jacobian_H(self):
        # Jacobian of the measurement model (h) with respect to the state
        return np.array([[1, 0, 0, 0],
                         [0, 1, 0, 0]])

    def predict(self, U):
        G = self.jacobian_G()  # Get the Jacobian of the motion model
        self.X = self.g(self.X, U)  # Predict the new state
        self.P = np.dot(np.dot(G, self.P), G.T) + self.Q  # Update the covariance
        return self.X

    def update(self, Z):
        # Measurement update using the predicted state
        H = self.jacobian_H()  # Get the Jacobian of the measurement model
        y = Z - self.h(self.X)  # Measurement residual (innovation)
        S = np.dot(np.dot(H, self.P), H.T) + self.R  # Innovation covariance
        K = np.dot(np.dot(self.P, H.T), np.linalg.inv(S))  # Kalman gain
        
        self.X = self.X + np.dot(K, y)  # Update state estimate
        self.P = np.dot(self.I - np.dot(K, H), self.P)  # Update the covariance
        return self.X


class GPSRectifier(Node):
    def __init__(self):
        super().__init__('gps_rectifier')
        
       
        self.subscription = self.create_subscription(GPSmsg, 'gps_data', self.gps_callback, 10)

        self.pub = self.create_publisher(GPSmsg, 'updated_state', 10)

        self.filtered_pub = self.create_publisher(GPSmsg, 'kalman_filtered_data', 10)

       
        self.ekf=ExtendedKF(4,2,2,0.1)

    
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

        U=np.array([[0],[0]])
        self.ekf.predict(U)
        X = self.ekf.update(measurement)
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
        self.get_logger().info('Published EKF GPS data.')

       
        if len(self.unfiltered_easting) % 10 == 0: 
            self.plot_data()

    def plot_data(self):
        plt.figure(figsize=(10, 5))

        # Plot UTM easting
        plt.subplot(1, 2, 1)
        plt.plot(self.unfiltered_easting, label='Unfiltered UTM Easting', color='blue')
        plt.plot(self.filtered_easting, label='EKF UTM Easting', color='red')
        plt.title('UTM Easting')
        plt.xlabel('time')
        plt.ylabel('Easting (m)')
        plt.legend()
        plt.grid()

        # Plot UTM northing
        plt.subplot(1, 2, 2)
        plt.plot(self.unfiltered_northing, label='Unfiltered UTM Northing', color='blue')
        plt.plot(self.filtered_northing, label='EKF UTM Northing', color='red')
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
    
if __name__ == '__main__':
    main()