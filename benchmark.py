import environment
import food
import test
import cells
import copy
from time import time

def main():
	starting_food_count = 100#input('Enter starting amount of food: ')
	starting_cell_count = 100#input('Enter starting amount of cells: ')
	environment.e = World = environment.Environment(starting_food_count,starting_cell_count)
	old_food_list_length = len(World.food_set)
	
	number_of_test_ticks = 10000#input('Enter number of test ticks: ')
	t1 = time()
	sum_runs = 0
	count_runs = 0
	max_run = 0
	for i in range(number_of_test_ticks):
		World.tick()
		t2 = time()
		this_run = 1/(t2-t1)
		sum_runs += this_run
		count_runs += 1
		#if this_run > max_run: max_run = this_run
		print 'food: ',len(World.food_set),'\t\tTick: ',i, this_run, ', avg:', sum_runs/count_runs
		t1 = time()
	
	
main()
