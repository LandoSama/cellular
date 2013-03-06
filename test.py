import unittest, food, environment, cells

#Tests for Environment
EnvironmentCreationTest = environment.CreationTest

#Tests for Cells
CellsCreationTest = cells.TestFunctions

#Tests for Food
FoodTest = food.CreationTest

if __name__ == "__main__":
	environment.Environment(10, 10)
	#environment.Environment(10, 10) #this should fail
	unittest.main()
