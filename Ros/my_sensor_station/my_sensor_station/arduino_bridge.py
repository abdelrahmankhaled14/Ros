import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Range
from std_msgs.msg import Float32
import serial


class ArduinoBridge(Node):
    def __init__(self):
        super().__init__('arduino_bridge')

        self.ultrasonic_pub = self.create_publisher(Range, '/ultrasonic', 10)
        self.pot_pub = self.create_publisher(Float32, '/pot_threshold', 10)

        self.declare_parameter('serial_port', '/dev/ttyACM0')
        self.declare_parameter('baud_rate', 115200)

        port = self.get_parameter('serial_port').value
        baud = self.get_parameter('baud_rate').value

        try:
            self.ser = serial.Serial(port, baud, timeout=0.05)
            self.get_logger().info(f'Connected to Arduino on {port} @ {baud}')
        except serial.SerialException as e:
            self.get_logger().fatal(f'Failed to open serial: {e}')
            raise

        self.timer = self.create_timer(0.05, self.read_serial)

    def read_serial(self):
        try:
            while self.ser.in_waiting > 0:
                line = self.ser.readline().decode('utf-8', errors='ignore').strip()
                if not (line.startswith('U:') and ',P:' in line):
                    continue

                parts = line.split(',')
                u_val = float(parts[0].split(':')[1])
                p_val = float(parts[1].split(':')[1])

                # Publish /ultrasonic (sensor_msgs/Range)
                range_msg = Range()
                range_msg.header.stamp = self.get_clock().now().to_msg()
                range_msg.header.frame_id = 'ultrasonic_link'
                range_msg.radiation_type = Range.ULTRASOUND
                range_msg.field_of_view = 0.5
                range_msg.min_range = 0.02
                range_msg.max_range = 4.0
                range_msg.range = float(u_val)
                self.ultrasonic_pub.publish(range_msg)

                # Publish /pot_threshold (std_msgs/Float32)
                self.pot_pub.publish(Float32(data=float(p_val)))

        except Exception as e:
            self.get_logger().warn(f'Serial parse error: {e}')


def main(args=None):
    rclpy.init(args=args)
    node = ArduinoBridge()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()