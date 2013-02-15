class Environment:
	cells = []
	width = height = 100
	
	def __init__():
		add_cells()
	
	def add_cells():
		count = raw_input("Number of cells: ")
		count = raw_input("Width of environment: ")
		count = raw_input("Height of environment: ")
		for i = 1 to count:
			cells.push(Cell(random.randint(0, width), random.randint(0, height))
			
	def tick()
		for cell in cells:
			cell.tick()
	
	def debug_output():
		for cell in cells:
			print "(", cell.x, ", ", cell.y, ")"
