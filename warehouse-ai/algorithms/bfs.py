from typing import List, Tuple, Optional
from environment.warehouse_grid import Warehouse, Position

def bfs_search(warehouse: Warehouse, start: Position, goal: Position):
    queue = [(start, [start])]
    visited = {start}
    explored = []

    while queue:
        curr, path = queue.pop(0)
        explored.append(curr)

        if curr == goal:
            return path, explored

        for n in [(curr.x, curr.y+1), (curr.x, curr.y-1), (curr.x+1, curr.y), (curr.x-1, curr.y)]:
            pos = Position(n[0], n[1])
            if warehouse.is_walkable(pos.x, pos.y) and pos not in visited:
                visited.add(pos)
                queue.append((pos, path + [pos]))
    return [], explored
