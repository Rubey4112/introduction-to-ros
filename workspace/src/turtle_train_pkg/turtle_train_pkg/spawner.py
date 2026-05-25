import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node

from turtlesim.srv import Spawn

class Spawner(Node):

    def __init__(self):
        super().__init__("turtle_spawner")

        self._num = 9

        self._client = self.create_client(Spawn, "/spawn")

        while not self._client.wait_for_service(timeout_sec=2.0):
            self.get_logger().info("Waiting for service...")

        for n in range(self._num):
            self._spawn()

    def _spawn(self):
        
        req = Spawn.Request()
        req.x = 0.0
        req.y = 0.0
        req.theta = 0.0

        self.future = self._client.call_async(req)
        self.future.add_done_callback(self._response_callback)

    def _response_callback(self, future):
        """ Log response from server """
        try:
            resp = future.result()
            self.get_logger().info(f"Result: {resp.name}")
        except Exception as e:
            self.get_logger().error(f"{str(e)}")

def main(args=None):
    """ Main entrypoint """

    node = None
    try:
        rclpy.init()
        node = Spawner()
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