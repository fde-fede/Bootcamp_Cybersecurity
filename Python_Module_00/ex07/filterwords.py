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
    s = [item for item in t if len(item) > size]
    print(s)