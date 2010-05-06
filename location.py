from common import *

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
