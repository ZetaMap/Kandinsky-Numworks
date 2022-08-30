"""This is a demo code
Source: https://my.numworks.com/python/zetamap/snake_lite
"""
print("""This is a demo code
Source: https://my.numworks.com/python/zetamap/snake_lite""")
__all__ = []

#############################################################

from random import randint as ri
from kandinsky import fill_rect as fr, draw_string as ds
from ion import *
from time import *
HEX=lambda v,l=4: '0'*(l-len(hex(v)[2:]))+hex(v)[2:]
INT=lambda v: int("0x"+v,16)
COMPRESS=lambda f,l=2,i=2: INT(''.join([HEX(f(ii),l) for ii in range(i)]))
def UNCOMPRESS(v,l=2,i=2):
  v=HEX(v,l*i)
  return [INT(v[l*ii:l*(ii+1)]) for ii in range(i)]
class Snake:
  c=[(50,50,50),(240,240,240),(0,255,0),"green","red","blue","red"]
  def __init__(s,leader_board=(),speed=10,power=2,size=10,score=1,inf_snake=False,gost=False,darkmode=True,rainbow=False,walls=True):
    if inf_snake: power=float("inf")
    if not darkmode: s.c[0],s.c[1]=s.c[1],s.c[0]
    try: get_keys()
    except NameError: s.c[6]="orange"
    s.lb,s.s,s.p,s.m,s.ti,s.g,s.go,s.r,s.w,s.bo=leader_board,1/speed,power,score,size,(320//size-1,220//size-1),gost,rainbow,walls,1 if walls else 0
  def nc(s):
    s.ch=[ri(s.bo,s.g[i]-s.bo) for i in range(2)]
    while COMPRESS(lambda i: s.ch[i]) in s.b: s.c=[ri(s.bo,s.g[i]-s.bo) for i in range(2)]
    fr(s.ch[0]*s.ti,2+s.ch[1]*s.ti,s.ti,s.ti,s.c[4])
  def dl(s):
    fr(0,2,320,220,"black")
    fr(0,2,(s.g[0]+1)*s.ti,(s.g[1]+1)*s.ti,s.c[5 if s.w else 0])
    if s.w: fr(s.ti//2,2+s.ti//2,s.g[0]*s.ti,s.g[1]*s.ti,s.c[0])
  def dt(s,text,x,y):
    for i,l in enumerate(text.replace('\t', "    ")):
      ds(l,x+10*i,y,s.c[1],s.c[0])
      if l!=' ': sleep(0.02)
  def ub(s,line1,line2):
    fr(20,82,280,50,s.c[4])
    fr(25,87,270,40,s.c[0])
    s.dt(line1,25,87)
    s.dt(line2,25,107)
    sleep(0.2)
    while True:
      if keydown(KEY_OK): return True
      elif keydown(KEY_BACKSPACE): return False
  def wake_up(s):
    s.t=monotonic()
    s.ta,s.te=(s.b[-1], UNCOMPRESS(s.b[-1])),UNCOMPRESS(s.b[0])
    if keydown(KEY_UP) and s.d[1]!=1: s.d=[0,-1]
    elif keydown(KEY_LEFT) and s.d[0]!=1: s.d=[-1,0]
    elif keydown(KEY_DOWN) and s.d[1]!=-1: s.d=[0,1]
    elif keydown(KEY_RIGHT) and s.d[0]!=-1: s.d=[1,0]
    fr(s.te[0]*s.ti,2+s.te[1]*s.ti,s.ti,s.ti,[ri(0,255) for i in range(3)] if s.r else s.c[3])
    for x in range(len(s.b)-1,0,-1): s.b[x]=s.b[x-1]
    s.b[0]=COMPRESS(lambda i: (s.te[i]+s.d[i])%s.g[i])
    if s.a>0:
      s.b.append(s.ta[0])
      s.a-=1
    elif s.ta[0] not in s.b: fr(s.ta[1][0]*s.ti,2+s.ta[1][1]*s.ti,s.ti,s.ti,s.c[0])
    if s.b[0]==COMPRESS(lambda i: s.ch[i]):
      s.a,s.sc=s.a+s.p,s.sc+s.m
      s.nc()
    s.te=UNCOMPRESS(s.b[0])
    if not s.go:
      if s.w and (s.te[0]==0 or s.te[1]==0 or s.te[0]==s.g[0] or s.te[1]==s.g[1]): return False
      for x in range(1,len(s.b)):
        if s.b[x]==s.b[0]: return False
    fr(s.te[0]*s.ti,2+s.te[1]*s.ti,s.ti,s.ti,s.c[2])
    ds(str(s.sc),7,7,s.c[1],s.c[0])
    return True
  def start(s):
    fr(0,0,320,2,s.c[6])
    try:
      while True:
        s.b,s.a,s.d,s.sc=[COMPRESS(lambda i: s.g[i]//2)],4,(1,0),0
        s.dl()
        s.nc()
        while s.wake_up():
          if keydown(KEY_BACKSPACE):
            s.ub("\t\tGame Paused!","  (OK, DELETE = Continue)")
            sleep(0.2)
            s.dl()
            fr(s.ch[0]*s.ti,2+s.ch[1]*s.ti,s.ti,s.ti,s.c[4])
            for i in s.b: 
              s.te=UNCOMPRESS(i)
              fr(s.te[0]*s.ti,2+s.te[1]*s.ti,s.ti,s.ti,[ri(0,255) for i in range(3)] if s.r else s.c[3])
          while monotonic()-s.t<s.s: sleep(0.0001)
        if not s.ub(' '*(3-len(str(s.sc))//2)+"You lose!\tScore: "+str(s.sc),"(OK = Retry, DELETE = Quit)"): break
      s.te=0
      print("Your score:",s.sc,"\nLeader board: (default settings)")
      for i,sc in enumerate(s.lb):
        if len(sc[0])>s.te: s.te=len(sc[0])
        print(' '+str(i+1)+'-',sc[0]+':',sc[1])
      fr(0,2,320,220,s.c[0])
      s.dt("Your score: "+str(s.sc),5,7)
      s.dt("Leader board:",5,32)
      for i,sc in enumerate(s.lb): s.dt(sc[0]+':'+' '*(s.te-len(sc[0])+2)+str(sc[1]),60,52+20*i)
      l=['>'*i+' '*(4-i)+s.lb[0][0]+':'+' '*(s.te-len(s.lb[0][0])+2)+str(s.lb[0][1])+' '*(4-i)+'<'*i for i in range(4)]
      while not keydown(KEY_OK) and not keydown(KEY_BACKSPACE):
        for i in l:
          sleep(0.2)
          if keydown(KEY_OK) or keydown(KEY_BACKSPACE): break
          ds(i,20,52,s.c[6],s.c[0])
    except KeyboardInterrupt: input(">>> ")
    
Snake(( # Leader board: ("name", score),
  ("Alteur", 38),
  ("ZetaMap", 30),

), # Game settings: power, speed, size, score, inf_snake, darkmode, rainbow, gost, walls
#  walls=False,
#  size=5, # 1 -> 80
#  darkmode=False
).start()
