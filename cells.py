import unittest, util, environment
import random, math
from vector import Vector

class Cell:
	def __init__(self,x,y):
		"""Cells begin with a specified position, without velocity, task or destination."""
		self.max_acceleration = 0.02
		self.max_speed = 0.1
		self.pos = Vector(float(x), float(y))
		self.vel = Vector(0.0, 0.0)
		self.task = None
		self.destination = None
		self.destination_type = None
		self.radius = 1
		self.energy = 0

		#closest piece of food
		self.closest_food = None
		self.distance_to_closest_food = None

	def get_task(self):
		"""Returns the task of the cell."""
		return self.task

	def get_destination(self):
		"""Returns the destination of the cell."""
		return self.destination

	def get_speed(self):
		"""Returns the speed of the cell."""
		return abs(self.vel)

	def update_coords(self):
		"""Changes the cell's position based on its velocity, a.k.a. movement."""
		self.pos = self.pos + self.vel

	def go_to(self,destination):
		"""Tells the cell to move to the destination specified.
		Destinations need to be in tuple form."""
		self.destination = destination
		self.task = 'move'

	def set_task(self,new_task):
		"""Sets the task of the cell."""
		self.task = new_task

	# sets a random destination and sets task to move
	def random_walk(self):
		"""The cell begins to move towards a random destination."""
		tempWorld = environment.Environment()
		self.destination = Vector(random.uniform(0,tempWorld.width),random.uniform(0,tempWorld.height))
		self.set_task('move')
		
	def set_food_as_destination(self):
		pass

	def accel_towards_destination(self):
		"""Accelerates the cell towards its destination."""
		# get total distance to dest
		total_distance = self.pos.distance_to(self.destination)
		# get x distance to dest
		xdist = abs(self.pos.x - self.destination.x)
		# get y distance to dest
		ydist = abs(self.pos.y - self.destination.y)

		if self.pos.x > self.destination.x:
			self.vel.x -= self.max_acceleration*xdist/total_distance
			if abs(self.vel.x) >= self.max_speed:
				self.vel.x = self.max_speed * (-1)
		else:
			self.vel.x += self.max_acceleration*xdist/total_distance
			if abs(self.vel.x) >= self.max_speed:
				self.vel.x = self.max_speed
			
		if self.pos.y > self.destination.x:
			self.pos.y -= self.max_acceleration*ydist/total_distance
			if abs(self.vel.y) >= self.max_speed:
				self.vel.y = self.max_speed * (-1)
		else:
			self.vel.y += self.max_acceleration*ydist/total_distance
			if abs(self.vel.y) >= self.max_speed:
				self.vel.y = self.max_speed
		
		self.update_coords()

	def slow_towards_destination(self):
		"""Slows a cell at the maximum rate until it reaches its destination."""
		# get total distance to dest
		total_distance = util.distance(self.pos.x,self.destination.x,self.pos.y,self.destination.y)
		xdist = abs(self.pos.x - self.destination.x)
		ydist = abs(self.pos.y - self.destination.x)
		# once the calculated number of ticks is 0, the cell ought to be at its destination
		ticks = int(self.get_speed()/self.max_acceleration)
		if ticks <= 0:
			self.vel.x = 0.0
			self.vel.y = 0.0
	
		if self.pos.x > self.destination.x:
			self.vel.x += self.max_acceleration*xdist/total_distance
			if abs(self.vel.x) > self.max_speed:
				self.vel.x = self.max_speed * (-1)
		else:
			self.vel.x -= self.max_acceleration*xdist/total_distance
			if abs(self.vel.x) > self.max_speed:
				self.vel.x = self.max_speed

		if self.pos.y > self.destination.y:
			self.vel.y += self.max_acceleration*ydist/total_distance
			if abs(self.vel.y) > self.max_speed:
				self.vel.y = self.max_speed * (-1)

		else:
			self.vel.y -= self.max_acceleration*ydist/total_distance
			if abs(self.vel.y) > self.max_speed:
				self.vel.y = self.max_speed

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

	def food_nearby_question_mark(self):
		pass
		
	def eat(self):
		e = environment.Environment()
		for f in e.food_at(self.pos, self.radius):
			self.energy += f.energy
			e.remove_food(f)

	def one_tick(self):
		"""What a cell does every arbitrary unit of time."""
		self.eat()
		
		if self.task == None:
			# food nearby? then go to it.
			if self.distance_to_closest_food < 20 and self.closest_food is not None:
				self.destination = self.closest_food.pos
				self.destination_type = 'food'
				self.task = 'move'
			# If the cell is doing nothing and there isn't any close food: Random Walk
			else:
				self.random_walk()
			
		elif self.task == 'move':
			if self.destination == None:
				# If the cell wants to move but has no destination, it's not allowed to move. Sorry, cell.
				self.task = None
			else:
				distance_to_destination = self.pos.distance_to(self.destination)
				if distance_to_destination > self.distance_to_start_slowing_down():
					# if cell.destination_type = food		
						# if food no longer exsits, self.task = stop
							# else accelerate towards desitnation

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

	def test_stop(self):
		"""Tests one_tick() removing the tasks and destinations of cells done stopping."""
		c = Cell(0,0)
		c.task = 'stop'
		c.one_tick()
		self.assertEquals(c.task,None)
		self.assertEquals(c.destination,None)

	def test_taskless(self):
		"""Tests one_tick() giving taskless cells a random walk."""
		c = Cell(0,0)
		# When a cell is spawned, it should have no task.
		self.assertEquals(c.task,None)
		c.one_tick()
		self.assertEquals(c.task,'move')
	
	def test_tick(self):
		"""Tests one_tick() accelerating cells who want to move."""
		c = Cell(0,0)
		c.task = 'move'
		c.destination = Vector(3,4)
		# Testing the cell moving from (0,0) to (3,4).
		c.one_tick()
		self.assertAlmostEquals(c.vel.x,0.012,5)
		self.assertAlmostEquals(c.vel.y,0.016,5)
		self.assertAlmostEquals(c.pos.x,0.012,5)
		self.assertAlmostEquals(c.pos.y,0.016,5)
		c.one_tick()
		self.assertAlmostEquals(c.vel.x,0.024,5)
		self.assertAlmostEquals(c.vel.y,0.032,5)
		self.assertAlmostEquals(c.pos.x,0.036,5)
		self.assertAlmostEquals(c.pos.y,0.048,5)
		c.one_tick()
		self.assertAlmostEquals(c.vel.x,0.036,5)
		self.assertAlmostEquals(c.vel.y,0.048,5)
		self.assertAlmostEquals(c.pos.x,0.072,5)
		self.assertAlmostEquals(c.pos.y,0.096,5)
		c.one_tick()
		self.assertAlmostEquals(c.vel.x,0.048,5)
		self.assertAlmostEquals(c.vel.y,0.064,5)
		self.assertAlmostEquals(c.pos.x,0.12,5)
		self.assertAlmostEquals(c.pos.y,0.16,5)
		c.one_tick()
		self.assertAlmostEquals(c.vel.x,0.06,5)
		self.assertAlmostEquals(c.vel.y,0.08,5)
		self.assertAlmostEquals(c.pos.x,0.18,5)
		self.assertAlmostEquals(c.pos.y,0.24,5)
		c.one_tick()
		self.assertAlmostEquals(c.vel.x,0.072,5)
		self.assertAlmostEquals(c.vel.y,0.096,5)
		self.assertAlmostEquals(c.pos.x,0.252,5)
		self.assertAlmostEquals(c.pos.y,0.336,5)
		# As you can see, this gets ugly/boring fast.

	def test_slow(self):
		"""Tests to see if the cell can identify that it needs to begin
		slowing down, and successfully slows down."""
		c = Cell(0,0)
		c.task = 'stop'
		c.destination = Vector(0.2,0.2)
		c.vel = Vector(0.1,0.1)
		c.one_tick()
		# Distance to start slowing down = .4472135
		# Distance = .2828427
		self.assertAlmostEquals(c.vel.x,0.0858578643762681,5)
		self.assertAlmostEquals(c.vel.y,0.0858578643762681,5)
		self.assertAlmostEquals(c.pos.x,0.0858578643762681,5)
		self.assertAlmostEquals(c.pos.y,0.0858578643762681,5)

	def test_position(self):
		"""Gives the cell a random position, and tests if the cell is
		at that position."""
		rand_pos = random.random(), random.random()
		c = Cell(rand_pos[0], rand_pos[1])
		self.assertEquals(c.pos.x, rand_pos[0])
		self.assertEquals(c.pos.y, rand_pos[1])

	def test_distance_func(self):
		"""Tests the accuracy distance function."""
		self.assertEquals(5.0, util.distance(0,3,0,4))
		self.assertEquals(5.0, util.distance(3,0,4,0))
		self.assertEquals(5.0, util.distance(6,9,8,4))
		self.assertEquals(5.0, util.distance(-3,-6,-4,-8))
		e = environment.Environment()
		self.assertEquals(0.0,util.distance(0.0, e.width, e.height, 0.0))
		self.assertEquals(5.0,util.distance(2.0, e.width-1, 3.0, e.height-1))

if __name__ == "__main__":
	unittest.main()
