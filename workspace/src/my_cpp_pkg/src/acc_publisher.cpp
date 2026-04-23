#include "rclcpp/rclcpp.hpp"
#include "my_interfaces/msg/accelerometer.hpp"

class AccPublisher : public rclcpp::Node
{

public:
  
  AccPublisher() : Node{"acc_publisher"}, counter_{0} // Call the parent constructor from the initilizer list 
  {

    publisher_ = this->create_publisher<my_interfaces::msg::Accelerometer>("my_acc", 10);

    timer_ = this->create_wall_timer(std::chrono::milliseconds(500), std::bind(&AccPublisher::timer_callback, this));

  }

private:
  // Member varibles
  rclcpp::Publisher<my_interfaces::msg::Accelerometer>::SharedPtr publisher_;
  rclcpp::TimerBase::SharedPtr timer_;
  size_t counter_;

  // Private methods
  void timer_callback() {
    
    auto msg = my_interfaces::msg::Accelerometer();
    msg.x = 0.5;
    msg.y = 0.1;
    msg.z = -9.81;

    publisher_->publish(msg);
    RCLCPP_INFO(this->get_logger(), "Publishing: x=%.2f, y=%.2f, z=%.2f", msg.x, msg.y, msg.z);

    counter_++;
  }
};

// Entry point
int main(int argc, char* argv[]) {
  
  rclcpp::init(argc, argv);

  auto node = std::make_shared<AccPublisher>();
  rclcpp::spin(node);

  rclcpp::shutdown();

  return 0;
}