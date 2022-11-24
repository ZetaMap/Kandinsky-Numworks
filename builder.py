#!/usr/bin/env python
from setuptools import find_packages
from os import listdir, path as os_path, remove, mkdir, system

# Setup files files environ
print("Cleaning files ...")
try: 
  mkdir("src/kandinsky.egg-info")
  remove("build")
  remove("dist")
  remove("setup.py")
  remove("src/kandinsky/__pycache__")
  remove("src/kandinsky/util/__pycache__")
  remove("src/kandinsky/util/stuff/__pycache__")
except: pass
DOC=""
with open("src/kandinsky/README.md", "rt", encoding="utf-8") as f:
  with open("README.md", "wt", encoding="utf-8") as ff: ff.write(f.read())
  DOC = f.read()

# Metadata
print("Generating setup.py ...")
METADATA = {
  "name": "kandinsky",
  "version": "2.1.dev2",
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
  "include_dirs": find_packages(where="src", include=".*"),
  "install_requires": ["pysdl2", "pysdl2-dll"],
  "include_package_data": True
}


def find_all(path='', exclude=[]):
  found = []
  for i in listdir(None if path == '' else path):
    if i not in exclude:
      if os_path.isdir(path+i): found.extend(find_all(path+i+'/'))
      else: found.append(path+i) 
  return found

# add all files in SOURCES.txt
with open("src/kandinsky.egg-info/SOURCES.txt", 'w') as f: 
  for i in find_all(exclude=["__pycache__", "publish.bat", "builder.py", ".git", ".github"]): f.write(i+'\n')

# replace __version__ in __init__.py
with open("src/kandinsky/__init__.py") as f: new_content = f.readlines()
for i in range(len(new_content)):
  if "__version__" in new_content[i]:
    new_content[i] = f"__version__ = '{METADATA['version']}'\n"
    break  
with open("src/kandinsky/__init__.py", 'w') as f: f.writelines(new_content)

# auto gen setup file
with open("setup.py", 'w') as f: 
  f.write(f"""# AUTO GENERATED FILE. DO NOT EDIT!
from setuptools import setup 
setup(**{METADATA})""")

# install build module, build, install, and clean
print("Installing build module ...")
system("pip install build")
print("\nBuilding library ...")
system("python -m build")
if input("\nWould you like to install library? [y|N]: ").lower() == 'y': system("pip install .")
else: print("Installation canceled. ")
print("All done")
