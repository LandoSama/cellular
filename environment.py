from cells import Cell
from food import Food
import random
import unittest
import math

class Environment:
	cell_list = []
	food_list = []
	width = height = 100
	
# __init__() 
#	generates 100x100 environment with count, count number of food and cells

	def __init__(self, food_count, cell_count):
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
			
	def tick(self):
		for cell in self.cell_list:
			self.food_list[:] = [food for food in self.food_list if not(cell.try_consume_food(food))]
			cell.one_tick()

class CreationTest(unittest.TestCase):
	def setUp(self):
		self.environment = Environment(10,10)
	def runTest(self):
		environment = self.environment
		self.assertTrue(environment.width > 0)
		self.assertTrue(environment.height > 0)
		
		print "Cell coords"
		for cell in environment.cell_list:
			self.assertTrue(cell.x >= 0 and cell.x <= environment.width and cell.y >= 0 and cell.y <= environment.height, "Cell location out of bounds.")
			print "(" + str(cell.x) + ", " + str(cell.y) + ")"
		print "Food coords before cells eat"
		for food in environment.food_list:
			self.assertTrue(food.x >= 0 and food.x <= environment.width and food.y >= 0 and food.y <= environment.height, "Food location out of bounds.")
			print "(" + str(food.x) + ", " + str(food.y) + ")"	
		environment.tick()
		print "Food coords after cells eat"
		for food in environment.food_list:
			self.assertTrue(food.x >= 0 and food.x <= environment.width and food.y >= 0 and food.y <= environment.height, "Food location out of bounds.")
			print "(" + str(food.x) + ", " + str(food.y) + ")"
			
		c = Cell(environment.width/2, environment.height/2)
		environment.cell_list.append(c)
		food_count = len(environment.food_list)
		
		environment.food_list.append(Food(environment.width/2, environment.height/2))		
		environment.tick()
		self.assertEqual(len(environment.food_list), food_count) 
		
		environment.food_list.append(Food(environment.width/2 + c.radius - 0.000001, environment.height/2))
		environment.tick()
		self.assertEqual(len(environment.food_list), food_count)
		
		environment.food_list.append(Food(environment.width/2 + c.radius, environment.height/2))
		environment.tick()
		self.assertEqual(len(environment.food_list), food_count + 1)
		
if __name__ == "__main__":
	unittest.main()
