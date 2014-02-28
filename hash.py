#!/usr/bin/python

import sys, hashlib

hash = hashlib.sha256()
filename = ''
if len(sys.argv) > 1:
  filename = sys.argv[1]
else:
  sys.stderr.write("Error: no filename given\n")
  sys.exit(1)

with open(filename, 'rb') as file:
  for chunk in iter(lambda: file.read(65536), b''):
  	hash.update(chunk)

print hash.hexdigest()