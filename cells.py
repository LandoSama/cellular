import unittest, util, environment
import random, math
from vector import Vector

class Cell:
	def __init__(self,x,y):
		"""Cells begin with a specified position, without velocity, task or destination."""
		self.max_acceleration = 0.0002
		self.max_speed = 0.001
		self.pos = Vector(float(x), float(y))
		self.vel = Vector(0.0, 0.0)
		self.task = None
		self.destination = None
		self.destination_type = None
		self.radius = .01
		self.energy = 0

		# Task jumptable!
		self.TaskTable			= {}
		self.TaskTable[None]		= self.task_none
		self.TaskTable["FindingFood"]	= self.task_finding_food
		self.TaskTable["GettingFood"]	= self.task_getting_food

#
#	"Task" functions, i.e. the cell's activities during each tick, depending on its task.

	def task_none(self):
		"""What the cell does should it have no task."""
		self.task = "FindingFood"

	def task_finding_food(self):
		#closest piece of food
		SIGHT_RANGE = .02

		close_food = environment.Environment().food_at(self.pos, SIGHT_RANGE)
		#If there is any food within distance SIGHT_RANGE, get the closest one.
		if len(close_food) > 0:
			closest_food = min(close_food, key = lambda food: self.pos.distance_to(food.pos))
		else: closest_food = None

		"""What the cell does should it be looking for food."""
		if closest_food is None:
			# If you can't see food, accelerate in a random direction.
			self.destination       = Vector(random.uniform(0,environment.Environment().width),
							 random.uniform(0,environment.Environment().height))
			self.destination_type  = "Exploration"
			self.accel_towards_destination()
		else:
			# Otherwise, the cell should try to get it.
			self.destination = closest_food.pos
			self.destination_type = "Food"
			self.task = "GettingFood"

	def task_getting_food(self):
		"""What the cell does when it has found food and is attempting to get it."""
		# If there exists some food item at the destination location,
		if len(environment.Environment().food_at(self.destination,.1)) != 0:
			distance_to_destination = util.distance(self.pos.x,self.destination.x,self.pos.y,self.destination.y)
			if distance_to_destination > self.distance_to_start_slowing_down():
				self.accel_towards_destination()
			else:
				self.slow_towards_destination()
		else:
			self.destination = self.destination_type = self.task = None
			self.closest_food = self.distance_to_closest_food = None

	def get_speed(self):
		"""Returns the speed of the cell."""
		return abs(self.vel)

	def update_coords(self):
		"""Changes the cell's position based on its velocity, a.k.a. movement."""
		self.pos += self.vel

	def set_task(self,new_task):
		"""Sets the task of the cell."""
		self.task = new_task

	def speed_limit(self):
		"""Prevents the cells from going over the speed limit."""
		if abs(self.vel.x) > self.max_speed:
			if self.vel.x > 0: 	self.vel.x = self.max_speed
			else: 			self.vel.x = self.max_speed*(-1)
		if abs(self.vel.y) > self.max_speed:
			if self.vel.y > 0: 	self.vel.y = self.max_speed
			else: 			self.vel.y = self.max_speed*(-1)

	def accel_towards_destination(self):
		"""Accelerates the cell towards its destination."""
		# get total, x, and y distances to destination
		total_distance = self.pos.distance_to(self.destination)
                xdist = abs(self.pos.x - self.destination.x)
                ydist = abs(self.pos.y - self.destination.y)

                # If the cell is right of the destination...
		if self.pos.x > self.destination.x:
			# ...accelerate left if it's closer than half the environment's size
			if xdist <= environment.Environment().width / 2.0:
				self.vel.x -= self.max_acceleration*xdist/total_distance
			# ...accelerate right if it's just faster to wrap around
			else:
				self.vel.x += self.max_acceleration*xdist/total_distance

		# If the cell is left of the destination...
		else:
			# ...accelerate right if it's closer than half the environment's size
			if xdist <= environment.Environment().width / 2.0:
				self.vel.x += self.max_acceleration*xdist/total_distance
			# ...accelerate left if it's just faster to wrap around
			else:
				self.vel.x -= self.max_acceleration*xdist/total_distance

		# If the cell is above the destination...
		if self.pos.y > self.destination.y:
			if ydist <= environment.Environment().height / 2.0:
				self.vel.y -= self.max_acceleration*ydist/total_distance
			else:
				self.vel.y += self.max_acceleration*ydist/total_distance

		# If the cell is below the destination...
		else:
			if ydist <= environment.Environment().height / 2.0:
                                self.vel.y += self.max_acceleration*ydist/total_distance
			else:
				self.vel.y -= self.max_acceleration*ydist/total_distance

		self.speed_limit()
			
	def slow_towards_destination(self):
		"""Slows a cell by directly reducing its velocity until it gets close to 0."""
		# Get total, x, and y distances to destination
		total_distance = self.pos.distance_to(self.destination)
		xdist = abs(self.pos.x - self.destination.x)
		ydist = abs(self.pos.y - self.destination.y)
		# Calculate how much each velocity will be reduced
		x_reduc = self.max_acceleration*xdist/total_distance
		y_reduc = self.max_acceleration*ydist/total_distance
		
		# If the velocity is less than what it will be reduced by, just make it zero.
		if abs(self.vel.x) <= x_reduc:
			self.vel.x = 0.0
		# Otherwise: if velocity is positive, subtract. If negative, add.
		elif self.vel.x > 0: self.vel.x -= x_reduc
		elif self.vel.x < 0: self.vel.x += x_reduc
		
		# Repeat for y velocity.
		if abs(self.vel.y) <= y_reduc:
			self.vel.y = 0.0
		elif self.vel.y > 0: self.vel.y -= y_reduc
		elif self.vel.y < 0: self.vel.y += y_reduc
		
		self.speed_limit()
		
	def distance_to_start_slowing_down(self):
		"""Calculates the distance from the destination that, once past,
		the cell ought to begin slowing down to reach its destination."""
		ticks		 = int(self.get_speed()/self.max_acceleration)
		dist		 = self.get_speed()
		temp_speed	 = self.get_speed()
		for i in xrange(ticks):
			temp_speed -= self.max_acceleration
			dist += temp_speed
		return dist
		
	def eat(self):
		for f in environment.Environment().food_at(self.pos, self.radius):
			self.energy += f.energy
			environment.Environment().remove_food(f)
			self.task			 = None
                        self.destination		 = None
                        self.closest_food		 = None
                        self.distance_to_closest_food	 = None

	def one_tick(self):
		"""What a cell does every arbitrary unit of time."""
		self.TaskTable[self.task]()
		self.update_coords()
		self.eat()

class TestFunctions(unittest.TestCase):
	def test_taskless(self):
		"""Tests one_tick() giving taskless cells a random walk."""
		c = Cell(0,0)
		# When a cell is spawned, it should have no task.
		self.assertEquals(c.task,None)
		c.one_tick()
		self.assertEquals(c.task,"FindingFood")

	def test_position(self):
		"""Gives the cell a random position, and tests if the cell is
		at that position."""
		rand_pos = random.random(), random.random()
		c = Cell(rand_pos[0], rand_pos[1])
		self.assertEquals(c.pos.x, rand_pos[0])
		self.assertEquals(c.pos.y, rand_pos[1])

	def test_distance_func(self):
		"""Tests the accuracy distance function."""
		self.assertEquals(.05, util.distance(.00, .03, .00,.04))
		self.assertEquals(.05, util.distance(.03, .00, .04,.00))
		self.assertEquals(.05, util.distance(.06, .09, .08,.04))
		self.assertEquals(.05, util.distance(-.03,-.06,-.04,-.08))
		e = environment.Environment()
		self.assertAlmostEquals(.00, util.distance(.00, e.width, e.height, 0.0))
		self.assertAlmostEquals(.05, util.distance(.02, e.width-.01, .03, e.height-.01))

if __name__ == "__main__":
	unittest.main()
