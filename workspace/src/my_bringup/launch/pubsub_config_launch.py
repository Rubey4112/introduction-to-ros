from launch import LaunchDescription
from launch_ros.actions import Node

from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    """ Launch multiple nodes """

    # Create a future that store the configurations that will be loaded at runtime
    config_file = LaunchConfiguration("config_file_arg") # Declare a the ROS 2 launch param "config_file_arg" as a future

    # Declare a launch argument for the YAML config file
    # Fill in the the ROS 2 launch param "config_file_arg" with the default value of the "pubsub_debug.yaml" file
    config_file_arg = DeclareLaunchArgument("config_file_arg", default_value="pubsub_debug.yaml", description="Path to the YAML config file")

    # Build the full path to the config file at runtime
    # at run time, the Python variable `config_file` will be filled in with the string name of the yaml configuration file
    config_path = PathJoinSubstitution([FindPackageShare("my_bringup"), "config", config_file])

    ld = LaunchDescription()
    nodes = []

    nodes.append(Node(
        name="publisher_1",
        package="my_cpp_pkg",
        executable="publisher_with_params",
        namespace="talkie",
        parameters=[config_path],
    ))

    nodes.append(Node(
        name="publisher_2",
        package="my_cpp_pkg",
        executable="publisher_with_params",
        namespace="talkie",
        parameters=[config_path],
    ))

    ld.add_action(config_file_arg)

    nodes.append(Node(
        name="subscriber_1",
        package="my_py_pkg",
        executable="minimal_subscriber",
        namespace="talkie",
    ))

    for node in nodes:
        ld.add_action(node)

    return ld