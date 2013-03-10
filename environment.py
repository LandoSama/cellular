import cells, food, random, unittest, util, singleton
from vector import Vector

class Environment(singleton.Singleton):
	def init_once(self, food_count, cells_count):
		"""Generate a 100x100 environment with specified amount of food and cells"""
		self.cell_list = []
		self.food_set = set()
		self.width = self.height = 100.0
		self.add_food(food_count)
		self.add_cells(cells_count)
		self.turn = 0

	def add_food(self, food_count):
		"""Add food_count number of foods at random locations"""
		for i in range(food_count):
			self.food_set.add(food.Food(random.randint(0, self.width), random.randint(0, self.height)))

	def add_cells(self, cell_count):
		for i in range(cell_count):
			self.cell_list.append(cells.Cell(random.randint(0, self.width), random.randint(0, self.height)))
			
	def update_closest_food(self):
		for cell in self.cell_list:
			closest = None
			closest_dist = None
			for food in self.food_set:
				dist = cell.pos.distance_to(food.pos)
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
		self.update_closest_food()
		for cell in self.cell_list:
			cell.one_tick()
		self.turn += 1

	def food_at(self, pos, r):
		return [food for food in self.food_set if pos.distance_to(food.pos) <= r]

	def remove_food(self, food):
		self.food_set.remove(food)
	
	def print_table(self,filename,comment=""):
		"""Prints a table to a textfile with the provided name, with the provided comment above it."""
		table_file = open(filename,"a")
		table_file.write("\n"+str(comment)+"\nCell_n\tx_pos\ty_pos\tx_vel\ty_vel\ttask\tx_dest\ty_dest\tradius\tenergy\n")
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
	def runTest(self):
		environment = Environment() #environment already initialized in test.py

		# test that environment is a singleton
		self.assertTrue(Environment() is environment)
		# test that environment initializes properly
		self.assertEquals(len(environment.cell_list), 10)
		self.assertEquals(len(environment.food_set), 10)
		self.assertTrue(environment.width > 0)
		self.assertTrue(environment.height > 0)
		
		# test that cells are within bounds
		for cell in environment.cell_list:
			self.assertTrue(cell.pos.x >= 0 and cell.pos.x <= environment.width and cell.pos.y >= 0 and cell.pos.y <= environment.height, "Cell location out of bounds.")
		# ..and food is within bounds
		for f in environment.food_set:
			self.assertTrue(f.x >= 0 and f.x <= environment.width and f.y >= 0 and f.y <= environment.height, "Food location out of bounds.")

		environment.cell_list = []
		# test that a cell will find and eat food underneath it
		c = cells.Cell(environment.width/2, environment.height/2)
		environment.cell_list.append(c)
		food_count = len(environment.food_set)

		environment.food_set.add(food.Food(environment.width/2, environment.height/2))		
		environment.tick()
		# test that food list count was decremented after food is eaten
		self.assertEqual(len(environment.food_set), food_count) 
		
		# test that food inside the cell is eaten
		environment.food_set.add(food.Food(environment.width/2 + c.radius - 0.000001, environment.height/2))
		environment.tick()
		self.assertEqual(len(environment.food_set), food_count)

		# test that food outside the cell is not eaten
		environment.food_set.add(food.Food(environment.width/2 + c.radius + 0.000001, environment.height/2))
		environment.tick()
		self.assertEqual(len(environment.food_set), food_count + 1)
		
		# test that add_cells adds the right number of cells
		num_cells = len(environment.cell_list)
		add_cells_count = random.randint(0,100)
		environment.add_cells(add_cells_count)
		self.assertEqual(len(environment.cell_list)-add_cells_count,num_cells)
		
if __name__ == "__main__": print 'no'; exit(-1)

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
