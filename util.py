import math, environment

def distance(x1,x2,y1,y2):
	"""Euclidean Distance on a Torus."""
	e = environment.Environment()
	xdiff = abs(x1 - x2)
	ydiff = abs(y1 - y2)
	return math.sqrt(min(xdiff, e.width  - xdiff)**2 + \
					 min(ydiff, e.height - ydiff)**2)				 
	#return vector.Vector(x1,y1).distance_to(vector.Vector(x2,y2))
