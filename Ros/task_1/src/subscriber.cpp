#include <memory>
#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/int32.hpp"

class AdderSubscriber : public rclcpp::Node {
public:
  AdderSubscriber() : Node("adder_subscriber"), topic_1(0), topic_2(0) {
    sub1_ = this->create_subscription<std_msgs::msg::Int32>(
      "topic_1", 10,
      [ this ](const std_msgs::msg::Int32::SharedPtr msg) {
        topic_1 = msg->data;          
        print_sum();                
      });

    sub2_ = this->create_subscription<std_msgs::msg::Int32>(
      "topic_2", 10,
      [ this ](const std_msgs::msg::Int32::SharedPtr msg) {
        topic_2 = msg->data;          
        print_sum();
      });
  }

private:
  void callback1(const std_msgs::msg::Int32::SharedPtr msg) {
    topic_1 = msg->data;          
    print_sum();                
  }

  void callback2(const std_msgs::msg::Int32::SharedPtr msg) {
    topic_2 = msg->data;          
    print_sum();
  }

  void print_sum() {
    int sum = topic_1 + topic_2;
    RCLCPP_INFO(this->get_logger(),
                "topic_1=%d  +  topic_2=%d  =  %d", topic_1, topic_2, sum);
  }

  rclcpp::Subscription<std_msgs::msg::Int32>::SharedPtr sub1_;
  rclcpp::Subscription<std_msgs::msg::Int32>::SharedPtr sub2_;

  int topic_1;
  int topic_2;
};

int main(int argc, char * argv[]) {
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<AdderSubscriber>());
  rclcpp::shutdown();
  return 0;
}