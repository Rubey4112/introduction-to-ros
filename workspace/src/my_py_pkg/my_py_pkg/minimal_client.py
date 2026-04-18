import random

import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node

from example_interfaces.srv import AddTwoInts

class MinimalClient(Node):

    def __init__(self):
        super().__init__("minimal_client")

        self._client = self.create_client(AddTwoInts, "add_ints")

        while not self._client.wait_for_service(timeout_sec=2.0):
            self.get_logger().info("Waiting for service...")
        self._timer = self.create_timer(2.0, self._client_callback)

    def _client_callback(self):
        """ Send request to server asking to add two integers """

        req = AddTwoInts.Request()
        req.a = random.randint(0, 10)
        req.b = random.randint(0, 10)
        
        self.future = self._client.call_async(req)
        self.future.add_done_callback(self._response_callback)
    
    def _response_callback(self, future):
        """ Log response from server """
        try:
            resp = future.result()
            self.get_logger().info(f"Result: {resp.sum}")
        except Exception as e:
            self.get_logger().error(f"{str(e)}")

def main(args=None):
    """ Main entrypoint """

    node = None
    try:
        rclpy.init()
        node = MinimalClient()
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

