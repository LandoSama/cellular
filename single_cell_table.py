def check_cell(n,filename):
	"""Used for pulling an individual cell's actions."""
	werd = "Single_Cell_"+str(n)+" "+filename
	f0 = open(filename,"r")
	f1 = f0.read()
	f0.close()
	f1 = f1.split("\n")
	fN = open(werd,"w")
	fN.write("\nt\tx_pos	y_pos	x_vel	y_vel	x_dest	y_dest	radius	energy	task\n")
	counter = 0
	ln = len(str(n))+5
	for line in f1:
		if line.startswith("Cell_"+str(n)+"\t"):
			fN.write(str(counter)+line[ln:]+"\n")
			counter +=1
	fN.close()

def main():
	filename = raw_input("For which document (include .txt)? ")
	while True:
		cell = input("Which cell would you like to make a table of? ")
        	check_cell(cell,filename)
main()
