#import os
##os.environ["KANDINSKY_ENABLE_DEBUG"]=''
##os.environ["KANDINSKY_OS_MODE"]='4'
##os.environ['KANDINSKY_SCREEN_SIZE'] = '520x240'
#os.environ['KANDINSKY_ZOOM_RATIO'] = '2'
#
#from math import *
#from __init__ import *
#from time import *
#
##get_keys()
#def draw(index, loop, clear):
#  if clear: fill_rect(0, 0, 350, 250, (255,255,255))
#  draw_string(str(1+(len(_list)+index if index < 0 else index)), 5, 5, (100,100,100))
#  draw_string("<", 219, 200, (100,100,100))
#  fill_rect(220, 215, 15, 1, (100,100,100))
#  fill_rect(235, 216, 1, -7, (100,100,100))
#  fill_rect(236, 208, -15, 1, (100,100,100))
#
#  draw_string("to skip", 245, 202, (100,100,100))
#  exec("""for p in range({}):
#    for i in range(496): 
#      try: set_pixel(160+round({}), 110+round({}), {})
#      except (OverflowError, ZeroDivisionError, ValueError):
#        continue
#      except KeyboardInterrupt: raise RuntimeError
#      except: raise
#  """.format(loop, _list[index][0], _list[index][1],
#    "(cos(p)*1000, sin(i)*1000, log10(i-p)*1000)" \
#      if _list[index][2] == True else "(0, 0, 0)"))
#
#def start():
#  x, loop = input("""{} equations found in the list.
#Let empty to run all.
#|-> """.format(len(_list))), input("""
#Let empty for default value.
#Loop: """)
#  loop = 400 if loop == '' else int(loop)
#  r = range(len(_list)) if x == '' else range(int(x)-1, int(x))
#
#  for ii in r:
#    time = monotonic()
#    try: draw(ii, loop, 1)
#    except (SyntaxError, IndexError): raise
#    except:
#      try: draw(ii, 1, 0)
#      except: pass
#    print("Drawn", ii+1, "in", int(monotonic()-time), "s")
#  draw_string("End", 5, 5, (100,100,100))
#     
#_list=[
##           for x         |           for y           | color?
#  ("cos(i)*111/(cos(p)+1)", "sin(i)*111/(sin(p)+1)"   , 1), #1
#  ("cos(i)*111+p"         , "sin(i)*111+p"            , 1), #2
#  ("cos(i)*111/(tan(p)+1)", "sin(i)*111/(sin(p)+1)"   , 1), #3
#  ("cos(i)*111/(tan(p)+1)", "tan(i)*111/(sin(p))"     , 1), #4
#  ("cos(i)*111/(1-cos(p)+1)", "sin(i)*111/(-sin(p)+1)", 1), #5
#  ("cos(i)*111/(cos(p)+1)", "sin(i)/(sin(p)+1)"       , 1), #6
#  ("cos(i)*111/(cos(p)+1)", "sin(i)*111/cos(p)**2"    , 1), #7
#  ("cos(i)*111/(cos(p)+1)", "sin(i)*111/(cos(p)**2+1)", 1), #8
#  ("cos(i)*111/(cos(p)+1)", "sin(i)*130/(tan(tan(p)))", 1), #9
#  ("tan(tan(i))*111/sin(p)", "tan(i)*111/cos(sin(p))" , 1), #10
#  ("cos(i)*p"             , "sin(i)*p"                , 1), #11
#  ("tan(tan(i))*p"        , "sin(i)*p"                , 1), #12  
#  ("cos(p)*i"             , "tan(p)*i"                , 0), #13
#  ("tan(tan(tan(i)))/tan(p)", "tan(i)*p/sin(p)"       , 1), #14
#  ("cos(tan(i))*p"        , "cos(i)*p"                , 1), #15
#  ("sin(i)*p*cos(sin(i))" , "sin(p)*111/cos(tan(i))"  , 1), #16
#  ("cos(p)*i*tan(cos(p))-111", "cos(i)*p/tan(i)"      , 1), #17
#  ("sin(cos(tan(p)))*i"   , "tan(i)*p"                , 1), #18
#  ("exp(abs(log(p)))*sin(i)", "log(p)/cos(i)*10"      , 1), #19
#  ("exp(abs(log(p,i)))*64*sin(i)", "log(p)/cos(i)*5"  , 1), #20
#  ("exp(abs(log(p)))*sin(i)", "sin(i)*50/sin(p)"      , 1), #21
#  ("cos(p)*50/(sin(i)+1)" , "abs(p)/cos(i)"           , 1), #22
#  ("asinh(p)/cos(i)"      , "cos(p)*111*sin(i)"       , 1), #23
#  ("acosh(p)*111/(tan(i)+1)", "cos(p)*150/asinh(i)"   , 1), #24
#  ("trunc(i)/cos(p)"      , "acosh(i)/-sin(p)"        , 0), #25
#  ("cos(i)*50/(tan(p)+1)" , "acosh(i)*5/-tan(p)"      , 1), #26
#  ("cos(i)*50/(tan(p)+1)" , "sin(i)*50/(cos(p))"      , 1), #27
#]
#
#start()
#
#exit()
#
#import os
#os.environ["KANDINSKY_OS_MODE"]="3"
#import __init__ as kandinsky
#from ion import keydown
#from time import perf_counter_ns
#from math import cos, sin, log10
#
#def wait_key():
#  while True:
#    for i in range(53):
#      if keydown(i):
#        while keydown(i): pass
#        return i
#
#def test(method, *args):
#  func = getattr(kandinsky, method)
#  values = []
#  for i in range(300):
#    time_is = perf_counter_ns()
#    func(*args)
#    values.append((perf_counter_ns()-time_is)/1000)
#    kandinsky.fill_rect(0, 0, 320, 220, "white")
#
#  #print(values)
#  print(method, "speed:", sum(values)/len(values), "µs; min:", min(values), "max:", max(values))
#
#kandinsky.draw_string("Welcome to kandinsky speed test program", 5, 50)
#kandinsky.draw_string("Press a key to start test ...", 15, 70)
#wait_key()
#kandinsky.fill_rect(0, 0, 320, 220, "white")
#
#test("set_pixel", 10, 10, "black")
#print("100*100: ", end='')
#test("fill_rect", 10, 10, 100, 100, "black")
#print("1*1: ", end='')
#test("fill_rect", 10, 10, 1, 1, "black")
#print("200*200: ", end='')
#test("fill_rect", 10, 10, 200, 200, "black")
#test("draw_string", "test string", 10, 10)
#print("100*100: ", end='')
#test("draw_circle", 110, 110, 100, "black")
#print("10*10: ", end='')
#test("draw_circle", 110, 110, 10, "black")
#print("100*100: ", end='')
#test("fill_circle", 110, 110, 100, "black")
#print("10*10: ", end='')
#test("fill_circle", 110, 110, 10, "black")
#for i in range(300): kandinsky.set_pixel(10+i, 10, (cos(i)*1000, sin(i)*1000, log10(i+1)*1000))
#values = []
#for i in range(300):
#  time_is = perf_counter_ns()
#  kandinsky.get_pixel(10+i, 10)
#  values.append((perf_counter_ns()-time_is)/1000)
#print("get_pixel speed:", sum(values)/len(values), "µs")
#for i in range(300):
#  time_is = perf_counter_ns()
#  kandinsky.color((cos(i)*1000, sin(i)*1000, log10(i+1)*1000))
#  values.append((perf_counter_ns()-time_is)/1000)
#print("color speed:", sum(values)/len(values), "µs")
#input(">>> ")
#
#exit()

"""This is a demo code
Source: https://my.numworks.com/python/zetamap/snake_lite
"""
print("""This is a demo code
Source: https://my.numworks.com/python/zetamap/snake_lite""")
__all__ = []

import os
#os.environ['KANDINSKY_ENABLE_DEBUG'] = ''
#os.environ['KANDINSKY_ZOOM_RATIO'] = '2'
#os.environ['KANDINSKY_SCREEN_SIZE'] = '1020x240'

#############################################################

from random import randint as ri
from __init__ import fill_rect as fr, draw_string as ds
from ion import keydown as kd
from time import monotonic as mt, sleep as sl

DECODE=lambda v: ((v&0xfff000)>>12, v&0xfff)
class Snake:
 c=[(50,50,50),(240,240,240),(0,255,0),"green","red","blue","#7ea2ce"]
 def __init__(s,leader_board=(),speed=10,power=2,size=10,score=1,inf_snake=False,gost=False,darkmode=True,rainbow=False,walls=True):
  if inf_snake: power=float("inf")
  if not darkmode: s.c[0],s.c[1]=s.c[1],s.c[0]
  try: from __init__ import get_keys
  except ImportError: 
   try: from ion import get_keys
   except ImportError: s.c[6]="#ffb531"
   else: s.c[6]="#c53431"
  s.lb,s.s,s.p,s.m,s.ti,s.g,s.go,s.r,s.w,s.bo=leader_board,1/speed,power,score,size,(320//size-1,220//size-1),gost,rainbow,walls,bool(walls)
 def nc(s):
  s.ch=[ri(s.bo,s.g[i]-s.bo) for i in range(2)]
  while s.ch[0]<<12|s.ch[1] in s.b: s.ch=[ri(s.bo,s.g[i]-s.bo) for i in range(2)]
  fr(s.ch[0]*s.ti,2+s.ch[1]*s.ti,s.ti,s.ti,s.c[4])
 def dl(s):
  fr(0,2,320,220,"black")
  fr(0,2,(s.g[0]+1)*s.ti,(s.g[1]+1)*s.ti,s.c[5 if s.w else 0])
  if s.w: fr(s.ti//2,2+s.ti//2,s.g[0]*s.ti,s.g[1]*s.ti,s.c[0])
 def dt(s,text,x,y):
  for i,l in enumerate(text.replace('\t', "    ")):
   ds(l,x+10*i,y,s.c[1],s.c[0])
   if l!=' ': sl(0.02)
 def ub(s,l1,l2):
  fr(20,82,280,50,s.c[4])
  fr(25,87,270,40,s.c[0])
  s.dt(l1,25,87)
  s.dt(l2,25,107)
  sl(0.2)
  while 1:
   sl(0.01)
   if kd(4): return 1
   elif kd(17): return 0
 def wu(s):
  s.t=mt()
  s.ta,s.te=(s.b[-1], DECODE(s.b[-1])),DECODE(s.b[0])
  if kd(0) and s.d[0]!=1: s.d=[-1,0]
  elif kd(1) and s.d[1]!=1: s.d=[0,-1]
  elif kd(2) and s.d[1]!=-1: s.d=[0,1]
  elif kd(3) and s.d[0]!=-1: s.d=[1,0]
  fr(s.te[0]*s.ti,2+s.te[1]*s.ti,s.ti,s.ti,[ri(0,255) for i in range(3)] if s.r else s.c[3])
  for x in range(len(s.b)-1,0,-1): s.b[x]=s.b[x-1]
  s.b[0]=((s.te[0]+s.d[0])%s.g[0])<<12|((s.te[1]+s.d[1])%s.g[1])
  if s.a>0:
   s.b.append(s.ta[0])
   s.a-=1
  elif s.ta[0] not in s.b: fr(s.ta[1][0]*s.ti,2+s.ta[1][1]*s.ti,s.ti,s.ti,s.c[0])
  if s.b[0]==s.ch[0]<<12|s.ch[1]:
   s.a,s.sc=s.a+s.p,s.sc+s.m
   s.nc()
  s.te=DECODE(s.b[0])
  if not s.go:
   if s.w and (s.te[0]==0 or s.te[1]==0 or s.te[0]==s.g[0] or s.te[1]==s.g[1]): return 0
   for x in range(1,len(s.b)):
    if s.b[x]==s.b[0]: return 0
  fr(s.te[0]*s.ti,2+s.te[1]*s.ti,s.ti,s.ti,s.c[2])
  ds(str(s.sc),7,7,s.c[1],s.c[0])
  return 1
 def start(s):
  fr(0,0,320,2,s.c[6])
  try:
   while 1:
    s.b,s.a,s.d,s.sc=[(s.g[0]//2)<<12|(s.g[1]//2)],4,(1,0),0
    s.dl()
    s.nc()
    while s.wu():
     if kd(17):
      s.ub("\t\tGame Paused!","  (OK, DELETE = Continue)")
      sl(0.2)
      s.dl()
      fr(s.ch[0]*s.ti,2+s.ch[1]*s.ti,s.ti,s.ti,s.c[4])
      for i in s.b:
       s.te=DECODE(i)
       fr(s.te[0]*s.ti,2+s.te[1]*s.ti,s.ti,s.ti,[ri(0,255) for i in range(3)] if s.r else s.c[3])
     while mt()-s.t<s.s: sl(0.01)
    if not s.ub(' '*(3-len(str(s.sc))//2)+"You lose!\tScore: "+str(s.sc),"(OK = Retry, DELETE = Quit)"): break
   s.te=0
   print("Your score:",s.sc,"\nLeader board: (default settings)")
   for i,sc in enumerate(s.lb):
    if len(sc[0])>s.te:s.te=len(sc[0])
    print(' '+str(i+1)+'-',sc[0]+':',sc[1])
   fr(0,2,320,220,s.c[0])
   s.dt("Your score: "+str(s.sc),5,7)
   s.dt("Leader board:",5,32)
   for i,sc in enumerate(s.lb): s.dt(sc[0]+':'+' '*(s.te-len(sc[0])+2)+str(sc[1]),60,52+20*i)
   l=['>'*i+' '*(4-i)+s.lb[0][0]+':'+' '*(s.te-len(s.lb[0][0])+2)+str(s.lb[0][1])+' '*(4-i)+'<'*i for i in range(4)]
   while not kd(4) and not kd(17):
    for i in l:
     sl(0.2)
     if kd(4) or kd(17): break
     ds(i,20,52,s.c[6],s.c[0])
  except KeyboardInterrupt: pass
  
Snake(( # Leader board: ("name", score),
 ("Alteur",38),
 ("ZetaMap",30),
 ("Nios",23),
 ("Alpha6Frost",17),

), # Game settings: power, speed, size, score, inf_snake, darkmode, rainbow, gost, walls
#  walls=False,
#  size=5, # 1 -> 80
#  darkmode=False
).start()
