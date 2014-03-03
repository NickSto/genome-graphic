#!/usr/bin/env python
from __future__ import division
import os
import sys
import Image
import argparse
import fastareader

OPT_DEFAULTS = {'size':'512x512', 'verbose':True, 'background':'255,255,255',
  'A':'0,255,0', 'T':'255,0,0', 'G':'255,255,255', 'C':'0,0,255'}
USAGE = "%(prog)s [options] genome.fasta"
DESCRIPTION = """Convert DNA sequence into a PNG image by representing each base
  with one colored pixel."""
EPILOG = """"""

def main():

  parser = argparse.ArgumentParser(
    description=DESCRIPTION, usage=USAGE, epilog=EPILOG)
  parser.set_defaults(**OPT_DEFAULTS)

  parser.add_argument('fasta', metavar='genome.fasta',
    help="""Input sequence. Can be in FASTA format or a plain text file
      containing only the sequence. Any non-ATGC characters (case-insensitive)
      will be skipped.""")
  parser.add_argument('-s', '--size',
    help="""The output image size, in pixels, in the format "widthxheight", e.g.
      "640x480". If the sequence is larger than the number of pixels in the
      image, it will be cut off. Default size: %(default)s""")
  parser.add_argument('-o', '--outfile', metavar='image.png',
    help="""Output filename. Overrides the default, which is
      to use the input filename base plus .png.""")
  parser.add_argument('-d', '--display', action='store_true',
    help="""Display the image instead of saving it.""")
  parser.add_argument('-c', '--clobber', action='store_true',
    help="""If the output filename already exists, overwrite it instead of
      throwing an error (the default).""")
  parser.add_argument('-v', '--verbose', action='store_true',
    help="""Verbose mode. On by default.""")
  parser.add_argument('-q', '--quiet', action='store_false', dest='verbose',
    help="""Quiet mode.""")
  group = parser.add_argument_group('Color customization', """Use these options
    to use custom colors for the background and the bases. Specify with a
    comma-delimited RGB value like "100,150,10".""")
  group.add_argument('-b', '--background', metavar='R,G,B',
    help="""default: %(default)s""")
  group.add_argument('-A', metavar='R,G,B',
    help="""default: %(default)s""")
  group.add_argument('-T', metavar='R,G,B',
    help="""default: %(default)s""")
  group.add_argument('-G', metavar='R,G,B',
    help="""default: %(default)s""")
  group.add_argument('-C', metavar='R,G,B',
    help="""default: %(default)s""")

  args = parser.parse_args()

  try:
    size = parse_int_str(args.size, delim='x', num_ints=2)
  except ValueError:
    parser.print_help()
    fail('\nError: Invalid size string "%s".' % args.size)

  fasta = fastareader.FastaLineGenerator(args.fasta)
  bases = fasta.bases()

  if not args.display:
    outfile = args.outfile if args.outfile else outfile_name(args.fasta)
    if os.path.exists(outfile) and not args.clobber:
      fail('Error: Output filename already taken: "%s"' % outfile)

  background = parse_int_str(args.background)

  colors = {}
  colors['A'] = parse_int_str(args.A)
  colors['T'] = parse_int_str(args.T)
  colors['G'] = parse_int_str(args.G)
  colors['C'] = parse_int_str(args.C)

  image = Image.new('RGB', size, background)
  pixels = image.load()

  done = False
  for i in range(image.size[1]):
    for j in range(image.size[0]):
      try:
        base = next(bases).upper()
      except StopIteration:
        done = True
        break
      if base in colors:
        pixels[j,i] = colors[base]
    if done:
      break

  if args.display:
    image.show()
  else:
    image.save(outfile, 'PNG')


def parse_int_str(string, delim=',', num_ints=3):
  """Parse string of delimited ints, return them in a tuple.
  Checks that they are ints, they are delimited by "delim", and there are
  "num_ints" of them.
  If not valid, raises ValueError."""
  ints = map(int, string.split(delim))
  if len(ints) != num_ints:
    raise ValueError
  else:
    return tuple(ints)


def outfile_name(infilename):
  base = infilename.split('.')[0]
  if not base:
    base = infilename
  return base+'.png'


def fail(message):
  sys.stderr.write(message+"\n")
  sys.exit(1)

if __name__ == '__main__':
  main()
