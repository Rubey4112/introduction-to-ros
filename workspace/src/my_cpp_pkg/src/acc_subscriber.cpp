#include "rclcpp/rclcpp.hpp"
#include "my_interfaces/msg/accelerometer.hpp"

class AccSubscriber : public rclcpp::Node 
{

public:

  AccSubscriber() : Node("acc_subscriber")
  {
    subscriber_ = this->create_subscription<my_interfaces::msg::Accelerometer>(
      "my_acc",
      10,
      std::bind(
        &AccSubscriber::listener_callback,
        this,
        std::placeholders::_1
      )
    );
  }

private:
  
  rclcpp::Subscription<my_interfaces::msg::Accelerometer>::SharedPtr subscriber_;

  void listener_callback(const my_interfaces::msg::Accelerometer& msg)
  {
    RCLCPP_INFO(this->get_logger(), "Accelerometer: x=%.2f, y=%.2f, z=%.2f", msg.x, msg.y, msg.z);
  }

};

int main(int argc, char* argv[])
{
  rclcpp::init(argc, argv);

  auto node = std::make_shared<AccSubscriber>();
  rclcpp::spin(node);

  rclcpp::shutdown();

  return 0;
}