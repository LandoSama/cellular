import math, unittest
import random

def distance(x1,x2,y1,y2):
	return	math.sqrt((x2-x1)**2 + (y2-y1)**2)

class Cell:
	def __init__(self,x,y):
		self.max_acceleration = 0.02
		self.max_speed = 0.1
		self.x = float(x)
		self.y = float(y)
		self.xvel = 0.0
		self.yvel = 0.0
		self.task = None
		#lets say that a destination is a tuple of the form (x,y) where x and y are real numbers
		self.destination = None

	def get_pos(self):
		return (self.x, self.y)

	def get_vel(self):
		return (self.xvel, self.yvel)

	def get_task(self):
		return self.task

	def get_destination(self):
		return self.destination

	def get_speed(self):
		return math.sqrt(abs(self.xvel) + abs(self.yvel))

	def update_coords(self):
		self.x += self.xvel
		self.y += self.yvel

	def set_task(self,new_task):
		self.task = new_task

	def random_walk(self):
		self.destination = random.random(),random.random()
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
	
			
	def slow_towards_destination(self):
		pass				

	def one_tick(self):
		if self.task == None:
			#no task, set task
			#default: random walk
			self.random_walk()
		elif self.task == 'move':
			if self.destination == None:
				self.task = None
				break
			
			distance_to_destination = distance(self.x,destination[0],self.y,destination[1])
			#check if we are almost at the destination or closer than our current speed			
			if distance_to_destination >= self.get_speed():
				#increase speed towards target
				self.accel_towards_destination()
			else:
				#start slowing to a stop
				self.task = 'stop'
				self.slow_towards_destination()

		elif self.task == 'stop':
			if self.get_speed() == 0:
				self.task = None
				self.destination = None
			else:
				#still slowing down
		elif self.task == 'wait':
			pass
			#durp sleep or something


class TestFunctions(unittest.TestCase):
	def test_position(self):
			rand_pos = random.random(), random.random()
			z = Cell(rand_pos[0], rand_pos[1])
			assert z.x ==rand_pos[0]
			assert z.y==rand_pos[1]


	def test_distance_func(self):
		"""Just to test the distance function."""
		assert 5 == distance(0,3,0,4)
		assert 5 == distance(3,0,4,0)
		assert 5 == distance(6,9,8,4)
		assert 5 == distance(-3,-6,-4,-8)
if __name__ == '__main__':
    unittest.main()





