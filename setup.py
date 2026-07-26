import os
import os.path as op
import platform
import subprocess
import sys
import multiprocessing  # Import multiprocessing to get CPU count
import configparser
from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext

# Ensure we're in Release mode
BUILD_TYPE = "Release"

# Read version from setup.cfg
def get_version():
    config = configparser.ConfigParser()
    config.read('setup.cfg')
    return config['metadata']['version']

class CMakeExtension(Extension):
    def __init__(self, name, cmake_lists_dir=".", sources=None, **kwa):
        sources = [] if sources is None else sources
        Extension.__init__(self, name, sources=sources, **kwa)
        self.cmake_lists_dir = os.path.abspath(cmake_lists_dir)


class cmake_build_ext(build_ext):
    def build_extensions(self):
        try:
            subprocess.check_output(["cmake", "--version"])
        except OSError:
            raise RuntimeError("Cannot find CMake executable")

        for ext in self.extensions:
            extpath = self.get_ext_fullpath(ext.name)
            extdir = op.abspath(op.dirname(extpath))
            extfile = op.splitext(op.basename(extpath))[0]
            tmpdir = self.build_temp
            
            # Define optimization flags for C/C++
            # Add -O3 and -ffast-math for maximum optimization
            optimization_flags = "-O3 -ffast-math"
            
            cmake_args = [
                "-DBLEND2D_STATIC=TRUE",
                "-DBLEND2DPY_TARGET_NAME={}".format(extfile),
                "-DCMAKE_BUILD_TYPE={}".format(BUILD_TYPE),
                "-DCMAKE_LIBRARY_OUTPUT_DIRECTORY_{}={}".format(
                    BUILD_TYPE.upper(), extdir
                ),
                "-DCMAKE_ARCHIVE_OUTPUT_DIRECTORY_{}={}".format(
                    BUILD_TYPE.upper(), extdir
                ),
                "-DPYTHON_EXECUTABLE={}".format(sys.executable),
            ]

            if platform.system() == "Windows":
                plat = "x64" if platform.architecture()[0] == "64bit" else "Win32"
                cmake_args += [
                    "-DCMAKE_WINDOWS_EXPORT_ALL_SYMBOLS=TRUE",
                    "-DCMAKE_RUNTIME_OUTPUT_DIRECTORY_{}={}".format(
                        BUILD_TYPE.upper(), extdir
                    ),
                ]
                if self.compiler.compiler_type == "msvc":
                    # For MSVC, use equivalent optimization flags
                    cmake_args += [
                        "-DCMAKE_GENERATOR_PLATFORM={}".format(plat),
                        "-DCMAKE_CXX_FLAGS=/O2 /fp:fast",
                        "-DCMAKE_C_FLAGS=/O2 /fp:fast",
                    ]
                else:
                    # For MinGW on Windows
                    cmake_args += [
                        "-G", "MinGW Makefiles",
                        "-DCMAKE_CXX_FLAGS={}".format(optimization_flags),
                        "-DCMAKE_C_FLAGS={}".format(optimization_flags),
                    ]
            elif platform.system() == "Linux":
                arm_flags = ""
                # if platform.machine() in ["aarch64", "arm64"]:
                #     # Add specific ARM64 flags to enable NEON and crypto extensions
                #     arm_flags = " -march=armv8-a+crypto -mfpu=neon-fp-armv8 -mneon-for-64bits"
                
                cmake_args += [
                    "-DCMAKE_C_FLAGS=-fPIC {} {}".format(optimization_flags, arm_flags),
                    "-DCMAKE_CXX_FLAGS=-fPIC {} {}".format(optimization_flags, arm_flags),
                ]
            elif platform.system() == "Darwin":  # macOS
                # Detect target architecture for macOS
                # Check for ARCHFLAGS environment variable set by cibuildwheel
                archflags = os.environ.get('ARCHFLAGS', '')
                target_arch = None
                
                if 'arm64' in archflags:
                    target_arch = 'arm64'
                elif 'x86_64' in archflags:
                    target_arch = 'x86_64'
                else:
                    # Try to detect from Python interpreter architecture
                    try:
                        result = subprocess.check_output(['file', sys.executable]).decode('utf-8')
                        if 'arm64' in result:
                            target_arch = 'arm64'
                        elif 'x86_64' in result:
                            target_arch = 'x86_64'
                    except:
                        pass
                
                # Fallback to system architecture
                if not target_arch:
                    machine = platform.machine()
                    if machine == 'arm64':
                        target_arch = 'arm64'
                    else:
                        target_arch = 'x86_64'
                
                print(f"Building for macOS architecture: {target_arch}")
                cmake_args += [
                    "-DCMAKE_OSX_ARCHITECTURES={}".format(target_arch),
                    "-DCMAKE_C_FLAGS={}".format(optimization_flags),
                    "-DCMAKE_CXX_FLAGS={}".format(optimization_flags),
                ]

            if not op.exists(tmpdir):
                os.makedirs(tmpdir)

            # Print confirmation message about optimization settings
            print(f"Building in {BUILD_TYPE} mode with optimization flags: {optimization_flags}")
            
            # Config and build the extension
            cmd = ["cmake", ext.cmake_lists_dir] + cmake_args
            subprocess.check_call(cmd, cwd=tmpdir)
            
            # Use all available CPU cores for the build
            cpu_count = multiprocessing.cpu_count()
            if platform.system() == "Windows":
                # MSBuild uses /m:N for parallel builds
                cmd = ["cmake", "--build", ".", "--config", BUILD_TYPE, "--", "/m:{}".format(cpu_count)]
            else:
                # Unix makefiles use -jN
                cmd = ["cmake", "--build", ".", "--config", BUILD_TYPE, "--", "-j{}".format(cpu_count)]
            print("Building with {} cores".format(cpu_count))
            subprocess.check_call(cmd, cwd=tmpdir)





# See setup.cfg for package metadata
setup(
    version=get_version(),
    ext_modules=[CMakeExtension("blend2d._capi")],
    cmdclass={"build_ext": cmake_build_ext},
    install_requires=["numpy"],
    python_requires=">=3.8",
    setup_requires=["numpy"],
)