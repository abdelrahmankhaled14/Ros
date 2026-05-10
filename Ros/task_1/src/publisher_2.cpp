
#include <chrono>
#include <functional>
#include <memory>
#include <iostream>

#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/int32.hpp"   

using namespace std::chrono_literals;

class Publisher : public rclcpp::Node {
public:
  
  Publisher(int value) : Node("publisher"), value_(value) {
    publisher_ = this->create_publisher<std_msgs::msg::Int32>("topic_2", 10);
    timer_ = this->create_wall_timer(
      500ms, std::bind(&Publisher::timer_callback, this));
  }

private:
  void timer_callback() {
    auto message = std_msgs::msg::Int32();   
    message.data = value_;                    
    RCLCPP_INFO(this->get_logger(), "Publishing: '%d'", message.data);
    publisher_->publish(message);
  }

  rclcpp::TimerBase::SharedPtr timer_;
  rclcpp::Publisher<std_msgs::msg::Int32>::SharedPtr publisher_;  
  int value_;   
};

int main(int argc, char * argv[]) {
  int input;
  std::cout << "Enter a number to publish: ";
  std::cin >> input;

  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<Publisher>(input));   
  rclcpp::shutdown();
  return 0;
}