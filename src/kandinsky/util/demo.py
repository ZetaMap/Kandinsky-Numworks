"""This is a demo code
Source: https://my.numworks.com/python/zetamap/snake_lite
"""
print("""This is a demo code
Source: https://my.numworks.com/python/zetamap/snake_lite""")
__all__ = []

#############################################################

from random import randint as ri
from kandinsky import fill_rect as fr,draw_string as ds
from ion import keydown as kd
from time import monotonic as mt,sleep as sl

DEC=lambda v:((v&0xfff000)>>12,v&0xfff)
ENC=lambda x,y:x<<12|y
BOOL=lambda t:(t.lower()if type(t)==str else t) in("yes","on","enabled","activated","true","1",1)
def wk(*b):
 while 1:
  for i in b:
   if kd(i):
    while kd(i):pass
    return i
mjust=lambda l,r,s,f=' ': l+f*((s-len(l))//len(f))+r
class Snake:
 c=["0.95","0.2","#00ff00","green","red","blue","#ffb531","1.0"]
 try:
  import os
  u=os.getlogin()or "You"
  try:
   from kandinsky import get_palette as gp
   c[6]=gp()["Toolbar"]
   c[7]=gp()["HomeBackground"]
  except:c[6]="#c53431"
 except:u="You"
 def __init__(s,leader_board=[],speed=10,power=2,size=10,score=1,inf_snake=False,gost=False,darkmode=True,rainbow=False,walls=True):
  if BOOL(inf_snake):power=float("inf")
  if BOOL(darkmode):s.c[0],s.c[1]=s.c[1],s.c[0]
  s.lb,s.s,s.p,s.m,s.t,s.g,s.go,s.r,s.w=leader_board,1/speed,power,score,size,(320//size,220//size),BOOL(gost),BOOL(rainbow),BOOL(walls)
 def nc(s):
  s.h=[ri(s.w,s.g[i]-s.w-1)for i in(0,1)]
  while ENC(s.h[0],s.h[1])in s.b:s.h=[ri(s.w,s.g[i]-s.w-1)for i in(0,1)]
  fr(s.h[0]*s.t,2+s.h[1]*s.t,s.t,s.t,s.c[4])
 def dl(s):
  fr(0,2,320,220,"0.0")
  fr(0,2,s.g[0]*s.t,s.g[1]*s.t,s.c[5*s.w])
  if s.w:fr(s.t//2,2+s.t//2,(s.g[0]-1)*s.t,(s.g[1]-1)*s.t,s.c[0])
 def dt(s,t,x,y):
  for i,l in enumerate(t.replace('\t',"    ")):
   ds(l,x+10*i,y,s.c[1],s.c[0])
   if l!=' ':sl(0.02)
 def ub(s,l1,l2):
  fr(20,82,280,50,s.c[4])
  fr(25,87,270,40,s.c[0])
  s.dt(l1,25,87)
  s.dt(l2,25,107)
  sl(0.2)
  while 1:
   sl(0.01)
   if kd(4):return 1
   elif kd(17):return 0
 def wu(s):
  s.mt=mt()
  s.ta,s.e=(s.b[-1],DEC(s.b[-1])),DEC(s.b[0])
  if kd(0)and s.d[0]!=1:s.d=[-1,0]
  elif kd(1)and s.d[1]!=1:s.d=[0,-1]
  elif kd(2)and s.d[1]!=-1:s.d=[0,1]
  elif kd(3)and s.d[0]!=-1:s.d=[1,0]
  fr(s.e[0]*s.t,2+s.e[1]*s.t,s.t,s.t,s.r and[ri(0,255) for _ in(0,1,2)]or s.c[3])
  for x in range(len(s.b)-1,0,-1):s.b[x]=s.b[x-1]
  s.b[0]=ENC((s.e[0]+s.d[0])%s.g[0],(s.e[1]+s.d[1])%s.g[1])
  if s.a>0:
   s.b.append(s.ta[0])
   s.a-=1
  elif s.ta[0]not in s.b:fr(s.ta[1][0]*s.t,2+s.ta[1][1]*s.t,s.t,s.t,s.c[0])
  if s.b[0]==ENC(s.h[0],s.h[1]):
   s.a,s.sc=s.a+s.p,s.sc+s.m
   s.nc()
  s.e=DEC(s.b[0])
  fr(s.e[0]*s.t,2+s.e[1]*s.t,s.t,s.t,s.c[2])
  ds(str(s.sc),7,7,s.c[1],s.c[0])
  if not s.go:
   if s.w and(s.e[0]==s.g[0]-1 or s.e[1]==s.g[1]-1 or s.e[0]==0 or s.e[1]==0):return 0
   for x in range(1,len(s.b)):
    if s.b[x]==s.b[0]:return 0
  return 1
 def start(s):
  fr(0,0,320,2,s.c[6])
  try:
   while 1:
    s.b,s.a,s.d,s.sc=[ENC(s.g[0]//2,s.g[1]//2)],4,(1,0),0
    s.dl()
    s.nc()
    while s.wu():
     if kd(17):
      s.ub("\t\tGame Paused!","  (OK, DELETE = Continue)")
      sl(0.2)
      s.dl()
      fr(s.h[0]*s.t,2+s.h[1]*s.t,s.t,s.t,s.c[4])
      for i in s.b:
       s.e=DEC(i)
       fr(s.e[0]*s.t,2+s.e[1]*s.t,s.t,s.t,s.r and[ri(0,255) for _ in(0,1,2)]or s.c[3])
     while mt()-s.mt<s.s:sl(0.01)
    if not s.ub(' '*(3-len(str(s.sc))//2)+"You lose!\tScore: %d"%s.sc,"(OK = Retry, DELETE = Quit)"):break
   e,p,s.lb,x,t=0,0,sorted(s.lb+((s.u,s.sc),),key=lambda v:v[1],reverse=1),"Your score:","Leader board:"
   print(x,s.sc,"\n",t+" (default settings)")
   for i,sc in enumerate(s.lb):
    if len(sc[0])>e:e=len(sc[0])+len(str(sc[1]))
    if sc[0]==s.u:p=i
    print(' %d-'%(i+1),sc[0]+':',sc[1])
   fr(0,2,320,220,s.c[0])
   s.dt(x+" %d"%s.sc,5,7)
   s.dt(t,5,32)
   for i,sc in enumerate(s.lb):
    s.lb[i]=mjust(sc[0]+':',str(sc[1]),e+3)
    s.dt(s.lb[i],60,52+20*i)
   while not kd(4)and not kd(17):
    for i in range(4):
     if kd(4)or kd(17):break
     ds('>'*i+' '*(4-i),20,52,s.c[6],s.c[0])
     ds(' '*(4-i)+'<'*i,20+(e+1)*16,52,s.c[6],s.c[0])
     ds(s.lb[p],60,52+20*p,s.c[bool(i%3)*5+1],s.c[0])
     sl(0.2)
  except KeyboardInterrupt:pass
class Menu:
 colors=[Snake.c[0],Snake.c[1],"0.38",Snake.c[6],"#2a78e0"]
 r,u=colors,1
 options=lambda s:[s.p[i][s.c[i]]for i in range(s.s)]
 def __init__(s,title,action,*options):
  s.t,s.a,s.p=title[0:25],action[0:28],options
  s.s=len(s.p)
  s.c,s.b=[],len(s.a)
  for i in s.p :
   assert len(i)>2,"need [label,default,values...]"
   s.c.append(int(i[1])+2)
 def mo(s,i,o,u):
  t,l=str(s.p[i][s.c[i]])[0:15],i%6
  ds('<'*u+' '*(17-2*u)+'>'*u,140,65+l*25,s.r[2],s.r[1])
  ds(t,150+(150-10*len(t))//2,65+l*25,o,s.r[1])
 def do(s):
  u=s.u-1*(s.u>0)
  u=(u-(u and u==u//6*6))//6*6
  for i in range(6):
   if u+i<s.s:
    t=str(s.p[u+i][0])[0:12]
    ds(t+' '*(12-len(t)),10,65+i*25,s.r[0],s.r[1])
    s.mo(u+i,s.r[2],0)
   else:fr(10,65+i*25,300,18,s.r[1])
  if s.s>6:s.sb(u)
 def sb(s,u):
  fr(314,65,3,140,s.r[2])
  o=140//((s.s+5)//6)
  p=o*(u//6)
  fr(314,65+p,3,o+(u==s.s//6*6)*(140-o-p),s.r[3])
 def da(s,i):
  c=s.r[3*(i==0)]
  ds("<",10,8,c,s.r[1])
  fr(13,16,13,1,c)
  fr(26,10,1,6,c)
  ds(s.a,160-5*s.b,36,s.r[3*(i==1)],s.r[1])
 def ds(s):
  fr(0,0,320,222,s.r[1])
  ds(s.t,160-5*len(s.t),8,s.r[4],s.r[1])
  s.da(s.u)
  s.do()
 def close(s,b=0):
  fr(0,0,320,222,s.r[1])
  if b:s.u=1
  return[]if b else s.options()
 def open(s):
  s.ds()
  r=-1
  while 1:
   if r in(5,17):return s.close(1)
   elif r in(4,52):
    if s.u<2:return s.close(s.u==0)
    r=-2
   elif r in(-1,1,2):
    if s.u<2:s.da(s.u+1)
    s.u=(s.u-1*(r==1)+1*(r==2))%(s.s+2)
    s.do()
    if s.u>1:s.mo(s.u-2,s.r[3],1)
    else:s.da(s.u)
   if r in(-2,0,3)and s.u>1:
    v=s.u-2
    s.c[v],l=s.c[v]+1*(r==3)-1*(r==0)if r>=0 else s.p[v][1]+2,s.c[v]
    o=s.c[v]
    if o==1:s.c[v]=len(s.p[v])-1
    if o==len(s.p[v]):s.c[v]=2
    if l!=o and s.p[v][0].lower()=="darkmode":#special
     s.r[0],s.r[1]=s.r[1],s.r[0]
     s.ds()
    s.mo(v,s.r[3],1)
   r=wk(0,1,2,3,4,5,17,52)
def intro(d):
 def pl(letter,x,y,size,color):
  for i,l in enumerate(letter):
   if l=='1':fr(x+size*(i%3),y+size*(i//3),size,size,color)
 a,x,ax,r,c,b,o,e='1'*9+"44334411",0,-110,0,Snake.c[6],Menu.r[1],["Play","Options","Quit"],0
 y=ay=120
 fr(0,0,320,222,b)
 for i,l in enumerate((31597,31725,23469,31207)):
  pl(bin(l)[2:],110+40*i,80,10,"0.0")
  sl(0.008)
 for i in range(len(a)):
  f=int(a[i])
  x+=((f==1)-(f==3))*10
  y+=((f==2)-(f==4))*10
  if ax<0:ax+=10
  else:
   i=int(a[i-11])
   ax+=((i==1)-(i==3))*10
   ay+=((i==2)-(i==4))*10
   fr(ax,ay,10,10,b)
  fr(x,y,10,10,"#00cc00")
  sl(0.05)
 pl("001001000001001",x,y,2,"0.0")
 pl("000001110001",x+10,y,2,"red")
 while 1:
  for i,l in enumerate(o):
   f=e==i
   fr(100,140+i*25,140,18,b)
   ds("> "*f+l+f*" <",110+(110-10*(len(l)+4*f))//2,140+i*25,c if f else Menu.r[0],b)
  r=wk(1,2,4,17,52)
  e=(e-1*(r==1)+1*(r==2))%3
  if r==17:return 1
  if r in(4,52):return[]if e==1 else 1 if e==2 else d
def game(*lb):
 o=[]
 while not o:
  o=intro(menu.options())or menu.open()
  if o==1:return
 Snake(lb,*o).start()

menu = Menu("Game Settings","Start Game",
 ["Speed",9]+list(range(1,26)),
 ["Power",1]+list(range(1,21)),
 ["Snake Size",9]+list(range(1,51)),
 ["Added Score",0]+list(range(1,21)),
 ["Expert Mode",1,"Yes","No"],
 ["Babu Mode",1,"Yes","No"],
 ["Darkmode",0,"Enabled","Disabled"],
 ["Rainbow",1,"On","Off"],
 ["Walls",0,"Yes","No"]
)

game(# Leader board: ("name",score),
  ("Alteur",38),
  ("Lidl Man",37),
  ("ZetaMap",31),
  ("Nios",23),
  ("Alpha6Frost",17),

)