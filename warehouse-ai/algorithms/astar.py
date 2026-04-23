import heapq
from typing import List, Tuple, Optional
from environment.warehouse_grid import Warehouse, Position

class Node:
    def __init__(self, pos: Position, parent: Optional['Node'] = None, g=0, h=0):
        self.pos = pos
        self.parent = parent
        self.g = g
        self.h = h
        self.f = g + h

    def __lt__(self, other):
        return self.f < other.f

def get_neighbors(warehouse: Warehouse, pos: Position):
    neighbors = []
    for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        nx, ny = pos.x + dx, pos.y + dy
        if warehouse.is_walkable(nx, ny):
            neighbors.append(Position(nx, ny))
    return neighbors

def a_star_search(warehouse: Warehouse, start: Position, goal: Position):
    heuristic = lambda p1, p2: abs(p1.x - p2.x) + abs(p1.y - p2.y)
    open_list = [Node(start, g=0, h=heuristic(start, goal))]
    closed_set = {}
    explored = []

    while open_list:
        curr = heapq.heappop(open_list)
        if curr.pos in closed_set and closed_set[curr.pos] <= curr.g: continue
        closed_set[curr.pos] = curr.g
        explored.append(curr.pos)

        if curr.pos == goal:
            path = []
            while curr:
                path.append(curr.pos)
                curr = curr.parent
            return path[::-1], explored

        for n in get_neighbors(warehouse, curr.pos):
            g = curr.g + 1
            if n not in closed_set or g < closed_set[n]:
                heapq.heappush(open_list, Node(n, curr, g, heuristic(n, goal)))
    return [], explored
