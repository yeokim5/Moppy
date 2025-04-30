// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from webots_ros2_msgs:srv/GetBool.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "webots_ros2_msgs/srv/detail/get_bool__rosidl_typesupport_introspection_c.h"
#include "webots_ros2_msgs/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "webots_ros2_msgs/srv/detail/get_bool__functions.h"
#include "webots_ros2_msgs/srv/detail/get_bool__struct.h"


#ifdef __cplusplus
extern "C"
{
#endif

void webots_ros2_msgs__srv__GetBool_Request__rosidl_typesupport_introspection_c__GetBool_Request_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  webots_ros2_msgs__srv__GetBool_Request__init(message_memory);
}

void webots_ros2_msgs__srv__GetBool_Request__rosidl_typesupport_introspection_c__GetBool_Request_fini_function(void * message_memory)
{
  webots_ros2_msgs__srv__GetBool_Request__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember webots_ros2_msgs__srv__GetBool_Request__rosidl_typesupport_introspection_c__GetBool_Request_message_member_array[1] = {
  {
    "ask",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_BOOLEAN,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(webots_ros2_msgs__srv__GetBool_Request, ask),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers webots_ros2_msgs__srv__GetBool_Request__rosidl_typesupport_introspection_c__GetBool_Request_message_members = {
  "webots_ros2_msgs__srv",  // message namespace
  "GetBool_Request",  // message name
  1,  // number of fields
  sizeof(webots_ros2_msgs__srv__GetBool_Request),
  webots_ros2_msgs__srv__GetBool_Request__rosidl_typesupport_introspection_c__GetBool_Request_message_member_array,  // message members
  webots_ros2_msgs__srv__GetBool_Request__rosidl_typesupport_introspection_c__GetBool_Request_init_function,  // function to initialize message memory (memory has to be allocated)
  webots_ros2_msgs__srv__GetBool_Request__rosidl_typesupport_introspection_c__GetBool_Request_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t webots_ros2_msgs__srv__GetBool_Request__rosidl_typesupport_introspection_c__GetBool_Request_message_type_support_handle = {
  0,
  &webots_ros2_msgs__srv__GetBool_Request__rosidl_typesupport_introspection_c__GetBool_Request_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_webots_ros2_msgs
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, webots_ros2_msgs, srv, GetBool_Request)() {
  if (!webots_ros2_msgs__srv__GetBool_Request__rosidl_typesupport_introspection_c__GetBool_Request_message_type_support_handle.typesupport_identifier) {
    webots_ros2_msgs__srv__GetBool_Request__rosidl_typesupport_introspection_c__GetBool_Request_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &webots_ros2_msgs__srv__GetBool_Request__rosidl_typesupport_introspection_c__GetBool_Request_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif

// already included above
// #include <stddef.h>
// already included above
// #include "webots_ros2_msgs/srv/detail/get_bool__rosidl_typesupport_introspection_c.h"
// already included above
// #include "webots_ros2_msgs/msg/rosidl_typesupport_introspection_c__visibility_control.h"
// already included above
// #include "rosidl_typesupport_introspection_c/field_types.h"
// already included above
// #include "rosidl_typesupport_introspection_c/identifier.h"
// already included above
// #include "rosidl_typesupport_introspection_c/message_introspection.h"
// already included above
// #include "webots_ros2_msgs/srv/detail/get_bool__functions.h"
// already included above
// #include "webots_ros2_msgs/srv/detail/get_bool__struct.h"


#ifdef __cplusplus
extern "C"
{
#endif

void webots_ros2_msgs__srv__GetBool_Response__rosidl_typesupport_introspection_c__GetBool_Response_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  webots_ros2_msgs__srv__GetBool_Response__init(message_memory);
}

void webots_ros2_msgs__srv__GetBool_Response__rosidl_typesupport_introspection_c__GetBool_Response_fini_function(void * message_memory)
{
  webots_ros2_msgs__srv__GetBool_Response__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember webots_ros2_msgs__srv__GetBool_Response__rosidl_typesupport_introspection_c__GetBool_Response_message_member_array[1] = {
  {
    "value",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_BOOLEAN,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(webots_ros2_msgs__srv__GetBool_Response, value),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers webots_ros2_msgs__srv__GetBool_Response__rosidl_typesupport_introspection_c__GetBool_Response_message_members = {
  "webots_ros2_msgs__srv",  // message namespace
  "GetBool_Response",  // message name
  1,  // number of fields
  sizeof(webots_ros2_msgs__srv__GetBool_Response),
  webots_ros2_msgs__srv__GetBool_Response__rosidl_typesupport_introspection_c__GetBool_Response_message_member_array,  // message members
  webots_ros2_msgs__srv__GetBool_Response__rosidl_typesupport_introspection_c__GetBool_Response_init_function,  // function to initialize message memory (memory has to be allocated)
  webots_ros2_msgs__srv__GetBool_Response__rosidl_typesupport_introspection_c__GetBool_Response_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t webots_ros2_msgs__srv__GetBool_Response__rosidl_typesupport_introspection_c__GetBool_Response_message_type_support_handle = {
  0,
  &webots_ros2_msgs__srv__GetBool_Response__rosidl_typesupport_introspection_c__GetBool_Response_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_webots_ros2_msgs
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, webots_ros2_msgs, srv, GetBool_Response)() {
  if (!webots_ros2_msgs__srv__GetBool_Response__rosidl_typesupport_introspection_c__GetBool_Response_message_type_support_handle.typesupport_identifier) {
    webots_ros2_msgs__srv__GetBool_Response__rosidl_typesupport_introspection_c__GetBool_Response_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &webots_ros2_msgs__srv__GetBool_Response__rosidl_typesupport_introspection_c__GetBool_Response_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif

#include "rosidl_runtime_c/service_type_support_struct.h"
// already included above
// #include "webots_ros2_msgs/msg/rosidl_typesupport_introspection_c__visibility_control.h"
// already included above
// #include "webots_ros2_msgs/srv/detail/get_bool__rosidl_typesupport_introspection_c.h"
// already included above
// #include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/service_introspection.h"

// this is intentionally not const to allow initialization later to prevent an initialization race
static rosidl_typesupport_introspection_c__ServiceMembers webots_ros2_msgs__srv__detail__get_bool__rosidl_typesupport_introspection_c__GetBool_service_members = {
  "webots_ros2_msgs__srv",  // service namespace
  "GetBool",  // service name
  // these two fields are initialized below on the first access
  NULL,  // request message
  // webots_ros2_msgs__srv__detail__get_bool__rosidl_typesupport_introspection_c__GetBool_Request_message_type_support_handle,
  NULL  // response message
  // webots_ros2_msgs__srv__detail__get_bool__rosidl_typesupport_introspection_c__GetBool_Response_message_type_support_handle
};

static rosidl_service_type_support_t webots_ros2_msgs__srv__detail__get_bool__rosidl_typesupport_introspection_c__GetBool_service_type_support_handle = {
  0,
  &webots_ros2_msgs__srv__detail__get_bool__rosidl_typesupport_introspection_c__GetBool_service_members,
  get_service_typesupport_handle_function,
};

// Forward declaration of request/response type support functions
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, webots_ros2_msgs, srv, GetBool_Request)();

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, webots_ros2_msgs, srv, GetBool_Response)();

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_webots_ros2_msgs
const rosidl_service_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_introspection_c, webots_ros2_msgs, srv, GetBool)() {
  if (!webots_ros2_msgs__srv__detail__get_bool__rosidl_typesupport_introspection_c__GetBool_service_type_support_handle.typesupport_identifier) {
    webots_ros2_msgs__srv__detail__get_bool__rosidl_typesupport_introspection_c__GetBool_service_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  rosidl_typesupport_introspection_c__ServiceMembers * service_members =
    (rosidl_typesupport_introspection_c__ServiceMembers *)webots_ros2_msgs__srv__detail__get_bool__rosidl_typesupport_introspection_c__GetBool_service_type_support_handle.data;

  if (!service_members->request_members_) {
    service_members->request_members_ =
      (const rosidl_typesupport_introspection_c__MessageMembers *)
      ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, webots_ros2_msgs, srv, GetBool_Request)()->data;
  }
  if (!service_members->response_members_) {
    service_members->response_members_ =
      (const rosidl_typesupport_introspection_c__MessageMembers *)
      ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, webots_ros2_msgs, srv, GetBool_Response)()->data;
  }

  return &webots_ros2_msgs__srv__detail__get_bool__rosidl_typesupport_introspection_c__GetBool_service_type_support_handle;
}
