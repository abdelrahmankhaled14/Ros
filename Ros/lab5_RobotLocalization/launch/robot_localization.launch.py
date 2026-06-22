"""
Example Launch File: Static Transform Publisher

This launch file demonstrates how to publish static transforms in ROS 2.
Static transforms are fixed, non-changing coordinate frame relationships.

Example transforms published:
  - map -> odom: Maps the global map frame to odometry origin
  - odom -> base_link: Odometry frame to robot base
  - base_link -> camera_link: Robot base to camera sensor
  - base_link -> lidar_link: Robot base to lidar sensor

Author: ROS 2 Course
"""

from ament_index_python.packages import get_package_share_directory
import os



from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    """Generate launch description with static transform publishers."""
    
    config_path = os.path.join(
    get_package_share_directory('lab3_RobotLocalization'),
        'config',
        'ekf.yaml'
    )

    return LaunchDescription([
        # Transform 1: map -> odom
        # This establishes the relationship between the global map frame
        # and the odometry frame (usually the starting position of the robot)


        
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            arguments=[
                '--x', '0.0',      # Translation (meters)
                '--y', '0.0',
                '--z', '0.05',
                '--roll', '0.0',   # Rotation (radians)
                '--pitch', '0.0',
                '--yaw', '0.0',
                '--frame-id', 'base_footprint',
                '--child-frame-id', 'base_link'
            ],
            name='base_footprint_to_base_link_broadcaster'
        ),

        # Transform 2: odom -> base_link
        # Defines the relationship between odometry frame and robot base center.
        # In a real system, this would be published by the robot's odometry node
        # and would change over time. For this static example, we fix it.
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            arguments=[
                '--x', '0.5',
                '--y', '-0.1',
                '--z', '0.0',
                '--roll', '0.0',
                '--pitch', '0.0',
                '--yaw', '0.0',
                '--frame-id', 'base_link',
                '--child-frame-id', 'imu_link'
            ],
            name='base_link_to_imu_link_broadcaster'
        ),

        # Transform 3: base_link -> camera_link
        # Specifies where the camera is mounted relative to the robot base.
        # Example: Camera is mounted 10 cm forward and 30 cm above the base center
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            arguments=[
                '--x', '0.2',      # 10 cm forward (X)
                '--y', '0.0',      # Center (Y)
                '--z', '0.25',      # 30 cm up (Z)
                '--roll', '0.0',
                '--pitch', '0.0',  # Pointing straight ahead
                '--yaw', '0.0',
                '--frame-id', 'base_link',
                '--child-frame-id', 'gps_link'
            ],
            name='base_link_to_gps_link_broadcaster'
        ),

        # Transform 4: base_link -> lidar_link
        # Specifies where the LiDAR is mounted.
        # Example: LiDAR is on top, center, 25 cm above base center
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            arguments=[
                '--x', '0.5',      # Center (X)
                '--y', '0.15',      # Center (Y)
                '--z', '0.1',     # 25 cm up (Z)
                '--roll', '0.0',
                '--pitch', '0.0',
                '--yaw', '0.785',
                '--frame-id', 'base_link',
                '--child-frame-id', 'ultrasonic1_link'
            ],
            name='base_link_to_ultrasonic1_link_broadcaster'
        ),
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            arguments=[
                '--x', '0.5',      # Center (X)
                '--y', '0.0',      # Center (Y)
                '--z', '0.1',     # 25 cm up (Z)
                '--roll', '0.0',
                '--pitch', '0.0',
                '--yaw', '0.0',
                '--frame-id', 'base_link',
                '--child-frame-id', 'ultrasonic2_link'
            ],
            name='base_link_to_ultrasonic2_link_broadcaster'
        ),

        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            arguments=[
                '--x', '0.5',      # Center (X)
                '--y', '-0.15',      # Center (Y)
                '--z', '0.1',     # 25 cm up (Z)
                '--roll', '0.0',
                '--pitch', '0.0',
                '--yaw', '-0.785',
                '--frame-id', 'base_link',
                '--child-frame-id', 'ultrasonic3_link'
            ],
            name='base_link_to_ultrasonic3_link_broadcaster'
        ),

        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            arguments=[
                '--x', '-0.1',      # Center (X)
                '--y', '0.15',      # Center (Y)
                '--z', '0.1',     # 25 cm up (Z)
                '--roll', '0.0',
                '--pitch', '0.0',
                '--yaw', '2.357142857',
                '--frame-id', 'base_link',
                '--child-frame-id', 'ultrasonic4_link'
            ],
            name='base_link_to_ultrasonic4_link_broadcaster'
        ),
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            arguments=[
                '--x', '-0.1',      # Center (X)
                '--y', '0',      # Center (Y)
                '--z', '0.1',     # 25 cm up (Z)
                '--roll', '0.0',
                '--pitch', '0.0',
                '--yaw', '3.14',
                '--frame-id', 'base_link',
                '--child-frame-id', 'ultrasonic5_link'
            ],
            name='base_link_to_ultrasonic5_link_broadcaster'
        ),
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            arguments=[
                '--x', '-0.1',      # Center (X)
                '--y', '-0.15',      # Center (Y)
                '--z', '0.1',     # 25 cm up (Z)
                '--roll', '0.0',
                '--pitch', '0.0',
                '--yaw', '-2.357142857',
                '--frame-id', 'base_link',
                '--child-frame-id', 'ultrasonic6_link'
            ],
            name='base_link_to_ultrasonic6_link_broadcaster'
        ),
        Node(
            package='robot_localization',
            executable='ekf_node',
            name='ekf_filter_node',
            output='screen',
            parameters=[config_path],
            remappings=[
                ('odometry/filtered', '/odometry/local')
            ]
        )




    ])