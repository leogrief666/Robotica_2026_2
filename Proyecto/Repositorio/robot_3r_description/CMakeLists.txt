cmake_minimum_required(VERSION 3.8)
project(robot_3r_description)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)

install(
  DIRECTORY urdf launch meshes rviz 
  DESTINATION share/${PROJECT_NAME}/
)

install(PROGRAMS
  scripts/trayectoria_3r.py
  DESTINATION lib/${PROJECT_NAME}
)

ament_package()
