"""
A start of a 3D engine. Use``OK`` to display the faces or edges of cube and ``←↑→↓+-`` to move it.

**NOTE**: This script only work on Upsilon because ``fill_polygon()`` function doesn't exist in others OS.
Source: https://my.numworks.com/python/antarctus/cube_move
"""

import os
if hasattr(os, "environ"):
  os.environ["KANDINSKY_OS_MODE"]= '0'
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

def render(cosx,sinx,cosy,siny,cosz,sinz):
  fill_rect(0,0,320,180,(0,0,0))

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
      draw_string("%d,%d"%(px,py), px, py, "white", "black", 1)
    draw_string("%f,%f,%f"%(cosx,cosy,cosz), 5, 0, "white", "black", 1)
    draw_string("%f,%f,%f"%(sinx,siny,sinz), 5, 12, "white", "black", 1)
      
    ""
    if FILL_MODEL: fill_polygon(polygon,COLORS[i%6])
    else:
      x1,y1=polygon[0]
      x2,y2=polygon[1]
      draw_line(x1,y1,x2,y2,COLORS[i//2%6])

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
draw_string("OK: fill on/off"+(' '*13)+"Arrows/+/-: move",5,207,"white","black",True)
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