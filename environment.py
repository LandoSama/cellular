import cells, food, random, unittest, util, singleton, vector

class Environment(singleton.Singleton):
	def init_once(self, food_count, cells_count):
		"""Generate a 1x1 environment with specified amount of food and cells"""
		self.cell_list = []
		self.food_set = set()
		self.width = self.height = 1.0
		self.add_food(food_count)
		self.add_cells(cells_count)
		self.turn = 0

	def add_food(self, food_count):
		"""Add food_count number of foods at random locations"""
		for i in range(food_count):
			self.food_set.add(food.Food(random.uniform(0, self.width), random.uniform(0, self.height)))
	def add_food_at_location(self, x, y):
		"""Add a food item at location"""
		self.food_set.add(food.Food(x, y))

	def add_cells(self, cell_count):
		for i in range(cell_count):
			self.cell_list.append(cells.Cell(random.uniform(0, self.width), random.uniform(0, self.height)))
			
	def add_cells_at_location(self,x,y):
		self.cell_list.append(cells.Cell(x, y))
							
	def tick(self):
		for cell in self.cell_list:
			cell.one_tick()
		self.turn += 1

	def food_at(self, pos, r):
		return [food for food in self.food_set if pos.distance_to(food.pos) <= r]

	def remove_food(self, food):
		self.food_set.remove(food)
	


	def kill_cell(self,cell):
		pos = cell.get_pos()
		self.cell_list.remove(cell)
		self.add_food_at_location(*pos)

	def remove_cell(self,cell):
		self.cell_list.remove(cell)

# print_table()
#	output a table of each cell state to a text file


	def print_table(self,filename,comment=""):
		"""Prints a table to a textfile with the provided name, with the provided comment above it."""
		table_file = open(filename,"a")
		table_file.write("\n"+str(comment)+"\nCell_n\tx_pos\ty_pos\tx_vel\ty_vel\tx_dest\ty_dest\tradius\tenergy\ttask\n")
		counter = 0
		for cell in self.cell_list:
			table_file.write("Cell_"+str(counter)+"\t"+str(round(cell.pos.x,4))+"\t"+str(round(cell.pos.y,4))+\
			"\t"+str(round(cell.vel.x,4))+"\t"+str(round(cell.vel.y,4))+"\t")
			if type(cell.destination) == type(None):
				table_file.write("None\tNone\t"+str(cell.radius)+"\t"+str(cell.energy)+"\t"+str(cell.task)+"\n")
			elif type(cell.destination) == vector.Point:
				table_file.write(str(round(cell.destination.x,4))+"\t"+str(round(cell.destination.y,4))+\
				"\t"+str(cell.radius)+"\t"+str(cell.energy)+"\t"+str(cell.task)+"\n")
			else: raise TypeError(str(type(cell.destination))+" "+str(cell.destination))
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
			self.assertTrue(f.pos.x >= 0 and f.pos.x <= environment.width and f.pos.y >= 0 and f.pos.y <= environment.height, "Food location out of bounds.")

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
