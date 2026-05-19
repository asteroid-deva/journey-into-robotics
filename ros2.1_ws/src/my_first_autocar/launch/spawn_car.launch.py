import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node

def generate_launch_description():
    pkg_name = 'my_first_autocar'
    
    urdf_path = os.path.join(
        get_package_share_directory(pkg_name),
        'urdf',
        'my_car.urdf'
    )
    
    with open(urdf_path, 'r') as infp:
        robot_desc = infp.read()

    slam_config_path = os.path.join(
        get_package_share_directory('slam_toolbox'),
        'config',
        'mapper_params_online_async.yaml'
    )

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

    # Spawns car from 0.5 meters in the air to prevent clipping
    spawn_entity = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=['-topic', 'robot_description', '-entity', 'my_car', '-z', '0.5'],
        output='screen'
    )

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
                'base_frame': 'base_link',  # REVERTED TO BASE_LINK
                'map_frame': 'map',
                'scan_topic': '/scan'
            }
        ]
    )

    return LaunchDescription([
        gazebo,
        robot_state_publisher,
        spawn_entity,
        slam_toolbox
    ])
