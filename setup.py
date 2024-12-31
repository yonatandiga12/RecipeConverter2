# import os
#
# import certifi
# from cx_Freeze import setup, Executable
# os.environ["SSL_CERT_FILE"] = os.path.join(os.getcwd(), "cacert.pem")
#
# # Include additional files and folders
# include_files = [
#     "DAL/conversions.xlsx",  # Include Excel file
#     "DAL/table.csv",         # Include CSV file
#     "pictures/",             # Include pictures folder
#     (certifi.where(), "cacert.pem"),  # Add certifi's CA bundle
# ]
#
# # Required packages based on imports
# packages = [
#     "os",
#     "threading",
#     "webbrowser",
#     "tkinter",
#     "csv",
#     "re",
#     "dataclasses",
#     "typing",
#     "numpy",
#     "pytesseract",
#     "selenium",
#     "bs4",
#     "importlib",
#     "importlib_resources",  # Explicitly include importlib.resources to avoid errors
# ]
#
# # Options for build
# build_options = {
#     "packages": packages,
#     "include_files": include_files,
# }
#
# # Define the executable
# executables = [
#     Executable(
#         "main.py",
#         target_name="RecipeConverter.exe",  # Name of the output executable
#     )
# ]
#
# # Setup configuration
# setup(
#     name="RecipeConverter",
#     version="1.0",
#     description="A recipe conversion tool.",
#     options={"build_exe": build_options},
#     executables=executables,
# )


import os
import sys
import certifi
from cx_Freeze import setup, Executable

# Handle platform-specific settings
base = None
if sys.platform == "win32":
    base = "Win32GUI"  # Use this for GUI applications
    #base = None

# Set SSL certificate path
os.environ["SSL_CERT_FILE"] = os.path.join(os.getcwd(), "cacert.pem")

# Include additional files and folders
include_files = [
    "DAL/",
    "DAL/conversions.xlsx",
    "DAL/table.csv",
    "pictures/",
    (certifi.where(), "cacert.pem"),
    ("chromedriver.exe", "chromedriver.exe"),  # Add chromedriver
]

# Required packages
packages = [
    "os",
    "threading",
    "webbrowser",
    "tkinter",
    "csv",
    "re",
    "dataclasses",
    "typing",
    "numpy",
    "pytesseract",
    "selenium",
    "bs4",
    "importlib",
    "importlib_resources",
]

# Build options
build_options = {
    "packages": packages,
    "include_files": include_files,
    "include_msvcr": True,  # Include Visual C++ runtime
    "excludes": ["tkinter.test", "unittest"],  # Exclude unnecessary modules
    "zip_include_packages": "*",  # Zip all packages
    "zip_exclude_packages": [],  # Don't exclude any packages from zip
}

executables = [
    Executable(
        script="main.py",
        base=base,
        target_name="RecipeConverter.exe"
    )
]

setup(
    name="RecipeConverter",
    version="1.0",
    description="A recipe conversion tool.",
    options={"build_exe": build_options},
    executables=executables,
)