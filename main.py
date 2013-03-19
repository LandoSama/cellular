import environment
import food
import test
import cells
import copy
import sys

def main():
	if len(sys.argv) == 2 and sys.argv[1] == '-':
		starting_food_count = 100
		starting_cell_count = 100
		number_of_test_ticks = 1000
	elif len(sys.argv) == 4:
		starting_food_count  = int(sys.argv[1])
		starting_cell_count  = int(sys.argv[2])
		number_of_test_ticks = int(sys.argv[3])
	else:
		starting_food_count = input('Enter starting amount of food: ')
		starting_cell_count = input('Enter starting amount of cells: ')
		number_of_test_ticks = input('Enter number of test ticks: ')
	World = environment.Environment(starting_food_count,starting_cell_count)
	
	for i in range(number_of_test_ticks):
		print 'Tick: ',i,'\t\tfood: ',len(World.food_set),'\t\tcells: ',len(World.cell_list)
		World.tick()
		#World.print_table("Main_Test.txt","Tick: "+str(i))
		
main()
