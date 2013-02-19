import unittest
TestCase = unittest.TestCase

class FoodTestCase(TestCase):
    def testCreate(self):
        n = Food()
        self.assertEquals(n.energy, 1)

class Food:
    def __init__(self, x, y):
        self.energy = 1
        self.set_location(x, y)
    
    def set_location(self, x, y):
        self.x = x
        self.y = y

if __name__ == "__main__":
    unittest.main()
