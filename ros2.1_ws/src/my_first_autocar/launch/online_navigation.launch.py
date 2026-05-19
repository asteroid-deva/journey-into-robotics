import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node

def generate_launch_description():
    pkg_name = 'my_first_autocar'
    
    urdf_path = os.path.join(get_package_share_directory(pkg_name), 'urdf', 'my_car.urdf')
    
    # We are still using YOUR custom shrunk robot parameters!
    params_path = os.path.join(get_package_share_directory(pkg_name), 'params', 'nav2_params.yaml')

    with open(urdf_path, 'r') as infp:
        robot_desc = infp.read()

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('gazebo_ros'), 'launch', 'gazebo.launch.py')]),
    )

    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{'robot_description': robot_desc, 'use_sim_time': True}]
    )

    spawn_entity = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=['-topic', 'robot_description', '-entity', 'my_car', '-z', '0.5'],
        output='screen'
    )

    # The Mathematical Duct Tape
    tf_footprint_to_link = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        name='static_transform_publisher',
        arguments=['0', '0', '0', '0', '0', '0', 'base_link', 'base_footprint'],
        output='screen'
    )

    # 1. THE MAPPER: SLAM Toolbox running live
    slam_config_path = os.path.join(get_package_share_directory('slam_toolbox'), 'config', 'mapper_params_online_async.yaml')
    slam_toolbox = Node(
        package='slam_toolbox',
        executable='async_slam_toolbox_node',
        name='slam_toolbox',
        output='screen',
        parameters=[
            slam_config_path, 
            {
                'use_sim_time': True,
                'odom_frame': 'odom',
                'base_frame': 'base_link',
                'map_frame': 'map',
                'scan_topic': '/scan'
            }
        ]
    )

    # 2. THE DRIVER: Nav2 Planners ONLY (Notice we use 'navigation_launch.py', not 'bringup_launch.py')
    # This specifically tells Nav2 NOT to look for a saved map!
    nav2_planners = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('nav2_bringup'), 'launch', 'navigation_launch.py')]),
        launch_arguments={
            'use_sim_time': 'true',
            'params_file': params_path
        }.items()
    )

    return LaunchDescription([
        gazebo,
        robot_state_publisher,
        spawn_entity,
        tf_footprint_to_link,
        slam_toolbox,
        nav2_planners
    ])
