from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        # GPS node
        Node(
            package='rusty',  
            executable='gps_node', 
            name='gps_driver',
            output='screen'
        ),
        
      
        Node(
            package="tf2_ros",  
            executable="static_transform_publisher",
            name="static_transform_publisher",
            arguments=["0", "0", "4", "0", "0", "0", "base_link", "gps"],  
            output="screen"
        )
    ])
