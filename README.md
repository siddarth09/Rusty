# Rusty

RUSTY is a warhouse robot capable of perfoming various tasks for a warehouse. 

![rusty v7](https://user-images.githubusercontent.com/60263608/148347287-8ba007b6-cd7a-4cb1-b73e-20ba1fec99a9.png)

## Installation

```bash
roscd
cd ../src
git clone https://github.com/siddarth09/Rusty.git
cd ..
catkin_make
```

## KALMAN FILTER 

This folder contains basic understanding of the kalman filter for 1-Dimensiona and multidimensional filters.

> The kalman filter is basically used to localise a robot in its environment by given sensor measurements.
> STEPS INVOLVED:
- Measurement update
- State transition update or motion update

## 3D mapping:
> Real time apperaence based mapping or RTAB-map is used to 3D map the environnment by using a laser scanner and a depth camera attached to the bot 
This mapping is one type of Graph-based SLAM which involves two mechanisms
- Front end: sensor update, Odometry update and loop closure 
- Back end: Graph Optimization, 2D or 3D map generation 
> IMPORTANT TERMINOLOGY:- 
1.Loop closure: Process of finding a match between the current and previously listed location. It uses visual bag of words and updates iteratively by checking and filtering through extraction of features in the map



##### LINK FOR THE RTAB-MAP DB file
- https://drive.google.com/file/d/1NHoYihwiK1kxBYBL2nZ9Up3olNRXoLSu/view?usp=sharing

## SLAM
Simultaneous localization and mapping (SLAM) is the computational problem of constructing or updating a map of an unknown environment while simultaneously keeping track of an agent's location within it. Here we are using RTAB-mapping, gmapping, Karto-slam packages to map the given environment for navigation purposes

To run Gmapping package
``` bash
roslaunch rusty gmapping.launch
```
To run Karto-SLAM package
```bash
roslaunch rusty karto_slam.launch
````
## NAVIGATION STACK
The navigation stack is updated with DWA planner algorithm which uses Djikastra's algorithm to find the shortest optimal path.

To use the navigation stack 
```bash
roslaunch rusty navigation.launch 
```
> -Fine tune the parameters per use case
> -Also to use the custom map file, you can specify the map_file:= <path of mapfile> 
  
  
## Different world available:
  
 - House-world, consits of a big map for the robot to be used a home service robot to pick and place objects
 - Office-world, small area for the robot to transverse itself in narrow spaces
 - Godown-world
  
  ```bash
  roslaunch rusty gazbeo.launch world_name:= <path-to-your-desired-world>
  ```
 
# USE CASES
  ## CASE 1: HOME SERVICE ROBOT
  Here rusty is used to pick and place virtual objects from one location to another.
  ```bash
  roslaunch rusty HomeService.launch 
  ```
  or
  ```bash
  
  ./homeservice.sh
  ```
