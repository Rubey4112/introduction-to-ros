import random

import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node

from geometry_msgs.msg import Point
from my_interfaces.srv import TriggerPoints

class TriggerPointsServer(Node):
    """ Server that responds with an array of random points """

    def __init__(self):
        super().__init__("trigger_points_server")

        # Creating a service object
        self._srv = self.create_service(TriggerPoints, "trigger_points", self._server_callback)

    def _server_callback(self, req, resp):
        """ Responds with array of random floats """
        
        self.get_logger().info(f"Received request: num_points={req.num_points}")

        resp.success = req.num_points > 0

        resp.points = []
        for _ in range(req.num_points):
            point = Point()
            point.x = random.uniform(-1.0, 1.0)
            point.y = random.uniform(-1.0, 1.0)
            point.z = random.uniform(-1.0, 1.0)
            resp.points.append(point)
        return resp

def main(args=None):
    """ Main entrypoint """

    node = None
    try:
        rclpy.init()
        node = TriggerPointsServer()
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
