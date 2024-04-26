import sys, os, shutil
from setuptools import setup

# Used by setup script to restore the version to 'null' in __init__.py after builded the library
RESTORE_VERSION = "--version-null" in sys.argv

# Version of library
VERSION = "2.7.2"

# Get the absolute path
PATH = __file__[:__file__.rfind('\\')+1 or __file__.rfind('/')+1]

# Copy README and FAQ
shutil.copy(PATH+"src/kandinsky/README.md", PATH+"README.md")
with open(PATH+"README.md", "rt", encoding="utf-8") as f: DOC = f.read()
shutil.copy(PATH+"src/kandinsky/FAQ.md", PATH+"FAQ.md")

# Set the version in __init__.py
with open(PATH+"src/kandinsky/__init__.py", "rt", encoding="utf-8") as f: buffer = f.readlines()
for i, l in enumerate(buffer):
  if "__version__" in l:
    if RESTORE_VERSION:
      if VERSION in l: buffer[i] = l.replace(VERSION, "null")
      else: buffer[i] = f"__version__ = \"null\"\n"
    elif "null" in l: buffer[i] = l.replace("null", VERSION)  
    else: buffer[i] = f"__version__ = \"{VERSION}\"\n"
    break
with open(PATH+"src/kandinsky/__init__.py", "wt", encoding="utf-8") as f: f.writelines(buffer)

# Stop here if restore version to 'null'
if RESTORE_VERSION: exit()

# Remove __pycache__ everywhere
def clean_pycache(path="."):
  """Clean __pycache__ directories recursively. Call this before setup()."""
  for file in os.listdir(path):
    new_path = os.path.join(path, file)
    if os.path.isdir(new_path): 
      if file == "__pycache__": 
        # Remove a file or a directory recursively using terminal commands.
        # This way avoid some permissions errors.
        if os.name == "nt": os.system(("rd /s" if os.path.isdir(new_path) else "del /f") + " /q \"" + new_path.replace('/', '\\') + "\"")
        else: os.system("rm -rf \"" + new_path.replace('\\', '/') + "\"")
      else: clean_pycache(new_path)
clean_pycache(PATH)

# Run setup
setup(
  name='kandinsky', 
  version=VERSION, 
  author='ZetaMap', 
  description='A small module allowing to link the kandinsky module, from the Numworks, to a window.', 
  license='MIT', 
  long_description=DOC, 
  long_description_content_type='text/markdown', 
  url='https://github.com/ZetaMap/Kandinsky-Numworks', 
  project_urls = {
    'GitHub Project': 'https://github.com/ZetaMap/Kandinsky-Numworks', 
    'My GitHub Page': 'https://github.com/ZetaMap/',
  }, 
  classifiers = [
    'Programming Language :: Python :: 3', 
    'License :: OSI Approved :: MIT License', 
    'Operating System :: Microsoft :: Windows', 
    'Operating System :: Unix', 
    'Operating System :: MacOS :: MacOS X',
  ], 
  package_dir = {"": "src"},
  packages = [
    "kandinsky",
    "kandinsky.util",
    "kandinsky.util.stuff",
    "kandinsky.util.data",
  ],
  package_data = {"": ["**"]},
  install_requires = [
    'pysdl2', 
    'pysdl2-dll',
    'pyobjc-core ; sys_platform=="darwin"',
    'pyobjc-framework-Cocoa ; sys_platform=="darwin"',
  ], 
  python_requires='>=3.6',
)
