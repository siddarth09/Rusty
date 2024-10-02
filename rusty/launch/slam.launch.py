from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='slam_toolbox',
            executable='online_async_node',
            output='screen',
            parameters=[{'slam_params_file': '/home/siddarth/ros2ws/src/Rusty/rusty/config/slam_params.yaml'},
                        {'use_sim_time': True}]
        )
    ])
