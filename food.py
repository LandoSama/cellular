import vector
import unittest
TestCase = unittest.TestCase
from cells import Cell

class Food:
	def __init__(self, x, y):
		self.energy = 0.5
		self.pos = vector.Point(x, y)

class CreationTest(TestCase):
	def setUp(self):
		self.food_obj = Food(1, 2)
	def runTest(self):
		self.assertEquals(self.food_obj.energy, 1)
		self.assertEquals(self.food_obj.pos.x, 1)
		self.assertEquals(self.food_obj.pos.y, 2)

if __name__ == "__main__":
	unittest.main()

