import rclpy
from rusty_msgs.msg import GPSmsg
from rclpy.node import Node 

import math 
import numpy as np
import matplotlib as plt



class KalmanFilter():
    def __init__(self,state_space, measurement, dt, control=0):
        self.X = np.zeros((state_space,1)) #State vector (initial) (4x1)
        #print(f"state \n {self.X}")
        self.P = np.eye(state_space) #Covariance Matrix
        
        #print(f"Covariance matrix of state \n {self.P}")

        #State transition Matrix 
        self.A = np.eye(state_space)
        for i in range (state_space//2):
            self.A[i,i+state_space//2]=dt
        #print(f"Transition state matrix \n {self.A}")

        #Control matrix 
        self.B = np.zeros((state_space,control))
        #print(f"Control matrix \n {self.B}")

        #Measurement Matrix (H)
        self.H = np.zeros((measurement,state_space))
        for i in range (measurement):
            self.H[i,i]=1
            
        #print(f"Measurement matrix \n {self.H}")

        #Process Noise covar (Q)

        self.Q=np.diag([0.01,0.01,0.01,0.01])

        self.R=np.eye(measurement)*0.005

        #Identity
        self.I= np.eye(state_space)


    def predict(self,U=np.zeros((1,1))):
            
            # Finding State and covariance (predicted)
            self.X = np.dot(self.A,self.X)
            self.P = np.dot(np.dot(self.A,self.P),self.A.T) + self.Q

            return self.X
        
    def update(self,Z):
            
            #Calculate kalman gain (K_k)
            Y=Z- np.dot (self.H,self.X)
            S=np.dot(np.dot(self.H,self.P),np.matrix.transpose(self.H))+self.R
            K = np.dot(np.dot(self.P,np.matrix.transpose(self.H)),np.linalg.inv(S))

            self.X=self.X+ np.dot(K,Y)
            self.P=np.dot(self.I-np.dot(K,self.H),self.P)

            return self.X


class GPS_Rectifier(Node):
    def __init__(self):
        super().__init__('gps_rectifier')
        self.subscription = self.create_subscription(GPSmsg, 'gps_data', self.gps_callback, 10)
        self.measurement=0.0
        
    def gps_callback(self, msg):
        #self.get_logger().info(f'Received GPS data: {msg}')
        
       
        latitude = msg.latitude
        longitude = msg.longitude
        altitude = msg.altitude
        utm_easting = msg.utm_easting
        utm_northing = msg.utm_northing
        zone = msg.zone
        # rectified_msg.letter = msg.letter  # Ensure this is a string
        self.measurement=np.array([[utm_easting],[utm_northing]])
        self.get_logger().info(f"Measurement {self.measurement}")
        
        kalman=KalmanFilter(4,2,0.1)
        kalman.predict()
        self.get_logger().info("Prediction done")
        X=kalman.update(self.measurement)
        self.get_logger().info(f"Updated states {X}")
        
        
        
def main():
    rclpy.init()
    gps_rectifier = GPS_Rectifier()
    rclpy.spin(gps_rectifier)
    gps_rectifier.destroy_node()
    rclpy.shutdown()
        
        







if __name__=="__main__":
    main()