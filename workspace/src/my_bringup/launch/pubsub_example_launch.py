from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    """ Launch multiple nodes """

    ld = LaunchDescription()
    nodes = []

    nodes.append(Node(
        name="publisher",
        package="my_cpp_pkg",
        executable="publisher_with_params",
        namespace="talkie",
        parameters=[{
            "message": "Greetings!",
            "timer_period": 0.5,
        }],
    ))

    nodes.append(Node(
        name="subscriber_1",
        package="my_py_pkg",
        executable="minimal_subscriber",
    ))

    nodes.append(Node(
        name="subscriber_2",
        package="my_py_pkg",
        executable="minimal_subscriber",
        namespace="talkie",
    ))

    nodes.append(Node(
        name="subscriber_3",
        package="my_py_pkg",
        executable="minimal_subscriber",
        namespace="talkie",
    ))

    for node in nodes:
        ld.add_action(node)

    return ld

