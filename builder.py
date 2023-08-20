#!/usr/bin/env python3

from setuptools import find_packages
from os import listdir, path as os_path, mkdir, system
from sys import argv, platform

# If True, just setup files and exit
JUST_SETUP = "-s" in argv


# Setup files files environ
def clear_files():
  def clear(path):
    try:
      if os_path.exists(path):
        if platform.startswith("win"): system(("rd /s" if os_path.isdir(path) else "del /f") + " /q \"" + path.replace('/', '\\') + "\" 2> nul")
        else: system("rm -rf \"" + path.replace('\\', '/') + "\" 2> /dev/null")
    except: pass
  print("Cleaning files ...")

  clear("build")
  if os_path.exists("dist") and len(listdir("dist")) and input("WARNING: dist folder not empty, delete? [y|N]") == 'y': clear("dist")
  clear("setup.py")
  clear("src/kandinsky.egg-info")
  clear("__pycache__")
  clear("src/kandinsky/__pycache__")
  clear("src/kandinsky/util/__pycache__")
  clear("src/kandinsky/util/stuff/__pycache__")

clear_files()
DOC="<unknown>"
with open("src/kandinsky/README.md", "rt", encoding="utf-8") as f:
  DOC = f.read()
  with open("README.md", "wt", encoding="utf-8") as ff: ff.write(DOC)
with open("src/kandinsky/FAQ.md", "rt", encoding="utf-8") as f:
  with open("FAQ.md", "wt", encoding="utf-8") as ff: ff.write(f.read())

# For me. Just to setup files, and exit
if JUST_SETUP: exit()

# Metadata
print("Generating setup.py ...")
METADATA = {
  "name": "kandinsky",
  "version": "2.6",
  "author": "ZetaMap",
  "description": "A small module allowing to link the kandinsky module, from the Numworks, to a window.",
  "license": 'MIT',
  "long_description": DOC,
  "long_description_content_type": 'text/markdown',
  "url": "https://github.com/ZetaMap/Kandinsky-Numworks",
  "project_urls": {
    "GitHub Project": "https://github.com/ZetaMap/Kandinsky-Numworks",
    "My GitHub Page": "https://github.com/ZetaMap/"
  },
  "classifiers": [
    'Programming Language :: Python :: 3',
    'License :: OSI Approved :: MIT License',
    'Operating System :: Microsoft :: Windows',
    'Operating System :: Unix',
    'Operating System :: MacOS :: MacOS X',
  ],
  "package_dir": {"": "src"},
  "include_dirs": find_packages(where="src", exclude="__pycache__", include="*.*"),
  "install_requires": ["pysdl2", "pysdl2-dll"],
  "include_package_data": True,
  "python_requires": '>=3.6',
}
# This is needed for MacOS because Tkinter give wrong widget id, so will get it manually
if platform == "darwin": METADATA["install_requires"].extend(["pyobjc-core", "pyobjc-framework-Cocoa"])

def find_all(path='', exclude=[]):
  found = []
  for i in listdir(None if path == '' else path):
    if i not in exclude:
      if os_path.isdir(path+i): found.extend(find_all(path+i+'/'))
      else: found.append(path+i)
  return found

mkdir("src/kandinsky.egg-info")

# add all files in SOURCES.txt
with open("src/kandinsky.egg-info/SOURCES.txt", 'w') as f:
  for i in find_all(exclude=["__pycache__", "publish.bat", "builder.py", ".git", ".github", "dist"]): f.write(i+'\n')

# replace __version__ in __init__.py
with open("src/kandinsky/__init__.py") as f: new_content = f.readlines()
for i in range(len(new_content)):
  if "__version__" in new_content[i]:
    new_content[i] = f"__version__ = \"{METADATA['version']}\"\n"
    break
with open("src/kandinsky/__init__.py", 'w') as f: f.writelines(new_content)

# auto gen setup file
with open("setup.py", 'w', encoding="utf-8") as f:
  f.write("""# AUTO GENERATED FILE. DO NOT EDIT!
from setuptools import setup
setup(
{}
)""".format('\n'.join([f"\t{k}={repr(v)}," for k, v in METADATA.items()])))

# install build module, build, install, and clean
print("Installing 'build' module ...")
system("pip install build")
print("\nBuilding library ...")
if system("python -m build") != 0: exit(1)
if input("\nInstall library? [y|N]: ").lower() == 'y': system("pip install .")
else: print("Installation canceled. ")
if input("\nClear setup files? [Y|n]: ").lower() != 'n':
  clear_files()
  # replace __version__ in __init__.py
  with open("src/kandinsky/__init__.py") as f: new_content = f.readlines()
  for i in range(len(new_content)):
    if "__version__" in new_content[i]:
      new_content[i] = f"__version__ = \"null\"\n"
      break
  with open("src/kandinsky/__init__.py", 'w') as f: f.writelines(new_content)

print("All done")
