#define CV_CPU_SIMD_FILENAME "/workspaces/android-app-python/.buildozer/android/platform/build-arm64-v8a_armeabi-v7a/build/other_builds/opencv/arm64-v8a__ndk_target_21/opencv/modules/core/test/test_intrin256.simd.hpp"
#define CV_CPU_DISPATCH_MODE AVX2
#include "opencv2/core/private/cv_cpu_include_simd_declarations.hpp"

#define CV_CPU_DISPATCH_MODE AVX512_SKX
#include "opencv2/core/private/cv_cpu_include_simd_declarations.hpp"

#define CV_CPU_DISPATCH_MODES_ALL AVX512_SKX, AVX2, BASELINE

#undef CV_CPU_SIMD_FILENAME
