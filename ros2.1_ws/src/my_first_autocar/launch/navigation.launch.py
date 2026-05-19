import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node

def generate_launch_description():
    pkg_name = 'my_first_autocar'
    
    urdf_path = os.path.join(get_package_share_directory(pkg_name), 'urdf', 'my_car.urdf')
    map_path = os.path.join(get_package_share_directory(pkg_name), 'maps', 'my_world_map.yaml')
    params_path = os.path.join(get_package_share_directory('nav2_bringup'), 'params', 'nav2_params.yaml')

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

    # FIX: The "Mathematical Duct Tape" to satisfy Nav2's hardcoded base_footprint!
    tf_footprint_to_link = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        name='static_transform_publisher',
        # Translates: X=0, Y=0, Z=0, Yaw=0, Pitch=0, Roll=0 from base_link to base_footprint
        arguments=['0', '0', '0', '0', '0', '0', 'base_link', 'base_footprint'],
        output='screen'
    )

    nav2 = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('nav2_bringup'), 'launch', 'bringup_launch.py')]),
        launch_arguments={
            'map': map_path,
            'use_sim_time': 'true',
            'params_file': params_path
        }.items()
    )

    return LaunchDescription([
        gazebo,
        robot_state_publisher,
        spawn_entity,
        tf_footprint_to_link,  # Inserted the duct tape here!
        nav2
    ])
