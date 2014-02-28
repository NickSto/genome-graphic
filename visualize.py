#!/usr/bin/python
# archive note: this was after I'd figured out how to (recursively) do every layer correctly
# and just after I figured out transparency. It's the last point before I re-wrote it to be
# iterative instead of recursive.

import Image, ImageDraw, sys, random

def main():

  image = Image.new("RGB", (512,512), (0,0,0))

  drawblocks(image, 1, (0,0), (512,512))

  image.show()

def randcolor():
  """Return a tuple of random color values"""
  color = []
  for i in range(3):
    color.append(random.randrange(0,255))
  return tuple(color)

def drawblocks(image, level, start, size):
  """Draw 8 color blocks inside a given rectangle.
  start = tuple of upper left corner coordinates
  size = tuple of (width,height) of block
  Returns True if it drew a new set of blocks, False if it did not because the
  block width or height would have been smaller than 1 pixel."""
  if start == (0,0):
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
  if start == (0,0):
    print "divided size into "+str((sub_width,sub_height))
  if sub_width < 4 or sub_height < 4:
    return False

  (x,y) = (xstart,ystart)
  while y < ystart+height:
    while x < xstart+width:
      if start == (0,0):
        print "drawing rectangle pos:"+str((x,y))+"\tsize: " \
          +str((x+sub_width-1, y+sub_height-1))
      #if start == (0,0):
      overlay = Image.new("RGB", image.size, color=(0,0,0))
      mask = Image.new("L", image.size, color=0)
      overdraw = ImageDraw.Draw(overlay)
      maskdraw = ImageDraw.Draw(mask)
      overdraw.rectangle([(x,y), (x+sub_width-1, y+sub_height-1)],
        fill=randcolor())
      maskdraw.rectangle([(x,y), (x+sub_width-1, y+sub_height-1)],
        fill=(256/level)-1)
      image.paste(overlay, (0,0), mask)
      drawblocks(image, level*2, (x,y), (sub_width,sub_height))
      x += sub_width
    y += sub_height
    x = xstart
  return True

if __name__ == "__main__":
  main()