import math

import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node

from geometry_msgs.msg import TransformStamped, Twist

import tf2_ros

class TurtleFollower(Node):
    """ Use TF2 listener to plot course and track main turtle """
    
    def __init__(self):
        super().__init__("turtle_follower")

        self.declare_parameter("leader", "turtle1")
        self.declare_parameter("follower", "turtle2")
        self.declare_parameter("period", 0.1)

        self._leader = self.get_parameter("leader").value
        self._follower = self.get_parameter("follower").value
        self._period = self.get_parameter("period").value

        self._publisher = self.create_publisher(Twist, f"/{self._follower}/cmd_vel", 10)

        self._tf_buffer = tf2_ros.Buffer()

        self._listener = tf2_ros.TransformListener(self._tf_buffer, self)

        self._timer = self.create_timer(self._period, self._follow)

        self.get_logger().info(f"Follower started: {self._follower} following {self._leader}")

    def _follow(self):
        """ Periodically steer the follower toward the leader """

        try:
            tf: TransformStamped = self._tf_buffer.lookup_transform(self._follower, self._leader, rclpy.time.Time())

            dx = tf.transform.translation.x
            dy = tf.transform.translation.y
            angle = math.atan2(dy, dx)

            twist = Twist()
            twist.linear.x = 2.0 * math.sqrt(dx**2 + dy**2)
            twist.angular.z = 4.0 * angle

            self._publisher.publish(twist)
        except Exception as e:
            self.get_logger().warn(f"Could not transform: {e}")

def main(args = None):
    """ Main entrypoint """

    node = None
    try:
        rclpy.init()
        node = TurtleFollower()
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

