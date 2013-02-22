import math, unittest
from random import random


class Cell:
	def __init__(self,x,y):
		self.max_acceleration = 1
		self.max_speed = 10
		self.speed = 0
		self.x = x
		self.y = y
		self.xvel = 0
		self.yvel = 0
		self.task = None
		self.destination = None
		self.radius = 1
		self.energy = 0
		
	def try_consume_food(self, food):
		x_diff = food.x - self.x
		y_diff = food.y - self.y
		if math.sqrt(x_diff*x_diff + y_diff*y_diff) < self.radius:
			#print "Food coord: (", food.x, ",", food.y, ")"
			#print "Cell coord: (", self.x, ",", self.y, ")"
			#print "Distance:", math.sqrt(x_diff*x_diff + y_diff*y_diff)
			self.energy += food.energy
			return True
		return False

	def get_pos(self):
		return (x_pos, y_pos)
	
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

	def one_tick(self):
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


class CreationTest(unittest.TestCase):
	def setUp(self):
		self.rand_pos = random(), random()
		self.cell = Cell(self.rand_pos[0], self.rand_pos[1])
	def runTest(self):
		self.assertEquals(self.cell.x, self.rand_pos[0])
		self.assertEquals(self.cell.y, self.rand_pos[1])

if __name__ == '__main__':
    unittest.main()

