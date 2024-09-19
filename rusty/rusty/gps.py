#! /usr/bin/python3

"""
$GPGGA,123313,4704.8062,N,01525.3878,E,1,09,1.1,359.7,M,43.7,M,,*4E
$GPGGA,HHMMSS.ss,AAAA.AAAA,la,OOOO.OOOO,lo,Q,NN,D.D,H.H,h,G.G,g,A.A,RRRR*CS

0	Message ID $GPGGA
1	HHMMSS.ss 	Time of position fix (UTC)
2	AAAA.AAAA 	Latitude degree and minutes (ddmm.mmmmmm)
3	la 	Direction of latitude (North or South)
4	OOOO.OOOO 	Longitude degree and minutes (dddmm.mmmmmm)
5	lo 	Direction of longitude (East or West)
6	Q 	GPS quality indicator:

    	0: no fix available
    	1: GPS fix
    	2: Differential GPS fix (DGPS)
      3: PPS fix
      4: Real Time Kinematic fix (RTK)
      5: Float RTK
    	6: Estimated (dead reckoning)
      7: Manual input mode
      8: simulation mode

7	NN 	Number of satellites in use (00 − 12)
8	D.D 	horizontale dilution of precision (meter)
9	H.H 	Antenna altitude (meter)
10	h 	Unit of antenna altitude (meter)
11	G.G 	geoidal separation the difference between the WGS-84 earth ellipsoid and mean-sea-level (geoid), "-" means mean-sea-level below ellipsoid
12	g 	Unit of geoidal separation (meter)
13	A.A 	Age of differential GPS data, time in seconds since last SC104 type 1 or 9 update, null field when DGPS is not used
14	RRRR 	Differential reference station ID (0000 to 1023)
15	CS 	Checksum
"""


import rclpy
from rclpy.node import Node
from std_msgs.msg import Header
from rusty_msgs.msg import GPSmsg 
import utm 
import time

def convert_to_decimal_degrees_latitude(degrees_minutes, direction):
    # Convert NMEA lat and longitude to decimal degrees
    if not degrees_minutes or len(degrees_minutes) < 4:
        return 0.0
    degrees = float(degrees_minutes[:2])
    minutes = float(degrees_minutes[2:])
    decimal_degrees = degrees+ (minutes / 60.0)
    if direction == 'S' or direction == 'W':
        decimal_degrees *= -1
    return decimal_degrees
  
def convert_to_decimal_degrees_longitude(degrees_minutes, direction):
    # Convert NMEA lat and longitude to decimal degrees
    if not degrees_minutes or len(degrees_minutes) < 4:
        return 0.0
    degrees = float(degrees_minutes[:3])
    minutes = float(degrees_minutes[3:])
    decimal_degrees = degrees+ (minutes / 60.0)
    if direction == 'S' or direction == 'W':
        decimal_degrees *= -1
    return decimal_degrees

def nmea_to_deg(lat_lon, orientation):
    if '.' in lat_lon:
        dot_index = lat_lon.index('.')
        deg = int(lat_lon[:dot_index-2])
        min = float(lat_lon[dot_index-2:])

        pos = deg + min / 60.0
        if orientation in ["W", "S"]:
            pos *= -1

        return f"{pos:.7f}"
    
    return ""
  
  
class GPSPublisher(Node):
    def __init__(self):
        super().__init__('gps_publisher')
        self.publisher_ = self.create_publisher(GPSmsg, 'gps_data', 10)
        self.timer = self.create_timer(1.0, self.publish_gps_data)
        self.gps_data = self.read_gps_data('/home/siddarth/ros2ws/src/Rusty/rusty/config/gps.txt')

    def read_gps_data(self, filename):
        with open(filename, 'r') as f:
            return f.readlines()

    def publish_gps_data(self):
        for line in self.gps_data:
            if line.startswith('$GPGGA'):
                gps_msg = GPSmsg()
                data = line.split(',')
                
                if len(data) < 15:  # Ensure there are enough data fields
                    self.get_logger().warn('Not enough data fields in GPS line.')
                    return
                
                latitude_str = data[2]
                latitude_dir = data[3]
                longitude_str = data[4]
                longitude_dir = data[5]
                altitude = float(data[9])
                
                # Convert latitude and longitude to decimal degrees
                latitude = convert_to_decimal_degrees_latitude(latitude_str, latitude_dir)
                longitude = convert_to_decimal_degrees_longitude(longitude_str, longitude_dir)
                
                
                # Convert latitude/longitude to UTM coordinates
                utm_data = utm.from_latlon(latitude, longitude)
                utm_easting = utm_data[0]
                utm_northing = utm_data[1]
                utm_zone = utm_data[2]
                utm_letter = utm_data[3]
                
                # Populate GPSmsg fields
                gps_msg.header = Header()
                gps_msg.header.stamp = self.get_clock().now().to_msg()
                gps_msg.header.frame_id = 'GPS1_Frame'
                
                gps_msg.latitude = latitude
                gps_msg.longitude = longitude
                gps_msg.altitude = altitude
                gps_msg.utm_easting = utm_easting
                gps_msg.utm_northing = utm_northing
                gps_msg.zone = utm_zone
                # gps_msg.letter = utm_letter  # Ensure this is a string
                
                self.publisher_.publish(gps_msg)
                self.get_logger().info(f'Published GPS data: {gps_msg}')
                time.sleep(1)

def main(args=None):
    rclpy.init(args=args)
    gps_publisher = GPSPublisher()
    rclpy.spin(gps_publisher)
    gps_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
