// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from webots_ros2_msgs:srv/GetBool.idl
// generated code does not contain a copyright notice

#ifndef WEBOTS_ROS2_MSGS__SRV__DETAIL__GET_BOOL__STRUCT_HPP_
#define WEBOTS_ROS2_MSGS__SRV__DETAIL__GET_BOOL__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__webots_ros2_msgs__srv__GetBool_Request __attribute__((deprecated))
#else
# define DEPRECATED__webots_ros2_msgs__srv__GetBool_Request __declspec(deprecated)
#endif

namespace webots_ros2_msgs
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct GetBool_Request_
{
  using Type = GetBool_Request_<ContainerAllocator>;

  explicit GetBool_Request_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->ask = false;
    }
  }

  explicit GetBool_Request_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_alloc;
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->ask = false;
    }
  }

  // field types and members
  using _ask_type =
    bool;
  _ask_type ask;

  // setters for named parameter idiom
  Type & set__ask(
    const bool & _arg)
  {
    this->ask = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    webots_ros2_msgs::srv::GetBool_Request_<ContainerAllocator> *;
  using ConstRawPtr =
    const webots_ros2_msgs::srv::GetBool_Request_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<webots_ros2_msgs::srv::GetBool_Request_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<webots_ros2_msgs::srv::GetBool_Request_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      webots_ros2_msgs::srv::GetBool_Request_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<webots_ros2_msgs::srv::GetBool_Request_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      webots_ros2_msgs::srv::GetBool_Request_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<webots_ros2_msgs::srv::GetBool_Request_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<webots_ros2_msgs::srv::GetBool_Request_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<webots_ros2_msgs::srv::GetBool_Request_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__webots_ros2_msgs__srv__GetBool_Request
    std::shared_ptr<webots_ros2_msgs::srv::GetBool_Request_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__webots_ros2_msgs__srv__GetBool_Request
    std::shared_ptr<webots_ros2_msgs::srv::GetBool_Request_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const GetBool_Request_ & other) const
  {
    if (this->ask != other.ask) {
      return false;
    }
    return true;
  }
  bool operator!=(const GetBool_Request_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct GetBool_Request_

// alias to use template instance with default allocator
using GetBool_Request =
  webots_ros2_msgs::srv::GetBool_Request_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace webots_ros2_msgs


#ifndef _WIN32
# define DEPRECATED__webots_ros2_msgs__srv__GetBool_Response __attribute__((deprecated))
#else
# define DEPRECATED__webots_ros2_msgs__srv__GetBool_Response __declspec(deprecated)
#endif

namespace webots_ros2_msgs
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct GetBool_Response_
{
  using Type = GetBool_Response_<ContainerAllocator>;

  explicit GetBool_Response_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->value = false;
    }
  }

  explicit GetBool_Response_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_alloc;
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->value = false;
    }
  }

  // field types and members
  using _value_type =
    bool;
  _value_type value;

  // setters for named parameter idiom
  Type & set__value(
    const bool & _arg)
  {
    this->value = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    webots_ros2_msgs::srv::GetBool_Response_<ContainerAllocator> *;
  using ConstRawPtr =
    const webots_ros2_msgs::srv::GetBool_Response_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<webots_ros2_msgs::srv::GetBool_Response_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<webots_ros2_msgs::srv::GetBool_Response_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      webots_ros2_msgs::srv::GetBool_Response_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<webots_ros2_msgs::srv::GetBool_Response_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      webots_ros2_msgs::srv::GetBool_Response_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<webots_ros2_msgs::srv::GetBool_Response_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<webots_ros2_msgs::srv::GetBool_Response_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<webots_ros2_msgs::srv::GetBool_Response_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__webots_ros2_msgs__srv__GetBool_Response
    std::shared_ptr<webots_ros2_msgs::srv::GetBool_Response_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__webots_ros2_msgs__srv__GetBool_Response
    std::shared_ptr<webots_ros2_msgs::srv::GetBool_Response_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const GetBool_Response_ & other) const
  {
    if (this->value != other.value) {
      return false;
    }
    return true;
  }
  bool operator!=(const GetBool_Response_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct GetBool_Response_

// alias to use template instance with default allocator
using GetBool_Response =
  webots_ros2_msgs::srv::GetBool_Response_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace webots_ros2_msgs

namespace webots_ros2_msgs
{

namespace srv
{

struct GetBool
{
  using Request = webots_ros2_msgs::srv::GetBool_Request;
  using Response = webots_ros2_msgs::srv::GetBool_Response;
};

}  // namespace srv

}  // namespace webots_ros2_msgs

#endif  // WEBOTS_ROS2_MSGS__SRV__DETAIL__GET_BOOL__STRUCT_HPP_
