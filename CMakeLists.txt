cmake_minimum_required(VERSION 2.8.3)
project(baxter_eyes)
 
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")

find_package(catkin REQUIRED COMPONENTS
  rospy
)

catkin_python_setup()

catkin_package(
   CATKIN_DEPENDS
   rospy
)
