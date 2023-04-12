import sys

counter = 0
for item in sys.argv[1:]:
	counter = counter + 1
if counter == 1:
	if sys.argv[1].isnumeric():
		number = int(sys.argv[1]) % 2
		if sys.argv[1] == '0':
			print("I'm Zero")
		elif number == 0:
			print("I'm Even")
		elif number == 1:
			print("I'm Odd")
	else:
		print("AssertionError: argument is not an integer")
elif counter < 1:
	exit()
else:
	print("AssertionError: more than one argument are provided")