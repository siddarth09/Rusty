#!/bin/sh
xterm  -e  " roslaunch rusty gazebo.launch " &
sleep 5
xterm  -e  " roslaunch rusty gmapping.launch" & 
sleep 5
xterm  -e  " roslaunch rusty teleop_key.launch" 