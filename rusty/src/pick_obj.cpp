#include <ros/ros.h>
#include <move_base_msgs/MoveBaseAction.h>
#include <actionlib/client/simple_action_client.h>
#include <std_msgs/UInt8.h>

typedef actionlib::SimpleActionClient<move_base_msgs::MoveBaseAction> MoveBaseClient;


int main(int argc, char** argv){
  // Initialize the simple_navigation_goals node
  ros::init(argc, argv, "pick_objects");
  ros::NodeHandle n;
  
  MoveBaseClient ac("move_base", true);
  //set up publisher to broadcast if robot is at goal marker
  ros::Publisher pub = n.advertise<std_msgs::UInt8>("/goal", 1);
  // Wait 5 sec for move_base action server to come up
  while(!ac.waitForServer(ros::Duration(5.0))){
    ROS_INFO("Waiting for the move_base action server to come up");
  }

  move_base_msgs::MoveBaseGoal goal;	
  std_msgs::UInt8 delivery_data;
  ROS_INFO("PARAM loaded");
  goal.target_pose.header.frame_id = "map";
  goal.target_pose.header.stamp = ros::Time::now();
  
  n.getParam("/pick_up/x", goal.target_pose.pose.position.x);
  n.getParam("/pick_up/w", goal.target_pose.pose.orientation.w);

  ac.sendGoal(goal);

  ac.waitForResult();

  if (ac.getState()==actionlib::SimpleClientGoalState::SUCCEEDED)
  {
    delivery_data.data = 1;
    pub.publish(delivery_data);
    ROS_INFO("PICK UP REACHED");
  }
  else{
    delivery_data.data = 2;
    pub.publish(delivery_data);
    ROS_INFO("Rusty did not reach the location");
  }

  //DROP Sequence
  ros::Duration(5).sleep();

  n.getParam("/drop/x", goal.target_pose.pose.position.x);
  n.getParam("/drop/w", goal.target_pose.pose.orientation.w);

  ac.sendGoal(goal);

  ac.waitForResult();

  if (ac.getState()==actionlib::SimpleClientGoalState::SUCCEEDED)
  {
    delivery_data.data = 3;
    pub.publish(delivery_data);
    ROS_INFO("PICK UP REACHED");
  }
  else{
    delivery_data.data = 2;
    pub.publish(delivery_data);
    ROS_INFO("Rusty did not reach the location");
  }
  return 0;
}
