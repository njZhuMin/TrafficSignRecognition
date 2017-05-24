cmake_minimum_required(VERSION 3.5)
project(getROI)

set(CUDA_USE_STATIC_CUDA_RUNTIME OFF)
find_package(OpenCV REQUIRED)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++0x")

set(SOURCE_FILES main.cpp)
set(CMAKE_EXE_LINKER_FLAGS)

add_executable(getROI ${SOURCE_FILES})
target_link_libraries(getROI ${OpenCV_LIBS})
