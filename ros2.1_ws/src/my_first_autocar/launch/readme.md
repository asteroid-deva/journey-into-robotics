
# 🚀 Launch Directory

This directory contains the master `launch.py` scripts used to orchestrate the robot's subsystems. Instead of starting 10 different nodes manually, these scripts handle the environment, TF trees and algorithm bringing-ups.

## 📋 Available Launch Files

### 1. `spawn_car.launch.py`
**The Foundation.** This script initializes the simulated world and drops the robot into it.
* **What it does:** Starts the Gazebo server/client, loads `my_car.urdf`, starts the `robot_state_publisher` and spawns the entity.
* **Usage:**
 ```bash
  ros2 launch my_first_autocar spawn_car.launch.py
  ```
### 2. navigation.launch.py
**Static Autonomous Driving.** This script is used for standard Nav2 point-to-point driving using a pre-saved map.

**What it does:** Spawns the robot, implements the TF base_footprint duct-tape fix, loads the saved .yaml map from the /maps folder and boots the nav2_bringup algorithms (AMCL, global/local planners).

**Usage:**

```Bash
ros2 launch my_first_autocar navigation.launch.py
```
### 3. online_navigation.launch.py
**The Explorer.** This is the advanced Frontier Exploration script. It bypasses the static map and builds one dynamically.

**What it does:** Wires async_slam_toolbox_node directly into the Nav2 path planners. The robot wakes up in the dark and maps the room (/scan to /map) while simultaneously calculating costmaps to avoid obstacles in real-time.

**Usage:**

```Bash
ros2 launch my_first_autocar online_navigation.launch.py
```
