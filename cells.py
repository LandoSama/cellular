import math, unittest
import random


class Cell:
	def __init__(self,x,y):
		self.radius = 1
		self.max_acceleration = 1
		self.max_speed = 10
		self.speed = 0
		self.x = x
		self.y = y
		self.xvel = 0
		self.yvel = 0
		self.task = None
		self.destination = None

	def get_pos(self):
		return (self.x, self.y)
	
	def update_speed(self):
		self.speed += math.sqrt(abs(self.xvel) + abs(self.yvel))
		
	def update_coords(self):
		self.x += self.xvel
		self.y += self.yvel

	def set_task(self,new_task):
		self.task = new_task

	def random_walk(self):
		#math.random(
		#randomly pick destination
		#set destination
		#set task to move
		self.set_task('move')
		pass

	def accel_towards_destination(self):
		# get x dist to dest
		# get y dist to dest
		if self.x > self.destination:
			self.xvel -= self.max_acceleration(x/(x+y))
		else:
			self.xvel += self.max_acceleration(x/(x+y))

	def stop(self):
		pass

	def destroy(self):
		#implement later
		pass

	def divide(self):
		child1, child2 = Cell(*self.get_pos()), Cell(*self.get_pos())
		self.destroy()
		return child1, child2

	def one_tick(self):
		if self.radius >=2:
			# create new cell
			self.divide()
		elif self.radius ==1:
			 self.radius += 1
		else:
			#this shouldn't happen
			pass

		if self.task == None:
			#no task, set task
			#default: random walk
			self.random_walk()
		elif self.task == 'move':
			pass
			#check if we have a destination
			#if yes,
				#accel to destination
				#check if we are at the destination or closer than our current speed
					#set task to stop
			#if no,
				#something fucked
		elif self.task == 'stop':
			pass
			#slow down to a stop
		elif self.task == 'wait':
			pass
			#durp sleep or something


class TestFunctions(unittest.TestCase):
	def test_init(self):
		x = random.random()
		y = random.random()
		test_cell = Cell(x, y)

		self.assertNotEqual(test_cell,None)
		self.assertEqual(test_cell.radius, 1)
		self.assertEquals(test_cell.max_acceleration, 1)
		self.assertEquals(test_cell.max_speed, 10)
		self.assertEquals(test_cell.speed,0)
		self.assertEquals(test_cell.x,x)
		self.assertEquals(test_cell.y,y)
		self.assertEquals(test_cell.xvel, 0)
		self.assertEquals(test_cell.yvel, 0)
		self.assertEquals(test_cell.task, None)
		self.assertEquals(test_cell.destination, None)

	def setUp(self):
			self.test_cell = Cell(random.random(), random.random())

	def test_divide(self):
		test_child1, test_child2 = self.test_cell.divide()

		# uncomment when destroy() is implemented
		#assert self == none

		cell_location = self.test_cell.get_pos()

		self.assertNotEqual(test_child1, None)
		self.assertNotEqual(test_child2, None)

		self.assertEqual(test_child1.get_pos(), cell_location)
		self.assertEqual(test_child2.get_pos(), cell_location)

	def test_destroy(self):
		pass
		#uncomment when destroy is implemented
		#test_cell = setup()
		#test_cell.test_destroy()
		#assert test_cell == None
		
if __name__ == '__main__':
    unittest.main()
