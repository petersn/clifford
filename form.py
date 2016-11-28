#!/usr/bin/python

from matplotlib import pyplot as plt

r = lambda x: x**0.8 * 30.0
g = lambda x: x**0.6 * 5.0 #- x**8.0 * 50.0
b = lambda x: x**0.4 * 2.0 #- x**4.0 * 10.0

plt.hold(True)
for f, color in [(r, "r"), (g, "g"), (b, "b")]:
	xs = [i * 1e-3 for i in xrange(1001)]
	plt.plot(xs, [max(0.0, min(1.0, f(x**10.0))) for x in xs], color)
plt.savefig("foo.png")

