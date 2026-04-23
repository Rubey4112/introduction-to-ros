#include <random>

#include "rclcpp/rclcpp.hpp"

#include "geometry_msgs/msg/point.hpp"
#include "my_interfaces/srv/trigger_points.hpp"

class TriggerPointsClient : public rclcpp::Node
{

public:

    TriggerPointsClient() : Node("trigger_points_client")
    {
        this->client_ = this->create_client<my_interfaces::srv::TriggerPoints>("trigger_points");

        while (!client_->wait_for_service(std::chrono::seconds(2)))
        {
            RCLCPP_WARN(this->get_logger(), "Waiting for service...");
        }
        std::srand(std::time(nullptr));

        timer_ = this->create_wall_timer(std::chrono::seconds(2), std::bind(&TriggerPointsClient::timer_callback, this));
    }

private:

    rclcpp::Client<my_interfaces::srv::TriggerPoints>::SharedPtr client_;
    rclcpp::TimerBase::SharedPtr timer_;

    void timer_callback()
    {
        auto req = std::make_shared<my_interfaces::srv::TriggerPoints::Request>();
        req->num_points = std::rand() % 11;

        client_->async_send_request(req, std::bind(&TriggerPointsClient::response_callback, this, std::placeholders::_1));
    }

    void response_callback(rclcpp::Client<my_interfaces::srv::TriggerPoints>::SharedFuture future)
    {
        auto resp = future.get();
        RCLCPP_INFO(this->get_logger(), "Success: %s", resp->success ? "true" : "false");

        for (const auto& point : resp->points)
        {
            RCLCPP_INFO(this->get_logger(), "Point: x=%.3f, y=%.3f, z=%.3f", point.x, point.y, point.z);
        }
    }

};

int main(int argc, char* argv[])
{
    rclcpp::init(argc, argv);

    auto node = std::make_shared<TriggerPointsClient>();

    rclcpp::spin(node);
    rclcpp::shutdown();

    return 0;
}