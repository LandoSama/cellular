import unittest
TestCase = unittest.TestCase

class Food:
	def __init__(self):
		self.energy = 1

class CreationTest(TestCase):
	def testCreate(self):
		n = Food()
	def runTest(self):
		self.assertEquals(n.energy, 1)

if __name__ == "__main__":
	unittest.main()
