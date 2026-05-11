# Hardware-in-the-Loop (HITL) Drone Simulation

## Overview
This project demonstrates a complete Hardware-In-The-Loop (HIL) simulation architecture. It integrates physical hardware (ESP32 + MPU6050 IMU) with a virtual physics environment (Gazebo) and an autopilot software (ArduPilot SITL) via ROS 2 and MAVROS.

The primary objective is to simulate an autonomous UAV landing on a moving platform. The physical IMU sensor dictates the state of the "virtual platform". Once the platform stabilizes within a safe tilt threshold (±5 degrees) for a specific duration, the ROS 2 decision node commands the ArduPilot to execute an autonomous LAND maneuver.

System Architecture
Hardware Layer: ESP32 Microcontroller + MPU6050 (6-DOF IMU)
Middleware & Communication: ROS 2 (Humble)
Flight Stack: ArduPilot Copter SITL
Physics Simulator: Gazebo 11 (Classic)
Bridge: MAVROS / MAVLink Protocol

🛠️ Prerequisites
Ubuntu 22.04 LTS
ROS 2 Humble
ArduPilot SITL & MAVProxy
Gazebo 11 & ardupilot_gazebo plugin
Python 3 dependencies: pyserial, pymavlink

## System Architecture
Physical motion data from the GY-521 is processed by the ESP32 and fed into the simulation loop. ArduPilot uses this real-world sensor telemetry to control the virtual drone dynamics within the Gazebo environment.

## Troubleshooting & Technical Notes
During the integration phase, a critical synchronization issue occurred where ArduPilot could not read the motor feedback correctly from Gazebo, leading to unstable behavior.

**Solution implemented:**
1.  **Gazebo Physics Configuration:** Adjusted the `real_time_update_rate` parameter in Gazebo from `-1` to `1000`. This ensured the simulation ran at a constant, reliable speed.
2.  **Controller Tuning:** Increased the `p_gain` to strengthen the motor response.

These adjustments successfully resolved the communication gap, allowing ArduPilot to accurately read motor feedback and stabilizing the overall HITL simulation.

###############################

#**Installation & Build**
1. Clone the repository
git clone https://github.com/SENIN-KULLANICI-ADIN/Autonomous-HIL-Landing.git
cd Autonomous-HIL-Landing
2. Build the ROS 2 workspace
colcon build
source install/setup.bash


#***Execution (How to Run)**
1. Physics Engine (Gazebo)
gazebo --verbose ~/ardupilot_gazebo/worlds/iris_arducopter_runway.world

2. Flight Controller (ArduPilot SITL)
sim_vehicle.py -v ArduCopter -f gazebo-iris --console --map

3. MAVROS Bridge
ros2 run mavros mavros_node --ros-args -p fcu_url:=udp://127.0.0.1:14550@14555 -p gcs_url:=udp://@127.0.0.1:14550

4. Hardware Sensor Bridge (ESP32)
sudo chmod 666 /dev/ttyUSB0
ros2 run platform_sensor sensor_bridge

5. Autonomous Landing Controller
ros2 run platform_sensor landing_controller








