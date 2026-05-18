import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node

from geometry_msgs.msg import TransformStamped
from turtlesim.msg import Pose

import tf2_ros

from my_py_pkg import util

class TurtleTFBroadcaster(Node):
    """ Continuously broadcast transform from world to turtle frame """

    def __init__(self):
        super().__init__("turtle_tf_broadcaster")

        self.declare_parameter("child", "turtle1")
        self.declare_parameter("parent", "world")
        self._child = self.get_parameter("child").value
        self._parent = self.get_parameter("parent").value

        self._subscription = self.create_subscription(Pose, f"/{self._child}/pose", self._broadcast, 10)

        # Create a tf2 transform broadcaster. This is very similar to creating a standard publisher
        self._broadcaster = tf2_ros.TransformBroadcaster(self)

        self.get_logger().info(f"Transform broadcaster started: {self._parent} to {self._child}")

    def _broadcast(self, msg):
        """ Broadcast the turtle pose as a transform """

        t = TransformStamped()
        t.header.stamp = self.get_clock().now().to_msg()
        t.header.frame_id = self._parent
        t.child_frame_id = self._child

        t.transform.translation.x = msg.x
        t.transform.translation.y = msg.y
        t.transform.translation.z = 0.0

        q = util.euler_to_quaternion(0.0, 0.0, msg.theta)
        t.transform.rotation.x = q[0]
        t.transform.rotation.y = q[1]
        t.transform.rotation.z = q[2]
        t.transform.rotation.w = q[3]

        # similer to self._publisher.publish(msg)
        self._broadcaster.sendTransform(t)


def main(args = None):
    """ Main entrypoint """

    node = None
    try:
        rclpy.init()
        node = TurtleTFBroadcaster()
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