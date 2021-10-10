"""This is a demo code
Source: https://my.numworks.com/python/andreanx/chromac
"""

from kandinsky import color, set_pixel, display
from cmath import pi, phase, sqrt

def hsv2color(h, s=1, v=1):
  h, c = (h/pi)%2, v*s
  x, m, k = c*(1-abs((h%(2/3))*3-1)), v-c, int(h*3)

  return color(
    round(255*(m+x*(k%3==1)+c*(k%5==0))), 
    round(255*(m+c*(k==1 or k==2)+x*(k%3==0))), 
    round(255*(m+x*(k%3==2)+c*(k==3 or k==4))))

def modsv(p,m): return not(m) or (p*m)%1

def chromac(xc=160, yc=110, rmax=110, ds=0, dv=0, tred=0, rev=False):
  xc, yc = round(xc), round(yc)

  for y in range(-rmax,rmax+1):
    xmin = round(sqrt(rmax**2-y**2).real)
    
    for x in range(-xmin,xmin+1):
      z = complex(x,y)
      r = abs(z)
      if r <= rmax: set_pixel(
        xc+x , yc+y,
        hsv2color((phase(z)-tred)*(1-2*rev), 
        modsv(r/rmax,ds),modsv(r/rmax,dv)))

sw, sh, r = 320,220, 45
lx3, ly2 = [r,(sw-1)/2,sw-1-r], [r,sh-1-r]
lx2=[(lx3[0]+lx3[1])/2,(lx3[1]+lx3[2])/2]

for x in range(2): chromac(lx2[x], sh/2, r, -1, not(x)*-1, x*pi/4, x%2)
for y in range(2):
  for x in range(3): chromac(lx3[x], ly2[y], r, not(y), x-1, (2+3*y+x)*pi/4, (x+y)%2)

display()