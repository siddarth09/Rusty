#include <ros/ros.h>
#include <visualization_msgs/Marker.h>
// #include <nav_msgs/Odometry.h>
#include <std_msgs/UInt8.h>

u_int8_t state=0;

void goalCallback(const std_msgs::UInt8::ConstPtr& msg)
{
   state = msg->data;
   return;
}

int main( int argc, char** argv )
{
  ros::init(argc, argv, "add_markers");

  ros::NodeHandle n;
  ros::Rate r(5);
  ros::Publisher marker_pub = n.advertise<visualization_msgs::Marker>("visualization_marker", 1);
  ros::Subscriber sub = n.subscribe("/goal", 1, goalCallback);
  bool service_done = false;

  // Set our initial shape type to be a cube
  uint32_t shape = visualization_msgs::Marker::CUBE;

  ROS_INFO("Subscribed to desired goal-position");

  while (ros::ok()) {
    
    ros::spinOnce();
    visualization_msgs::Marker marker;
    
    marker.header.frame_id = "/map";
    marker.header.stamp = ros::Time::now();

    
    marker.ns = "Delivery_box";
    marker.id = 0;
    
    marker.type = shape;
    
    marker.scale.x = 0.5;
    marker.scale.y = 0.5;
    marker.scale.z = 0.5;
    

    
    marker.color.r = 0.0f;
    marker.color.g = 0.0f;
    marker.color.b = 1.0f;
    marker.color.a = 1.0;

    switch (state)
    {
      case 0: 
        {
          
          marker.action = visualization_msgs::Marker::ADD;
          
          n.getParam("/pick_up/x", marker.pose.position.x);
          
          n.getParam("/pick_up/w", marker.pose.orientation.w);
          break;
        } 

        case 1:   
          {
            sleep(2);
            
            marker.action = visualization_msgs::Marker::DELETE;
            break;
          } 

        case 2: 
          {
            marker.action = visualization_msgs::Marker::DELETE;
            break;
          }

        case 3:  
          {
            sleep(5);
            
            marker.action = visualization_msgs::Marker::ADD;
            
            n.getParam("/drop/x", marker.pose.position.x);
           
            n.getParam("/drop/w", marker.pose.orientation.w);
            service_done = true;
            break;
          }

    } 

   
    while (marker_pub.getNumSubscribers() < 1)
    {
      if (!ros::ok())
      {
        return 0;
      }
      ROS_WARN("Please create a subscriber to the marker");
      sleep(1);
    }

    
    marker_pub.publish(marker);

    
    if (service_done) {
      ROS_INFO(" Reached");
      sleep(7);
      return 0;
      }

    r.sleep();
  } 

  return 0;
} 
