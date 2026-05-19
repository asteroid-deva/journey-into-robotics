<div align="center">
  
# 🚘 My First Autocar: Core Package
  
[![ROS 2](https://img.shields.io/badge/ROS_2-Humble-3498db?logo=ros&logoColor=white)](https://docs.ros.org/en/humble/)
[![Python](https://img.shields.io/badge/Python-3.10-f1c40f?logo=python&logoColor=white)]()
[![Gazebo](https://img.shields.io/badge/Sim-Gazebo-ff69b4?logo=gazebo&logoColor=white)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

*The core ROS 2 package containing the URDF, Nav2 configurations and SLAM integrations for a fully autonomous differential-drive robot.*

</div>

## 📂 Package Architecture

This package is structured to cleanly separate physics, perception and configuration. 

| Directory | Description |
| :--- | :--- |
| 📁 **`launch/`** | Contains Python-based launch files to spin up complex multi-node systems (Gazebo, RViz, Nav2, SLAM). |
| 📁 **`maps/`** | Stores the `.yaml` and `.pgm` static occupancy grids generated via SLAM. |
| 📁 **`params/`** | Custom ROS 2 parameters (e.g, overriding Nav2 default costmaps for our specific robot radius). |
| 📁 **`urdf/`** | The XML-based Unified Robot Description Format files that define the robot's physical and visual properties. |

## ⚙️ Quick Build Instructions

If you are pulling this package into a fresh workspace, build and source it using `colcon`:

```bash
cd ~/ros2.1_ws
colcon build --packages-select my_first_autocar
source install/setup.bash
