import pygame, sys, threading
from pygame.locals import *
Thread = threading.Thread

pygame.init()
fpsClock = pygame.time.Clock()
display_width = 1000
display_height = 700
windowSurfaceObj = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Nautical Cell Force 2')

redColor = pygame.Color(255,0,0)
greenColor = pygame.Color(0,255,0)
blueColor = pygame.Color(0,0,255)
whiteColor = pygame.Color(255,255,255)
mousex, mousey = 0,0

def convert_to_display_loc((x,y)):
    x = int(round((x*display_width)))
    y = int(round((y*display_height)))
    return (x,y)

# main display loop
class Display(Thread):
    def __init__(self,environment):
        Thread.__init__(self)
        self.environment = environment
    def run(self):
        while True:
            windowSurfaceObj.fill(whiteColor)
            for cell in self.environment.cell_list:
                # is the 20 width and the height?
                pygame.draw.circle(windowSurfaceObj, redColor, convert_to_display_loc((cell.x, cell.y)), 20, 0)
            for food in self.environment.food_set:
                pygame.draw.circle(windowSurfaceObj, greenColor, convert_to_display_loc((food.x, food.y)), 10, 10)
        
            for event in pygame.event.get():
                if event.type ==QUIT:
                    pygame.quit()
    
            pygame.display.update()
            fpsClock.tick(30)

def display(environment):
    dis = Display(environment)
    dis.start()
    
