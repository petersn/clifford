#!/usr/bin/python

import os, multiprocessing

#sx = [-1.0,  1.0]
#sy = [-1.0, -0.5]
#a  = [-1.7, -1.7]
#b  = [ 1.9,  1.9]
#c  = [ 0.8,  0.8]
#d  = [ 1.2,  1.2]

#a  = [-1.7, +1.0]
#b  = [ 1.9, -0.6]
#c  = [ 0.8,  1.1]
#d  = [ 1.2,  0.55]
first =  [-1.4, 1.6, 1.0, 0.7]
second = [1.7, 1.7, 0.6, 1.2]
third =  [1.5, -1.8, 1.6, 0.9]
fourth = [-1.8, -2.0, -0.5, -0.9]

#all_sets = [first, second, third, fourth]
#all_sets = [first, third]

FRAMES = 100

def execute_on(global_i):
	set_index = global_i / FRAMES
	i = global_i % FRAMES
	target_path = "images/frame%04i.png" % (global_i + 1)
	set1, set2 = all_sets[set_index], all_sets[set_index+1]
	const = i/(FRAMES-1.0)
	lerp = lambda (a, b): (1.0 - const) * a + const * b
	params = tuple(map(lerp, zip(set1, set2))) + (target_path,)
	command = "./clifford 10 -1 -1 1 0.5 %f %f %f %f | python render.py %s" % params
	if os.path.exists(target_path):
		print "Skipping %i" % (global_i+1)
		return
	os.system(command)
	print "Frame %i/%i" % (global_i+1, FRAMES * (len(all_sets)-1))

p = multiprocessing.Pool(5)
p.map(execute_on, range(FRAMES * (len(all_sets)-1)))

