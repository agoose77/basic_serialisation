class Vector:

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        return "Vector(x={}, y={}, z={})".format(self.x, self.y, self.z)