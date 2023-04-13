import sys

if len(sys.argv) > 1:
    final_string = ' '.join(sys.argv[1:])
    print(''.join(reversed(final_string.swapcase())))
else:
    exit()