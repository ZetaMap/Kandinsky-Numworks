"""
A start of a 3D engine. Use``OK`` to display the faces or edges of cube and ``←↑→↓+-`` to move it.

**NOTE**: This script work better on Upsilon because ``fill_polygon()`` function doesn't exist in others OS. So we need to re-implement this and is consuming a lot of resources.
Source: https://my.numworks.com/python/antarctus/cube_move
"""
try:
  import os
  if hasattr(os, "environ"):
    os.environ["KANDINSKY_OS_MODE"]= '0'
    os.environ['KANDINSKY_ZOOM_RATIO'] = '2'
except: pass
from math import cos,sin,pi
from kandinsky import *
from time import sleep
from ion import *


MODEL=[]
COLORS=[(255,0,0),(255,255,0),(0,255,0),(0,255,255),(0,0,255),(255,0,255)]
FILL_MODEL=False

def cube3d(x1,y1,z1,x2,y2,z2):
  if FILL_MODEL:
    points3d([[x1,y1,z1],[x1,y2,z1],[x2,y2,z1],[x2,y1,z1]])
    points3d([[x1,y2,z1],[x1,y2,z2],[x2,y2,z2],[x2,y2,z1]])
    points3d([[x1,y1,z2],[x1,y2,z2],[x2,y2,z2],[x2,y1,z2]])
    points3d([[x1,y1,z2],[x1,y2,z2],[x1,y2,z1],[x1,y1,z1]])
    points3d([[x2,y1,z2],[x2,y1,z1],[x2,y2,z1],[x2,y2,z2]])
    points3d([[x2,y1,z2],[x2,y1,z1],[x1,y1,z1],[x1,y1,z2]])

  else:
    points3d([[x1,y1,z1],[x1,y2,z1]])
    points3d([[x1,y1,z1],[x2,y1,z1]])
    points3d([[x2,y1,z1],[x2,y2,z1]])
    points3d([[x1,y2,z1],[x2,y2,z1]])
    points3d([[x1,y1,z2],[x1,y2,z2]])
    points3d([[x1,y1,z2],[x2,y1,z2]])
    points3d([[x2,y1,z2],[x2,y2,z2]])
    points3d([[x1,y2,z2],[x2,y2,z2]])
    points3d([[x1,y1,z1],[x1,y1,z2]])
    points3d([[x2,y1,z1],[x2,y1,z2]])
    points3d([[x1,y2,z1],[x1,y2,z2]])
    points3d([[x2,y2,z1],[x2,y2,z2]])

def points3d(XYZpoints):
  MODEL.append(XYZpoints)

# Compatibility
def line(x1,y1,x2,y2,c):
  w=x2-x1
  h=y2-y1
  if abs(w)>=abs(h):
    d=h/w
    for i in range(0,w,(w>0)*2-1):
      set_pixel(x1+i,y1+int(d*i+0.5),c)
  else:
    d=w/h
    for i in range(0,h,(h>0)*2-1):
      set_pixel(x1+int(d*i+0.5),y1+i,c)

def polygone(p,c):
    p = list(p)
    p_len = len(p)

    for y in range(min([[0,222]]+p, key=lambda v: v[1])[1], max([[0,0]]+p, key=lambda v: v[1])[1]):
      switches = []
      last_point = p_len-1

      for i in range(p_len):
        point_y, last_point_y = p[i][1], p[last_point][1]
        if ((point_y < y and last_point_y >= y) or (last_point_y < y and point_y >= y)) and point_y != last_point_y:
          switches.append(round(p[i][0]+1*(y-point_y)/(last_point_y-point_y)*(p[last_point][0]-p[i][0])))
        last_point = i

      switches.sort()
      for x in range(0, len(switches), 2):
        if switches[x] >= 320*2: break
        if switches[x+1] > 0: fill_rect(switches[x], y, switches[x+1]-switches[x], 1, c)

try:
  line=draw_line
  string=draw_string
except: string=lambda t,x,y,c,bg,f: draw_string(t,x,y,c,bg)
try: polygone=fill_polygon
except: pass

# 3d to 2d render
def render(cosx,sinx,cosy,siny,cosz,sinz):
  fill_rect(0,0,320,200,(0,0,0))

  for i in range(len(MODEL)):
    polygon = []
    
    for p in MODEL[i]:
      #Rotations
      x,y,z=p
      y, z = xturn(y,z,cosx,sinx)
      x, z = yturn(x,z,cosy,siny)
      x, y = zturn(x,y,cosz,sinz)
      
      #Projections
      px,py=int(x*100/(z+300))+160, int(y*100/(z+300))+100
      polygon.append([px,py])

      #debug
      string("%d,%d"%(px,py), px, py, "white", "black", 1)
    string("%f,%f,%f"%(cosx,cosy,cosz), 5, 0, "white", "black", 1)
    string("%f,%f,%f"%(sinx,siny,sinz), 5, 12, "white", "black", 1)
      
    if FILL_MODEL: 
      if True:
        polygone(polygon,COLORS[i%6])
    else:
      x1,y1=polygon[0]
      x2,y2=polygon[1]
      line(x1,y1,x2,y2,COLORS[i//2%6])

# ???
def xturn(y,z,cosx,sinx):
  return y*cosx-z*sinx,y*sinx+z*cosx

def yturn(x,z,cosy,siny):
  return z*siny+x*cosy,z*cosy-x*siny

def zturn(x,y,cosz,sinz):
  return x*cosz-y*sinz,x*sinz+y*cosz

cube3d(-100,-100,-100,100,100,100)

xrot=yrot=zrot=xoffset=yoffset=0

fill_rect(0,0,320,222,(0,)*3)
string("OK: fill on/off"+(' '*13)+"Arrows/+/-: move",5,207,"white","black",True)
while True:
  xrot+=pi/90*(keydown(KEY_UP)-keydown(KEY_DOWN))
  yrot+=pi/90*(keydown(KEY_LEFT)-keydown(KEY_RIGHT))
  zrot+=pi/90*(keydown(KEY_MINUS)-keydown(KEY_PLUS))

  if keydown(KEY_OK):
    FILL_MODEL = not FILL_MODEL
    MODEL.clear()
    cube3d(-100,-100,-100,100,100,100)
    sleep(0.2)

  render(cos(xrot),sin(xrot),cos(yrot),sin(yrot),cos(zrot),sin(zrot))
#  sleep(0.01)