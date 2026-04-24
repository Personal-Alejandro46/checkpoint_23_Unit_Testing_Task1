# tortoisebot_waypoints

## How to Test — PASS Condition
In the test/waypoints_test.py file, define:

TARGET_X = 0.5
TARGET_Y = 0.5
(Values that the robot is capable of reaching)

## How to Test — FAIL Condition
Change the values to unreachable coordinates:

TARGET_X = 99.0
TARGET_Y = 99.0

## Running the Tests
Execute the following commands to build the workspace and run the test suite:

```bash
# Source ROS Noetic environment
source /opt/ros/noetic/setup.bash

# Build and source the workspace
cd ~/simulation_ws && catkin_make && source devel/setup.bash

# Run the test
rostest tortoisebot_waypoints waypoints_test.test --reuse-master
```