#include "rclcpp/rclcpp.hpp"
#include "turtlesim/msg/pose.hpp"
#include "string"
#include "simple_turtle_patrol/msg/robot_status.hpp"

class StatusPublisher : public rclcpp::Node
{
public:
    StatusPublisher() : Node("status_publisher"), lap_count_(0), prev_theta_(0.0), first_pose_received_(false)
    {
        this->declare_parameter("status_rate", 5.0);
        double rate = this->get_parameter("status_rate").as_double();
        
        status_pub_ = this->create_publisher<simple_turtle_patrol::msg::RobotStatus>(
            "/robot/status", 10);
            
        pose_sub_ = this->create_subscription<turtlesim::msg::Pose>(
            "/turtle1/pose",
            10,
            [this](const turtlesim::msg::Pose::SharedPtr msg)
            {
                currentpose_ = *msg;

                if (first_pose_received_)
                {
                    if (prev_theta_ > 2.0 && msg->theta < -2.0)
                    {
                        lap_count_++;
                        RCLCPP_INFO(this->get_logger(), "Lap completed! Total laps: %d", lap_count_);
                    }
                }
                else
                {
                    first_pose_received_ = true;
                }
                prev_theta_ = msg->theta;
            });
            
        auto interval = std::chrono::milliseconds(static_cast<int>(1000.0 / rate));
        timer_ = this->create_wall_timer(interval, [this]()
        {
            if (!first_pose_received_)
            {
                return;
            }
            auto status_msg = simple_turtle_patrol::msg::RobotStatus();
            status_msg.pose.x = currentpose_.x;
            status_msg.pose.y = currentpose_.y;
            status_msg.pose.theta = currentpose_.theta;
            
            if (std::abs(currentpose_.linear_velocity) < 0.01 && std::abs(currentpose_.angular_velocity) < 0.01)
            {
                status_msg.state = "stopped";
            }
            else
            {
                status_msg.state = "running";
            }

            status_msg.lap_count = lap_count_;
            status_msg.temperature = 25.0f + (lap_count_ * 1.5f) + (currentpose_.linear_velocity * 2.0f);

            status_pub_->publish(status_msg);
        });

        RCLCPP_INFO(this->get_logger(), "Status Publisher started.");
    }

private:
    int lap_count_;
    float prev_theta_;
    bool first_pose_received_;
    turtlesim::msg::Pose currentpose_;
    rclcpp::Publisher<simple_turtle_patrol::msg::RobotStatus>::SharedPtr status_pub_;
    rclcpp::Subscription<turtlesim::msg::Pose>::SharedPtr pose_sub_;
    rclcpp::TimerBase::SharedPtr timer_;
};

int main(int argc, char **argv)
{
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<StatusPublisher>());
    rclcpp::shutdown();
    return 0;
}