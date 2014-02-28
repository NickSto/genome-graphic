#!/usr/bin/python
# archive note: this was when I was figuring out a problem with the tiling,
# and had lots of debug statements

import Image, ImageDraw, sys, random

def main():

  counts = {256:0, 64:0, 32:0, 8:0}

  im = Image.new('RGB', (512,512), (0,0,0))
  draw = ImageDraw.Draw(im)

  drawblocks(draw, (0,0), (512,512), counts)

  print "256x128: "+str(counts[256])
  print "64x64: "+str(counts[64])
  print "32x16: "+str(counts[32])
  print "8x8: "+str(counts[8])


  del draw

  im.show()

def randcolor():
  """Return a random color tuple"""
  color = []
  for i in range(3):
    color.append(random.randrange(0,255))
  return tuple(color)

def drawblocks(draw, start, size, counts):
  """Draw 8 color blocks inside a given rectangle.
  start = tuple of upper left corner coordinates
  size = tuple of (width,height) of block
  Returns True if it drew a new set of blocks, False if it did not because the
  block width or height would have been smaller than 1 pixel."""
  if start == (256,0):
    print "inside drawblocks(draw, "+str(start)+", "+str(size)+")"
  (xstart,ystart) = start
  (width,height) = size
  if width/height == 2:
    sub_width = width/4
    sub_height = height/2
  elif width/height == 1:
    sub_width = width/2
    sub_height = height/4
  else:
    sys.stderr.write("Error: asked to draw a block of unexpected aspect ratio: "
      +"width/height = "+str(width/height)+"\n")
    return
  if start == (256,0):
    print "divided size into "+str((sub_width,sub_height))
  if sub_width < 8 or sub_height < 8:
    return False
  if start == (256,0):
    print "we're not too small"

  (x,y) = (xstart,ystart)
  while y < ystart+height:
    while x < xstart+width:
      if start == (256,0):
        print "drawing rectangle "+str((x,y))
      draw.rectangle([(x,y), (x+sub_width-1, y+sub_height-1)], fill=randcolor())
      if sub_width == 256 and sub_height == 128:
        counts[256]+=1
      elif sub_width == 64 and sub_height == 64:
        counts[64]+=1
      elif sub_width == 32 and sub_height == 16:
        counts[32]+=1
      elif sub_width == 8 and sub_height == 8:
        counts[8]+=1
      else:
        sys.stderr.write("Error: unexpected block size: "+str(sub_width)+"x"
          +str(sub_height))
      drawblocks(draw, (x,y), (sub_width,sub_height), counts)
      if x == 256 and y == 0:
        print "called drawblocks(draw, ("+str(x)+", "+str(y)+"), (" \
          +str(sub_width)+", "+str(sub_height)+")"
      x += sub_width
      # print "x is now "+str(x)
    y += sub_height
    x = xstart
    # x = 0
  return True

if __name__ == "__main__":
  main()