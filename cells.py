<<<<<<< HEAD
import math

class Cell: 
=======
import math, unittest
from random import randint

class Cell:
>>>>>>> 0.1.cells
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


class TestFunctions(unittest.TestCase):
	def test_position(self):
			rand_pos = randint(1, 100), randint(1,100)
			z = Cell(rand_pos[0], rand_pos[1])
			assert z.x ==rand_pos[0]
			assert z.y==rand_pos[1]

if __name__ == '__main__':
    unittest.main()

