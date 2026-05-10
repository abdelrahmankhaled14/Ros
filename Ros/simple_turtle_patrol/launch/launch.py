import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    pkg_name = 'simple_turtle_patrol'
    
    # Path to YAML file
    config_file = os.path.join(
        get_package_share_directory(pkg_name),
        'params',
        'patrol_params.yaml'
    )

    turtlesim_node = Node(
        package='turtlesim',
        executable='turtlesim_node',
        name='turtlesim'
    )

    patrol_controller_node = Node(
        package=pkg_name,
        executable='patrol_controller',
        name='patrol_controller',
        parameters=[config_file]
    )

    status_publisher_node = Node(
        package=pkg_name,
        executable='status_publisher',
        name='status_publisher',
        parameters=[config_file]
    )

    return LaunchDescription([
        turtlesim_node,
        patrol_controller_node,
        status_publisher_node
    ])