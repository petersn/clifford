#!/usr/bin/python

import sys, struct, numpy
from PIL import Image

GAIN = 40.0

# First get the image size.
width, height = struct.unpack("<II", sys.stdin.read(8))
#print "Image size: %sx%s" % (width, height)

# Read in the actual image data.
image_data = sys.stdin.read(4 * width * height)
array = numpy.fromstring(image_data, dtype=numpy.float32)
array.resize((width, height))

# Normalize the array.
array *= (255.0 / array.max()) * GAIN
#array *= 700.0
array.clip(0, 255, array)

# Show the image.
image = Image.fromarray(array.astype(numpy.int8), "L")
image = image.resize((1600, 1600), Image.ANTIALIAS)
image.save(sys.argv[1])
#image.show()

