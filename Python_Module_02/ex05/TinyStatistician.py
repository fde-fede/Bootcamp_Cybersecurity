import math

class TinyStatistician:
    def mean(self, x):
        if len(x) == 0 or isinstance(x, str):
            return None
        for i in x:
            if not isinstance(i, int) and not isinstance(i, float):
                return None
        else:
            return sum(x) / len(x)

    def median(self, x):
        if len(x) == 0 or isinstance(x, str):
            return None
        for i in x:
            if not isinstance(i, int) and not isinstance(i, float):
                return None
        else:
            x.sort()
            if len(x) % 2 == 0:
                return ((x[(len(x) // 2) - 1]) + (x[len(x) // 2])) / 2
            else:
                return x[int(len(x)) // 2]

    def quartiles(self, x):
        if len(x) == 0 or isinstance(x, str):
            return None
        for i in x:
            if not isinstance(i, int) and not isinstance(i, float):
                return None
        else:
            x.sort()
            q1 = x[len(x) // 4 ]
            q3 = x[len(x) // 4 * 3 ]
            return q1, q3

    def var(self, x):
        if len(x) == 0 or isinstance(x, str):
            return None
        for i in x:
            if not isinstance(i, int) and not isinstance(i, float):
                return None
        else:
            mean = self.mean(x)
            a = 0
            for i in x:
                a += (i - mean) ** 2
            return a / len(x)
    
    def std(self, x):
        if len(x) == 0 or isinstance(x, str):
            return None
        for i in x:
            if not isinstance(i, int) and not isinstance(i, float):
                return None
        else:
            return math.sqrt(self.var(x))