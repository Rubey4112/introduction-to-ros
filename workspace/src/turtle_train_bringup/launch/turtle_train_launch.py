from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    """ Launch multiple nodes """

    ld = LaunchDescription()
    nodes = []

    nodes.append(Node(
        name="turtlesim",
        package="turtlesim",
        executable="turtlesim_node",
    ))

    # nodes.append(Node(
    #     name="teleop",
    #     package="turtlesim",
    #     executable="turtle_teleop_key",
    # ))

    nodes.append(Node(
        name="spawner",
        package="turtle_train_pkg",
        executable="turtle_spawner",
    ))

    for n in range(1, 11):
        nodes.append(Node(
            name=f"turtle_broadcaster_{n}",
            package="turtle_train_pkg",
            executable="pose_broadcaster",
            parameters=[{
                "child": f"turtle{n}",
            }],
        ))

    for n in range(1, 10):
        nodes.append(Node(
            name=f"turtle_follower_{n}",
            package="turtle_train_pkg",
            executable="follower",
            parameters=[{
                "leader": f"turtle{n}",
                "follower": f"turtle{n+1}",
            }],
        ))

    for node in nodes:
        ld.add_action(node)

    return ld