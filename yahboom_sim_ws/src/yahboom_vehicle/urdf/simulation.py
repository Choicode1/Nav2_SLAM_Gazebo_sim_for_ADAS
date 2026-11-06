"""Gazebo differential-drive approximation using the supplied vehicle geometry."""
from pathlib import Path
import xml.etree.ElementTree as ET


def simulation_description(share):
    root = ET.parse(Path(share) / "urdf" / "yahboom.urdf").getroot()
    # Only replace visuals. Keep the validated collision/inertial/sensor model.
    visuals = {"base_link": "body", "zq_Link": "front_left", "yq_Link": "front_right",
               "zh_Link": "rear_left", "yh_Link": "rear_right"}
    for link in root.findall("link"):
        for visual in link.findall("visual"):
            link.remove(visual)
        part = visuals.get(link.get("name"))
        if part:
            visual = ET.SubElement(link, "visual")
            geometry = ET.SubElement(visual, "geometry")
            ET.SubElement(geometry, "mesh", filename=f"package://yahboom_vehicle/meshes/pi5/{part}.dae")
    for mesh in root.findall(".//mesh"):
        mesh.set("filename", (Path(share) / mesh.get("filename").split("package://yahboom_vehicle/")[1]).as_uri())
    for joint in root.findall("joint"):
        if joint.find("child").get("link") == "base_link":
            joint.find("origin").set("xyz", "0 0 0.04525")
    wheels = []
    for link_name in ("zq_Link", "zh_Link", "yq_Link", "yh_Link"):
        joint = next(j for j in root.findall("joint") if j.find("child").get("link") == link_name)
        joint.set("type", "continuous")
        axis = joint.find("axis")
        if axis is None:
            axis = ET.SubElement(joint, "axis")
        axis.set("xyz", "0 1 0")
        ET.SubElement(joint, "dynamics", damping="0.01", friction="0.0")
        wheels.append(joint.get("name"))
        link = root.find(f"link[@name='{link_name}']")
        for collision in link.findall("collision"):
            link.remove(collision)
        collision = ET.SubElement(link, "collision")
        ET.SubElement(collision, "origin", xyz="0 0 0", rpy="1.57079632679 0 0")
        ET.SubElement(ET.SubElement(collision, "geometry"), "cylinder", radius="0.024", length="0.0215")
        gazebo = ET.SubElement(root, "gazebo", reference=link_name)
        for key, value in {"mu1": "1.0", "mu2": "0.1", "fdir1": "1 0 0"}.items():
            ET.SubElement(gazebo, key).text = value
    gazebo = ET.SubElement(root, "gazebo")
    drive = ET.SubElement(gazebo, "plugin", name="yahboom_drive", filename="libgazebo_ros_diff_drive.so")
    ros = ET.SubElement(drive, "ros")
    for remapping in ("cmd_vel:=/cmd_vel", "odom:=/odom"):
        ET.SubElement(ros, "remapping").text = remapping
    for key, value in {
        "num_wheel_pairs": "2", "update_rate": "50", "max_wheel_torque": "2",
        "max_wheel_acceleration": "1", "publish_odom": "true", "publish_odom_tf": "true",
        "publish_wheel_tf": "false", "odometry_frame": "odom",
        "robot_base_frame": "base_footprint", "odometry_source": "1",
    }.items():
        ET.SubElement(drive, key).text = value
    for left, right in zip(wheels[:2], wheels[2:]):
        for key, value in {"left_joint": left, "right_joint": right,
                           "wheel_separation": "0.135", "wheel_diameter": "0.048"}.items():
            ET.SubElement(drive, key).text = value
    state = ET.SubElement(gazebo, "plugin", name="yahboom_joints", filename="libgazebo_ros_joint_state_publisher.so")
    ET.SubElement(state, "update_rate").text = "30"
    for joint in wheels:
        ET.SubElement(state, "joint_name").text = joint
    laser = ET.SubElement(root, "gazebo", reference="laser_frame")
    sensor = ET.SubElement(laser, "sensor", name="yahboom_lidar", type="ray")
    ET.SubElement(sensor, "always_on").text = "true"
    ET.SubElement(sensor, "update_rate").text = "10"
    ray = ET.SubElement(sensor, "ray")
    horizontal = ET.SubElement(ET.SubElement(ray, "scan"), "horizontal")
    for key, value in {"samples": "720", "resolution": "1", "min_angle": "-3.14159265", "max_angle": "3.14159265"}.items():
        ET.SubElement(horizontal, key).text = value
    distance = ET.SubElement(ray, "range")
    for key, value in {"min": "0.12", "max": "8.0", "resolution": "0.01"}.items():
        ET.SubElement(distance, key).text = value
    plugin = ET.SubElement(sensor, "plugin", name="yahboom_scan", filename="libgazebo_ros_ray_sensor.so")
    ET.SubElement(ET.SubElement(plugin, "ros"), "remapping").text = "~/out:=/scan"
    ET.SubElement(plugin, "output_type").text = "sensor_msgs/LaserScan"
    ET.SubElement(plugin, "frame_name").text = "laser_frame"
    return ET.tostring(root, encoding="unicode")
