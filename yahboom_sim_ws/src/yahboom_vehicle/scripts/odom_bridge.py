#!/usr/bin/env python3
# Adapted from hkit_yahboom_ws/amr_server/odom_tf_broadcaster.py.
import copy
import rclpy
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data
from nav_msgs.msg import Odometry
from geometry_msgs.msg import TransformStamped
from tf2_ros import TransformBroadcaster


class OdomBridge(Node):
    def __init__(self):
        super().__init__("yahboom_odom_bridge")
        self.publish_tf = self.declare_parameter("publish_odom_tf", True).value
        self.source_frame = self.declare_parameter("source_frame", "odom_frame").value
        self.source_child = self.declare_parameter("source_child", "base_footprint").value
        self.tf = TransformBroadcaster(self)
        self.publisher = self.create_publisher(Odometry, "/odom", 10)
        self.subscription = self.create_subscription(
            Odometry, "/odom_raw", self.on_odom, qos_profile_sensor_data)

    def on_odom(self, incoming):
        if (incoming.header.frame_id != self.source_frame
                or incoming.child_frame_id != self.source_child):
            self.get_logger().warning(
                "Unexpected /odom_raw frames; check source_frame/source_child",
                throttle_duration_sec=5.0)
            return
        message = copy.deepcopy(incoming)
        # Rename the known wheel-odometry frame consistently for LMS and Nav2.
        message.header.frame_id = "odom"
        message.child_frame_id = "base_footprint"
        self.publisher.publish(message)
        if self.publish_tf:
            transform = TransformStamped()
            transform.header = message.header
            transform.child_frame_id = message.child_frame_id
            transform.transform.translation.x = message.pose.pose.position.x
            transform.transform.translation.y = message.pose.pose.position.y
            transform.transform.translation.z = message.pose.pose.position.z
            transform.transform.rotation = message.pose.pose.orientation
            self.tf.sendTransform(transform)


def main():
    rclpy.init()
    node = OdomBridge()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
