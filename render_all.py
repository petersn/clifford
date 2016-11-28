#!/usr/bin/python

import os
from multiprocessing import Pool

images = os.listdir("images")

def f(img):
	if not img.endswith(".bz2"):
		return
	img = os.path.join("images", img)
	target = img.replace(".bz2", ".png")
	if os.path.exists(target):
		print "SKIPPING", target
		return
	command = "bzcat %s | python render.py %s" % (img, target)
	print command
	os.system(command)

p = Pool(1)
p.map(f, images)

