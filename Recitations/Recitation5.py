class person(object):
    def __init__(self, name, age, height, weight):
        self.name = name
        self.age = age
        self.height = height
        self.weight = weight

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_age(self):
        return self.age

    def set_age(self, age):
        self.age = age

    def get_height(self):
        return self.height

    def set_height(self, height):
        self.height = height

    def get_weight(self):
        return self.weight

    def set_weight(self, weight):
        self.weight = weight

    def __eq__(self, other):
        return self.name == other.name
############################################

class Shape(object):
    def area(self):
        raise NotImplementedError

    def Perimeter(self):
        return NotImplementedError

    def __eq__(self, other):
        return self.area() == other.area()

    def __lt__(self, other):
        return self.area() < other.area()

class Rectangle(Shape):
    def __init__(self, side1, side2):
        self.side1 = side1
        self.side2 = side2

    def area(self):
        return self.side1 * self.side2

    def Perimeter(self):
        return (self.side1+ self.side2) * 2

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return 3.1419 * radius ** 2

    def Perimeter(self):
        return 2 * 3.1419 * radius

class Square(Rectangle):
    def __init__(self, side):
        Rectangle.__init__(self, side, side)

    
