"""
A Start of an 3D engine for Numworks.

Source: https://my.numworks.com/python/antarctus/cube_move
"""

import os
os.environ["KANDINSKY_OS_MODE"]='0'
os.environ['KANDINSKY_ZOOM_RATIO'] = '2'
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

try:
  line=draw_line
except:
  pass


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
      draw_string(f"{px},{py}",px,py, "white", "black",True)

    if FILL_MODEL: fill_polygon(polygon,COLORS[i%6])
    else: line(*polygon[0],*polygon[1],COLORS[i//2%6])

# ???
def xturn(y,z,cosx,sinx):
  return y*cosx-z*sinx,y*sinx+z*cosx

def yturn(x,z,cosy,siny):
  return z*siny+x*cosy,z*cosy-x*siny

def zturn(x,y,cosz,sinz):
  return x*cosz-y*sinz,x*sinz+y*cosz

cube3d(-100,-100,-100,100,100,100)

xrot=0
yrot=0
zrot=0

fill_rect(0,0,320,222,(0,)*3)
draw_string("OK: fill on/off\t\t\t\tArrows: move",5,207,"white","black",True)
while True:
  xrot+=pi/90*(keydown(KEY_UP)-keydown(KEY_DOWN))
  yrot+=pi/90*(keydown(KEY_LEFT)-keydown(KEY_RIGHT))

  if keydown(KEY_OK):
    FILL_MODEL = not FILL_MODEL
    MODEL.clear()
    cube3d(-100,-100,-100,100,100,100)
    sleep(0.2)

  render(cos(xrot),sin(xrot),cos(yrot),sin(yrot),cos(zrot),sin(zrot))
  sleep(0.01)
