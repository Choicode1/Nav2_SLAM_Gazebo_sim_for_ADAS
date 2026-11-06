#!/usr/bin/env python3
"""Publish the shared NAV2 module configuration, including for late subscribers."""
import json

import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, DurabilityPolicy, ReliabilityPolicy
from std_msgs.msg import String


class VehicleConfig(Node):
    def __init__(self):
        super().__init__('yahboom_vehicle_config')
        self.declare_parameter('sim_mode', True)
        qos = QoSProfile(depth=1, durability=DurabilityPolicy.TRANSIENT_LOCAL,
                         reliability=ReliabilityPolicy.RELIABLE)
        self.publisher = self.create_publisher(String, '/vehicle_config', qos)
        config = {'robot': 'yahboom', 'platform': 'yahboom', 'level': '2d',
                  'sim_mode': self.get_parameter('sim_mode').value}
        self.publisher.publish(String(data=json.dumps(config)))
        self.get_logger().info(f'Published vehicle configuration: {config}')


def main():
    rclpy.init()
    node = VehicleConfig()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
