#include <ros/ros.h>
#include <move_base_msgs/MoveBaseAction.h>
#include <actionlib/client/simple_action_client.h>
#include <iostream>

// Define a client for to send goal requests to the move_base server through a SimpleActionClient
typedef actionlib::SimpleActionClient<move_base_msgs::MoveBaseAction> MoveBaseClient;

float pose(float pose)
{
  MoveBaseClient ac("move_base", true);
  //float pose_arr[2]={-15.0,10.0};

  
  // Wait 5 sec for move_base action server to come up
  while(!ac.waitForServer(ros::Duration(5.0)))
  {
    ROS_INFO("Waiting for the move_base action server to come up");
  }

  move_base_msgs::MoveBaseGoal goal;
  goal.target_pose.header.frame_id = "map";
  goal.target_pose.header.stamp = ros::Time::now();

  ROS_INFO("GOING  TO POSITION %f",pose);
  goal.target_pose.pose.position.x = pose;
  goal.target_pose.pose.orientation.w = 1.0;
    
    
  

   // Send the goal position and orientation for the robot to reach
  ROS_INFO("Sending goal to rusty");
  ac.sendGoal(goal);

  // Wait an infinite time for the results
  ac.waitForResult();

  // Check if the robot reached its goal
  if(ac.getState() == actionlib::SimpleClientGoalState::SUCCEEDED)
    ROS_INFO("Rusty as reached");
  else
    ROS_INFO("Rusty could not reach ");

  return 0;
}



int main(int argc, char** argv)
{
  // Initialize the simple_navigation_goals node
  ros::init(argc, argv, "pick_drop");
  ROS_INFO("PICK GOAL");
  pose(-6.0);
  ros::Duration(0.5).sleep();
  ROS_INFO("DROP GOAL");
  pose(10.0);
  
  
  return 0;
}