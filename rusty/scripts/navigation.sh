#!/bin/sh
xterm  -e  " roslaunch rusty gazebo.launch " &
sleep 5
xterm  -e  " roslaunch rusty navigation.launch" & 
sleep 5
