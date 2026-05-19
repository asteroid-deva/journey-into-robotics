<div align="center">

#  My First Car — ROS 2 & Gazebo



### 🌌 My First Step Into Robotics Simulation

*A beginner ROS 2 differential-drive robot project built using Gazebo, URDF, and keyboard teleoperation.*

</div>

---

# 📖 Overview

This project serves as the **"Hello World" of ROS 2 robotics development**.  
The goal was to create and spawn a custom differential-drive robot in **Gazebo**, then control it using keyboard inputs through ROS 2 topics.

It helped me understand:

- 🧠 ROS 2 communication architecture  
- 📡 Publisher ↔ Subscriber systems  
- ⚙️ Gazebo simulation workflows  
- 🤖 URDF robot descriptions  
- 🎮 Teleoperation systems  
- 🛠️ ROS 2 package structure and build systems  

---

# 🏗️ Project Architecture

To make the simulation work, four major components communicate together:

---

## 🤖 1. URDF (Robot Description)

The URDF file defines:

- Robot structure
- Links and joints
- Wheel mechanics
- Physical properties
- Collision models
- Friction and inertia

It essentially tells Gazebo:

> *"What the robot physically is."*

---

## 🔌 2. Gazebo Plugin

The Gazebo plugin acts as a **Subscriber Node**.

It:

- listens to the `/cmd_vel` topic
- receives movement commands
- applies force to the wheels
- updates robot motion inside the simulation

---

## 🎮 3. Teleop Node

The teleop node acts as a **Publisher**.

It:

- reads keyboard input
- converts keys into `geometry_msgs/Twist`
- publishes movement commands to `/cmd_vel`

---

## 🚀 4. Launch File

The launch file automates the entire startup process.

It:

- launches Gazebo
- loads the URDF
- spawns the robot
- initializes the ROS 2 nodes

---

# 📦 Dependencies & Installation

Before building the package, install the required ROS 2 dependencies.

## 🛠️ Install Gazebo ROS Packages

```bash
# Update package lists
sudo apt update

# Install Gazebo ROS integration
sudo apt install ros-humble-gazebo-ros-pkgs

# Install default ROS2 keyboard teleop package
sudo apt install ros-humble-teleop-twist-keyboard
````

---

# ⚙️ Build Instructions

## 1️⃣ Create the Workspace & Package

```bash
cd ~/ros2_ws/src
ros2 pkg create my_first_car
```

---

## 2️⃣ Create Required Directories

Inside the package:

```text
my_first_car/
├── launch/
├── urdf/
└── scripts/
```

---

## 3️⃣ Write the Files

### 📄 URDF File

Create:

```text
urdf/my_car.urdf
```

---

### 📄 Launch File

Create:

```text
launch/spawn_car.launch.py
```

---

## 4️⃣ Update `CMakeLists.txt`

Add the installation block before:

```cmake
ament_package()
```

This ensures ROS 2 copies launch and URDF files into the install workspace correctly.

---

## 5️⃣ Build the Workspace

```bash
# Always build from workspace root
cd ~/ros2_ws

colcon build --packages-select my_first_car
```

---

## 6️⃣ Source & Launch

```bash
source /opt/ros/humble/setup.bash
source install/setup.bash

ros2 launch my_first_car spawn_car.launch.py
```

> ⚠️ First Gazebo launch may take 30–60 seconds
> because default models are downloaded in the background.

---

<div align="center">

# 🎮 Upgrade — Custom WASD Controller
</div>

The default ROS 2 teleop node uses:

```text
I  J  K  L
```

which feels awkward for gaming-style movement.

So I created a custom Python teleoperation node:

```text
wasd_teleop.py
```

that provides standard:

```text
W A S D
```

controls.

---

# ✨ Features

## ⌨️ Native WASD Controls

* `W` → Forward
* `S` → Backward
* `A` → Left
* `D` → Right

---

## 📡 ROS 2 Publisher Node

The script publishes:

```text
geometry_msgs/Twist
```

messages directly to:

```text
/cmd_vel
```

---

## 🧹 No Terminal Spam

Initially, holding keys caused:

```text
wwwwwwww
```

spam in the terminal due to terminal mode switching.

This was solved by:

✅ locking the terminal in RAW mode during execution.

---

## ⚡ Dynamic Speed Controls

Added support for:

* increasing speed
* decreasing speed
* angular velocity tuning

similar to the default ROS 2 teleop package.

---

# ▶️ Running the Custom Controller

## Make Script Executable

```bash
chmod +x wasd_teleop.py
```

---

## Update `CMakeLists.txt`

Add:

```cmake
install(PROGRAMS ...)
```

before:

```cmake
install(DIRECTORY ...)
```

---

## Rebuild Workspace

```bash
cd ~/ros2_ws
colcon build
```

---

## Run the Controller

```bash
ros2 run my_first_car wasd_teleop.py
```

---



