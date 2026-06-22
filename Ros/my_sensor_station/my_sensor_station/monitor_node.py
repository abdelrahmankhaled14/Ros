import rclpy
from rclpy.node import Node
from rclpy.parameter import Parameter
from sensor_msgs.msg import LaserScan, Range
from std_msgs.msg import Float32, Bool
import math


class MonitorNode(Node):
    def __init__(self):
        super().__init__('monitor_node')

        # Parameter: default alert threshold
        self.declare_parameter('alert_threshold', 0.8)
        self.alert_threshold = self.get_parameter('alert_threshold').value

        # Internal state
        self.laser_min = float('inf')
        self.laser_mean = float('inf')
        self.laser_max = float('inf')
        self.ultrasonic_range = float('inf')

        # Subscribers
        self.create_subscription(LaserScan, '/scan', self.scan_callback, 10)
        self.create_subscription(Range, '/ultrasonic', self.ultrasonic_callback, 10)
        self.create_subscription(Float32, '/pot_threshold', self.pot_callback, 10)

        # Publishers
        self.min_dist_pub = self.create_publisher(Float32, '/min_distance', 10)
        self.alert_pub = self.create_publisher(Bool, '/alert', 10)

        # Timer: publish fused outputs at 10 Hz
        self.create_timer(0.1, self.timer_callback)

        self.get_logger().info(
            f'Monitor node started. Initial threshold: {self.alert_threshold:.2f} m'
        )

    def scan_callback(self, msg: LaserScan):
        """Basic statistics on LaserScan (min, mean, max)."""
        valid = [
            r for r in msg.ranges
            if not (math.isnan(r) or math.isinf(r)) and msg.range_min <= r <= msg.range_max
        ]

        if valid:
            self.laser_min = min(valid)
            self.laser_mean = sum(valid) / len(valid)
            self.laser_max = max(valid)
        else:
            self.laser_min = float('inf')
            self.laser_mean = float('inf')
            self.laser_max = float('inf')

    def ultrasonic_callback(self, msg: Range):
        if msg.min_range <= msg.range <= msg.max_range:
            self.ultrasonic_range = msg.range
        else:
            self.ultrasonic_range = float('inf')

    def pot_callback(self, msg: Float32):
        """Live update from potentiometer; sync to ROS parameter."""
        self.alert_threshold = msg.data
        self.set_parameters([
            Parameter('alert_threshold', Parameter.Type.DOUBLE, float(msg.data))
        ])
        self.get_logger().debug(f'Threshold updated: {self.alert_threshold:.2f} m')

    def timer_callback(self):
        # Use large placeholder if no data yet
        laser = self.laser_min if self.laser_min != float('inf') else 999.0
        ultra = self.ultrasonic_range if self.ultrasonic_range != float('inf') else 999.0

        min_dist = min(laser, ultra)

        # Publish /min_distance
        self.min_dist_pub.publish(Float32(data=float(min_dist)))

        # Publish /alert
        is_alert = min_dist < self.alert_threshold
        self.alert_pub.publish(Bool(data=is_alert))


def main(args=None):
    rclpy.init(args=args)
    node = MonitorNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()