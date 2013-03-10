import environment
import food
import test
import cells
import copy

def main():
	starting_food_count = input('Enter starting amount of food: ')
	starting_cell_count = input('Enter starting amount of cells: ')
	World = environment.Environment(starting_food_count,starting_cell_count)
	old_food_list_length = len(World.food_set)
	
	number_of_test_ticks = input('Enter number of test ticks: ')
	for i in range(number_of_test_ticks):
		print 'food: ',len(World.food_set),'\t\tTick: ',i
		World.tick()
		World.print_table("Main_Test.txt","Tick: "+str(i))	
main()
