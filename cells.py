import unittest, util, environment
import random, math
import pygame
from vector import Vector, Point
from functools import partial
from operator import itemgetter, attrgetter

def call(a, f):
	return f(a)
	
def random_color():
    randomcolor = pygame.Color(random.randint(0,255),random.randint(0,255),random.randint(0,255))
    return randomcolor

class Cell:
	def __init__(self, x, y, mass=0.3, energy=0.1):
		"""Cells begin with a specified position, without velocity, task or destination."""
		# Position, Velocity and Acceleration vectors:
		self.pos = Point(float(x), float(y))
		self.vel = Vector(0.0, 0.0)
		self.acl = Vector(0.0, 0.0)

		# Arbitrary constants:
		self.K			= 0.5			# K is a resistance constant.
		self.density		= .0001			# density is used to calculate radius

		# Required for motion:
		self.mass		 = mass
		self.walk_force		 = 0.001
		self.exerted_force	 = Vector(0.0, 0.0)

		# Required for logic:
		self.task		 = None
		self.destination	 = None
		self.destination_type	 = None
		self.radius		 = ( 3*self.mass*self.density / (4*math.pi) )**(1/3.0)
		self.energy		 = energy

		# Task jumptable:
		self.TaskTable			= {}
		self.TaskTable[None]		= self.task_none
		self.TaskTable["FindingFood"]	= self.task_finding_food
		self.TaskTable["GettingFood"]	= self.task_getting_food

		# Misc:
		self.color = random_color()

#
#	"Task" functions, i.e. the cell's activities during each tick, depending on its task.

	def task_none(self):
		"""What the cell does should it have no task."""
		self.task = "FindingFood"

	def task_finding_food(self):
		#closest piece of food
		SIGHT_RANGE = 0.1 + self.radius

		close_food = environment.Environment().food_at(self.pos, SIGHT_RANGE)
		#If there is any food within distance SIGHT_RANGE, get the closest one.
		if len(close_food) > 0:
			#closest_food = min(close_food, key = lambda food: self.pos.distance_to(food.pos))
			closest_food = min(close_food, key = partial(reduce, call, (attrgetter("pos"), attrgetter("distance_to"), partial(call, self.pos))))# food: self.pos.distance_to(food.pos))
		else: closest_food = None

		"""What the cell does should it be looking for food."""
		if closest_food is None:
			# If you can't see food, accelerate in a random direction.
			x = random.uniform(0,environment.Environment().width)
			y = random.uniform(0,environment.Environment().height)
			self.destination = Point(x, y)
			self.destination_type  = "Exploration"
			self.calc_force()
		else:
			# Otherwise, the cell should try to get it.
			self.destination = closest_food.pos
			self.destination_type = "Food"
			self.task = "GettingFood"

	def task_getting_food(self):
		"""What the cell does when it has found food and is attempting to get it."""
		# If there exists some food item at the destination location,
		if len(environment.Environment().food_at(self.destination, 0)) != 0:
			distance_to_destination = self.pos.distance_to(self.destination)
			if distance_to_destination > self.distance_to_start_slowing_down():
				self.calc_force()
		else:
			self.destination = self.destination_type = self.task = None
			self.closest_food = self.distance_to_closest_food = None

	def update_coords(self):
		"""Updates the cell's position, velocity and acceleration in that order."""
		self.pos += self.vel
		self.vel += self.acl
		self.acl = self.exerted_force - self.vel*self.K*(self.radius**2)/self.mass
		self.exerted_force = Vector(0.0,0.0)

	def calc_force(self):
		"""Cells calculate how much force they are exerting (prior to resistance)."""
		self.exerted_force = (self.destination - self.pos)*self.walk_force / (abs(self.destination - self.pos)*self.mass)
		if self.energy > 0:
			self.energy -= self.walk_force*1
		else:	self.mass -= self.walk_force*3

	def distance_to_start_slowing_down(self):
		"""Calculates the distance from the destination that, once past,
		the cell ought to begin slowing down to reach its destination."""
		return (abs(self.vel) * self.mass) / (self.K * self.radius**2)

	def eat(self):
		for f in environment.Environment().food_at(self.pos, self.radius):
			self.energy += f.energy/2.0
			self.mass += f.energy/2.0
			environment.Environment().remove_food(f)
			self.task			 = None
			self.destination		 = None
			self.closest_food		 = None
			self.distance_to_closest_food	 = None

	def weight_management(self):
		self.radius = ( 3*self.mass*self.density / (4*math.pi) )**(1/3.0)

	def life_and_death(self):
		if self.energy >= 0.5 and self.mass >= 0.6: #hardcoded threshold
			#stats of both babbyz
			newMass		 = self.mass/2.0
			newEnergy	 = (self.energy - 3)/2.0

			#make babby 1
			x1 = random.uniform(self.pos.x-0.01,self.pos.x+0.01)
			y1 = random.uniform(self.pos.y-0.01,self.pos.y+0.01)
			environment.Environment().add_cells_at_location(x1,y1,newMass,newEnergy)
			
			#make babby 2
			x2 = random.uniform(self.pos.x-0.01,self.pos.x+0.01)
			y2 = random.uniform(self.pos.y-0.01,self.pos.y+0.01)
			environment.Environment().add_cells_at_location(x2,y2,newMass,newEnergy)
						
			#make two cells at slightly different positions
			environment.Environment().remove_cell(self)
#		elif self.energy <= 0:			Now it is if the mass is below a certain point
		elif self.mass <= 0.1:
			environment.Environment().kill_cell(self)
			
	def one_tick(self):
		"""What a cell does every arbitrary unit of time."""
		self.TaskTable[self.task]()
		self.update_coords()
		self.eat()
		self.weight_management()
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
