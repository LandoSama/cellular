from cells import Cell
from food import Food
import random
import unittest
import math

class Environment(object):
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

# print_table()
#	output a table of each cell state to a text file

	def print_table(self,filename):
		"""Prints a table to a textfile with the provided name."""
		table_file = open(filename,"a")
		table_file.write("\nCell_n\tx_pos\ty_pos\tx_vel\ty_vel\ttask\tx_dest\ty_dest\tradius\tenergy\n")
		counter = 0
		for cell in self.cell_list:
			table_file.write("Cell_"+str(counter)+"\t"+str(round(cell.x,4))+"\t"+str(round(cell.y,4))+\
			"\t"+str(round(cell.xvel,4))+"\t"+str(round(cell.yvel,4))+"\t"+str(cell.task)+"\t")
			if type(cell.destination) == type(None):
				table_file.write("None\tNone\t"+str(cell.radius)+"\t"+str(cell.energy)+"\n")
			elif type(cell.destination) == type((0,0)):
				table_file.write(str(round(cell.destination[0],4))+"\t"+str(round(cell.destination[1],4))+\
				"\t"+str(cell.radius)+"\t"+str(cell.energy)+"\n")
			else: print type(cell.destination),cell.destination,"\n"
			counter += 1
		table_file.close()
		

class CreationTest(unittest.TestCase):
	def setUp(self):
		self.environment = Environment(10,10)
	def runTest(self):
# test that environment initializes properly 
		environment = self.environment
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
		
#if __name__ == "__main__":
#	unittest.main()

def debug_print_table():
	"""This probably shouldn't be at the end of the file, but nano doesn't have copy and paste."""
	tbl = "Debug_Cell_Table.txt"
	Env = Environment(0,0)
	Env.cell_list.append(Cell(0,0))
	Env.cell_list.append(Cell(1,2))
	Env.cell_list.append(Cell(7,5))
	Env.cell_list.append(Cell(6,9))
	Env.cell_list.append(Cell(-7,-7))
	Env.print_table(tbl)
	Env.tick()
	Env.print_table(tbl)
	Env.tick()
	Env.print_table(tbl)
	for run in xrange(5):
		Env.tick()
	Env.print_table(tbl)
	for run in xrange(50):
		Env.tick()
	Env.print_table(tbl)
