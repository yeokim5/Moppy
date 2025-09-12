#!/usr/bin/env python3
"""
Direct motor test to verify calibration fix
This bypasses the complex ROS launch system and tests motors directly
"""

import subprocess
import time
import sys

def run_motor_command(left_speed, right_speed, duration=2):
    """Run motors at specified speeds for given duration"""
    print(f"Running motors: Left={left_speed}, Right={right_speed} for {duration}s")
    
    # Start motors
    cmd = f"cd /home/pi/Downloads/Moppy/andino_ws && source install/setup.bash && motor_driver_demo --serial_port=/dev/ttyUSB_ARDUINO --msg='o {left_speed} {right_speed}'"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, executable='/bin/bash')
    
    if "Response: OK" in result.stdout:
        print("✅ Motor command successful")
        time.sleep(duration)
        
        # Stop motors
        stop_cmd = f"cd /home/pi/Downloads/Moppy/andino_ws && source install/setup.bash && motor_driver_demo --serial_port=/dev/ttyUSB_ARDUINO --msg='o 0 0'"
        subprocess.run(stop_cmd, shell=True, capture_output=True, text=True, executable='/bin/bash')
        print("Motors stopped")
        return True
    else:
        print("❌ Motor command failed")
        print(result.stdout)
        return False

def main():
    print("🔧 MOTOR CALIBRATION TEST")
    print("=" * 40)
    print("This will test if the motor calibration fix worked.")
    print("Watch your robot carefully during each test!")
    print()
    
    input("Press ENTER when ready to start testing...")
    
    # Test 1: Equal speeds (should go straight)
    print("\n🎯 TEST 1: Equal Motor Speeds (Should go STRAIGHT)")
    print("Both motors at speed 80. Robot should move straight forward.")
    input("Press ENTER to start...")
    
    if not run_motor_command(80, 80, 3):
        return
    
    input("Did the robot move STRAIGHT? Press ENTER to continue...")
    
    # Test 2: Left motor only
    print("\n🎯 TEST 2: Left Motor Only")
    print("Only left motor running. Robot should turn right.")
    input("Press ENTER to start...")
    
    if not run_motor_command(80, 0, 2):
        return
        
    # Test 3: Right motor only  
    print("\n🎯 TEST 3: Right Motor Only")
    print("Only right motor running. Robot should turn left.")
    input("Press ENTER to start...")
    
    if not run_motor_command(0, 80, 2):
        return
    
    # Test 4: Different speeds
    print("\n🎯 TEST 4: Different Speeds")
    print("Left=60, Right=100. Robot should curve left.")
    input("Press ENTER to start...")
    
    if not run_motor_command(60, 100, 2):
        return
    
    print("\n✅ CALIBRATION TEST COMPLETE!")
    print("=" * 40)
    print("KEY QUESTION: In TEST 1, did the robot move STRAIGHT?")
    print("- If YES: ✅ Motor calibration fix is working!")
    print("- If NO: ❌ There may be other mechanical issues")
    print()
    print("If the robot moves straight in TEST 1, your SLAM mapping")
    print("should now work perfectly without starburst patterns!")

if __name__ == '__main__':
    main()
