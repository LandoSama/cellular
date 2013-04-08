import pygame, sys, threading
from pygame.locals import *
import pygame.gfxdraw
Thread = threading.Thread

pygame.init()
fpsClock = pygame.time.Clock()
display_width = 700
display_height = 700
windowSurfaceObj = pygame.display.set_mode((display_width,display_height))#, pygame.HWSURFACE|pygame.FULLSCREEN|pygame.DOUBLEBUF)
pygame.display.set_caption('Nautical Cell Force 2')

redColor = pygame.Color(255,0,0)
greenColor = pygame.Color(0,255,0)
blueColor = pygame.Color(0,0,255)
whiteColor = pygame.Color(255,255,255)
mousex, mousey = 0,0

COMICSANS = pygame.font.SysFont("Comic Sans MS", 30)

def convert_to_display_loc(pos):
	return int(pos.x*display_width), int(pos.y*display_height)

# main display loop
class Display(Thread):
	def __init__(self,environment):
		Thread.__init__(self)
		self.environment = environment
	def draw(self, circle, radius, color):
		real_x, real_y = convert_to_display_loc(circle.pos)
		x_all = [real_x]
		y_all = [real_y]
		if circle.pos.x < radius:
			x_all.append(display_width + real_x)
		elif circle.pos.x > 1 - radius:
			x_all.append(real_x - display_width)
		if circle.pos.y < radius:
			y_all.append(display_height + real_y)
		elif circle.pos.y > 1 - radius:
			y_all.append(real_y - display_height)
		for x in x_all:
			for y in y_all:
				pygame.gfxdraw.aacircle(windowSurfaceObj, x, y, int(radius*display_width), color)
				pygame.gfxdraw.filled_circle(windowSurfaceObj, x, y, int(radius*display_width), color)
	def run(self):
		assert(display_width == display_height)
		while True:
			windowSurfaceObj.fill(whiteColor)
			# environment's food set is changing while the for loop runs, so we must lock it so that we do not iterate over a changing set
			self.environment.lock.acquire()
			for food in self.environment.food_set:
				windowSurfaceObj.fill(greenColor, (convert_to_display_loc(food.pos), (3,3)))
			for cell in self.environment.cell_list:
				self.draw(cell, cell.radius, redColor)
			self.environment.lock.release()
			
			#windowSurfaceObj.blit(COMICSANS.render("%dfps %d cells" % (fps, len(self.environment.cell_list)), 1, (0,0,0)), (0, 0))
		
			for event in pygame.event.get():
				if event.type == QUIT or event.type == MOUSEBUTTONUP:
					pygame.quit()
					return
					
			pygame.display.flip()
			print 1000/fpsClock.tick(60)

def display(environment):
	dis = Display(environment)
	dis.start()
	# return the thread so that main can check if it is alive
	return dis
