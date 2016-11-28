#!/usr/bin/python

import subprocess, random, os, struct, sys

if len(sys.argv) != 2:
	print "Usage: python make_background.py fill_fraction"
	exit()

fill_fraction = float(sys.argv[1])

variation = 5e-3
trajectories = 100000
#trajectories = 1000

# Get good parameters.
data = subprocess.check_output(["./finder", str(fill_fraction)])
params = map(float, data.split("\n")[:4])
print "Params:", params

score_line = data.strip().rsplit("\n", 1)[1]
print score_line

# Render the parameters, and slight variations.
def render(params):
	assert len(params) == 4
	param_string = struct.pack("<ffff", *params).encode("hex")
	dest = "images/output_%.2f_%s.bz2" % (fill_fraction, param_string)
	os.system("./clifford %i %f %f %f %f | bzip2 > %s" % ((trajectories,) + tuple(params) + (dest,)))
	return dest

err = lambda x: x + random.normalvariate(0, variation)

p1 = render(params)
#render(map(err, params), "output_e1.png")
#render(map(err, params), "output_e2.png")
#os.system("convert output.png output_e1.png output_e2.png -combine final_output.png")

