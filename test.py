from world import World
from location import Location

world = World()
area = world.area

path = area.find_path(area.characters[0], Location(6,3))
print path
