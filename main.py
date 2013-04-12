import environment
import food
import test
import cells
import copy
import sys
import display



def main():
	if len(sys.argv) == 2 and sys.argv[1] == '-':
		starting_food_count = 100
		starting_cell_count = 100
	elif len(sys.argv) == 4:
		starting_food_count  = int(sys.argv[1])
		starting_cell_count  = int(sys.argv[2])
	else:
		starting_food_count = input('Enter starting amount of food: ')
		starting_cell_count = input('Enter starting amount of cells: ')
	World = environment.Environment(starting_food_count,starting_cell_count)
	
	# dis is a thread
	dis = display.display(World)

	# dis is a tick counter
	i = 0
	while True:
		i += 1
		# if the user exited pygame, close the rest of the program
		if dis.isAlive() ==False:
			sys.exit()
		print 'Tick:',i,'\t\tfood: ',len(World.food_set),'\t\tcells: ',len(World.cell_list)

		World.tick()
		World.print_table("Main_Test.txt","Tick: "+str(i))

	# if the main loop is over, close the graphics thread
	dis._Thread__stop()
		
main()
