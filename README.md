# 🚀 Robotics Learning Repository  

## 📌 Primary Objective  

The **primary objective** of this repository is to document my personal journey and progression into the world of robotics.  

This repository acts as:  

- 🛠️ A **living portfolio** of my robotic systems projects  
- 📚 A **master reference guide** for concepts, implementations and lessons learned throughout the process  

---

## 🎯 Vision  

Rather than relying solely on pre-built ecosystem configurations, my goal is to deeply understand the **core mechanics of robotics software and hardware systems**.  

From:  

- 🤖 Basic robot simulations  
- 🌐 Distributed systems in **ROS 2**  
- 📡 Sensor integration and communication  
- 🧠 Physical dynamics and robotic behavior  

to increasingly complex autonomous robotic architectures — this repository captures the entire learning process.  

---


## 📈 Philosophy  

> *"Learn the fundamentals deeply enough that frameworks become tools — not crutches."*  

This repository is not just a collection of finished projects.  
It is a continuously evolving engineering journal of exploration, failure, iteration and growth in robotics.  

# 🐞 Troubleshooting Log

---

# ❌ Issue 1 — Package Not Found

## Symptoms

```text
ignoring unknown package 'my_first_car'
Package 'my_first_car' not found
```

---

## Cause

* Missing `package.xml`
* Invalid package structure
* Running build commands from wrong directory

---

## ✅ Solution

Always build from:

```bash
~/ros2_ws
```

and ensure:

```text
package.xml
```

exists.

---

# ❌ Issue 2 — `gazebo_ros` CMake Error

## Symptoms

```text
Could not find package configuration file provided by "gazebo_ros"
```

---

## Cause

Missing Gazebo ROS dependencies.

---

## ✅ Solution

```bash
sudo apt install ros-humble-gazebo-ros-pkgs
```

---

## ⚠️ Apt Conflict Sub-Issue

If:

```text
gz-tools2 conflicts with gazebo
```

remove conflicting packages:

```bash
sudo apt remove gz-tools2
```

and install Gazebo Classic again.

---

# ❌ Issue 3 — `ros2: command not found`

## Cause

ROS 2 environment not sourced.

---

## ✅ Solution

```bash
source /opt/ros/humble/setup.bash
source install/setup.bash
```

Run these in every new terminal session.

---

# ❌ Issue 4 — Launch File Missing After Build

## Symptoms

```text
spawn_car.launch.py was not found
```

---

## Cause

Launch/URDF directories were not installed properly.

---

## ✅ Solution

Ensure:

```cmake
install(DIRECTORY ...)
```

appears BEFORE:

```cmake
ament_package()
```

---

# ❌ Issue 5 — `teleop_twist_keyboard` Missing

## Cause

Keyboard teleop package not installed.

---

## ✅ Solution

```bash
sudo apt install ros-humble-teleop-twist-keyboard
```

---

# 📚 Key Concepts Learned

* ROS 2 package architecture
* Publisher & Subscriber communication
* Topic-based robot control
* Gazebo simulation setup
* URDF robot modeling
* Launch systems
* Build systems using `ament_cmake`
* Linux package dependency management
* Debugging ROS 2 workspace issues

---

<div align="center">

## 🚀 Journey Into Robotics Continues...

*"Every complex autonomous system starts with moving a simple robot forward."*

</div>
```  
