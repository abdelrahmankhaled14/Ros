from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    # Launch argument: alert_threshold
    alert_threshold_arg = DeclareLaunchArgument(
        'alert_threshold',
        default_value='0.8',
        description='Default alert threshold in meters (overridden by potentiometer)'
    )

    # 1. RPLIDAR A1 node
    rplidar_node = Node(
        package='rplidar_ros',
        executable='rplidar_node',
        name='rplidar_node',
        parameters=[{
            'serial_port': '/dev/ttyUSB0',
            'serial_baudrate': 115200,
            'frame_id': 'laser',
            'inverted': False,
            'angle_compensate': True,
        }],
        output='screen'
    )

    # 2. Static TF: ultrasonic_link -> laser (co-located sensors)
    static_tf = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        arguments=['0', '0', '0', '0', '0', '0', 'laser', 'ultrasonic_link'],
        output='screen'
    )

    # 3. Arduino bridge
    arduino_bridge = Node(
        package='my_sensor_station',
        executable='arduino_bridge',
        name='arduino_bridge',
        parameters=[{
            'serial_port': '/dev/ttyACM0',
            'baud_rate': 115200,
        }],
        output='screen'
    )

    # 4. Monitor / fusion node
    monitor_node = Node(
        package='my_sensor_station',
        executable='monitor_node',
        name='monitor_node',
        parameters=[{
            'alert_threshold': LaunchConfiguration('alert_threshold')
        }],
        output='screen'
    )

    return LaunchDescription([
        alert_threshold_arg,
        rplidar_node,
        static_tf,
        arduino_bridge,
        monitor_node,
    ])  