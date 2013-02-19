import math, unittest
import random

def distance(a,b):
	pass

class Cell:
	def __init__(self,x,y):
		self.max_acceleration = 1.0
		self.max_speed = 10.0
		self.x = float(x)
		self.y = float(y)
		self.xvel = 0.0
		self.yvel = 0.0
		self.task = None
		#lets say that a destination is a tuple of the form (x,y) where x and y are real numbers
		self.destination = None

	def get_pos(self):
		return (self.x, self.y)

	#def update_speed(self):
	#	self.speed += math.sqrt(abs(self.xvel) + abs(self.yvel))

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
		# get total distance to dest
		total_distance = distance(self.x,self.destination[0],self.y,self.destination[1]
		# get x distance to dest
		xdist = abs(self.x - self.destination[0]
		# get y distance to dest
		ydist = abs(self.y - self.destination[1]

		if self.x > self.destination:
			self.xvel -= self.max_acceleration(xdist/total_distance)
			if abs(self.xvel) >= self.max_speed:
				self.xvel = self.max_speed * (-1)
		else:
			self.xvel += self.max_acceleration(xdist/total_distance)
			if abs(self.xvel) >= self.max_speed:
				self.xvel = self.max_speed
			
		if self.y > self.destination:
			self.y -= self.max_acceleration(ydist/total_distance)
			if abs(self.yvel) >= self.max_speed:
				self.yvel = self.max_speed * (-1)
		else:
			self.yvel += self.max_acceleration(ydist/total_distance)
			if abs(self.yvel) >= self.max_speed:
				self.yvel = self.max_speed
				
		self.update_coords()
				
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
				#check if we are at the destination or closer than our current speed
					#set task to stop
				#if we are further away than that
					#self.accel_towards_destination()
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
			rand_pos = random.random(), random.random()
			z = Cell(rand_pos[0], rand_pos[1])
			assert z.x ==rand_pos[0]
			assert z.y==rand_pos[1]

if __name__ == '__main__':
    unittest.main()





