from vector import Vector

if __name__ == '__main__':
    v3 = Vector([[1, 1], [1, 2]])
    v2 = Vector([[1, 1], [1, 9]])
    print((v3.dot(v2)).values)