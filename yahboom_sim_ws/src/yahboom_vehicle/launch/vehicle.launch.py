import os
import runpy
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, OpaqueFunction
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

from launch_ros.parameter_descriptions import ParameterValue

def launch_vehicle(context):
    simulation = LaunchConfiguration("sim_mode").perform(context).lower() == "true"
    share = get_package_share_directory("yahboom_vehicle")
    with open(os.path.join(share, "urdf", "yahboom.urdf"), encoding="utf-8") as stream:
        description = stream.read()
    if simulation:
        description = runpy.run_path(os.path.join(share, "urdf", "simulation.py"))["simulation_description"](share)
    actions = [
        Node(package="yahboom_vehicle", executable="vehicle_config.py",
             parameters=[{"sim_mode": simulation}], output="screen"),
        Node(package="robot_state_publisher", executable="robot_state_publisher",
             parameters=[{"robot_description": description, "use_sim_time": simulation}],
             remappings=[("robot_description", "/yahboom/robot_description")] if simulation else [],
             output="screen"),
    ]
    if not simulation:
        actions.append(Node(package="yahboom_vehicle", executable="odom_bridge.py", output="screen",
             parameters=[{"publish_odom_tf": ParameterValue(
                 LaunchConfiguration("publish_odom_tf"), value_type=bool)}]))
    return actions


def generate_launch_description():
    return LaunchDescription([
        DeclareLaunchArgument("sim_mode", default_value="true", choices=["true", "false"]),
        DeclareLaunchArgument("publish_odom_tf", default_value="true"),
        OpaqueFunction(function=launch_vehicle),
    ])
