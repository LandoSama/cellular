import math, unittest
import random

def distance(x1,x2,y1,y2):
	"""Standard Distance Formula."""
	return	math.sqrt((x2-x1)**2 + (y2-y1)**2)

class Cell:
	def __init__(self,x,y):
		"""Cells begin with a specified position, without velocity, task or destination."""
		self.max_acceleration = 0.02
		self.max_speed = 0.1
		self.x = float(x)
		self.y = float(y)
		self.xvel = 0.0
		self.yvel = 0.0
		self.task = None
		#lets say that a destination is a tuple of the form (x,y) where x and y are real numbers
		self.destination = None
		self.radius = 1
		self.energy = 0
		
	def try_consume_food(self, food):
		x_diff = food.x - self.x
		y_diff = food.y - self.y
		if math.sqrt(x_diff*x_diff + y_diff*y_diff) < self.radius:
			#print "Food coord: (", food.x, ",", food.y, ")"
			#print "Cell coord: (", self.x, ",", self.y, ")"
			#print "Distance:", math.sqrt(x_diff*x_diff + y_diff*y_diff)
			self.energy += food.energy
			return True
		return False

	def get_pos(self):
		"""Returns the position of the cell in tuple form."""
		return (self.x, self.y)

	def get_vel(self):
		"""Returns the velocity of the cell in tuple form."""
		return (self.xvel, self.yvel)

	def get_task(self):
		"""Returns the task of the cell."""
		return self.task

	def get_destination(self):
		"""Returns the destination of the cell."""
		return self.destination

	def get_speed(self):
		"""Returns the speed of the cell."""
		return math.sqrt(abs(self.xvel) + abs(self.yvel))

	def update_coords(self):
		"""Changes the cell's position based on its velocity, a.k.a. movement."""
		self.x += self.xvel
		self.y += self.yvel

	def go_to(self,destination):
		"""Tells the cell to move to the destination specified.
		Destinations need to be in tuple form."""
		self.destination = destination
		self.task = 'move'

	def set_task(self,new_task):
		"""Sets the task of the cell."""
		self.task = new_task

	def random_walk(self):
		"""The cell begins to move towards a random destination."""
		self.destination = random.random(),random.random()
		self.set_task('move')

	def accel_towards_destination(self):
		"""Accelerates the cell towards its destination."""
		# get total distance to dest
		total_distance = distance(self.x,self.destination[0],self.y,self.destination[1])
		# get x distance to dest
		xdist = abs(self.x - self.destination[0])
		# get y distance to dest
		ydist = abs(self.y - self.destination[1])

		if self.x > self.destination[0]:
			self.xvel -= self.max_acceleration*xdist/total_distance
			if abs(self.xvel) >= self.max_speed:
				self.xvel = self.max_speed * (-1)
		else:
			self.xvel += self.max_acceleration*xdist/total_distance
			if abs(self.xvel) >= self.max_speed:
				self.xvel = self.max_speed
			
		if self.y > self.destination[1]:
			self.y -= self.max_acceleration*ydist/total_distance
			if abs(self.yvel) >= self.max_speed:
				self.yvel = self.max_speed * (-1)
		else:
			self.yvel += self.max_acceleration*ydist/total_distance
			if abs(self.yvel) >= self.max_speed:
				self.yvel = self.max_speed
		
		self.update_coords()
			
	def slow_towards_destination(self):
		"""Slows a cell at the maximum rate until it reaches its destination."""
		# get total distance to dest
		total_distance = distance(self.x,self.destination[0],self.y,self.destination[1])
		xdist = abs(self.x - self.destination[0])
		ydist = abs(self.y - self.destination[1])
		# once the calculated number of ticks is 0, the cell ought to be at its destination
		ticks = int(self.get_speed()/self.max_acceleration)
		if ticks <= 0:
			self.xvel = 0.0
			self.yvel = 0.0
	
		if self.x > self.destination[0]:
			self.xvel += self.max_acceleration*xdist/total_distance
			if abs(self.xvel) > self.max_speed:
				self.xvel = self.max_speed * (-1)
		else:
			self.xvel -= self.max_acceleration*xdist/total_distance
			if abs(self.xvel) > self.max_speed:
				self.xvel = self.max_speed

		if self.y > self.destination[1]:
			self.yvel += self.max_acceleration*ydist/total_distance
			if abs(self.yvel) > max_speed:
				self.yvel = self.max_speed * (-1)

		else:
			self.yvel -= self.max_acceleration*ydist/total_distance
			if abs(self.yvel) > self.max_speed:
				self.yvel = self.max_speed

		self.update_coords()
		
	def distance_to_start_slowing_down(self):
		"""Calculates the distance from the destination that, once past,
		the cell ought to begin slowing down to reach its destination."""
		ticks = int(self.get_speed()/self.max_acceleration)
		dist = self.get_speed()
		temp_speed = self.get_speed()
		for i in xrange(ticks):
			temp_speed -= self.max_acceleration
			dist += temp_speed
		return dist

	def one_tick(self):
		"""What a cell does every arbitrary unit of time."""
		if self.task == None:
			# If the cell is doing nothing, reset to the default: Random Walk
			self.random_walk()
		elif self.task == 'move':
			if self.destination == None:
				# If the cell wants to move but has no destination, it's not allowed to move. Sorry, cell.
				self.task = None
			else:
				distance_to_destination = distance(self.x,self.destination[0],self.y,self.destination[1])			
				if distance_to_destination > self.distance_to_start_slowing_down():
					# Keep accelerating until told to do otherwise.
					self.accel_towards_destination()
				else:
					# The cell is to begin to slow down once it has passed its "Hey cell, slow down!" distance.
					self.task = 'stop'

		elif self.task == 'stop':
			if self.get_speed() == 0:
				# If the cell has stopped moving, it's done its job.
				self.task = None
				self.destination = None
			else:
				# If the cell wants to stop but hasn't yet, deaccelerate.
				self.slow_towards_destination()

class TestFunctions(unittest.TestCase):
	"""Fingers Crossed."""
	
	def test_tick(self):
		"""Tests various applications of the one_tick() func."""
		# When a cell is spawned, it should have no task.
		c = Cell(0,0)
		self.assertEquals(c.task,None)
		# Having no task, one_tick should give the cell a random walk.
		c.one_tick()
		self.assertEquals(c.task,'move')
		# The cell should not yet have gained speed. Testing task 'stop':
		c.task = 'stop'
		c.one_tick()
		self.assertEquals(c.task,None)
		self.assertEquals(c.destination,None)
		# Now testing the cell moving from 0,0 to 3,4:
		c.task = 'move'
		c.destination = (3,4)
		c.one_tick()
		self.assertAlmostEquals(c.xvel,0.012,5)
		self.assertAlmostEquals(c.yvel,0.016,5)
		self.assertAlmostEquals(c.x,0.012,5)
		self.assertAlmostEquals(c.y,0.016,5)
		c.one_tick()
		self.assertAlmostEquals(c.xvel,0.024,5)
		self.assertAlmostEquals(c.yvel,0.032,5)
		self.assertAlmostEquals(c.x,0.036,5)
		self.assertAlmostEquals(c.y,0.048,5)
		c.one_tick()
		self.assertAlmostEquals(c.xvel,0.036,5)
		self.assertAlmostEquals(c.yvel,0.048,5)
		self.assertAlmostEquals(c.x,0.072,5)
		self.assertAlmostEquals(c.y,0.096,5)
		c.one_tick()
		self.assertAlmostEquals(c.xvel,0.048,5)
		self.assertAlmostEquals(c.yvel,0.064,5)
		self.assertAlmostEquals(c.x,0.12,5)
		self.assertAlmostEquals(c.y,0.16,5)
		c.one_tick()
		self.assertAlmostEquals(c.xvel,0.06,5)
		self.assertAlmostEquals(c.yvel,0.08,5)
		self.assertAlmostEquals(c.x,0.18,5)
		self.assertAlmostEquals(c.y,0.24,5)
		c.one_tick()
		self.assertAlmostEquals(c.xvel,0.072,5)
		self.assertAlmostEquals(c.yvel,0.096,5)
		self.assertAlmostEquals(c.x,0.252,5)
		self.assertAlmostEquals(c.y,0.336,5)
		# As you can see, this gets ugly/boring fast.		

	def test_slow(self):
		"""Tests to see if the cell can identify that it needs to begin
		slowing down, and successfully slows down."""
		c = Cell(0,0)
		c.task = 'stop'
		c.destination = (0.2,0.2)
		c.xvel = 0.1
		c.yvel = 0.1
		c.one_tick()
		# Distance to start slowing down = .4472135
		# Distance = .2828427
		self.assertAlmostEquals(c.xvel,0.0858578643762681,5)
		self.assertAlmostEquals(c.yvel,0.0858578643762681,5)
		self.assertAlmostEquals(c.x,0.0858578643762681,5)
		self.assertAlmostEquals(c.y,0.0858578643762681,5)
		

	def test_position(self):
		"""Gives the cell a random position, and tests if the cell is
		at that position."""
		rand_pos = random.random(), random.random()
		c = Cell(rand_pos[0], rand_pos[1])
		self.assertEquals(c.x,rand_pos[0])
		self.assertEquals(c.y,rand_pos[1])

	def test_distance_func(self):
		self.assertEquals(5.0,distance(0,3,0,4))
		self.assertEquals(5.0,distance(3,0,4,0))
		self.assertEquals(5.0,distance(6,9,8,4))
		self.assertEquals(5.0,distance(-3,-6,-4,-8))

if __name__ == "__main__":
	unittest.main()
