#include "rclcpp/rclcpp.hpp"
#include "example_interfaces/msg/string.hpp"

class MinimalSubscriber : public rclcpp::Node 
{

public:

  MinimalSubscriber() : Node("minimal_subscriber")
  {
    subscriber_ = this->create_subscription<example_interfaces::msg::String>(
      "my_topic",
      10,
      std::bind(
        &MinimalSubscriber::listener_callback,
        this,
        std::placeholders::_1
      )
    );
  }

private:
  
  rclcpp::Subscription<example_interfaces::msg::String>::SharedPtr subscriber_;

  void listener_callback(const example_interfaces::msg::String& msg)
  {
    RCLCPP_INFO(this->get_logger(), "Received message: '%s'", msg.data.c_str());
  }

};

int main(int argc, char* argv[])
{
  rclcpp::init(argc, argv);

  auto node = std::make_shared<MinimalSubscriber>();
  rclcpp::spin(node);

  rclcpp::shutdown();

  return 0;
}