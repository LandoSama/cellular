import unittest, util, environment as env
import random, math

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
		self.destination_type = None
		self.radius = 1
		self.energy = 0

		#closest piece of food
		self.closest_food = None
		self.distance_to_closest_food = None

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
		return math.sqrt((self.xvel)**2 + (self.yvel)**2)

	def update_coords(self):
		"""Changes the cell's position based on its velocity, a.k.a. movement."""
		self.x += self.xvel
		self.y += self.yvel
		self.x = self.x % env.Environment().width
		self.y = self.y % env.Environment().height

	def go_to(self,destination):
		"""Tells the cell to move to the destination specified.
		Destinations need to be in tuple form."""
		self.destination = destination
		self.task = 'move'

	def set_task(self,new_task):
		"""Sets the task of the cell."""
		self.task = new_task

# sets a random destination and sets task to move
#

	def random_walk(self):
		"""The cell begins to move towards a random destination."""
		self.destination = random.uniform(0,env.Environment().width),random.uniform(0,env.Environment().height),
		self.set_task('move')
		
	def set_food_as_destination(self):
		pass

	def speed_limit(self):
                """Prevents the cells from going over the speed limit."""
                if abs(self.xvel) > self.max_speed:
                        if self.xvel > 0:       self.xvel = self.max_speed
                        else:                   self.xvel = self.max_speed*(-1)
                if abs(self.yvel) > self.max_speed:
                        if self.yvel > 0:       self.yvel = self.max_speed
                        else:                   self.yvel = self.max_speed*(-1)

	def accel_towards_destination(self):
		"""Accelerates the cell towards its destination."""
		# get total, x, and y distances to destination
		total_distance = util.distance(self.x,self.destination[0],self.y,self.destination[1])
		xdist = abs(self.x - self.destination[0])
		ydist = abs(self.y - self.destination[1])
                # If the cell is right of the destination, accelerate left
		if self.x > self.destination[0]:
			self.xvel -= self.max_acceleration*xdist/total_distance
		# If the cell is left of the destination, accelerate right
		else:
			self.xvel += self.max_acceleration*xdist/total_distance
			
		# If the cell is above the destination, accelerate downwards
		if self.y > self.destination[1]:
			self.yvel -= self.max_acceleration*ydist/total_distance
		# If the cell is below the destination, accelerate upwards
		else:
			self.yvel += self.max_acceleration*ydist/total_distance
		self.speed_limit()
			
	def slow_towards_destination(self):
		"""Slows a cell by directly reducing its velocity until it gets close to 0."""
		# Get total, x, and y distances to destination
		total_distance = util.distance(self.x,self.destination[0],self.y,self.destination[1])
		xdist = abs(self.x - self.destination[0])
		ydist = abs(self.y - self.destination[1])
		# Calculations how much of each velocity will be reduced
                x_reduc = self.max_acceleration*xdist/total_distance
		y_reduc = self.max_acceleration*ydist/total_distance
		
		# If the velocity is less than what it will be reduced by, just make it zero.
		if abs(self.xvel) <= x_reduc:
                        self.xvel = 0.0
                # Otherwise: if velocity is positive, subtract. If negative, add.
                elif self.xvel > 0:     self.xvel -= x_reduc
                elif self.xvel < 0:     self.xvel += x_reduc
                else:                   pass
                
                # Repeat for y velocity.
                if abs(self.yvel) <= y_reduc:
                        self.yvel = 0.0
                elif self.yvel > 0:     self.yvel -= y_reduc
                elif self.yvel < 0:     self.yvel += y_reduc
                else:                   pass
		self.speed_limit()
		
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
		e = env.Environment()
		for f in e.food_at(self.x, self.y, self.radius):
			self.energy += f.energy
			e.remove_food(f)
			self.task = None
                        self.destination = None
                        self.closest_food = None
                        self.distance_to_closest_food = None

	def one_tick(self):
		"""What a cell does every arbitrary unit of time."""
		if self.task == None:
			# food nearby? then go to it.
			if self.distance_to_closest_food < 20:
				self.destination = (self.closest_food.x,self.closest_food.y)
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
				distance_to_destination = util.distance(self.x,self.destination[0],self.y,self.destination[1])			
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
		self.update_coords()
		self.eat()

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
		c.destination = (3,4)
		# Testing the cell moving from (0,0) to (3,4).
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
		"""Tests the accuracy distance function."""
		self.assertEquals(5.0,util.distance(0,3,0,4))
		self.assertEquals(5.0,util.distance(3,0,4,0))
		self.assertEquals(5.0,util.distance(6,9,8,4))
		self.assertEquals(5.0,util.distance(-3,-6,-4,-8))

if __name__ == "__main__":
	unittest.main()
