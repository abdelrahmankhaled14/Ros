# launch/topic_examples.launch.py
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='liner_velocity',
            executable='liner_velocity',
            name='velocity',
            output='screen',
        ),
        Node(
            package='teleop_twist_keyboard',
            executable='teleop_twist_keyboard',
            name='keyboard',
            output='screen',
        ),
    ])