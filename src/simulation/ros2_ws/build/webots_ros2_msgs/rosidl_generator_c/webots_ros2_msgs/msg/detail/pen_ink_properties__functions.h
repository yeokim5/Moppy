// generated from rosidl_generator_c/resource/idl__functions.h.em
// with input from webots_ros2_msgs:msg/PenInkProperties.idl
// generated code does not contain a copyright notice

#ifndef WEBOTS_ROS2_MSGS__MSG__DETAIL__PEN_INK_PROPERTIES__FUNCTIONS_H_
#define WEBOTS_ROS2_MSGS__MSG__DETAIL__PEN_INK_PROPERTIES__FUNCTIONS_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stdlib.h>

#include "rosidl_runtime_c/visibility_control.h"
#include "webots_ros2_msgs/msg/rosidl_generator_c__visibility_control.h"

#include "webots_ros2_msgs/msg/detail/pen_ink_properties__struct.h"

/// Initialize msg/PenInkProperties message.
/**
 * If the init function is called twice for the same message without
 * calling fini inbetween previously allocated memory will be leaked.
 * \param[in,out] msg The previously allocated message pointer.
 * Fields without a default value will not be initialized by this function.
 * You might want to call memset(msg, 0, sizeof(
 * webots_ros2_msgs__msg__PenInkProperties
 * )) before or use
 * webots_ros2_msgs__msg__PenInkProperties__create()
 * to allocate and initialize the message.
 * \return true if initialization was successful, otherwise false
 */
ROSIDL_GENERATOR_C_PUBLIC_webots_ros2_msgs
bool
webots_ros2_msgs__msg__PenInkProperties__init(webots_ros2_msgs__msg__PenInkProperties * msg);

/// Finalize msg/PenInkProperties message.
/**
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_webots_ros2_msgs
void
webots_ros2_msgs__msg__PenInkProperties__fini(webots_ros2_msgs__msg__PenInkProperties * msg);

/// Create msg/PenInkProperties message.
/**
 * It allocates the memory for the message, sets the memory to zero, and
 * calls
 * webots_ros2_msgs__msg__PenInkProperties__init().
 * \return The pointer to the initialized message if successful,
 * otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_webots_ros2_msgs
webots_ros2_msgs__msg__PenInkProperties *
webots_ros2_msgs__msg__PenInkProperties__create();

/// Destroy msg/PenInkProperties message.
/**
 * It calls
 * webots_ros2_msgs__msg__PenInkProperties__fini()
 * and frees the memory of the message.
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_webots_ros2_msgs
void
webots_ros2_msgs__msg__PenInkProperties__destroy(webots_ros2_msgs__msg__PenInkProperties * msg);

/// Check for msg/PenInkProperties message equality.
/**
 * \param[in] lhs The message on the left hand size of the equality operator.
 * \param[in] rhs The message on the right hand size of the equality operator.
 * \return true if messages are equal, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_webots_ros2_msgs
bool
webots_ros2_msgs__msg__PenInkProperties__are_equal(const webots_ros2_msgs__msg__PenInkProperties * lhs, const webots_ros2_msgs__msg__PenInkProperties * rhs);

/// Copy a msg/PenInkProperties message.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source message pointer.
 * \param[out] output The target message pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer is null
 *   or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_webots_ros2_msgs
bool
webots_ros2_msgs__msg__PenInkProperties__copy(
  const webots_ros2_msgs__msg__PenInkProperties * input,
  webots_ros2_msgs__msg__PenInkProperties * output);

/// Initialize array of msg/PenInkProperties messages.
/**
 * It allocates the memory for the number of elements and calls
 * webots_ros2_msgs__msg__PenInkProperties__init()
 * for each element of the array.
 * \param[in,out] array The allocated array pointer.
 * \param[in] size The size / capacity of the array.
 * \return true if initialization was successful, otherwise false
 * If the array pointer is valid and the size is zero it is guaranteed
 # to return true.
 */
ROSIDL_GENERATOR_C_PUBLIC_webots_ros2_msgs
bool
webots_ros2_msgs__msg__PenInkProperties__Sequence__init(webots_ros2_msgs__msg__PenInkProperties__Sequence * array, size_t size);

/// Finalize array of msg/PenInkProperties messages.
/**
 * It calls
 * webots_ros2_msgs__msg__PenInkProperties__fini()
 * for each element of the array and frees the memory for the number of
 * elements.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_webots_ros2_msgs
void
webots_ros2_msgs__msg__PenInkProperties__Sequence__fini(webots_ros2_msgs__msg__PenInkProperties__Sequence * array);

/// Create array of msg/PenInkProperties messages.
/**
 * It allocates the memory for the array and calls
 * webots_ros2_msgs__msg__PenInkProperties__Sequence__init().
 * \param[in] size The size / capacity of the array.
 * \return The pointer to the initialized array if successful, otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_webots_ros2_msgs
webots_ros2_msgs__msg__PenInkProperties__Sequence *
webots_ros2_msgs__msg__PenInkProperties__Sequence__create(size_t size);

/// Destroy array of msg/PenInkProperties messages.
/**
 * It calls
 * webots_ros2_msgs__msg__PenInkProperties__Sequence__fini()
 * on the array,
 * and frees the memory of the array.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_webots_ros2_msgs
void
webots_ros2_msgs__msg__PenInkProperties__Sequence__destroy(webots_ros2_msgs__msg__PenInkProperties__Sequence * array);

/// Check for msg/PenInkProperties message array equality.
/**
 * \param[in] lhs The message array on the left hand size of the equality operator.
 * \param[in] rhs The message array on the right hand size of the equality operator.
 * \return true if message arrays are equal in size and content, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_webots_ros2_msgs
bool
webots_ros2_msgs__msg__PenInkProperties__Sequence__are_equal(const webots_ros2_msgs__msg__PenInkProperties__Sequence * lhs, const webots_ros2_msgs__msg__PenInkProperties__Sequence * rhs);

/// Copy an array of msg/PenInkProperties messages.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source array pointer.
 * \param[out] output The target array pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer
 *   is null or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_webots_ros2_msgs
bool
webots_ros2_msgs__msg__PenInkProperties__Sequence__copy(
  const webots_ros2_msgs__msg__PenInkProperties__Sequence * input,
  webots_ros2_msgs__msg__PenInkProperties__Sequence * output);

#ifdef __cplusplus
}
#endif

#endif  // WEBOTS_ROS2_MSGS__MSG__DETAIL__PEN_INK_PROPERTIES__FUNCTIONS_H_
