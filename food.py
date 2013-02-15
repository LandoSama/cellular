import unittest
TestCase = unittest.TestCase

class FoodTestCase(TestCase):
    def testCreate(self):
        n = Food()
        self.assertEquals(n.energy, 1)

class Food:
    def __init__(self):
        self.energy = 1

if __name__ == "__main__":
    unittest.main()
