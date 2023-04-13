import sys

if len(sys.argv) > 3:
    print("AssertionError: too many arguments")
    exit()
if len(sys.argv) <= 2:
    print("Usage: python operations.py <number1> <number2>")
    exit()
for item in sys.argv[1:]:
    try:
        A = int(sys.argv[1])
        B = int(sys.argv[2])
    except TypeError:
        print("AssertionError: only integers")
        exit()
A = int(sys.argv[1])
B = int(sys.argv[2])
print("Sum:		", (A+B))
print("Difference:	", (A-B))
print("Product:	", (A*B))
if B == 0:
    print("Quotient:	 ERROR (division by zero)")
    print("Remainder:	 ERROR (modulo by zero)")
else:
	print("Quotient:	", (A/B))
	print("Remainder:	", (A%B))