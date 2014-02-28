#!/usr/bin/python

import Image, ImageDraw, sys, random

WIDTH = 512
BLOCK = 16

def randcolor():
  """Return a random color tuple"""
  color = []
  for i in range(3):
    color.append(random.randrange(0,255))
  return tuple(color)

im = Image.new('RGB', (512,512), (0,0,0))
draw = ImageDraw.Draw(im)
x = y = 0
for i in range(0,WIDTH,BLOCK):
  for j in range(0,WIDTH,BLOCK):
    draw.rectangle([(x,y),(x+BLOCK,y+BLOCK)], fill=randcolor())
    x += BLOCK
  x = 0
  y += BLOCK
del draw 

# write to stdout
#im.save(sys.stdout, "PNG")
im.show()

