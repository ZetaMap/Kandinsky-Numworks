"""This is a demo code
Source: https://my.numworks.com/python/golem64/snake
"""
print("""This is a demo code
Source: https://my.numworks.com/python/golem64/snake""")
__all__ = []

#############################################################

#Version 1.7 STABLE
#Tip: You should try to press
#some keys in the menu...
from random import *
from kandinsky import *
from ion import *
from time import *
#from pomme import * 
def oscolor():
  try:
    get_keys()
  except:
    return 'orange'
  else:
    return 'red'
def lastPos(i,x,y):
  if i[-1]==3:
    pos=[x-10,y]
  elif i[-1]==2:
    pos=[x,y-10]
  elif i[-1]==0:
    pos=[x+10,y]
  elif i[-1]==1:
    pos=[x,y+10]
  pos[0],pos[1]=checkTeleport(pos[0],pos[1])
  return pos
def newApple(appleC,bgC):
  applex=randint(0,31)*10+4
  appley=randint(0,21)*10+5
  while get_pixel(applex,appley)!=bgC:
    applex=randint(0,31)*10+4
    appley=randint(0,21)*10+5
  fill_rect(applex-4,appley-4,10,10,appleC)
  return applex,appley
def checkTeleport(x,y):
  if x<4:
    x=314
  if x>314:
    x=4
  if y<5:
    y=215
  if y>215:
    y=5
  return x,y
def getMove(u):
  for k in range(4):
    if keydown(k)==True and u+k!=3: return k
  return u
def clearDraw(): fill_rect(0,0,320,222,(255,255,255))
def clearHome(): print('\n'*13)
def redraw():
  draw_string("(DELETE to exit)",0,0)
  printLetter([1,1,1,1,0,0,1,1,1,0,0,1,1,1,1],70,80,10,(0,204,0))
  fill_rect(95,80,2,4,(0,0,0))
  fill_rect(95,86,2,4,(0,0,0))
  fill_rect(100,84,4,2,(255,0,0))
  fill_rect(104,82,2,2,(255,0,0))
  fill_rect(104,86,2,2,(255,0,0))
  printLetter([1,1,1,1,0,1,1,0,1,1,0,1,1,0,1],110,80,10,(0,0,0))
  printLetter([1,1,1,1,0,1,1,1,1,1,0,1,1,0,1],150,80,10,(0,0,0))
  printLetter([1,0,1,1,0,1,1,1,0,1,0,1,1,0,1],190,80,10,(0,0,0))
  printLetter([1,1,1,1,0,0,1,1,1,1,0,0,1,1,1],230,80,10,(0,0,0))
def printLetter(letter,x,y,size,color):
  for yi in range(5):
    for xi in range(3):
      if letter[yi*3+xi]==1:
        fill_rect(x+(xi*size),y+(yi*size),size,size,color)
def menu():
  clearDraw()
  printLetter([1,1,1,1,0,1,1,0,1,1,0,1,1,0,1],110,80,10,(0,0,0))
  printLetter([1,1,1,1,0,1,1,1,1,1,0,1,1,0,1],150,80,10,(0,0,0))
  printLetter([1,0,1,1,0,1,1,1,0,1,0,1,1,0,1],190,80,10,(0,0,0))
  printLetter([1,1,1,1,0,0,1,1,1,1,0,0,1,1,1],230,80,10,(0,0,0))
  anim=[1,1,1,1,1,1,1,1,1,4,4,3,3,4,4,1,1]
  ax=0
  ay=120
  aendx=-110
  aendy=120
  u=1
  aback=0
  for i in range(len(anim)):
    ax=ax+((anim[i]==1)-(anim[i]==3))*10
    ay=ay+((anim[i]==2)-(anim[i]==4))*10
    if aendx<0:
      aendx=aendx+10
    else:
      aendx=aendx+((anim[i-11]==1)-(anim[i-11]==3))*10
      aendy=aendy+((anim[i-11]==2)-(anim[i-11]==4))*10
      fill_rect(aendx,aendy,10,10,(255,255,255))
    fill_rect(ax,ay,10,10,(0,204,0))
#    aback=lastPos(anim,ax,ay)
#    if u==26 or u==24:
#      fill_rect(ax-1,ay-1,3,1,(0,0,0))
#      fill_rect(ax-1,ay+1,3,1,(0,0,0))
#      fill_rect(aback[0],aback[1],10,10,(0,204,0))
#    elif u==34 or u==25:
#      fill_rect(ax-1,ay-1,1,3,(0,0,0))
#      fill_rect(ax+1,ay-1,1,3,(0,0,0))
#      fill_rect(aback[0]-2,aback[1]-2,5,5,(0,204,0))
    sleep(0.05)
  fill_rect(ax+5,ay,2,4,(0,0,0))
  fill_rect(ax+5,ay+6,2,4,(0,0,0))
  fill_rect(ax+10,ay+4,4,2,(255,0,0))
  fill_rect(ax+14,ay+2,2,2,(255,0,0))
  fill_rect(ax+14,ay+6,2,2,(255,0,0))
  draw_string("(DELETE to exit)",0,0)
  draw_string("> Play <",125,140,oscolor())
  draw_string("  Options  ",110,165)
  darkMode=0
  Speed=0.05
  power=5
  score=1
  exit=0
  sel=1
  while keydown(KEY_OK)!=True and exit==0:
    if keydown(KEY_DOWN) and sel==1:
      draw_string("  Play  ",125,140)
      draw_string("> Options <",110,165,oscolor())
      sel=2
    elif keydown(KEY_UP) and sel==2:
      draw_string("> Play <",125,140,oscolor())
      draw_string("  Options  ",110,165)
      sel=1
    if keydown(KEY_LEFTPARENTHESIS) and keydown(KEY_RIGHTPARENTHESIS):
      draw_string("Dark mode enabled !",80,195)
      darkMode=1
    if keydown(KEY_BACKSPACE):
      exit=1  
    sleep(0.1)
  if sel==2 and exit!=1:
    fill_rect(0,130,300,60,(255,255,255))
    Speed=0.05
    power=5
    score=1
    draw_string("Speed:"+str(Speed),50,140,oscolor(),'white')
    draw_string("Power:+"+str(power),200,140)
    draw_string("Score:+"+str(score),50,170)
    draw_string("Play",220,170)
    sel=1
    sleep(0.2)
    while keydown(KEY_OK)!=True or sel!=4:
      if keydown(KEY_RIGHT):
        sel=sel+1
      elif keydown(KEY_DOWN):
        sel=sel+2
      elif keydown(KEY_LEFT):
        sel=sel-1
      elif keydown(KEY_UP):
        sel=sel-2
      if sel<0:
        sel=0
      if sel>4:
        sel=4
      if sel==1:
        draw_string("Speed:"+str(Speed),50,140,oscolor(),'white')
        draw_string("Power:+"+str(power),200,140)
        draw_string("Score:+"+str(score),50,170)
        draw_string("Play",220,170)
        if keydown(KEY_OK):
          clearHome()
          Speed=input("Speed:")
          redraw()
      elif sel==2:
        draw_string("Speed:"+str(Speed),50,140)
        draw_string("Power:+"+str(power),200,140,oscolor(),'white')
        draw_string("Score:+"+str(score),50,170)
        draw_string("Play",220,170)
        if keydown(KEY_OK):
          clearHome()
          power=int(input("Power:+"))
          redraw()
      elif sel==3:
        draw_string("Speed:"+str(Speed),50,140)
        draw_string("Power:+"+str(power),200,140)
        draw_string("Score:+"+str(score),50,170,oscolor(),'white')
        draw_string("Play",220,170)
        if keydown(KEY_OK):
          clearHome()
          score=int(input("Score:"))
          redraw()
      elif sel==4:
        draw_string("Speed:"+str(Speed),50,140)
        draw_string("Power:+"+str(power),200,140)
        draw_string("Score:+"+str(score),50,170)
        draw_string("Play",220,170,oscolor(),'white')
      if (keydown(KEY_LEFTPARENTHESIS) and keydown(KEY_RIGHTPARENTHESIS)) or darkMode==1:
        draw_string("Dark mode enabled !",80,195)
        darkMode=1
      if keydown(KEY_BACKSPACE):
        exit=1
        break
      sleep(0.1)
  if exit!=1:
    if darkMode==1:
      launch(1,Speed,power,score)
    elif darkMode==0:
      launch(0,Speed,power,score)
  elif exit==1:
    clearDraw()
    return
def launch(darkmode=0,speed=0.05,applePower=5,appleScore=1):
  bgC=(248,252,248)
  borderC=(0,0,0)
  snakeC=(0,204,0)
  appleC=(248,0,0)
  if darkmode==1:
    bgC=(0,0,0)
    borderC=(0,0,204)
  fill_rect(0,0,320,222,bgC)
#  fill_rect(315,0,5,222,borderC)
#  fill_rect(0,0,5,222,borderC)
#  fill_rect(0,0,320,1,(197,52,49))
  fill_rect(0,221,320,1,(0,0,0))
  try:
    get_keys()
  except:
    fill_rect(0,0,320,1,(255,181,49))
  else:
    fill_rect(0,0,320,1,(197,52,49))
  snake=[3,3,3,3,3]
  x=154
  y=115
  endx=104
  endy=115
  u,v=3,3
  length=5
  applex,appley=newApple(appleC,bgC)
  score,touched=0,0
  while touched!=borderC and touched!=snakeC:
    if keydown(0) or keydown(1) or keydown(2) or keydown(3):
      u=getMove(u)
    if keydown(KEY_BACKSPACE):
      while keydown(KEY_BACKSPACE):
        sleep(0.1)
      while keydown(KEY_BACKSPACE)!=True:
        sleep(0.1)
      while keydown(KEY_BACKSPACE):
        sleep(0.1)
    snake.append(u)
    if x==applex and y==appley:
      length=length+float(applePower)
      applex,appley=newApple(appleC,bgC)
      score=score+int(appleScore)
    x=x+((u==3)-(u==0))*10
    y=y+((u==2)-(u==1))*10
    x,y=checkTeleport(x,y)
    if length:
      length=length-1
    else:
      snake.remove(snake[0])
      endx=endx+((v==3)-(v==0))*10
      endy=endy+((v==2)-(v==1))*10
      endx,endy=checkTeleport(endx,endy)
      v=snake[0]
      fill_rect(endx-4,endy-4,10,10,bgC)
    touched=get_pixel(x,y)
    if x<0 or x>320 or y<0 or y>220:
      touched=borderC
    if touched!=appleC and touched!=bgC:
      touched=borderC
    fill_rect(x-4,y-4,10,10,snakeC)
    back=lastPos(snake,x,y)
    if u==3 or u==0:
      fill_rect(x,y-4,2,4,(0,0,0))
      fill_rect(x,y+2,2,4,(0,0,0))
      fill_rect(back[0]-4,back[1]-4,10,10,snakeC)
    elif u==2 or u==1:
      fill_rect(x-4,y,4,2,(0,0,0))
      fill_rect(x+2,y,4,2,(0,0,0))
      fill_rect(back[0]-4,back[1]-4,10,10,snakeC)
    sleep(float(speed))
# EPILEPSY WARNING !!!
#    snakeC=(randint(0,255),randint(0,255),randint(0,255))
    while snakeC==appleC or snakeC==bgC:
       snakeC=(randint(0,255),randint(0,255),randint(0,255))
  #  beau()
    if len(snake)==640:
      if darkmode==1:
        draw_string("You win !",120,100,'white','black')
        draw_string("(You reached the max length)",20,120,'white','black')
      else:
        draw_string("You win !",120,100)
        draw_string("(You reached the max length)",20,120) 
      touched=borderC
  if darkmode==1:
    draw_string("Score:"+str(score),10,10,'white','black')
    draw_string("(OK=play again, DELETE=Menu)",10,30,'white','black')
  else:
    draw_string("Score:"+str(score),10,10)
    draw_string("(OK=play again, DELETE=Menu)",10,30)
  choice=0
  while choice==0:
    if keydown(KEY_OK):
      choice=1
      launch(darkmode,speed,applePower,appleScore)
    elif keydown(KEY_BACKSPACE):
      choice=2
      menu()
  print("Score:",score)
menu()