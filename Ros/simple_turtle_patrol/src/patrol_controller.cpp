#include "rclcpp/rclcpp.hpp"
#include "geometry_msgs/msg/twist.hpp"
#include "std_srvs/srv/empty.hpp"

class PatrolController : public rclcpp::Node
{
public:
    PatrolController() : Node("patrol_controller"), is_running_(true)
    {
        this->declare_parameter("linear_speed", 1.5);
        this->declare_parameter("angular_speed", 1.0);

        linear_speed_ = this->get_parameter("linear_speed").as_double();
        angular_speed_ = this->get_parameter("angular_speed").as_double();

        param_sub_ = this->add_on_set_parameters_callback(
            [this](const std::vector<rclcpp::Parameter> &params)
            {
                rcl_interfaces::msg::SetParametersResult result;
                result.successful = true;
                for (const auto &param : params)
                {
                    if (param.get_name() == "linear_speed")
                    {
                        linear_speed_ = param.as_double();
                    }
                    else if (param.get_name() == "angular_speed")
                    {
                        angular_speed_ = param.as_double();
                    }
                }
                return result;
            });

        cmd_vel_pub_ = this->create_publisher<geometry_msgs::msg::Twist>("/turtle1/cmd_vel", 10);

        stop_service_ = this->create_service<std_srvs::srv::Empty>(
            "/stop",
            [this](const std::shared_ptr<std_srvs::srv::Empty::Request> req,
                   std::shared_ptr<std_srvs::srv::Empty::Response> res)
            {
                (void)req;
                (void)res;
                is_running_ = false;
                RCLCPP_INFO(this->get_logger(), "Service /stop called. Turtle stopped.");
            });

        continue_service_ = this->create_service<std_srvs::srv::Empty>(
            "/continue",
            [this](const std::shared_ptr<std_srvs::srv::Empty::Request> req,
                   std::shared_ptr<std_srvs::srv::Empty::Response> res)
            {
                (void)req;
                (void)res;
                is_running_ = true;
                RCLCPP_INFO(this->get_logger(), "Service /continue called. Turtle resuming patrol.");
            });

        timer_ = this->create_wall_timer(
            std::chrono::milliseconds(100),
            [this]()
            {
                auto msg = geometry_msgs::msg::Twist();
                if (is_running_)
                {
                    msg.linear.x = linear_speed_;
                    msg.angular.z = angular_speed_;
                }
                else
                {
                    msg.linear.x = 0.0;
                    msg.angular.z = 0.0;
                }
                cmd_vel_pub_->publish(msg);
            });

        RCLCPP_INFO(this->get_logger(), "Patrol Controller started. Turtle is moving.");
    }

private:
    bool is_running_;
    double linear_speed_;
    double angular_speed_;

    rclcpp::Publisher<geometry_msgs::msg::Twist>::SharedPtr cmd_vel_pub_;
    rclcpp::Service<std_srvs::srv::Empty>::SharedPtr stop_service_;
    rclcpp::Service<std_srvs::srv::Empty>::SharedPtr continue_service_;
    rclcpp::TimerBase::SharedPtr timer_;
    rclcpp::node_interfaces::OnSetParametersCallbackHandle::SharedPtr param_sub_;
};

int main(int argc, char **argv)
{
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<PatrolController>());
    rclcpp::shutdown();
    return 0;
}