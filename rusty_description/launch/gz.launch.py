import os
from launch import LaunchDescription
from launch.actions import SetEnvironmentVariable, DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from ament_index_python.packages import get_package_share_directory
from launch_ros.actions import Node

def generate_launch_description():
    pkg_share = get_package_share_directory('rusty_description')
    ros_gz_sim = get_package_share_directory('ros_gz_sim')
    default_model_path = os.path.join(pkg_share, 'urdf', 'rusty.urdf')  # Ensure this is a .urdf file
    world_path = os.path.join(
        get_package_share_directory('rusty_description'),
        'worlds',
        'empty_world.world'
    )
    x_pose = LaunchConfiguration('x_pose', default='0.0')
    y_pose = LaunchConfiguration('y_pose', default='0.0')

    use_sim_time = LaunchConfiguration('use_sim_time', default='true')

    # Ensure the right Ignition version is being used (Harmonic)
    set_ign_version_cmd = SetEnvironmentVariable('IGN_GAZEBO_VERSION', 'harmonic')

    # Gazebo server (simulation) launch command
    gzserver_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(ros_gz_sim, 'launch', 'gz_sim.launch.py')
        ),
        launch_arguments={
            'gz_args': f'-r -s -v4 {world_path}', 
            'on_exit_shutdown': 'true'
        }.items()
    )

    # Gazebo client (GUI) launch command
    gzclient_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(ros_gz_sim, 'launch', 'gz_sim.launch.py')
        ),
        launch_arguments={'gz_args': '-g -v4'}.items()
    )

    # Node to publish the robot state (robot_state_publisher)
    robot_state_publisher_node = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_share +'/launch/', 'robot_state_publisher.launch.py')
        ),
        launch_arguments={'use_sim_time': use_sim_time}.items()
    )

    # Node to spawn the robot in Ignition Gazebo
    spawn_robot_node = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_share +'/launch/', 'spawn_rusty.launch.py')
        ),
        launch_arguments={
            'x_pose': x_pose,
            'y_pose': y_pose
        }.items()
    )

    bridge_params = os.path.join(
    get_package_share_directory('rusty_description'),
    'config',
    'gz_params.yaml'
    )

    start_gazebo_ros_bridge_cmd = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=[
            '--ros-args',
            '-p',
            f'config_file:={bridge_params}',
        ],
        output='screen',
    )

    start_gazebo_ros_image_bridge_cmd = Node(
    package='ros_gz_image',
    executable='image_bridge',
    arguments=['/camera/image_raw'],
    output='screen',
)
    # Time synchronization between ROS 2 and Ignition
    clock_bridge_node = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        name='clock_bridge',
        output='screen',
        arguments=['/clock@rosgraph_msgs/msg/Clock@gz.msgs.Clock'],
        remappings=[('/world/default/clock', '/clock')]  # Synchronize clocks
    )

    # Launch description
    ld = LaunchDescription()

    # Add actions to the launch description
    ld.add_action(set_ign_version_cmd)        # Set the correct Ignition version
    ld.add_action(gzserver_cmd)               # Start the Gazebo server
    ld.add_action(gzclient_cmd)               # Start the Gazebo client
    ld.add_action(robot_state_publisher_node) # Start the robot state publisher
    ld.add_action(spawn_robot_node)           # Spawn the robot in Gazebo
    ld.add_action(clock_bridge_node)          # Start the clock synchronization
    ld.add_action(start_gazebo_ros_bridge_cmd)
    ld.add_action(start_gazebo_ros_image_bridge_cmd)

    return ld
