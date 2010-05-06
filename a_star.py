import heapq
import copy

class Node:
    def __init__(self, area, unit, loc, cost, hcost=0):
        self.area = area          # area, constant all the time
        self.unit = unit          # unit, constant all the time
        self.loc = loc            # current location
        self.cost = cost          # cost to get to this node
        self.hcost = hcost        # estimated heuristic cost to goal
        self.parent = None        # link to parent node in tree

    def set_parent(self, parent):
        self.parent = parent

    # return a list of child nodes according to the set of legal moves
    def get_children(self):
        children = []
        loc = self.loc
        for l in loc.get_adjacent_tiles():
            if self.area.can_pass(self.unit, l):
                # new node, FIXME: variable cost
                child = Node(self.area, self.unit, l, self.cost+1)
                child.hcost = loc.distance_to(l)
                children.append(child)
        return children


    # return a list of nodes from the start position to the goal position
    def get_path(self, start):
        print self.loc
        current = self
        path = []
        # start at the goal and follow the parent chain to the beginning
        path.append(current.loc)
        while current.loc != start.loc:
            up = current.parent
            path.append(up.loc)
            current = up

        # reverse the list to give the start-to-goal ordering
        path.reverse()
        return path

def find_path(area, unit, loc):
    # priority queue to store nodes
    pq = []
    heapq.heapify(pq)

    #dictionary to store previously visited nodes
    visited = {}

    # put the initial node on the queue
    start = Node(area, unit, unit.location(), 0)
    heapq.heappush(pq, start)

    while (len(pq) > 0):
        node = heapq.heappop(pq)
        if node.loc not in visited:
            if node.loc == loc:
                return node.get_path(start)
            else:
                children = node.get_children()
                for child in children:
                    child.set_parent(node)
                    heapq.heappush(pq, child)
                visited[node.loc] = True
                pq.sort(compare)  # keep less costly nodes at the front
    return None

# comparison function for keeping our priority queue in order
# keep less costly nodes toward the front of the queue (explore first)
def compare(a,b):
    if (a.cost+a.hcost) < (b.cost+b.hcost): return -1
    elif (a.cost+a.hcost) == (b.cost+b.hcost): return 0
    else: return 1
