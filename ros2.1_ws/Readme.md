<div align="center">
  
#  ROS 2 Autonomous Explorer  
##  From Scratch to Self-Driving



### 🤖 Building a Fully Autonomous Differential-Drive Robot  
Using **ROS 2 Humble • Gazebo • SLAM Toolbox • Nav2**

</div>

---

# 📖 Overview

Welcome to my journey of building a fully autonomous self-driving robot completely from scratch using:

- ⚙️ ROS 2 (Humble)
- 🌍 Gazebo
- 🧠 SLAM Toolbox
- 🛰️ Nav2 Navigation Stack

This repository is more than a collection of code.  
It is a **battle-tested engineering logbook** documenting:

- every architectural upgrade
- every catastrophic failure
- every debugging nightmare
- and every solution that brought the robot back to life

---

# 🛠️ Phase 1 — Foundation  
## *(URDF • Physics • Teleoperation)*

### 🎯 Goal

Spawn a custom differential-drive robot inside Gazebo and manually control it using keyboard input.

---

# 🏗️ Workspace Initialization

```bash
source /opt/ros/humble/setup.bash

mkdir -p ~/ros2.1_ws/src
cd ~/ros2.1_ws/src

ros2 pkg create --build-type ament_cmake my_first_autocar

cd ~/ros2.1_ws
colcon build
````

---

# ⚙️ System Architecture

---

## 🤖 URDF Robot Model

Created:

```
my_car.urdf
```

containing:

* robot chassis
* differential wheels
* caster wheel
* Gazebo diff-drive plugin

---

## 🚀 Launch System

Created:

```
spawn_car.launch.py
```

which:

* launches Gazebo
* publishes robot state
* spawns the robot entity

---

## 📦 Build System Integration

Added:

```
urdf/
launch/
```

directories into:

```
CMakeLists.txt
```

---

# 🐛 Bug 1 — `[kdl_parser]` Warning & Physics Crash

---

## ❌ The Error

The terminal screamed about:

```
base_link having inertia
```

and the robot completely failed to spawn correctly.

---

## ⚠️ Failed Attempt

Tried introducing:

```
base_footprint
```

as a dummy link.

---

## ✅ The REAL Fix

The dummy link silently destroyed the odometry chain.

The actual culprit?

```xml
</gazebo>
```

A broken XML typo inside the URDF.

Fixing the malformed tag instantly restored Gazebo physics.

---

# 👁️ Phase 2 — Perception & Mapping

## *(SLAM Toolbox)*

### 🎯 Goal

Give the robot **eyes** using LiDAR and generate a live 2D map of the world.

---

# 🔍 Sensor Integration

Injected a simulated:

```
LiDAR ray sensor
```

attached to:

```
lidar_link
```

inside the URDF.

---

# 🧠 SLAM Integration

Updated:

```
spawn_car.launch.py
```

to launch:

```
async_slam_toolbox_node
```

---

# 🐛 Bug 2 — RViz Dropping LiDAR Frames

## ❌ Error

```
Message Filter dropping message...
discarding message because the queue is full
```

---

## ✅ Fix

Forced RViz to synchronize with Gazebo simulation time.

```bash
ros2 run rviz2 rviz2 --ros-args -p use_sim_time:=true
```

---

# 🐛 Bug 3 — “No Map Received”

## ❌ Error

SLAM worked perfectly in terminal logs, but RViz refused to display the map.

---

## ✅ Fix (Part 1 — QoS)

Changed RViz Map Display:

```
Durability Policy:
Volatile → Transient Local
```

---

## ✅ Fix (Part 2 — Wake-Up Drive)

SLAM required motion to initialize properly.

Driving the robot forward a few inches using the WASD teleop script instantly triggered map generation.

---

# 💾 Saving the Map

```bash
mkdir -p ~/ros2.1_ws/src/my_first_autocar/maps

cd ~/ros2.1_ws/src/my_first_autocar/maps

ros2 run nav2_map_server map_saver_cli -f my_world_map
```

---

# ⚠️ Side Error

```text id="1tp9ah"
ros2: command not found
```

Cause:

Forgot to source ROS 2 in a fresh terminal.

---

# 🧠 Phase 3 — Autonomous Navigation

## *(Nav2 Stack)*

### 🎯 Goal

Load the saved map and achieve autonomous path planning with obstacle avoidance.

---

# 🚀 System Upgrade

Installed Nav2:

```bash
sudo apt install ros-humble-navigation2 ros-humble-nav2-bringup
```

---

# 📄 Created

```
navigation.launch.py
```

which launches:

* Gazebo
* robot URDF
* Nav2 bringup stack

---

# 🐛 Bug 4 — The Empty String Crash

## ❌ Error

```
[Errno 2] No such file or directory: ''
```

Gazebo became a zombie process.

RViz lost the map entirely.

---

## ✅ Fix

Explicitly defined Nav2 parameter path:

```python
params_path = os.path.join(
    get_package_share_directory('nav2_bringup'),
    'params',
    'nav2_params.yaml'
)
```

---

# 🐛 Bug 5 — The Ghost of `base_footprint`

## ❌ Error

```
Couldn't transform from lidar_link to base_footprint
```

Nav2 lifecycle manager crashed.

---

## ✅ Fix — Mathematical Duct Tape™

Created a fake transform bridge using:

```python
Node(
    package='tf2_ros',
    executable='static_transform_publisher',
    arguments=[
        '0', '0', '0',
        '0', '0', '0',
        'base_link',
        'base_footprint'
    ]
)
```

This satisfied Nav2 without breaking Gazebo physics.

---

# 🐛 Bug 6 — Colcon Cache Trap

## ❌ Error

Old crashes persisted despite fixing the code.

---

## ✅ Nuclear Wipe Solution

```bash
cd ~/ros2.1_ws

rm -rf build install log

colcon build --packages-select my_first_autocar
```

---

# 🐛 Bug 7 — The Giant Robot Illusion

## ❌ Error

Nav2 believed the robot was trapped inside walls.

Huge purple danger zones filled the map.

---

## ✅ Fix

Nav2 default parameters assumed an industrial-sized robot.

Changed:

```yaml
robot_radius: 0.22
```

to:

```yaml
robot_radius: 0.05
```

inside both:

* global costmap
* local costmap

---

# 🚀 Phase 4 — The Ultimate Explorer

## *(Online Mapping + Live Navigation)*

### 🎯 Final Goal

The robot must:

✅ wake up in an unknown environment
✅ generate a map live
✅ navigate autonomously simultaneously

---

# 🧠 Brain Transplant

Created:

```
online_navigation.launch.py
```

---

# 🔄 Architectural Changes

Removed:

* Map Server
* AMCL Localization

Connected:

```
async_slam_toolbox_node
```

directly into Nav2 planners.

---

# 🐛 Bug 8 — Malformed Map Panic

## ❌ Error

```
Sensor origin out of map bounds
Received map message is malformed
```

---

## ✅ Fix — Jumpstart Method

At startup SLAM generated a microscopic map.

Solution:

Drive forward manually for a few inches before setting a Nav2 goal.

This expands the map safely.

---

# 🐛 Bug 9 — Sensor Pitching & Fake Walls

## ❌ Error

During hard braking:

* LiDAR tilted downward
* floor detected as obstacle
* fake walls appeared under robot

Controls also became extremely laggy.

---

# ✅ Physics Fix

Reduced caster wheel friction:

```xml
<gazebo reference="caster_wheel">
  <mu1>0.0</mu1>
  <mu2>0.0</mu2>
</gazebo>
```

---

# ✅ Software Fix

Ignored laser hits below 5cm:

```yaml
min_obstacle_height: 0.05
```

---

# ✅ Performance Fix

Minimized Gazebo window.

This improved:

* CPU availability
* Real Time Factor
* Nav2 responsiveness

dramatically.

---

# 🏆 Final Result

The robot successfully:

✅ navigates autonomously
✅ performs live SLAM
✅ avoids dynamic obstacles
✅ explores unknown environments in real time

---

# 💾 Final Map Save

```bash
ros2 run nav2_map_server map_saver_cli -f my_giant_world_map
```

---

<div align="center">

# 🌌 Mission Status: SUCCESS

### *The fog of war has been lifted.*

🚗 ➜ 🧠 ➜ 🛰️ ➜ 🤖

</div>
```  
