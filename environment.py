from cells import Cell
import random
import unittest

class Environment:
	cellList = []
	width = height = 100
	
	def __init__(self, count):
		#width = raw_input("Width of environment: ")
		#height = raw_input("Height of environment: ")
		self.add_cells(count)
	
	def add_cells(self, count):
		for i in range(1, int(count)):
			self.cellList.append(Cell(random.randint(0, self.width), random.randint(0, self.height)))
			
	def tick(self):
		for cell in self.cellList:
			cell.tick()
	
	def debug_output(self):
		for cell in self.cellList:
			print "(" + str(cell.x) + ", " + str(cell.y) + ")"

class CreationTest(unittest.TestCase):
	def testCreate(self):
		self.environment = Environment(10)
	def runTest(self):
		assert self.environment.width > 0 and self.environment.height > 0, 'Environment has no dimensions'
		self.environment.debug_output()

if __name__ == "__main__":
	unittest.main()
