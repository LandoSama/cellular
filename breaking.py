import unittest
import cells, environment, food

class BreakTest(unittest.TestCase):
	def setUp(self):
		self.e = environment.Environment(0, 0)
	def new_environment_exception(self):
		excepted = False
		try:
			ep = environment.Environment(10, 10)
		except environment.ExistenceError:
			excepted = True
		self.assertTrue( excepted )
	#Also ensure that environment() called when there is no existing
	#environment will fail loudly
	#e._instance
	def food_out_of_bounds(self):
		excepted = False
		try:
			f = food.Food(-1, -1)
		except ValueError:
			excepted = True
		self.assertTrue( excepted )
	def negative_init(self):
		excepted = False
		environment._instnace = None
		try:
			self.e = environment.Environment(-10,-10)
		except ValueError:
			excepted = True
		self.assertTrue(excepted)
	def creature_out_of_bounds(self):
		excepted = False
		try:
			n = Cells.Cell(-1,-1)
		except ValueError:
			excepted = True
		self.assertTrue(excepted)
	def cell_speed_euclid(self):
		n = Cells.Cell(0,0)
		n.xvel = n.yvel = 0.5
		#Check that cell velocity is euclidean distance
		self.assertEquals( (0.5**2 + 0.5**2)**0.5, n.get_speed() )
	def cell_out_of_bounds(self):
		n = Cells.Cell(0,0)
		self.e.cell_list.append(n)
		n.xvel = n.yvel = -1
		self.e.tick()
		self.assertTrue( 0 <= n.x <= self.e.width )
		self.assertTrue( 0 <= n.y <= self.e.height )
	def invalid_destination(self):
		n = Cells.Cell(0,0)
		self.e.cell_list.append(n)
		n.go_to(-10,-10)
		[ self.e.tick() for i in range(200) ]
		self.assertTrue( 0 <= n.x <= self.e.width )
		self.assertTrue( 0 <= n.y <= self.e.height )
	def invalid_task(self):
		excepted = False
		n = Cells.Cell(0,0)
		self.e.cell_list.append(n)
		n.go_to(0.1,0.1)
		n.task = "ccx"
		try:
			[ self.e.tick() for i in range(200) ]
		except:
			excepted = True
		self.assertTrue(excepted)
	def coord_non_update(self):
		n = Cells.Cell(0,0)
		self.e.cell_list.append(n)
		n.xvel = n.yvel = 0.1
		n.task = None
		e.tick()
		self.assertNotEqual( n.x, 0 )
		self.assertNotEqual( n.y, 0 )
if __name__ == "__main__":
	unittest.main()
