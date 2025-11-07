"""
Build script to create Windows executable using PyInstaller
Run this script to create a standalone .exe file
"""
import os
import sys
import subprocess
import shutil

def build_executable():
    """Build the Windows executable"""
    print("=" * 60)
    print("Building Path of Exile Build Guide Executable")
    print("=" * 60)
    print()

    # Check if PyInstaller is installed
    try:
        import PyInstaller
        print("PyInstaller found!")
    except ImportError:
        print("PyInstaller not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("PyInstaller installed!")

    print()
    print("Building executable...")
    print()

    # PyInstaller command
    cmd = [
        "pyinstaller",
        "--onefile",
        "--windowed",
        "--name=PoEBuildGuide",
        "--add-data=templates;templates",
        "--add-data=static;static",
        "--hidden-import=flask",
        "--hidden-import=flask_cors",
        "--hidden-import=lxml",
        "--icon=NONE",
        "app.py"
    ]

    try:
        subprocess.check_call(cmd)
        print()
        print("=" * 60)
        print("Build successful!")
        print("=" * 60)
        print()
        print("The executable can be found in the 'dist' folder")
        print("File: dist/PoEBuildGuide.exe")
        print()
        print("You can copy this file anywhere and run it without Python installed!")
        print()

        # Create a distribution folder with necessary files
        dist_folder = "distribution"
        if os.path.exists(dist_folder):
            shutil.rmtree(dist_folder)

        os.makedirs(dist_folder, exist_ok=True)

        # Copy executable
        if os.path.exists("dist/PoEBuildGuide.exe"):
            shutil.copy("dist/PoEBuildGuide.exe", dist_folder)

        # Copy README
        if os.path.exists("README.md"):
            shutil.copy("README.md", dist_folder)

        print(f"Distribution package created in '{dist_folder}/' folder")
        print()

    except subprocess.CalledProcessError as e:
        print()
        print("=" * 60)
        print("Build failed!")
        print("=" * 60)
        print(f"Error: {e}")
        print()
        sys.exit(1)


if __name__ == "__main__":
    build_executable()
