#!/usr/bin/python

import Image, ImageDraw, sys, random

WIDTH = 512

def randcolor():
  """Return a random color tuple"""
  color = []
  for i in range(3):
    color.append(random.randrange(0,255))
  return tuple(color)

def drawblocks(draw,start,size):
  """Draw 8 color blocks inside a given rectangle.
  start = tuple of upper left corner coordinates
  size = tuple of (width,height) of block
  Returns True if it drew a new set of blocks, False if it did not because the
  block width or height would have been smaller than 1 pixel."""
  (x,y) = start
  (width,height) = size
  if width/height == 2:
    xblock = width/4
    yblock = height/2
  elif width/height == 1:
    xblock = width/2
    yblock = height/4
  else:
    sys.stderr.write("Error: asked to draw a block of unexpected aspect ratio: "
      +"width/height = "+str(width/height)+"\n")
    return
  if xblock < 1 or yblock < 1:
    return False
  for i in range(0,height,yblock):
    for j in range(0,width,xblock):
      draw.rectangle([(x,y),(x+xblock-1,y+yblock-1)], fill=randcolor())
      x += xblock
    x = 0
    y += yblock
  return True

def drawrecursive(draw, start, size):
  """Draw the full stack of blocks via recursive calls.
  Looks like I really should refactor this into drawblocks()."""
  (xstart,ystart) = start
  (width,height) = size
  drawblocks(draw, start, size)
  # shrink width/height for next blocks
  if width/height == 2:
    new_width = width/4
    new_height = height/2
  elif width/height == 1:
    new_width = width/2
    new_height = height/4
  else:
    sys.stderr.write("Error: asked to draw a block of unexpected aspect ratio: "
      +"width/height = "+str(width/height)+"\n")
    return
  
  # recursive call
  if new_width < 32 or new_height < 16:
    return False
  else:
    (x,y) = (xstart,ystart)
    drawrecursive(draw, (x,y), (new_width,new_height))
    drawrecursive(draw, (x+new_width,y), (new_width,new_height))
    drawrecursive(draw, (x,y+new_height), (new_width,new_height))
    drawrecursive(draw, (x+new_width,y+new_height), (new_width,new_height))
    if width/height == 2:
      drawrecursive(draw, (x+(2*new_width),y), (new_width,new_height))
      drawrecursive(draw, (x+(3*new_width),y), (new_width,new_height))
      drawrecursive(draw, (x+(2*new_width),y+new_height), (new_width,new_height))
      drawrecursive(draw, (x+(3*new_width),y+new_height), (new_width,new_height))
    elif width/height == 1:
      drawrecursive(draw, (x,y+(2*new_height)), (new_width,new_height))
      drawrecursive(draw, (x+new_width,y+(2*new_height)), (new_width,new_height))
      drawrecursive(draw, (x,y+(3*new_height)), (new_width,new_height))
      drawrecursive(draw, (x+new_width,y+(3*new_height)), (new_width,new_height))

    
    #while y < height:
    #while x < width:
    #  drawrecursive(draw, (x,y), (new_width,new_height))
    #  print "calling drawrecursive(draw, ("+str(x)+","+str(y)+"), " \
    #    +str(new_width)+","+str(new_height)+"))"
    #  x += new_width
    #  x = xstart
    #  y += new_height
    
    #  for j in range(0, width, new_width):
    #    #draw.rectangle([(x,y),(x+xblock-1,y+yblock-1)], fill=randcolor())
    #    drawrecursive(draw, (x,y), (new_width,new_height))
    #    x += new_width
    #  x = xstart
    #  y += new_height
    print "Stopping."

im = Image.new('RGB', (512,512), (0,0,0))
draw = ImageDraw.Draw(im)

drawrecursive(draw,(0,0),(512,512))

del draw

im.show()
