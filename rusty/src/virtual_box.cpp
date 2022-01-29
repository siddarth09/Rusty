#include <ros/ros.h>
#include <visualization_msgs/Marker.h>

float position( float pose )
{
    ros::NodeHandle n;
    ros::Rate r(1);
   ros::Publisher marker_pub = n.advertise<visualization_msgs::Marker>("visualization_marker", 1);

  uint32_t shape = visualization_msgs::Marker::CUBE;
  while (ros::ok())
  {
    visualization_msgs::Marker marker;
    // Set the frame ID and timestamp.  See the TF tutorials for information on these.
    marker.header.frame_id = "/map";
    marker.header.stamp = ros::Time::now();
    marker.ns = "BOX";
    marker.id = 0;
    marker.type = shape;
    marker.action = visualization_msgs::Marker::ADD;

    marker.pose.position.x = pose;
    ROS_INFO("POSITION:%f",pose);
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

    // Cycle between different shapes
   

    r.sleep();
    return 0.0;
  }
}
int main(int argc,char **argv)
{
    ros::init(argc, argv, "basic_shapes");
    ROS_INFO("PICK OBJECT");
    position(-6.0);
    ros::Duration(0.5).sleep();
    ROS_INFO("DROP OBJECT");
    position(25.0);
    return 0;
}