import math
import environment

def distance(x1,x2,y1,y2):
	"""Euclidean Distance on a Torus."""
	e = environment.Environment()
	return	math.sqrt(min(|x1 - x2|, e.width - |x1 - x2|)^2 + min(|y1 - y2|, e.height - |y1-y2|)^2)
