#include <memory>
#include <chrono>

#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"
#include "geometry_msgs/msg/twist.hpp"

using std::placeholders::_1;

class Subscriber : public rclcpp::Node
{
public:
    Subscriber() : Node("subscriber")
    {
        subscription_ = this->create_subscription<geometry_msgs::msg::Twist>(
            "/cmd_vel", 1000,
            std::bind(&Subscriber::topic_callback, this, _1));

        publisher_ = this->create_publisher<std_msgs::msg::String>(
            "/cmd_vel_limited", 1000);

        timer_ = this->create_wall_timer(
            std::chrono::milliseconds(1000),
            std::bind(&Subscriber::callback, this));
    }

private:
void topic_callback(const geometry_msgs::msg::Twist::SharedPtr msg)
{
    auto out_msg = std_msgs::msg::String();

    if (std::abs(msg->linear.x) > 1.0 ||
        std::abs(msg->linear.y) > 1.0 ||
        std::abs(msg->linear.z) > 1.0)
    {
        RCLCPP_WARN(this->get_logger(), "Velocity too high!");
        out_msg.data = "LIMIT EXCEEDED";
    }
    else
    {
        out_msg.data = "OK";
    }
    std::cout<<"anything";
    publisher_->publish(out_msg);
}

    void callback()
    {
        RCLCPP_INFO(this->get_logger(), "Timer running...");
    }

    rclcpp::Publisher<std_msgs::msg::String>::SharedPtr publisher_;
    rclcpp::Subscription<geometry_msgs::msg::Twist>::SharedPtr subscription_;
    rclcpp::TimerBase::SharedPtr timer_;
};

int main(int argc, char *argv[])
{
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<Subscriber>());
    rclcpp::shutdown();
    return 0;
}