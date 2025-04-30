// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from webots_ros2_msgs:srv/EmitterSendString.idl
// generated code does not contain a copyright notice
#include "webots_ros2_msgs/srv/detail/emitter_send_string__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"

// Include directives for member types
// Member `value`
#include "rosidl_runtime_c/string_functions.h"

bool
webots_ros2_msgs__srv__EmitterSendString_Request__init(webots_ros2_msgs__srv__EmitterSendString_Request * msg)
{
  if (!msg) {
    return false;
  }
  // value
  if (!rosidl_runtime_c__String__init(&msg->value)) {
    webots_ros2_msgs__srv__EmitterSendString_Request__fini(msg);
    return false;
  }
  return true;
}

void
webots_ros2_msgs__srv__EmitterSendString_Request__fini(webots_ros2_msgs__srv__EmitterSendString_Request * msg)
{
  if (!msg) {
    return;
  }
  // value
  rosidl_runtime_c__String__fini(&msg->value);
}

bool
webots_ros2_msgs__srv__EmitterSendString_Request__are_equal(const webots_ros2_msgs__srv__EmitterSendString_Request * lhs, const webots_ros2_msgs__srv__EmitterSendString_Request * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // value
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->value), &(rhs->value)))
  {
    return false;
  }
  return true;
}

bool
webots_ros2_msgs__srv__EmitterSendString_Request__copy(
  const webots_ros2_msgs__srv__EmitterSendString_Request * input,
  webots_ros2_msgs__srv__EmitterSendString_Request * output)
{
  if (!input || !output) {
    return false;
  }
  // value
  if (!rosidl_runtime_c__String__copy(
      &(input->value), &(output->value)))
  {
    return false;
  }
  return true;
}

webots_ros2_msgs__srv__EmitterSendString_Request *
webots_ros2_msgs__srv__EmitterSendString_Request__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  webots_ros2_msgs__srv__EmitterSendString_Request * msg = (webots_ros2_msgs__srv__EmitterSendString_Request *)allocator.allocate(sizeof(webots_ros2_msgs__srv__EmitterSendString_Request), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(webots_ros2_msgs__srv__EmitterSendString_Request));
  bool success = webots_ros2_msgs__srv__EmitterSendString_Request__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
webots_ros2_msgs__srv__EmitterSendString_Request__destroy(webots_ros2_msgs__srv__EmitterSendString_Request * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    webots_ros2_msgs__srv__EmitterSendString_Request__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
webots_ros2_msgs__srv__EmitterSendString_Request__Sequence__init(webots_ros2_msgs__srv__EmitterSendString_Request__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  webots_ros2_msgs__srv__EmitterSendString_Request * data = NULL;

  if (size) {
    data = (webots_ros2_msgs__srv__EmitterSendString_Request *)allocator.zero_allocate(size, sizeof(webots_ros2_msgs__srv__EmitterSendString_Request), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = webots_ros2_msgs__srv__EmitterSendString_Request__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        webots_ros2_msgs__srv__EmitterSendString_Request__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
webots_ros2_msgs__srv__EmitterSendString_Request__Sequence__fini(webots_ros2_msgs__srv__EmitterSendString_Request__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      webots_ros2_msgs__srv__EmitterSendString_Request__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

webots_ros2_msgs__srv__EmitterSendString_Request__Sequence *
webots_ros2_msgs__srv__EmitterSendString_Request__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  webots_ros2_msgs__srv__EmitterSendString_Request__Sequence * array = (webots_ros2_msgs__srv__EmitterSendString_Request__Sequence *)allocator.allocate(sizeof(webots_ros2_msgs__srv__EmitterSendString_Request__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = webots_ros2_msgs__srv__EmitterSendString_Request__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
webots_ros2_msgs__srv__EmitterSendString_Request__Sequence__destroy(webots_ros2_msgs__srv__EmitterSendString_Request__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    webots_ros2_msgs__srv__EmitterSendString_Request__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
webots_ros2_msgs__srv__EmitterSendString_Request__Sequence__are_equal(const webots_ros2_msgs__srv__EmitterSendString_Request__Sequence * lhs, const webots_ros2_msgs__srv__EmitterSendString_Request__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!webots_ros2_msgs__srv__EmitterSendString_Request__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
webots_ros2_msgs__srv__EmitterSendString_Request__Sequence__copy(
  const webots_ros2_msgs__srv__EmitterSendString_Request__Sequence * input,
  webots_ros2_msgs__srv__EmitterSendString_Request__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(webots_ros2_msgs__srv__EmitterSendString_Request);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    webots_ros2_msgs__srv__EmitterSendString_Request * data =
      (webots_ros2_msgs__srv__EmitterSendString_Request *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!webots_ros2_msgs__srv__EmitterSendString_Request__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          webots_ros2_msgs__srv__EmitterSendString_Request__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!webots_ros2_msgs__srv__EmitterSendString_Request__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}


bool
webots_ros2_msgs__srv__EmitterSendString_Response__init(webots_ros2_msgs__srv__EmitterSendString_Response * msg)
{
  if (!msg) {
    return false;
  }
  // result
  return true;
}

void
webots_ros2_msgs__srv__EmitterSendString_Response__fini(webots_ros2_msgs__srv__EmitterSendString_Response * msg)
{
  if (!msg) {
    return;
  }
  // result
}

bool
webots_ros2_msgs__srv__EmitterSendString_Response__are_equal(const webots_ros2_msgs__srv__EmitterSendString_Response * lhs, const webots_ros2_msgs__srv__EmitterSendString_Response * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // result
  if (lhs->result != rhs->result) {
    return false;
  }
  return true;
}

bool
webots_ros2_msgs__srv__EmitterSendString_Response__copy(
  const webots_ros2_msgs__srv__EmitterSendString_Response * input,
  webots_ros2_msgs__srv__EmitterSendString_Response * output)
{
  if (!input || !output) {
    return false;
  }
  // result
  output->result = input->result;
  return true;
}

webots_ros2_msgs__srv__EmitterSendString_Response *
webots_ros2_msgs__srv__EmitterSendString_Response__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  webots_ros2_msgs__srv__EmitterSendString_Response * msg = (webots_ros2_msgs__srv__EmitterSendString_Response *)allocator.allocate(sizeof(webots_ros2_msgs__srv__EmitterSendString_Response), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(webots_ros2_msgs__srv__EmitterSendString_Response));
  bool success = webots_ros2_msgs__srv__EmitterSendString_Response__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
webots_ros2_msgs__srv__EmitterSendString_Response__destroy(webots_ros2_msgs__srv__EmitterSendString_Response * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    webots_ros2_msgs__srv__EmitterSendString_Response__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
webots_ros2_msgs__srv__EmitterSendString_Response__Sequence__init(webots_ros2_msgs__srv__EmitterSendString_Response__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  webots_ros2_msgs__srv__EmitterSendString_Response * data = NULL;

  if (size) {
    data = (webots_ros2_msgs__srv__EmitterSendString_Response *)allocator.zero_allocate(size, sizeof(webots_ros2_msgs__srv__EmitterSendString_Response), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = webots_ros2_msgs__srv__EmitterSendString_Response__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        webots_ros2_msgs__srv__EmitterSendString_Response__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
webots_ros2_msgs__srv__EmitterSendString_Response__Sequence__fini(webots_ros2_msgs__srv__EmitterSendString_Response__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      webots_ros2_msgs__srv__EmitterSendString_Response__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

webots_ros2_msgs__srv__EmitterSendString_Response__Sequence *
webots_ros2_msgs__srv__EmitterSendString_Response__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  webots_ros2_msgs__srv__EmitterSendString_Response__Sequence * array = (webots_ros2_msgs__srv__EmitterSendString_Response__Sequence *)allocator.allocate(sizeof(webots_ros2_msgs__srv__EmitterSendString_Response__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = webots_ros2_msgs__srv__EmitterSendString_Response__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
webots_ros2_msgs__srv__EmitterSendString_Response__Sequence__destroy(webots_ros2_msgs__srv__EmitterSendString_Response__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    webots_ros2_msgs__srv__EmitterSendString_Response__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
webots_ros2_msgs__srv__EmitterSendString_Response__Sequence__are_equal(const webots_ros2_msgs__srv__EmitterSendString_Response__Sequence * lhs, const webots_ros2_msgs__srv__EmitterSendString_Response__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!webots_ros2_msgs__srv__EmitterSendString_Response__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
webots_ros2_msgs__srv__EmitterSendString_Response__Sequence__copy(
  const webots_ros2_msgs__srv__EmitterSendString_Response__Sequence * input,
  webots_ros2_msgs__srv__EmitterSendString_Response__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(webots_ros2_msgs__srv__EmitterSendString_Response);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    webots_ros2_msgs__srv__EmitterSendString_Response * data =
      (webots_ros2_msgs__srv__EmitterSendString_Response *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!webots_ros2_msgs__srv__EmitterSendString_Response__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          webots_ros2_msgs__srv__EmitterSendString_Response__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!webots_ros2_msgs__srv__EmitterSendString_Response__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
