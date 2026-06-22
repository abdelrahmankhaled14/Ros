#include <memory>

#include "rclcpp/rclcpp.hpp"

#include "rclcpp/qos.hpp"

#include "sensor_msgs/msg/imu.h"

using std::placeholders::_1;

class orientation_analysis : public rclcpp::Node {
public:
  orientation_analysis() : Node("orientation_analysis") {
    // Create the subscription listening on "topic" with queue size 10
    // _1 stands for "the first argument passed to the callback."
    // When ROS 2 receives a message, it calls your callback and "hands over" that message. 
    //_1 tells std::bind: "When you get an argument from ROS, take that first argument
    //  and plug it into the topic_callback function."

    subscription_imu_data_ = this->create_subscription<>(
      "/imu/data", 10, std::bind(&orientation_analysis::topic_callback, this, _1));

    subscription_ = this->create_subscription<std_msgs::msg::String>(
      "topic", 10, std::bind(&orientation_analysis::topic_callback, this, _1));

  }

private:
  void topic_callback(const std_msgs::msg::String & msg) const {
    RCLCPP_INFO(this->get_logger(), "I heard: '%s'", msg.data.c_str());
  }
  
  rclcpp::Subscription<sensor_msgs::msg::Imu>::SharedPtr subscription_imu_data_;
  rclcpp::Subscription<std_msgs::msg::String>::SharedPtr subscription_ekf_data_;
};

int main(int argc, char * argv[]) {
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<orientation_analysis>());
  rclcpp::shutdown();
  return 0;
}