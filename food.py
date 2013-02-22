import unittest
TestCase = unittest.TestCase

class Food:
	def __init__(self):
		self.energy = 1

class CreationTest(TestCase):
	def setUp(self):
		self.food_obj = Food()
	def runTest(self):
		self.assertEquals(self.food_obj.energy, 1)

if __name__ == "__main__":
	unittest.main()
