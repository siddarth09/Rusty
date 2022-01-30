#include <ros/ros.h>
#include <visualization_msgs/Marker.h>

#include <iostream>
#include <nav_msgs/Odometry.h>



float po;
void posecallback(const nav_msgs::Odometry::ConstPtr& msg)
{
    po=msg->pose.pose.position.x;
    std::cout<<"POSITION:"<<po;
}

int main(int argc,char **argv)
{
  ros::init(argc, argv, "basic_shapes");
  ros::NodeHandle n;
  ros::Rate r(1);
  ros::Publisher marker_pub = n.advertise<visualization_msgs::Marker>("visualization_marker", 1);

  ros::Subscriber sub=n.subscribe("odom",10,posecallback);

  uint32_t shape = visualization_msgs::Marker::CUBE;
  float position_arr[2]={-6.0,10.0};
  for (int i=0;i<3;i++)
  {
    if(po<=position_arr[i])
    {
       while (ros::ok())
        {
          visualization_msgs::Marker marker;
          
          marker.header.frame_id = "/map";
          marker.header.stamp = ros::Time::now();
          marker.ns = "BOX";
          marker.id = 0;
          marker.type = shape;
          marker.action = visualization_msgs::Marker::ADD;

          marker.pose.position.x = po;
          ROS_INFO("POSITION:%f",po);
          marker.pose.position.y = 0;
          marker.pose.position.z = 0;
          marker.pose.orientation.x = 0.0;
          marker.pose.orientation.y = 0.0;
          marker.pose.orientation.z = 0.0;
          marker.pose.orientation.w = 1.0;

          marker.scale.x = 3.0;
          marker.scale.y = 3.0;
          marker.scale.z = 2.0;

          marker.color.r = 0.0f;
          marker.color.g = 1.0f;
          marker.color.b = 0.0f;
          marker.color.a = 1.0;
          marker.lifetime = ros::Duration(20);

          while (marker_pub.getNumSubscribers() >= 1)
          {
            if (!ros::ok())
            {
              return 0;
            }
            ROS_WARN_ONCE("Please create a subscriber to the marker");
            sleep(1);
          }
          marker_pub.publish(marker);
          r.sleep();
        }
       

       ros::Duration(5.0).sleep();
      
    }
  }
  
  
 
}
