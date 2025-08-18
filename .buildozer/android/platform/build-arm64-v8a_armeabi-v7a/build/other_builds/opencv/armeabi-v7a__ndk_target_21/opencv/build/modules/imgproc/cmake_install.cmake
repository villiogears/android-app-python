# Install script for directory: /workspaces/android-app-python/.buildozer/android/platform/build-arm64-v8a_armeabi-v7a/build/other_builds/opencv/armeabi-v7a__ndk_target_21/opencv/modules/imgproc

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/workspaces/android-app-python/.buildozer/android/platform/build-arm64-v8a_armeabi-v7a/build/other_builds/opencv/armeabi-v7a__ndk_target_21/opencv/build/install")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "Release")
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
  set(CMAKE_CROSSCOMPILING "TRUE")
endif()

# Set default install directory permissions.
if(NOT DEFINED CMAKE_OBJDUMP)
  set(CMAKE_OBJDUMP "/home/codespace/.buildozer/android/platform/android-ndk-r25b/toolchains/llvm/prebuilt/linux-x86_64/bin/llvm-objdump")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "libs" OR NOT CMAKE_INSTALL_COMPONENT)
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/sdk/native/libs/armeabi-v7a/libopencv_imgproc.so" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/sdk/native/libs/armeabi-v7a/libopencv_imgproc.so")
    file(RPATH_CHECK
         FILE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/sdk/native/libs/armeabi-v7a/libopencv_imgproc.so"
         RPATH "")
  endif()
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/sdk/native/libs/armeabi-v7a" TYPE SHARED_LIBRARY OPTIONAL FILES "/workspaces/android-app-python/.buildozer/android/platform/build-arm64-v8a_armeabi-v7a/build/other_builds/opencv/armeabi-v7a__ndk_target_21/opencv/build/lib/armeabi-v7a/libopencv_imgproc.so")
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/sdk/native/libs/armeabi-v7a/libopencv_imgproc.so" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/sdk/native/libs/armeabi-v7a/libopencv_imgproc.so")
    if(CMAKE_INSTALL_DO_STRIP)
      execute_process(COMMAND "/home/codespace/.buildozer/android/platform/android-ndk-r25b/toolchains/llvm/prebuilt/linux-x86_64/bin/llvm-strip" "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/sdk/native/libs/armeabi-v7a/libopencv_imgproc.so")
    endif()
  endif()
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "dev" OR NOT CMAKE_INSTALL_COMPONENT)
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "dev" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/sdk/native/jni/include/opencv2" TYPE FILE OPTIONAL FILES "/workspaces/android-app-python/.buildozer/android/platform/build-arm64-v8a_armeabi-v7a/build/other_builds/opencv/armeabi-v7a__ndk_target_21/opencv/modules/imgproc/include/opencv2/imgproc.hpp")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "dev" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/sdk/native/jni/include/opencv2/imgproc/hal" TYPE FILE OPTIONAL FILES "/workspaces/android-app-python/.buildozer/android/platform/build-arm64-v8a_armeabi-v7a/build/other_builds/opencv/armeabi-v7a__ndk_target_21/opencv/modules/imgproc/include/opencv2/imgproc/hal/hal.hpp")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "dev" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/sdk/native/jni/include/opencv2/imgproc/hal" TYPE FILE OPTIONAL FILES "/workspaces/android-app-python/.buildozer/android/platform/build-arm64-v8a_armeabi-v7a/build/other_builds/opencv/armeabi-v7a__ndk_target_21/opencv/modules/imgproc/include/opencv2/imgproc/hal/interface.h")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "dev" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/sdk/native/jni/include/opencv2/imgproc" TYPE FILE OPTIONAL FILES "/workspaces/android-app-python/.buildozer/android/platform/build-arm64-v8a_armeabi-v7a/build/other_builds/opencv/armeabi-v7a__ndk_target_21/opencv/modules/imgproc/include/opencv2/imgproc/imgproc.hpp")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "dev" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/sdk/native/jni/include/opencv2/imgproc" TYPE FILE OPTIONAL FILES "/workspaces/android-app-python/.buildozer/android/platform/build-arm64-v8a_armeabi-v7a/build/other_builds/opencv/armeabi-v7a__ndk_target_21/opencv/modules/imgproc/include/opencv2/imgproc/imgproc_c.h")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "dev" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/sdk/native/jni/include/opencv2/imgproc" TYPE FILE OPTIONAL FILES "/workspaces/android-app-python/.buildozer/android/platform/build-arm64-v8a_armeabi-v7a/build/other_builds/opencv/armeabi-v7a__ndk_target_21/opencv/modules/imgproc/include/opencv2/imgproc/types_c.h")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "dev" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/sdk/native/jni/include/opencv2/imgproc/detail" TYPE FILE OPTIONAL FILES "/workspaces/android-app-python/.buildozer/android/platform/build-arm64-v8a_armeabi-v7a/build/other_builds/opencv/armeabi-v7a__ndk_target_21/opencv/modules/imgproc/include/opencv2/imgproc/detail/gcgraph.hpp")
endif()

