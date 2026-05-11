# Hardware-in-the-Loop (HITL) Drone Simulation

## Overview
This project implements a Hardware-in-the-Loop (HITL) simulation by integrating an ESP32 microcontroller and a GY-521 (MPU6050) sensor with ArduPilot and the Gazebo simulator. The physical sensor data directly influences the simulated drone's autonomous flight and landing behavior.

## Technologies & Tools
*   **Hardware:** ESP32, GY-521 (IMU)
*   **Software:** ArduPilot (SITL/HITL mode)
*   **Simulation:** Gazebo

## System Architecture
Physical motion data from the GY-521 is processed by the ESP32 and fed into the simulation loop. ArduPilot uses this real-world sensor telemetry to control the virtual drone dynamics within the Gazebo environment.

## Troubleshooting & Technical Notes
During the integration phase, a critical synchronization issue occurred where ArduPilot could not read the motor feedback correctly from Gazebo, leading to unstable behavior.

**Solution implemented:**
1.  **Gazebo Physics Configuration:** Adjusted the `real_time_update_rate` parameter in Gazebo from `-1` to `1000`. This ensured the simulation ran at a constant, reliable speed.
2.  **Controller Tuning:** Increased the `p_gain` to strengthen the motor response.

These adjustments successfully resolved the communication gap, allowing ArduPilot to accurately read motor feedback and stabilizing the overall HITL simulation.
