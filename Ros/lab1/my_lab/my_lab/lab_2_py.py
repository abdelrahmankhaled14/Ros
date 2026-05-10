import rclpy
from rclpy.node import Node

from std_msgs.msg import Float32
from std_msgs.msg import Bool

class Subscriber(Node):

    def __init__(self):
        super().__init__('subscriber')
        self.subscription = self.create_subscription(
            Float32,
            'distance',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning
        self.publisher_ = self.create_publisher(
            Bool, '/cmd/stop', 10)

    def listener_callback(self, msg):
        if(msg.data < 1.0):
            # Publish a boolean message to the /cmd/stop topic
            stop_msg = Bool()
            stop_msg.data = True
            self.publisher_.publish(stop_msg)
        else:
            self.get_logger().info(f'Received distance: {msg.data:.2f} m')

def main(args=None):
    rclpy.init(args=args)

    subscriber = Subscriber()

    rclpy.spin(subscriber)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
