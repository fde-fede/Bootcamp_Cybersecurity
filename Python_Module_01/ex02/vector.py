def is_float_list(lst):
    if not isinstance(lst, list) or len(lst) == 0:
        print("The vector values are not a list type")
        return False
    for item in lst:
        if not isinstance(item, int) and not isinstance(item, float):
            return False
    return True

def is_list_list(lst):
    if not isinstance(lst, list) or len(lst) == 0:
        print("The list values are not a list type")
        return False
    for item in lst:
        if not is_float_list(item):
            print("The list values are not a list type")
            return False
    return True

def is_rectangular(lst):
    if not is_list_list(lst):
        return False
    size = len(lst[0])
    for elem in lst:
        if len(elem) != size:
            return False
    return True

def is_range(tpl):
    if not isinstance(tpl, tuple) or len(tpl) != 2:
        return False
    if not isinstance(tpl[0], int) and isinstance(tpl[1], int) and tpl[0] < tpl[1]:
        return True
    return False

class Vector:
    def __init__(self, values):
        self.values = []
        if isinstance(values, list):
            if is_float_list(values):
                self.shape = (1, len(values))
                self.values.append(values.copy())
            elif is_list_list(values) and is_rectangular(values):
                self.shape = (len(values), len(values[0]))
                for elem in values:
                    self.values.append(elem.copy())
            else:
                raise ValueError("Invalid list for Vector")
        elif isinstance(values, int):
            self.shape = (values, 1)
            for i in range(values):
                self.values.append([float(i)])
        elif is_range(values):
            self.shape = (values[1] - values[0], 1)
            for i in range(values[0], values[1]):
                self.values.append([float(i)])
        else:
            raise ValueError("Invalid values for Vector")

    def __add__(self, other):
        new = Vector(self.values)
        if isinstance(other, Vector) and self.shape == other.shape:
            for i in range(self.shape[0]):
                for j in range(self.shape[1]):
                    new.values[i][j] += self.values[i][j]
        else:
            raise ValueError("Type is not Vector or shape is not the same")
        return new
    
    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        new = Vector(self.values)
        if isinstance(other, Vector) and self.shape == other.shape:
            for i in range(self.shape[0]):
                for j in range(self.shape[1]):
                    new.values[i][j] -= self.values[i][j]
        else:
            raise ValueError("Type is not Vector or shape is not the same")
        return new
    
    def __rsub__(self, other):
        return self.__sub__(other)

    def __mul__(self, scale):
        new = Vector(self.values)
        if isinstance(scale, int) or isinstance(scale, float):
            for i in range(self.shape[0]):
                for j in range(self.shape[1]):
                    new.values[i][j] *= scale
        else:
            raise ValueError("Type is not Vector or shape is not the same")
        return new
    
    def __rmul__(self, scale):
        return self.__mul__(scale)

    def __truediv__(self, scale):
        new = Vector(self.values)
        if isinstance(scale, int) or isinstance(scale, float):
            for i in range(self.shape[0]):
                for j in range(self.shape[1]):
                    new.values[i][j] /= scale
        else:
            raise ValueError("Type is not Vector or shape is not the same")
        return new
    
    def __rtruediv__(self, scale):
        return self.__truediv__(scale)
    
    def __str__(self):
        for item in self:
            s = s + item
        return s
    
    def __repr__(self):
        for item in self:
            print(item)
    
    def dot(self, oper):
        if self.shape[1] != oper.shape[0]:
            raise ValueError("Dot product is not possible")
        product = [[0] * oper.shape[1] for i in range(self.shape[0])]
        print(product)
        for i in range(self.shape[0]):
            for j in range(oper.shape[1]):
                for k in range(self.shape[1]):
                    product[i][j] += self.values[i][k] * oper.values[k][j]
        return Vector(product)


    def T(self):
        values = [[0] * self.shape[0] for i in range(self.shape[1])]
        for i in range(self.shape[0]):
            for j in range(self.shape[1]):
                values[j][i] = self.values[i][j]
        return Vector(values)
