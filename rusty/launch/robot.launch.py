# combined_launch.py
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
import time
import xacro
import os
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    
    robot_gazebo= IncludeLaunchDescription(
      PythonLaunchDescriptionSource([os.path.join(
         get_package_share_directory('rusty_description'), 'launch'),
         '/gazebo.launch.py'])
      )
    robot_rviz= IncludeLaunchDescription(
      PythonLaunchDescriptionSource([os.path.join(
         get_package_share_directory('rusty_description'), 'launch'),
         '/display.launch.py'])
      )
    return LaunchDescription([
        # Include the first launch file
        robot_gazebo,
        robot_rviz
    ])
