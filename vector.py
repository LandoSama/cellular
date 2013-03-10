from math import sqrt
import environment

class Vector(object):
	__slots__ = ('x', 'y')
	"""Vector in toroidal space defined by the dimensions of Environment()."""
	def __init__(self, x, y):
		self.x = x
		self.y = y
	def __add__(self, other):
		"""Sum and mod vectors."""
		e = environment.Environment()
		xdiff = (self.x + other.x) % e.width
		ydiff = (self.y + other.y) % e.width
		return Vector(xdiff, ydiff)
	def __sub__(self, other):
		"""Return shortest difference vector pointing from other to self."""
		e = environment.Environment()
		halfwidth = e.width/2
		halfheight = e.width/2
		xdiff = ((self.x - other.x + halfwidth) % e.width) - halfwidth
		ydiff = ((self.y - other.y + halfheight) % e.width) - halfheight
		return Vector(xdiff, ydiff)
	def __neg__(self):
		return Vector(-self.x, -self.y)
	def __abs__(self):
		"""Magnitude of the vector."""
		return (self.x**2 + self.y**2)**0.5
	def __repr__(self):
		return '(' + str(self.x) + ',' + str(self.y) + ')'
	def distance_to(self, other):
		e = environment.Environment()
		xdiff = abs(self.x - other.x)
		ydiff = abs(self.y - other.y)
		return sqrt(min(xdiff, e.width  - xdiff)**2 + \
					min(ydiff, e.height - ydiff)**2)
		#return abs(self - other)


class VectorAroundZero(object):
	"""Vector in toroidal space (x,y) with -0.5 <= x,y <= 0.5"""
	"""I think this is cleaner. Might be an argument for having a [-0.5, 0.5] coordinate system."""
	"""Adapting the program to use this would be some work though."""
	__slots__ = ('_x', '_y')
	def __init__(self, x, y): self.x = x; self.y = y
	def __repr__(self): return '(' + str(self._x) + ',' + str(self._y) + ')'
	def __add__(self, other): return VectorAroundZero(self._x + other._x, self._y + other._y)
	def __sub__(self, other): return self + -other
	def __neg__(self): return VectorAroundZero(-self._x, -self._y)
	def __abs__(self): return (self._x**2 + self._y**2)**0.5
	def distance_to(self, other): return abs(self - other)
	@property
	def x(self   ): return self._x
	@x.setter
	def x(self, x): self._x = ((x + 0.5) % 1) - 0.5
	@property
	def y(self   ): return self._y
	@y.setter
	def y(self, y): self._y = ((y + 0.5) % 1) - 0.5
