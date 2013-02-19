from cells import Cell
from food import Food
import random
import unittest

class Environment:
	cell_list = []
	food_list = []
	width = height = 100
	
	def __init__(self, food_count, cell_count):
		#width = raw_input("Width of environment: ")
		#height = raw_input("Height of environment: ")
		self.add_food(food_count)
		self.add_cells(cell_count)
	
	def add_food(self, food_count):
		for i in range(1, int(food_count)):
			self.food_list.append(Food(random.randint(0, self.width), random.randint(0, self.height)))

	def add_cells(self, cell_count):
		for i in range(1, int(cell_count)):
			self.cell_list.append(Cell(random.randint(0, self.width), random.randint(0, self.height)))
			
	def tick(self):
		for cell in self.cell_list:
			cell.one_tick()
	
	def debug_output(self):
		print "Cell coords"
		for cell in self.cell_list:
			print "(" + str(cell.x) + ", " + str(cell.y) + ")"
		print "Food coords"
		for food in self.food_list:
			print "(" + str(food.x) + ", " + str(food.y) + ")"

class EnvironmentTestCase(unittest.TestCase):
	def runTest(self):
		environment = Environment(10, 10)
		assert environment.width > 0 and environment.height > 0, 'Environment has no dimensions'
		environment.debug_output()

if __name__ == "__main__":
	unittest.main()
