import sys
import string

if len(sys.argv) < 3:
    print("ERROR")
elif len(sys.argv) > 3:
    print("ERROR")
else:
	try:
		size = int(sys.argv[2])
	except ValueError:
		print("ERROR")
		exit()
    
	t = sys.argv[1].translate(str.maketrans('', '', string.punctuation))
	t = t.split(' ')
	i = 0
	while i < len(t):
		if len(t[i]) <= size:
			t.pop(i)
		else:
			i += 1
	print(t)