from common import *

class Direction:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

    def __repr__(self):
        return "<Direction: %s>" % self.name

    def opposite(self):
        if self == NORTH:
            return SOUTH
        elif self == NORTH_EAST:
            return SOUTH_WEST
        elif self == SOUTH_EAST:
            return NORTH_WEST
        elif self == SOUTH:
            return NORTH
        elif self == SOUTH_WEST:
            return NORTH_EAST
        elif self == NORTH_WEST:
            return SOUTH_EAST

NORTH = Direction("n")
SOUTH = Direction("s")
SOUTH_EAST = Direction("se")
SOUTH_WEST = Direction("sw")
NORTH_EAST = Direction("ne")
NORTH_WEST = Direction("nw")

class Location:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return "(%d, %d)" % (self.x, self.y)

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __hash__(self):
        return (self.x << 16) + self.y
        
    def get_adjacent_tiles(self):
        return [
            Location(self.x, self.y - 1),
            Location(self.x + 1, self.y - is_even(self.x)), 
            Location(self.x + 1, self.y + is_odd(self.x)),
            Location(self.x, self.y + 1),
            Location(self.x - 1, self.y + is_odd(self.x)),
            Location(self.x - 1, self.y - is_even(self.x))
        ]

    def distance_to(self, loc):
        a = self
        b = loc
        hdistance = abs(a.x - b.x)
        if (is_even(a.x) and is_odd(b.x) and (a.y < b.y)) or \
                (is_even(b.x) and is_odd(a.x) and (b.y < a.y)):
            vpenalty = 1
        else:
            vpenalty = 0
        return max(hdistance, abs(a.y - b.y) + vpenalty + hdistance/2);

    def relative_dir(self, loc):
        diff = self.diff(loc)
        if diff == Location(0,0):
            return None
        if diff.y < 0 and diff.x >= 0 and abs(diff.x) >= abs(diff.y):
            return NORTH_EAST
        if diff.y < 0 and diff.x < 0 and abs(diff.x) >= abs(diff.y):
            return NORTH_WEST
        if diff.y < 0 and abs(diff.x) < abs(diff.y):
            return NORTH
        if diff.y >= 0 and diff.x >= 0 and abs(diff.x) >= abs(diff.y):
            return SOUTH_EAST
        if diff.y >= 0 and diff.x < 0 and abs(diff.x) >= abs(diff.y):
            return SOUTH_WEST
        if diff.y >= 0 and abs(diff.x) < abs(diff.y):
            return SOUTH

        #impossible
        return None

    def diff(self, other):
        return self.sum(other.neg())

    def neg(self):
        n = Location(-self.x, -self.y - is_odd(self.x))
        return n
        
    def sum(self, other):
        a = Location(self.x, self.y)
        b = other
        if is_odd(a.x) and is_odd(b.x):
            a.y = a.y + 1
        a.x = a.x + b.x
        a.y = a.y + b.y

        return a
