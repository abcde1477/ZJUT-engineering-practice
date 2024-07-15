# Install script for directory: /home/jetson/2024-7-8/ws/src/yahboomcar_carry_robot

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/home/jetson/2024-7-8/ws/install")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "")
  endif()
  message(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
endif()

# Set the component getting installed.
if(NOT CMAKE_INSTALL_COMPONENT)
  if(COMPONENT)
    message(STATUS "Install component: \"${COMPONENT}\"")
    set(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  else()
    set(CMAKE_INSTALL_COMPONENT)
  endif()
endif()

# Install shared libraries without execute permission?
if(NOT DEFINED CMAKE_INSTALL_SO_NO_EXE)
  set(CMAKE_INSTALL_SO_NO_EXE "1")
endif()

# Is this installation the result of a crosscompile?
if(NOT DEFINED CMAKE_CROSSCOMPILING)
  set(CMAKE_CROSSCOMPILING "FALSE")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/yahboomcar_carry_robot" TYPE FILE FILES "/home/jetson/2024-7-8/ws/devel/include/yahboomcar_carry_robot/laserTrackerPIDConfig.h")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/yahboomcar_carry_robot" TYPE FILE FILES "/home/jetson/2024-7-8/ws/devel/include/yahboomcar_carry_robot/laserWarningPIDConfig.h")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/yahboomcar_carry_robot" TYPE FILE FILES "/home/jetson/2024-7-8/ws/devel/include/yahboomcar_carry_robot/laserAvoidancePIDConfig.h")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/yahboomcar_carry_robot" TYPE FILE FILES "/home/jetson/2024-7-8/ws/devel/include/yahboomcar_carry_robot/obstacleLaserPIDConfig.h")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/python2.7/dist-packages/yahboomcar_carry_robot" TYPE FILE FILES "/home/jetson/2024-7-8/ws/devel/lib/python2.7/dist-packages/yahboomcar_carry_robot/__init__.py")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  execute_process(COMMAND "/usr/bin/python2" -m compileall "/home/jetson/2024-7-8/ws/devel/lib/python2.7/dist-packages/yahboomcar_carry_robot/cfg")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/python2.7/dist-packages/yahboomcar_carry_robot" TYPE DIRECTORY FILES "/home/jetson/2024-7-8/ws/devel/lib/python2.7/dist-packages/yahboomcar_carry_robot/cfg")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/pkgconfig" TYPE FILE FILES "/home/jetson/2024-7-8/ws/build/yahboomcar_carry_robot/catkin_generated/installspace/yahboomcar_carry_robot.pc")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/yahboomcar_carry_robot/cmake" TYPE FILE FILES
    "/home/jetson/2024-7-8/ws/build/yahboomcar_carry_robot/catkin_generated/installspace/yahboomcar_carry_robotConfig.cmake"
    "/home/jetson/2024-7-8/ws/build/yahboomcar_carry_robot/catkin_generated/installspace/yahboomcar_carry_robotConfig-version.cmake"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/yahboomcar_carry_robot" TYPE FILE FILES "/home/jetson/2024-7-8/ws/src/yahboomcar_carry_robot/package.xml")
endif()

