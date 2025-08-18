# Install script for directory: /workspaces/android-app-python/.buildozer/android/platform/build-arm64-v8a_armeabi-v7a/build/other_builds/opencv/arm64-v8a__ndk_target_21/opencv

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/workspaces/android-app-python/.buildozer/android/platform/build-arm64-v8a_armeabi-v7a/build/other_builds/opencv/arm64-v8a__ndk_target_21/opencv/build/install")
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

if(CMAKE_INSTALL_COMPONENT STREQUAL "samples" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/samples" TYPE FILE FILES "/workspaces/android-app-python/.buildozer/android/platform/build-arm64-v8a_armeabi-v7a/build/other_builds/opencv/arm64-v8a__ndk_target_21/opencv/build/CMakeFiles/install/opencv_android/samples/build.gradle")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "samples" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/samples/gradle/wrapper" TYPE FILE FILES "/workspaces/android-app-python/.buildozer/android/platform/build-arm64-v8a_armeabi-v7a/build/other_builds/opencv/arm64-v8a__ndk_target_21/opencv/platforms/android/gradle-wrapper/gradle/wrapper/gradle-wrapper.jar")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "samples" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/samples/gradle/wrapper" TYPE FILE FILES "/workspaces/android-app-python/.buildozer/android/platform/build-arm64-v8a_armeabi-v7a/build/other_builds/opencv/arm64-v8a__ndk_target_21/opencv/platforms/android/gradle-wrapper/gradle/wrapper/gradle-wrapper.properties")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "samples" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/samples/." TYPE FILE FILES "/workspaces/android-app-python/.buildozer/android/platform/build-arm64-v8a_armeabi-v7a/build/other_builds/opencv/arm64-v8a__ndk_target_21/opencv/platforms/android/gradle-wrapper/gradlew.bat")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "samples" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/samples/." TYPE FILE PERMISSIONS OWNER_READ OWNER_WRITE OWNER_EXECUTE GROUP_READ GROUP_EXECUTE WORLD_READ WORLD_EXECUTE FILES "/workspaces/android-app-python/.buildozer/android/platform/build-arm64-v8a_armeabi-v7a/build/other_builds/opencv/arm64-v8a__ndk_target_21/opencv/platforms/android/gradle-wrapper/gradlew")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "samples" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/samples/." TYPE FILE FILES "/workspaces/android-app-python/.buildozer/android/platform/build-arm64-v8a_armeabi-v7a/build/other_builds/opencv/arm64-v8a__ndk_target_21/opencv/platforms/android/gradle-wrapper/gradle.properties")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "samples" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/samples" TYPE FILE FILES "/workspaces/android-app-python/.buildozer/android/platform/build-arm64-v8a_armeabi-v7a/build/other_builds/opencv/arm64-v8a__ndk_target_21/opencv/build/CMakeFiles/install/opencv_android/settings.gradle")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "dev" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/sdk/native/jni/include/opencv2" TYPE FILE FILES "/workspaces/android-app-python/.buildozer/android/platform/build-arm64-v8a_armeabi-v7a/build/other_builds/opencv/arm64-v8a__ndk_target_21/opencv/build/cvconfig.h")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "dev" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/sdk/native/jni/include/opencv2" TYPE FILE FILES "/workspaces/android-app-python/.buildozer/android/platform/build-arm64-v8a_armeabi-v7a/build/other_builds/opencv/arm64-v8a__ndk_target_21/opencv/build/opencv2/opencv_modules.hpp")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "dev" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/sdk/native/jni" TYPE FILE FILES "/workspaces/android-app-python/.buildozer/android/platform/build-arm64-v8a_armeabi-v7a/build/other_builds/opencv/arm64-v8a__ndk_target_21/opencv/build/unix-install/OpenCV.mk")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "dev" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/sdk/native/jni" TYPE FILE FILES "/workspaces/android-app-python/.buildozer/android/platform/build-arm64-v8a_armeabi-v7a/build/other_builds/opencv/arm64-v8a__ndk_target_21/opencv/build/unix-install/OpenCV-arm64-v8a.mk")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "dev" OR NOT CMAKE_INSTALL_COMPONENT)
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/sdk/native/jni/abi-arm64-v8a/OpenCVModules.cmake")
    file(DIFFERENT _cmake_export_file_changed FILES
         "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/sdk/native/jni/abi-arm64-v8a/OpenCVModules.cmake"
         "/workspaces/android-app-python/.buildozer/android/platform/build-arm64-v8a_armeabi-v7a/build/other_builds/opencv/arm64-v8a__ndk_target_21/opencv/build/CMakeFiles/Export/dfc1c36b0b5e57cb58990e6992b52a24/OpenCVModules.cmake")
    if(_cmake_export_file_changed)
      file(GLOB _cmake_old_config_files "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/sdk/native/jni/abi-arm64-v8a/OpenCVModules-*.cmake")
      if(_cmake_old_config_files)
        string(REPLACE ";" ", " _cmake_old_config_files_text "${_cmake_old_config_files}")
        message(STATUS "Old export file \"$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/sdk/native/jni/abi-arm64-v8a/OpenCVModules.cmake\" will be replaced.  Removing files [${_cmake_old_config_files_text}].")
        unset(_cmake_old_config_files_text)
        file(REMOVE ${_cmake_old_config_files})
      endif()
      unset(_cmake_old_config_files)
    endif()
    unset(_cmake_export_file_changed)
  endif()
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/sdk/native/jni/abi-arm64-v8a" TYPE FILE FILES "/workspaces/android-app-python/.buildozer/android/platform/build-arm64-v8a_armeabi-v7a/build/other_builds/opencv/arm64-v8a__ndk_target_21/opencv/build/CMakeFiles/Export/dfc1c36b0b5e57cb58990e6992b52a24/OpenCVModules.cmake")
  if(CMAKE_INSTALL_CONFIG_NAME MATCHES "^([Rr][Ee][Ll][Ee][Aa][Ss][Ee])$")
    file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/sdk/native/jni/abi-arm64-v8a" TYPE FILE FILES "/workspaces/android-app-python/.buildozer/android/platform/build-arm64-v8a_armeabi-v7a/build/other_builds/opencv/arm64-v8a__ndk_target_21/opencv/build/CMakeFiles/Export/dfc1c36b0b5e57cb58990e6992b52a24/OpenCVModules-release.cmake")
  endif()
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "dev" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/sdk/native/jni/abi-arm64-v8a" TYPE FILE FILES
    "/workspaces/android-app-python/.buildozer/android/platform/build-arm64-v8a_armeabi-v7a/build/other_builds/opencv/arm64-v8a__ndk_target_21/opencv/build/unix-install/OpenCVConfig-version.cmake"
    "/workspaces/android-app-python/.buildozer/android/platform/build-arm64-v8a_armeabi-v7a/build/other_builds/opencv/arm64-v8a__ndk_target_21/opencv/build/unix-install/abi-arm64-v8a/OpenCVConfig.cmake"
    )
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "dev" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/sdk/native/jni" TYPE FILE FILES
    "/workspaces/android-app-python/.buildozer/android/platform/build-arm64-v8a_armeabi-v7a/build/other_builds/opencv/arm64-v8a__ndk_target_21/opencv/build/unix-install/OpenCVConfig-version.cmake"
    "/workspaces/android-app-python/.buildozer/android/platform/build-arm64-v8a_armeabi-v7a/build/other_builds/opencv/arm64-v8a__ndk_target_21/opencv/build/unix-install/OpenCVConfig.cmake"
    )
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "dev" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/sdk/native/jni" TYPE FILE FILES "/workspaces/android-app-python/.buildozer/android/platform/build-arm64-v8a_armeabi-v7a/build/other_builds/opencv/arm64-v8a__ndk_target_21/opencv/platforms/android/android.toolchain.cmake")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "libs" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/." TYPE FILE PERMISSIONS OWNER_READ OWNER_WRITE GROUP_READ WORLD_READ FILES "/workspaces/android-app-python/.buildozer/android/platform/build-arm64-v8a_armeabi-v7a/build/other_builds/opencv/arm64-v8a__ndk_target_21/opencv/LICENSE")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "libs" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/." TYPE FILE PERMISSIONS OWNER_READ OWNER_WRITE GROUP_READ WORLD_READ FILES "/workspaces/android-app-python/.buildozer/android/platform/build-arm64-v8a_armeabi-v7a/build/other_builds/opencv/arm64-v8a__ndk_target_21/opencv/platforms/android/README.android")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "dev" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/sdk/etc" TYPE FILE FILES
    "/workspaces/android-app-python/.buildozer/android/platform/build-arm64-v8a_armeabi-v7a/build/other_builds/opencv/arm64-v8a__ndk_target_21/opencv/platforms/scripts/valgrind.supp"
    "/workspaces/android-app-python/.buildozer/android/platform/build-arm64-v8a_armeabi-v7a/build/other_builds/opencv/arm64-v8a__ndk_target_21/opencv/platforms/scripts/valgrind_3rdparty.supp"
    )
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for each subdirectory.
  include("/workspaces/android-app-python/.buildozer/android/platform/build-arm64-v8a_armeabi-v7a/build/other_builds/opencv/arm64-v8a__ndk_target_21/opencv/build/3rdparty/cpufeatures/cmake_install.cmake")
  include("/workspaces/android-app-python/.buildozer/android/platform/build-arm64-v8a_armeabi-v7a/build/other_builds/opencv/arm64-v8a__ndk_target_21/opencv/build/3rdparty/libjpeg-turbo/cmake_install.cmake")
  include("/workspaces/android-app-python/.buildozer/android/platform/build-arm64-v8a_armeabi-v7a/build/other_builds/opencv/arm64-v8a__ndk_target_21/opencv/build/3rdparty/libtiff/cmake_install.cmake")
  include("/workspaces/android-app-python/.buildozer/android/platform/build-arm64-v8a_armeabi-v7a/build/other_builds/opencv/arm64-v8a__ndk_target_21/opencv/build/3rdparty/libwebp/cmake_install.cmake")
  include("/workspaces/android-app-python/.buildozer/android/platform/build-arm64-v8a_armeabi-v7a/build/other_builds/opencv/arm64-v8a__ndk_target_21/opencv/build/3rdparty/openjpeg/cmake_install.cmake")
  include("/workspaces/android-app-python/.buildozer/android/platform/build-arm64-v8a_armeabi-v7a/build/other_builds/opencv/arm64-v8a__ndk_target_21/opencv/build/3rdparty/libpng/cmake_install.cmake")
  include("/workspaces/android-app-python/.buildozer/android/platform/build-arm64-v8a_armeabi-v7a/build/other_builds/opencv/arm64-v8a__ndk_target_21/opencv/build/3rdparty/openexr/cmake_install.cmake")
  include("/workspaces/android-app-python/.buildozer/android/platform/build-arm64-v8a_armeabi-v7a/build/other_builds/opencv/arm64-v8a__ndk_target_21/opencv/build/3rdparty/protobuf/cmake_install.cmake")
  include("/workspaces/android-app-python/.buildozer/android/platform/build-arm64-v8a_armeabi-v7a/build/other_builds/opencv/arm64-v8a__ndk_target_21/opencv/build/3rdparty/quirc/cmake_install.cmake")
  include("/workspaces/android-app-python/.buildozer/android/platform/build-arm64-v8a_armeabi-v7a/build/other_builds/opencv/arm64-v8a__ndk_target_21/opencv/build/3rdparty/carotene/hal/cmake_install.cmake")
  include("/workspaces/android-app-python/.buildozer/android/platform/build-arm64-v8a_armeabi-v7a/build/other_builds/opencv/arm64-v8a__ndk_target_21/opencv/build/3rdparty/ittnotify/cmake_install.cmake")
  include("/workspaces/android-app-python/.buildozer/android/platform/build-arm64-v8a_armeabi-v7a/build/other_builds/opencv/arm64-v8a__ndk_target_21/opencv/build/include/cmake_install.cmake")
  include("/workspaces/android-app-python/.buildozer/android/platform/build-arm64-v8a_armeabi-v7a/build/other_builds/opencv/arm64-v8a__ndk_target_21/opencv/build/modules/cmake_install.cmake")
  include("/workspaces/android-app-python/.buildozer/android/platform/build-arm64-v8a_armeabi-v7a/build/other_builds/opencv/arm64-v8a__ndk_target_21/opencv/build/doc/cmake_install.cmake")
  include("/workspaces/android-app-python/.buildozer/android/platform/build-arm64-v8a_armeabi-v7a/build/other_builds/opencv/arm64-v8a__ndk_target_21/opencv/build/data/cmake_install.cmake")
  include("/workspaces/android-app-python/.buildozer/android/platform/build-arm64-v8a_armeabi-v7a/build/other_builds/opencv/arm64-v8a__ndk_target_21/opencv/build/platforms/android/service/cmake_install.cmake")

endif()

if(CMAKE_INSTALL_COMPONENT)
  set(CMAKE_INSTALL_MANIFEST "install_manifest_${CMAKE_INSTALL_COMPONENT}.txt")
else()
  set(CMAKE_INSTALL_MANIFEST "install_manifest.txt")
endif()

string(REPLACE ";" "\n" CMAKE_INSTALL_MANIFEST_CONTENT
       "${CMAKE_INSTALL_MANIFEST_FILES}")
file(WRITE "/workspaces/android-app-python/.buildozer/android/platform/build-arm64-v8a_armeabi-v7a/build/other_builds/opencv/arm64-v8a__ndk_target_21/opencv/build/${CMAKE_INSTALL_MANIFEST}"
     "${CMAKE_INSTALL_MANIFEST_CONTENT}")
