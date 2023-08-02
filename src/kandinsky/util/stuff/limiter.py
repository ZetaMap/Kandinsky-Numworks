# This script try to limit the heap size of python (max RAM to use).
#
# On Windows we don't have a dynamic heap limiter like Unix (Linux and MacOS)
# with the 'resource' module.
# So will manualy create classes and limit the actual job with his PID.
# This way call kernel methods so it can fail, if the throttling attempt fails,
# it will attempt to emulate latency with small latencies with 'time' module,
# but in general it works pretty well.
#
# For Linux and MacOS is more simple, will just import the 'resource' module
# and set the size python heap.
# And if the request fails, doing same thing of windows if failed.
#
#
# Windows example: https://stackoverflow.com/a/16791778
# Unix example: https://stackoverflow.com/a/53617847

from sys import platform
from sdl2._internal import prettywarn

__all__ = [
  "set_heap",
  "usleep"
]



if platform == "win32":
  import ctypes

  PROCESS_SET_QUOTA = 0x100
  PROCESS_TERMINATE = 0x1
  JobObjectExtendedLimitInformation = 9
  JOB_OBJECT_LIMIT_PROCESS_MEMORY = 0x100

  class IO_COUNTERS(ctypes.Structure):
    _fields_ = [
      ('ReadOperationCount', ctypes.c_uint64),
      ('WriteOperationCount', ctypes.c_uint64),
      ('OtherOperationCount', ctypes.c_uint64),
      ('ReadTransferCount', ctypes.c_uint64),
      ('WriteTransferCount', ctypes.c_uint64),
      ('OtherTransferCount', ctypes.c_uint64)
    ]

  class JOBOBJECT_BASIC_LIMIT_INFORMATION(ctypes.Structure):
    _fields_ = [
      ('PerProcessUserTimeLimit', ctypes.c_int64),
      ('PerJobUserTimeLimit', ctypes.c_int64),
      ('LimitFlags', ctypes.c_uint32),
      ('MinimumWorkingSetSize', ctypes.c_void_p),
      ('MaximumWorkingSetSize', ctypes.c_void_p),
      ('ActiveProcessLimit', ctypes.c_uint32),
      ('Affinity', ctypes.c_void_p),
      ('PriorityClass', ctypes.c_uint32),
      ('SchedulingClass', ctypes.c_uint32)
    ]

  class JOBOBJECT_EXTENDED_LIMIT_INFORMATION(ctypes.Structure):
    _fields_ = [
      ('BasicLimitInformation', JOBOBJECT_BASIC_LIMIT_INFORMATION),
      ('IoInfo', IO_COUNTERS),
      ('ProcessMemoryLimit', ctypes.c_void_p),
      ('JobMemoryLimit', ctypes.c_void_p),
      ('PeakProcessMemoryUsed', ctypes.c_void_p),
      ('PeakJobMemoryUsed', ctypes.c_void_p)
    ]

  # Set memory limit for process with specfied 'pid', to specified 'size' in bytes
  def set_heap(pid, size):
    assert size < 0 or size > 4095, "heap size must be greater than 4096 bytes or -1"

    job_info = JOBOBJECT_EXTENDED_LIMIT_INFORMATION()

    job = ctypes.windll.kernel32.CreateJobObjectA(None, None)
    assert job != 0, "ouch... that hurt, fatal error"

    assert ctypes.windll.kernel32.QueryInformationJobObject(
      job,
      JobObjectExtendedLimitInformation,
      ctypes.POINTER(JOBOBJECT_EXTENDED_LIMIT_INFORMATION)(job_info),
      ctypes.sizeof(JOBOBJECT_EXTENDED_LIMIT_INFORMATION),
      ctypes.POINTER(ctypes.c_uint32)(ctypes.c_uint32())
    ), "cannot create job handle"

    job_info.BasicLimitInformation.LimitFlags |= JOB_OBJECT_LIMIT_PROCESS_MEMORY
    job_info.ProcessMemoryLimit = size
    assert ctypes.windll.kernel32.SetInformationJobObject(
      job,
      JobObjectExtendedLimitInformation,
      ctypes.POINTER(JOBOBJECT_EXTENDED_LIMIT_INFORMATION)(job_info),
      ctypes.sizeof(JOBOBJECT_EXTENDED_LIMIT_INFORMATION)
    ), "cannot create new job informations, probably invalid heap size"

    process = ctypes.windll.kernel32.OpenProcess(PROCESS_SET_QUOTA | PROCESS_TERMINATE, False, pid)
    assert process != 0, f"process '{pid}' not found"

    assert ctypes.windll.kernel32.AssignProcessToJobObject(job, process), "cannot assign new process informations"
    assert ctypes.windll.kernel32.CloseHandle(job), "failed to closing job handle"
    assert ctypes.windll.kernel32.CloseHandle(process), "failed closing process handle"

else:
  import resource
  set_heap = lambda pid, size: resource.prlimit(pid, resource.RLIMIT_DATA, (size, resource.getrlimit(resource.RLIMIT_DATA)[1]))


# Try to find an real time clock to do microseconds sleeps
if platform == "win32":
  # Try to use module win-precise-time to get more sleeps precision
  try:
    import win_precise_time as _wpt
    usleep = lambda us: _wpt.sleep_until_ns(int(_wpt.time_ns()+us*1000))
  except:
    import time as _time
    prettywarn("win-precise-time module is not installed. Using time module to do usleep (emulation will be less accurate)", RuntimeWarning)
    def usleep(us):
      t = _time.perf_counter_ns()+us*1000
      while _time.perf_counter_ns() < t: _time.sleep(1e-9)

elif platform == "linux":
  try:
    import ctypes
    usleep = ctypes.CDLL("libc.so.6").usleep
    del ctypes
  except:
    # On some linux distribution, this library is not installed by default
    import time as _time
    prettywarn("libc6 library is not installed. Using time module to do usleep (emulation will be less accurate)", RuntimeWarning)
    usleep = lambda us: _time.sleep(us/10e6)

else:
  # MacOS don't have libc6 library and idk for other OS so just do a normal sleep
  import time as _time
  usleep = lambda us: _time.sleep(us/10e6)



# Other stuff, 
# because there is a bug when window changing monitor 
# (only on macos... again... this is a poor platform)
def get_monitors():
  import ctypes
  class RECT(ctypes.Structure):
    _fields_ = [
      ('left', ctypes.c_long),
      ('top', ctypes.c_long),
      ('right', ctypes.c_long),
      ('bottom', ctypes.c_long)
      ]
    def dump(self):
      return [int(val) for val in (self.left, self.top, self.right, self.bottom)]

  retval = {}
  def cb(hMonitor, hdcMonitor, lprcMonitor, dwData):
    retval.update({hMonitor: lprcMonitor.contents.dump()})
    return True
  ctypes.windll.user32.EnumDisplayMonitors(0, 0, ctypes.WINFUNCTYPE(ctypes.c_int, ctypes.c_ulong, ctypes.c_ulong, ctypes.POINTER(RECT), ctypes.c_double)(cb), 0)
  return retval
