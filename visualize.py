#!/usr/bin/python
import sys
import random
import hashlib
import Image
import ImageDraw

def main():

  if len(sys.argv) == 1:
    print """USAGE:
  $ ./visualize.py genome.fa outfile.png pxsize
The last two arguments are optional, but must be in those positions.
If no outfile name is given, it will attempt to display the image directly.
If no pxsize is given, the default is 512. A power of 2 is highly
recommended as the resulting image will be much better laid out."""
    sys.exit(0)

  DEFAULT_SIZE = (512,512)
  size = DEFAULT_SIZE
  if len(sys.argv) > 3:
    user_size = int(sys.argv[3])
    size = (user_size,user_size)

  # can skip hashing and specify the seed as an option (for testing)
  if len(sys.argv) > 4:
    seed = sys.argv[4]
  else:
    seed = get_hash(sys.argv[1])
  print "seed: "+seed
  random.seed(seed)
  level = 1
  layers = []
  image = draw_layer(size, level)
  while 1:
    level+=1
    layers.append(draw_layer(size, level))
    if layers[-1] == False:
      break
    # opacity = 256/2**level                        # opacity #1
    # opacity = 256/2**(level-1)                    # opacity #2
    # opacity = 256*(level/2)/2**(level-1)          # opacity #3
    opacity = 256*(level/float(2**level))         # opacity #4
    print "opacity: "+str(int(opacity/2.56))+"%"
    mask = Image.new("L", size, color=opacity)
    image.paste(layers[-1], (0,0), mask)

  if len(sys.argv) > 2:
    image.save(sys.argv[2])
  else:
    image.show()

def draw_layer(image_size, level):
  """Draw every block for a particular layer
  (blocks of a particular pixel size).
  Returns an image of the finished layer."""
  (image_width,image_height) = image_size
  (width, height) = block_size(image_size, level)
  if width < 1 or height < 1:
    return False
  print "width, height: "+str(width)+", "+str(height)
  layer = Image.new("RGB", image_size, (0,0,0))
  draw = ImageDraw.Draw(layer)
  (x,y) = (0,0)
  while y < image_height:
    while x < image_width:
      draw.rectangle([(x,y), (x+width-1, y+height-1)], fill=randcolor())
      x += width
    y += height
    x = 0
  return layer

def get_hash(filepath):
  """Compute hash of the file"""
  hashed = hashlib.sha256()
  with open(filepath, 'rb') as filehandle:
    for chunk in iter(lambda: filehandle.read(65536), b''):
      hashed.update(chunk)
  return hashed.hexdigest()

def randcolor():
  """Return a tuple of random color values"""
  color = []
  for i in range(3):
    color.append(random.randrange(0,255))
  return tuple(color)

def block_size(image_size, level):
  """Compute the block width and height for this layer."""
  (width,height) = image_size
  while level > 0:
    width = width/2
    height = height/4
    level-=1
    if level < 1:
      break
    width = width/4
    height = height/2
    level-=1
  return (width,height)

def format_genome():
  """Eventually I'd like to attempt to process the genome file into a standard
  format, stripping out details of representation that can change the output,
  such as:
    - upper/lowercase
    - line endings
    - chromosome naming
    - chromosome order
    - noncanonical chromosomes"""

def check_genome():
  """Eventually I'd like this to check assumptions I might make about the
  genome file. A first check would be that it contains all the chromosomes, in
  the format ''>chr1' or ''>1'. If these assumptions (which format_genome()
  depends on) aren't met, and the format isn't recognized, then default to a
  straight digest of the unmodified file."""

if __name__ == "__main__":
  main()