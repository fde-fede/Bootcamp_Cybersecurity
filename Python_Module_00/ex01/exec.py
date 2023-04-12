import sys

final_string = ' '.join(sys.argv[1:])

print(''.join(reversed(final_string.swapcase())))
