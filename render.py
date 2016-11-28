#!/usr/bin/python

import sys, struct, numpy
from PIL import Image

GAIN = 2.0
#GAIN *= 4.0
#GAIN *= 2.0
#OUTPUT_SIZE = 2466, 3366

# First get the image size.
width, height = struct.unpack("<II", sys.stdin.read(8))
print "Image size: %sx%s" % (width, height)

OUTPUT_SIZE = width, height

# Read in the actual image data.
print "Reading."
image_data = sys.stdin.read(4 * width * height)
print "Fromstringing."
array = numpy.fromstring(image_data, dtype=numpy.float32)
print "Resizing."
array.resize((height, width))
print "Transposing."
numpy.transpose(array)

print "Building."
# Normalize the array.
array *= (1.0 / array.max())

#red = array.copy()
red = 1 - numpy.exp(-40.0 * array)
#red **= 0.8
#red *= 255 * 30.0
red *= 255
red.clip(0, 255, red)
#red = 0

#excess = array.copy()
#excess **= 8.0

#cut_down = (1.0 + 4e-3 - 1.0 * array).copy()
#cut_down.clip(0, 1, cut_down)

#green = array.copy()
green = (1 - numpy.exp(-400.0 * array)) #* cut_down ** 1000.0
#green **= 0.6
#green *= 255 * 5.0
#green -= 255 * excess * 50.0
green *= 255
green.clip(0, 255, green)
#green = 0

#excess2 = array.copy()
#excess2 **= 4.0

#blue = array.copy()
blue = (1 - numpy.exp(-1000.0 * array)) #* cut_down ** 100.0 #(1 - numpy.exp(-2.0 * (1 - array)))
#blue **= 0.4
#blue *= 255 * 2.0
#blue -= 255 * excess2 * 10.0
blue *= 255
blue.clip(0, 255, blue)
#blue = 0
#blue = 0

print "Joining."
target_array = numpy.zeros(OUTPUT_SIZE[::-1] + (3,), "uint8")
target_array[..., 0] = red
target_array[..., 1] = green
target_array[..., 2] = blue

# Show the image.
print "From arraying."
#image = Image.fromarray(array.astype(numpy.int8), "L")
image = Image.fromarray(target_array)
#print "Resizing."
#image = image.resize(OUTPUT_SIZE, Image.ANTIALIAS)
print "Saving."
image.save(sys.argv[1])
print "Done."
#image.show()

