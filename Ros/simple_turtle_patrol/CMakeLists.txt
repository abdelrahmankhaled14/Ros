cmake_minimum_required(VERSION 3.8)
project(simple_turtle_patrol)
if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()
# find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(std_srvs REQUIRED)
find_package(turtlesim REQUIRED)
find_package(rosidl_default_generators REQUIRED)


# what i added for the custom message
rosidl_generate_interfaces(${PROJECT_NAME}
  "msg/RobotStatus.msg"
  DEPENDENCIES geometry_msgs
)

# Install the launch directory so ros2 launch can find the file
install(DIRECTORY launch params DESTINATION share/${PROJECT_NAME})

#for the nodes Executables
add_executable(patrol_controller src/patrol_controller.cpp)
ament_target_dependencies(patrol_controller rclcpp geometry_msgs std_srvs turtlesim)

add_executable(status_publisher src/status_publisher.cpp)
ament_target_dependencies(status_publisher rclcpp geometry_msgs std_srvs turtlesim)

# Install targets
install(TARGETS
  patrol_controller
  status_publisher
  DESTINATION lib/${PROJECT_NAME}
)
#to make the custom message available to the nodes
rosidl_get_typesupport_target(cpp_typesupport_target ${PROJECT_NAME} "rosidl_typesupport_cpp")
target_link_libraries(status_publisher "${cpp_typesupport_target}")


if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  # the following line skips the linter which checks for copyrights
  # comment the line when a copyright and license is added to all source files
  set(ament_cmake_copyright_FOUND TRUE)
  # the following line skips cpplint (only works in a git repo)
  # comment the line when this package is in a git repo and when
  # a copyright and license is added to all source files
  set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()
