
#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/int32.hpp"
#include <chrono>
#include <fstream>
#include <string>

class Temp_publisher : public rclcpp::Node
{
public:
    Temp_publisher() : Node("temp_publisher")
    {
        publisher_ = this->create_publisher<std_msgs::msg::Int32>("topic1", 10);

        timer_ = this->create_wall_timer(
            std::chrono::milliseconds(500),
            std::bind(&Temp_publisher::timer_callback, this)
        );
    }

private:
    void timer_callback()
    {
        std::ifstream file("/sys/class/thermal/thermal_zone0/temp");

        if (!file.is_open())
        {
            RCLCPP_ERROR(this->get_logger(), "Failed to open temperature file");
            return;
        }

        int temp_raw;
        file >> temp_raw;   // read directly as int

        int temp_c = temp_raw;  // convert from millidegree

        auto message = std_msgs::msg::Int32();
        message.data = temp_c;

        RCLCPP_INFO(this->get_logger(), "Publishing: %d °C", message.data);
        publisher_->publish(message);
        file.close();
    }

    rclcpp::TimerBase::SharedPtr timer_;
    rclcpp::Publisher<std_msgs::msg::Int32>::SharedPtr publisher_;
};

int main(int argc, char * argv[])
{
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<Temp_publisher>());
    rclcpp::shutdown();
    return 0;
}