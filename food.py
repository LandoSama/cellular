import unittest
TestCase = unittest.TestCase

class Food:
    def __init__(self, x, y):
        self.energy = 1
        self.set_location(x, y)
    
    def set_location(self, x, y):
        self.x = x % environment.width
        self.y = y % environment.height

class CreationTest(TestCase):
	def setUp(self):
		self.food_obj = Food(1, 2)
	def runTest(self):
		self.assertEquals(self.food_obj.energy, 1)
		self.assertEquals(self.food_obj.x, 1)
		self.assertEquals(self.food_obj.y, 2)

if __name__ == "__main__":
	unittest.main()

