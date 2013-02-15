import math

class Cell: 
	def __init__(self,x,y)
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
		
	def random_walk(self):
		#randomly pick destination
		#set destination
		#set task to move
		pass
		
	def accel_towards_destination(self):
		pass
	
	def one_tick(self):
		if self.task == None:
			#no task, set task
			#default: random walk
			self.random_walk()
		elif self.task == 'move':
			#check if we have a destination
			#if yes,
				#accel to destination
				#check if we are at the destination or closer than our current speed
					#set task to stop
			#if no,
				#something fucked
		elif self.task == 'stop':
			#slow down to a stop
		elif self.task == 'wait':
			#durp sleep or something
			
			
		
	
		
	
        
     
