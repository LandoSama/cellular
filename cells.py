import unittest, util, environment
import random, math
from vector import Vector, Point
from functools import partial
from operator import itemgetter, attrgetter
import weakref

def call(a, f):
	return f(a)

class Cell:
	BASE_ENERGY = .001
	
	def __init__(self,x,y):
		"""Cells begin with a specified position, without velocity, task or destination."""

		self.pos = Point(float(x), float(y))	# Woo vectors!
		self.vel = Vector(0.0, 0.0)
		self.acl = Vector(0.0, 0.0)

		# Required for motion.
		self.mass		 = 1
		self.K			 = .1			# K is a resistance constant.
		self.walk_force		 = 0.001
		self.exerted_force	 = Vector(0.0, 0.0)

		# Required for logic.
		self.task		 = None
		self.destination	 = None
		self.destination_type	 = None
		self.radius		 = .01
		self.energy		 = Cell.BASE_ENERGY

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
		SIGHT_RANGE = 0.2

		close_food = environment.Environment().food_at(self.pos, SIGHT_RANGE)
		if len(close_food) == 0:
			"""What the cell does should it be looking for food."""
			#If you can't see food, accelerate in a random direction.
			x = random.uniform(0, environment.Environment().width)
			y = random.uniform(0, environment.Environment().height)
			self.destination = Point(x, y)
			self.destination_type  = "Exploration"
			self.calc_force()
		else:
			#If there is any food within distance SIGHT_RANGE, get the closest one.
			#closest_food = min(close_food, key = lambda food: self.pos.distance_to(food.pos))
			closest_food = min(close_food, key = partial(reduce, call, (attrgetter("pos"), attrgetter("distance_to"), partial(call, self.pos))))# food: self.pos.distance_to(food.pos))
			
			def stop_getting_food(food):
				"""After the food gets eaten, stop trying to get it."""
				self.destination = self.destination_type = self.task = None
			self.task = "GettingFood"
			self.destination_type = "Food"
			#weakref.proxy calls stop_getting_food when the food is destroyed.
			self.destination = weakref.proxy(closest_food.pos, stop_getting_food)
			self.food_target = weakref.ref(closest_food)

	def task_getting_food(self):
		"""What the cell does when it has found food and is attempting to get it."""
		#assert(len(environment.Environment().food_at(self.destination, 0)) != 0)
		distance_to_destination = self.pos.distance_to(self.destination)
		if distance_to_destination > self.distance_to_start_slowing_down():
			self.calc_force()
		if distance_to_destination <= self.radius:
			self.eat(self.food_target())

	def get_speed(self):
		"""Returns the speed of the cell."""
		return abs(self.vel)

	def update_coords(self):
		"""Updates the cell's position, velocity and acceleration in that order."""
		prev_vel = Vector(self.vel.x, self.vel.y)
		
		self.pos += self.vel# + self.acl/2
		self.vel += self.acl
		if self.mass == 1:
			self.acl = self.exerted_force - self.vel*self.K
		else: self.acl = (self.exerted_force - self.vel*self.K)/self.mass
		#acl is change in velocity
		#displacement = (prev_vel + self.exerted_force/self.mass/2)
		#self.energy -= self.exerted_force*displacement
		self.energy -= self.exerted_force*prev_vel
		self.exerted_force = Vector(0.0,0.0)

	def calc_force(self):
		"""Cells calculate how much force they are exerting (prior to resistance)."""
		self.exerted_force = (self.destination - self.pos)*self.walk_force / abs(self.destination - self.pos)
		#print self.energy
		#self.energy -= self.exerted_force*self.vel
	
	"""
	Justification for change to return self.get_speed() * 999/2:
		dist = temp_speed + .999*temp_speed + ...
			 = sum(temp_speed*i)
			 = temp_speed * sum i=.0 to .999(i) / 1000
			 = temp_speed * sum i=0 to 999(i/1000)
			 = temp_speed * sum i=0 to 999(i) / 1000
			 = temp_speed * (999(1000)/2) / 1000
			 = temp_speed * 999/2
	Then that was abandoned, and changed to changed to return get_speed()/self.K:
		#dist = temp_speed + temp_speed(1-self.K) + temp_speed*(1-self.K)^2 ... + temp_speed
		sum[i=0 to infinity](temp_speed*(1-self.K)^i)
		temp_speed*sum((1-self.k)^i)
		temp_speed*1
				   ------------
				   1-(1-self.K)
		temp_speed
		----------
		self.K
	"""

	"""Changes the cell's position based on its velocity, a.k.a. movement."""
	def distance_to_start_slowing_down(self):
		"""Calculates the distance from the destination that, once past,
		the cell can reach without additional force."""
		return self.get_speed()/self.K #this is faster and should be equivalent to the below loop

	def eat(self, food):
		#for f in environment.Environment().food_at(self.pos, self.radius):
		self.energy += food.energy
		environment.Environment().remove_food(food)
		#The above line automatically resets our task and destination by calling stop_getting_food()

	def life_and_death(self):
		if self.energy >= 5*Cell.BASE_ENERGY: #hardcoded threshold
			#make babby 1
			x1 = random.uniform(self.pos.x-0.01,self.pos.x+0.01)
			y1 = random.uniform(self.pos.y-0.01,self.pos.y+0.01)
			environment.Environment().add_cells_at_location(x1,y1)
			
			#make babby 2
			x2 = random.uniform(self.pos.x-0.01,self.pos.x+0.01)
			y2 = random.uniform(self.pos.y-0.01,self.pos.y+0.01)
			environment.Environment().add_cells_at_location(x2,y2)
						
			#make two cells at slightly different positions
			environment.Environment().remove_cell(self)
		elif self.energy <= 0:
			environment.Environment().kill_cell(self)
			
	def one_tick(self):
		"""What a cell does every arbitrary unit of time."""
		self.TaskTable[self.task]()
		self.update_coords()
		self.life_and_death()

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
