class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y


    def __add__(self, other):
        return(self.x + other.x, self.y + other.y)

a = Vector(5, 3)
b = Vector(-4, 1)

print(a + b)
