import environment
import food
import test
import cells
import copy
from time import time

def main():
	starting_food_count = 100#input('Enter starting amount of food: ')
	starting_cell_count = 100#input('Enter starting amount of cells: ')
	World = environment.Environment(starting_food_count,starting_cell_count)
	old_food_list_length = len(World.food_set)
	
	number_of_test_ticks = 10000#input('Enter number of test ticks: ')
	t1 = time()
	for i in range(number_of_test_ticks):
		t2 = time()
		print 'food: ',len(World.food_set),'\t\tTick: ',i, 1/(t2-t1)
		World.tick()
		t1 = t2

if __name__ == 'main': main()
