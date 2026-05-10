import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32
import random
class DistancePublisher(Node):
    def __init__(self):
        super().__init__('distance_publisher')
        self.publisher_ = self.create_publisher(Float32, 'distance', 10)
        timer_period = 1  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

    def timer_callback(self):
        msg = Float32()
        msg.data = random.uniform(0.0, 5.0)  # Simulated distance value
        self.publisher_.publish(msg)
        self.get_logger().info(f'Publishing: {msg.data:.2f} m')
        self.i += 1
def main(args=None):
    rclpy.init(args=args)
    distancepublisher = DistancePublisher()
    rclpy.spin(distancepublisher)
    distancepublisher.destroy_node()
    rclpy.shutdown()
if __name__ == '__main__':    main()        

