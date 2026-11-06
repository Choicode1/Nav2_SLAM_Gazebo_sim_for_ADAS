# Nav2_SLAM_Gazebo_sim_for_ADAS
## 환경
| 구성 | 버전 및 패키지 |
| :--- | :--- |
| OS | Ubuntu 22.04 |
| ROS | ROS 2 Humble |
| Simulator | Gazebo Classic 11 |
| Robot Control | ros2_control |
| Controller | ros2_controllers |
| SLAM | slam_toolbox |
| Navigation | Nav2 |
| Visualization | RViz2 |
| Robot Description | URDF / Xacro |

## 환경 설정
```
sudo apt update && sudo apt upgrade -y
sudo apt install -y \
  libasio-dev \
  ros-humble-gazebo-ros-pkgs \
  ros-humble-ros2-control \
  ros-humble-ros2-controllers \
  ros-humble-gazebo-ros2-control \
  ros-humble-teleop-twist-keyboard \
  ros-humble-joint-state-publisher \
  ros-humble-joint-state-publisher-gui \
  ros-humble-xacro \
  ros-humble-gazebo-plugins \
  ros-humble-velodyne-description \
  ros-humble-image-transport-plugins \
  ros-humble-rviz2 \
  ros-humble-ackermann-steering-controller \
  ros-humble-ackermann-msgs \
  ros-humble-steering-controllers-library \
  ros-humble-slam-toolbox \
  ros-humble-nav2-map-server \
  ros-humble-pointcloud-to-laserscan \
  ros-humble-navigation2 \
  ros-humble-nav2-bringup
```

