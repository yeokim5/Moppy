## Simulation

- [x] Set up Webots simulation environment
- [x] Create 3D room models with various layouts and obstacles
- [x] Implement robot model with accurate physical properties
- [x] Configure LIDAR sensor simulation
- [x] Configure camera sensor simulation
- [ ] Create data capture pipeline from sensors
- [ ] Implement `room_simulator.py` with configuration options
- [ ] Develop `lidar_capture.py` to collect and save sensor data
- [ ] Generate CSV exports of LIDAR data
- [ ] Capture and save camera image datasets
- [ ] Validate simulation data quality and format

---

## Setup Instructions

1. **Install WSL**

   - [Windows Subsystem for Linux (WSL) Installation Guide](https://learn.microsoft.com/en-us/windows/wsl/install)

2. **Install Webots on Windows**

   - Follow the guide: [Installing Webots on Windows](https://docs.ros.org/en/humble/Tutorials/Advanced/Simulators/Webots/Installation-Windows.html#id5)

3. **Install ROS 2 (Humble) on WSL**

   - Follow the guide: [Installing ROS 2 on Ubuntu (WSL)](https://docs.ros.org/en/humble/Installation/Ubuntu-Install-Debs.html)

4. **Download the Andino Webots Package**

   - Repository: [andino_webots GitHub](https://github.com/Ekumen-OS/andino_webots?tab=readme-ov-file)

5. **Modify Setup for WSL**

   - Create a custom launch file for WSL and Windows integration:  
     `andino_webots_windows.launch.py`

6. **Run the Simulation**

   In WSL terminal:

   ```bash
   source /opt/ros/humble/setup.bash
   source install/local_setup.bash
   export WEBOTS_HOME=/mnt/c/Program\ Files/Webots

   # Launch Andino in Webots
   ros2 launch andino_webots andino_webots_windows.launch.py

   # Run SLAM toolbox
   ros2 launch andino_slam slam_toolbox_online_async.launch.py

   # Open RViz2
   ros2 run rviz2 rviz2
   ```

   In RViz2:

   - Add **Laser Scan** (`/scan`)
   - Add **Odometry** (`/odom`)
   - Add **Map** (`/map`)

   Control robot manually:

   ```bash
   ros2 run teleop_twist_keyboard teleop_twist_keyboard
   ```

7. **Run SLAM and Save Map**

   - Save the map:

     ```bash
     ros2 run nav2_map_server map_saver_cli -f my_map
     ```

   - Run the map server:

     ```bash
     ros2 run nav2_map_server map_server --ros-args -p yaml_filename:=my_map.yaml
     ```

   - Visualize the saved map:

     ```bash
     ros2 run rviz2 rviz2
     ```

   - (Alternative) View map image:

     ```bash
     eog my_map.pgm
     ```

---

## Comments

- **Environment Setup:**

  - Working on a Windows PC and laptop.
  - Using WSL to overcome compatibility issues.
  - Initially attempted Gazebo but faced limitations with WSL/Windows integration.
  - Considered NVIDIA Isaac Sim (very powerful but GPU-heavy) — not feasible for current hardware.
  - Webots was selected as a more lightweight and practical alternative.

- **Robot Selection:**

  - Requirements: small, affordable, LIDAR support, and Webots compatibility.
  - Chose the **Andino** robot: [Andino GitHub Repository](https://github.com/Ekumen-OS/andino/tree/humble/andino_hardware).

- **Progress:**
  - Successfully set up the Andino robot in Webots.
  - Able to save and visualize room maps (images linked).

---

## Lessons Learned

- There’s **always an alternative** — leverage AI to explore options.  
  (Found Webots after initial struggles.)

- Always **read official documentation carefully** (e.g., GitHub READMEs).

  - AI is great for debugging and quick advice but **not** a replacement for manuals and docs.
  - Different devices might have different outcomes — **test on multiple systems** if possible.

- Some things **might not be possible** or practical.

  - Quickly validate feasibility (using AI or documentation) to avoid wasting time.
  - Example: trying to configure Docker inside WSL + run Windows Webots.

- **Documentation matters:**
  - Andino robot had **two** ways to spawn robots:
    - All at once (map + robots together)
    - Separately

---
