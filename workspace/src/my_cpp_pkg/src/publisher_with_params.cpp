#include "rclcpp/rclcpp.hpp"
#include "example_interfaces/msg/string.hpp"

class PublisherWithParams : public rclcpp::Node
{

public:
  
  PublisherWithParams() : Node{"publisher_with_params"} // Call the parent constructor from the initilizer list 
  {
    this->declare_parameter("message", "Hello");
    this->declare_parameter("timer_period", 1.0);

    message_ = this->get_parameter("message").as_string();
    timer_period_ = this->get_parameter("timer_period").as_double();
    
    param_cb_handle_ = this->add_post_set_parameters_callback(std::bind(&PublisherWithParams::post_parameters_callback, this, std::placeholders::_1));

    publisher_ = this->create_publisher<example_interfaces::msg::String>("my_topic", 10);
    timer_ = this->create_wall_timer(std::chrono::duration<double>(timer_period_), std::bind(&PublisherWithParams::timer_callback, this));

  }

private:
  // Member varibles
  rclcpp::Publisher<example_interfaces::msg::String>::SharedPtr publisher_;
  rclcpp::TimerBase::SharedPtr timer_;
  rclcpp::node_interfaces::PostSetParametersCallbackHandle::SharedPtr param_cb_handle_;
  std::string message_;
  double timer_period_;
  
  // Private methods
  void post_parameters_callback(const std::vector<rclcpp::Parameter> &parameters) {
    
    for (const auto &param : parameters) {
        if (param.get_name() == "message") {
          message_ = param.as_string();
          RCLCPP_INFO(this->get_logger(), "Set %s to %s", param.get_name().c_str(), param.as_string().c_str());
        }
        else if (param.get_name() == "timer_period"){
          timer_period_ = param.as_double();
          RCLCPP_INFO(this->get_logger(), "Set %s to %.2lf", param.get_name().c_str(), param.as_double());

          timer_->cancel();
          timer_ = this->create_wall_timer(std::chrono::duration<double>(timer_period_), std::bind(&PublisherWithParams::timer_callback, this));
        }
        else {
          RCLCPP_WARN(this->get_logger(), "Unknown parameter: %s", param.get_name().c_str());
        }
    }

  }

  void timer_callback() {
    
    auto msg = example_interfaces::msg::String();
    msg.data = message_;

    publisher_->publish(msg);
    RCLCPP_INFO(this->get_logger(), "Publishing: %s", msg.data.c_str());

  }

};

// Entry point
int main(int argc, char* argv[]) {
  
  rclcpp::init(argc, argv);

  auto node = std::make_shared<PublisherWithParams>();
  rclcpp::spin(node);

  rclcpp::shutdown();

  return 0;
}