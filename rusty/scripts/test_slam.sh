#!/bin/sh
xterm  -e  " roslaunch rusty gazebo.launch " &
sleep 5
xterm  -e  " roslaunch rusty kartoSLAM.launch" & 
sleep 5
xterm  -e  " roslaunch rusty teleop_key.launch" 
