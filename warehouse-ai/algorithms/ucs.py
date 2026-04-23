import heapq
from typing import List, Tuple, Optional
from environment.warehouse_grid import Warehouse, Position

class Node:
    def __init__(self, pos: Position, parent: Optional['Node'] = None, g=0):
        self.pos = pos
        self.parent = parent
        self.g = g

    def __lt__(self, other):
        return self.g < other.g

def ucs_search(warehouse: Warehouse, start: Position, goal: Position):
    open_list = [Node(start, g=0)]
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

        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nx, ny = curr.pos.x + dx, curr.pos.y + dy
            if warehouse.is_walkable(nx, ny):
                n = Position(nx, ny)
                g = curr.g + 1
                if n not in closed_set or g < closed_set[n]:
                    heapq.heappush(open_list, Node(n, curr, g))
    return [], explored
