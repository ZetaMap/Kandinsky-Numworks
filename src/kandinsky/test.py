from math import *
from kandinsky import *

x, y = 100, 100
fill_rect(0,0,320,222,(0,)*3)

def s(a): return 105 * sin(a / 10)

for a in range(9999):
  set_pixel(x+int(s(a)), y+int(cos(a / 10) * s(a * .95)), "red")
exit()
import os
os.environ["KANDINSKY_OS_MODE"]="3"
from time import *
from __init__ import *
from random import *
from math import *
from test import *

b=[[[[321, 155], [-12, 170], [232, 265]], [[112, 164], [327, -24], [167, 300]], [[168, -21], [323, 126], [346, -44]], [[128, 245], [281, 102], [17, 165]], [[23, 164], [110, 162], [355, 35]], [[-26, 245], [75, 65], [221, 152]], [[239, 283], [9, -27], [203, -30]], [[165, 275], [366, 4], [345, 101]], [[30, 233], [121, -18], [167, 292]], [[-97, 219], [147, 221], [-85, 131]], [[9, 163], [-49, 286], [295, 10]], [[306, 205], [313, 276], [25, 98]], [[24, 76], [4, 257], [206, -51]], [[-82, 299], [372, 103], [385, 47]], [[32, 8], [284, 214], [18, 162]], [[269, 47], [279, 115], [261, 257]], [[244, -10], [209, 280], [370, 177]], [[207, -33], [217, 53], [75, 82]], [[237, -80], [-2, 131], [297, 230]], [[196, 32], [203, 20], [129, -98]], [[112, 66], [394, 77], [353, 194]], [[395, 62], [311, 168], [-1, -55]], [[90, 118], [-12, 138], [340, 38]], [[297, 170], [374, 24], [210, 3]], [[-16, 124], [388, 221], [-55, 265]], [[219, -78], [185, -47], [310, 289]], [[-4, 203], [90, 12], [210, 217]], [[31, 94], [174, 100], [337, 22]], [[285, -6], [338, 41], [208, 181]], [[37, 163], [56, 149], [123, 108]], [[354, 81], [266, 158], [-96, 104]], [[151, -54], [224, -25], [338, 67]], [[346, 250], [363, 263], [-20, -13]], [[142, 22], [271, 107], [-57, 37]], [[119, 273], [-89, 268], [144, 263]], [[133, 186], [131, 24], [-61, -1]], [[-5, 18], [161, 291], [276, 213]], [[169, 189], [323, 216], [-91, -60]], [[166, -16], [-87, -21], [59, -61]], [[383, 145], [-26, 48], [271, 42]], [[320, 143], [178, 41], [327, -12]], [[-60, 186], [71, 264], [-16, -45]], [[94, 47], [78, -50], [227, 258]], [[263, 6], [-60, -92], [370, -87]], [[307, -39], [274, -100], [101, 246]], [[151, 275], [289, 7], [313, 164]], [[17, 23], [165, 23], [40, 95]], [[-32, 199], [18, 188], [110, 81]], [[51, -43], [166, 196], [374, 20]], [[195, 264], [340, 130], [58, -27]], [[90, -36], [116, 130], [-98, -61]], [[100, 23], [38, 24], [-7, 24]], [[162, 145], [273, 157], [346, 60]], [[248, 21], [272, 238], [259, 109]], [[288, 184], [-63, 46], [396, 21]], [[77, 67], [223, -41], [334, 80]], [[246, -21], [135, 48], [395, 113]], [[161, -76], [308, -75], [382, 90]], [[-39, 245], [300, -24], [263, 34]], [[359, 291], [109, 134], [277, 91]], [[24, -95], [-45, 96], [304, -23]], [[300, 214], [352, 195], [1, 274]], [[339, -38], [-36, -5], [322, 73]], [[70, 274], [268, 182], [139, 283]], [[337, 111], [221, -94], [-87, -39]], [[212, -74], [38, 16], [139, 176]], [[218, 267], [215, 100], [-31, 153]], [[41, 91], [84, 140], [62, 209]], [[41, 40], [-42, 195], [387, 47]], [[-75, 276], [184, -95], [186, 235]], [[216, -79], [-45, 268], [371, 35]], [[169, 8], [-46, 245], [135, 260]], [[21, 68], [143, 159], [-96, 67]], [[165, 274], [-41, 207], [6, 35]], [[-84, 115], [377, -18], [156, 55]], [[-20, 221], [26, 45], [-34, 120]], [[172, 123], [-96, 215], [238, 23]], [[-13, 107], [166, -98], [320, 293]], [[-71, 170], [249, -78], [174, 230]], [[322, 87], [289, 202], [211, 119]], [[220, 92], [38, -95], [315, 131]], [[154, 207], [150, -89], [-21, 112]], [[143, 154], [360, 212], [16, 175]], [[-14, 108], [-95, 169], [260, 68]], [[81, 204], [367, -28], [248, 135]], [[97, 159], [303, 65], [90, 289]], [[325, 162], [154, 270], [90, 74]], [[245, 82], [361, 78], [-50, 64]], [[310, -5], [37, 228], [203, 72]], [[-40, -5], [-1, 194], [315, 187]], [[186, 231], [19, 139], [100, -65]], [[63, 287], [97, -21], [381, 7]], [[-4, 209], [52, 218], [6, -82]], [[-65, 55], [300, 115], [63, 23]], [[395, -94], [269, 91], [-90, 39]], [[380, 86], [14, 6], [231, -78]], [[-60, 4], [203, 135], [343, 205]], [[-29, 111], [58, 220], [-38, 156]], [[167, -60], [365, 177], [236, 184]], [[207, 286], [50, 268], [239, 46]]]]

values = []
for i in range(len(b[0])):
  time_is = perf_counter()
  fill_polygon(b[0][i],(cos(i)*1000, sin(i)*1000, log10(i+1)*1000))
  values.append(perf_counter()-time_is)
  fill_rect(0, 0, 320, 222, "white")
print("fill_polygon", "speed:", sum(values)/len(values)*10**6, "μs")
o=sum([sum([sum(y) for y in x]) for x in b[0]])
print((o/sqrt(o)/0.15)*2)

exit()

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
import os
os.environ["KANDINSKY_OS_MODE"]="3"
import __init__ as kandinsky
from ion import keydown
from time import perf_counter_ns
from math import cos, sin, log10

def wait_key():
  while True:
    for i in range(53):
     if keydown(i):
        while keydown(i): pass
        return i

def test(method, *args):
  func = getattr(kandinsky, method)
  values = []
  for i in range(300):
    time_is = perf_counter_ns()
    func(*args)
    values.append((perf_counter_ns()-time_is)/1000)
    kandinsky.fill_rect(0, 0, 320, 220, "white")

  #print(values)
  print(method, "speed:", sum(values)/len(values), "µs; min:", min(values), "max:", max(values))

kandinsky.draw_string("Welcome to kandinsky speed test program", 5, 50)
kandinsky.draw_string("Press a key to start test ...", 15, 70)
#wait_key()
input()
kandinsky.fill_rect(0, 0, 320, 220, "white")

test("set_pixel", 10, 10, "black")
print("100*100: ", end='')
test("draw_line", 10, 10, 150, 100, "black")
print("10*10: ", end='')
test("draw_line", 20, 20, 50, 30, "black")
print("1*1: ", end='')
test("draw_line", 20, 20, 21, 21, "black")
print("30*30: ", end='')
test("draw_line", 20, 20, 40, 20, "black")
test("draw_line", 20, 20, 20, 40, "black")
test("draw_string", "test string", 10, 10)
for i in range(300): kandinsky.set_pixel(10+i, 10, (cos(i)*1000, sin(i)*1000, log10(i+1)*1000))
values = []
for i in range(300):
  time_is = perf_counter_ns()
  kandinsky.get_pixel(10+i, 10)
  values.append((perf_counter_ns()-time_is)/1000)
print("get_pixel speed:", sum(values)/len(values), "µs")
for i in range(300):
  time_is = perf_counter_ns()
  kandinsky.color((cos(i)*1000, sin(i)*1000, log10(i+1)*1000))
  values.append((perf_counter_ns()-time_is)/1000)
print("color speed:", sum(values)/len(values), "µs")
input(">>> ")

exit()

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
