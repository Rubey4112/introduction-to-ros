import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from example_interfaces.msg import String

class PublisherWithParams(Node):
    """ Publisher example that periodically sends out a string """

    def __init__(self):
        super().__init__("publisher_with_params")

        self.declare_parameter("message", "Hello")
        self.declare_parameter("timer_period", 1.0)

        self._message = self.get_parameter("message").value
        self._timer_period = self.get_parameter("timer_period").value

        self._publisher = self.create_publisher(String, "my_topic", 10)
        self._timer = self.create_timer(self._timer_period, self._timer_callback)

        self.add_post_set_parameters_callback(self._post_parameters_callback)

    def _post_parameters_callback(self, params: list[rclpy.Parameter]):
        """ Set parameters after node started """

        for param in params:
            if param.name == "message":
                # Update `message` Parameter
                self._message = param.value
                self.get_logger().info(f"Set {param.name} to {param.value}")

            elif param.name == "timer_period":
                # Update `timer_period` Parameter
                self._timer_period = param.value
                self.get_logger().info(f"Set {param.name} to {param.value}")

                self._timer.cancel()
                self._timer = self.create_timer(self._timer_period, self._timer_callback)
            
            else:
                self.get_logger().warn(f"Unknown parameter: {param.name}")

    def _timer_callback(self):
        """ Publishes a simple message to topic """

        msg = String()
        msg.data = self._message

        self._publisher.publish(msg)
        self.get_logger().info(f"Publishing: {msg.data}")

def main(args = None):
    """ Main entrypoint """

    node = None
    try:
        rclpy.init()
        node = PublisherWithParams()
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