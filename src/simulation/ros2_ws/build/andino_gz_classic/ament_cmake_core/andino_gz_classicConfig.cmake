# generated from ament/cmake/core/templates/nameConfig.cmake.in

# prevent multiple inclusion
if(_andino_gz_classic_CONFIG_INCLUDED)
  # ensure to keep the found flag the same
  if(NOT DEFINED andino_gz_classic_FOUND)
    # explicitly set it to FALSE, otherwise CMake will set it to TRUE
    set(andino_gz_classic_FOUND FALSE)
  elseif(NOT andino_gz_classic_FOUND)
    # use separate condition to avoid uninitialized variable warning
    set(andino_gz_classic_FOUND FALSE)
  endif()
  return()
endif()
set(_andino_gz_classic_CONFIG_INCLUDED TRUE)

# output package information
if(NOT andino_gz_classic_FIND_QUIETLY)
  message(STATUS "Found andino_gz_classic: 0.0.1 (${andino_gz_classic_DIR})")
endif()

# warn when using a deprecated package
if(NOT "" STREQUAL "")
  set(_msg "Package 'andino_gz_classic' is deprecated")
  # append custom deprecation text if available
  if(NOT "" STREQUAL "TRUE")
    set(_msg "${_msg} ()")
  endif()
  # optionally quiet the deprecation message
  if(NOT ${andino_gz_classic_DEPRECATED_QUIET})
    message(DEPRECATION "${_msg}")
  endif()
endif()

# flag package as ament-based to distinguish it after being find_package()-ed
set(andino_gz_classic_FOUND_AMENT_PACKAGE TRUE)

# include all config extra files
set(_extras "")
foreach(_extra ${_extras})
  include("${andino_gz_classic_DIR}/${_extra}")
endforeach()
