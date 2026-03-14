import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from example_interfaces.msg import String

class MinimalSubscriber(Node):
    """ Subscriber example that prints messages to the console """

    def __init__(self):
        super().__init__("minimal_subscriber")

        self._subscription = self.create_subscription(String, "my_topic", self._listener_callback, 10)

    def _listener_callback(self, msg: String):
        """ Prints message to the console """

        self.get_logger().info(f"Received message: {msg.data}")

def main(args = None):
    """ Main entrypoint """

    node = None
    try:
        rclpy.init()
        node = MinimalSubscriber()
        rclpy.spin(node)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        if node is not None:
            node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()

if __name__ == "__main__":
    main()