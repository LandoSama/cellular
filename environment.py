from cells import Cell
from food import Food
import random
import unittest
import math

def distance(x1,x2,y1,y2):
	"""Euclidian Distance Formula."""
	return	math.sqrt((x2-x1)**2 + (y2-y1)**2)

class Environment(object):
	_instance = None
	cell_list = []
	food_list = []
	width = height = 100
	
# __new__() 
#	generates 100x100 environment with count, count number of food and cells
	def __new__(cls, *args, **kwargs):
		if not cls._instance:
			return super(Environment, cls).__new__(
				cls, *args, **kwargs)
		return cls._instance

# __init__() 
#	generates 100x100 environment with count, count number of food and cells
	def __init__(self, *args):
		if Environment._instance is None:
			Environment._instance = self
			food_count = args[0]
			cell_count = args[1]
			self.add_food(food_count)
			self.add_cells(cell_count)
	
# add_food()
#	add food_count number of foods at random locations

	def add_food(self, food_count):
		for i in range(food_count):
			self.food_list.append(Food(random.randint(0, self.width), random.randint(0, self.height)))

# add_cells()
#	

	def add_cells(self, cell_count):
		for i in range(cell_count):
			self.cell_list.append(Cell(random.randint(0, self.width), random.randint(0, self.height)))
			
	def update_closest_food(self):
		for cell in self.cell_list:
			closest = None
			closest_dist = None
			tup = cell.get_pos()
			x1 = tup[0]
			y1 = tup[1]
			for food in self.food_list:
				x2 = food.x
				y2 = food.y
				dist = distance(x1,x2,y1,y2)
				if closest == None:
					closest = food
					closest_dist = dist
				else:
					if dist < closest_dist:
						closest = food
						closest_dist = dist
					else:
						pass
			cell.closest_food = closest
			cell.distance_to_closest_food = closest_dist
			
				
			
			
	
	def tick(self):
		for cell in self.cell_list:
			self.food_list[:] = [food for food in self.food_list if not(cell.try_consume_food(food))]
			self.update_closest_food(self)
			cell.one_tick()
			
	

class CreationTest(unittest.TestCase):
	def setUp(self):
		self.environment = Environment(10,10)
	def runTest(self):
		environment = self.environment
		
# test that environment initializes properly
		x = Environment()
		y = Environment()
		self.assertTrue(x is y)
		
		self.assertEquals(len(environment.cell_list), 10)
		
		self.assertTrue(environment.width > 0)
		self.assertTrue(environment.height > 0)
		
# test that cells are within bounds

		print "Cell coords"
		for cell in environment.cell_list:
			self.assertTrue(cell.x >= 0 and cell.x <= environment.width and cell.y >= 0 and cell.y <= environment.height, "Cell location out of bounds.")
			print "(" + str(cell.x) + ", " + str(cell.y) + ")"

# food is within bounds

		print "Food coords before cells eat"
		for food in environment.food_list:
			self.assertTrue(food.x >= 0 and food.x <= environment.width and food.y >= 0 and food.y <= environment.height, "Food location out of bounds.")
			print "(" + str(food.x) + ", " + str(food.y) + ")"	

# put a cell in the environment and a food in the environment in the middle 
# tick the time; then see if the cell eats the food

		c = Cell(environment.width/2, environment.height/2)
		environment.cell_list.append(c)
		food_count = len(environment.food_list)
		
		environment.food_list.append(Food(environment.width/2, environment.height/2))		
		environment.tick()
#	check that food list count was deincremented after food is eaten
		self.assertEqual(len(environment.food_list), food_count) 
		
# add another food to test that food epsilon from the boundry of the cell is eaten
		environment.food_list.append(Food(environment.width/2 + c.radius - 0.000001, environment.height/2))
		environment.tick()
		self.assertEqual(len(environment.food_list), food_count)

# add another food just on the boundry of the radius and see that it is not eaten		
		environment.food_list.append(Food(environment.width/2 + c.radius, environment.height/2))
		environment.tick()
		self.assertEqual(len(environment.food_list), food_count + 1)
		
# tests add_cells that the right number of cells are added
		num_cells = len(self.environment.cell_list)
		add_cells_count = random.randint(0,100)
		self.environment.add_cells(add_cells_count)
		self.assertEqual(len(self.environment.cell_list)-add_cells_count,num_cells)

# test add_food that the right number of food are added
#	needs to be done
		
if __name__ == "__main__":
	unittest.main()
