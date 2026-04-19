import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from my_interfaces.msg import Accelerometer

class AccPublisher(Node):
    """ Publisher example that periodically sends out dummy accelerometer data """

    def __init__(self):
        super().__init__("minimal_publisher")

        self._publisher = self.create_publisher(Accelerometer, "my_acc", 10)
        self._timer = self.create_timer(0.5, self._timer_callback)

        self._counter = 0

    def _timer_callback(self):
        """ Publishes a simple message to topic """

        msg = Accelerometer()
        msg.x = 0.5
        msg.y = 0.1
        msg.z = -9.81

        self._publisher.publish(msg)
        self.get_logger().info(f"Publishing: ({msg.x} {msg.y} {msg.z})")

        self._counter += 1

def main(args = None):
    """ Main entrypoint """

    node = None
    try:
        rclpy.init()
        node = AccPublisher()
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