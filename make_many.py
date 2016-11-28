#!/usr/bin/python

import os
from multiprocessing import Pool

def f(x):
	command = "./make_background.py %s" % x
	print "RUNNING:", command
	os.system(command)

p = Pool(4)
p.map(f, [0.8]*12)

