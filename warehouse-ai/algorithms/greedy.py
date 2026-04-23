import heapq
from environment.warehouse_grid import Warehouse, Position

def greedy_best_first_search(warehouse: Warehouse, start: Position, goal: Position):
    heuristic = lambda p: abs(p.x - goal.x) + abs(p.y - goal.y)
    open_list = [(heuristic(start), start, [start])]
    visited = {start}
    explored = []

    while open_list:
        h, curr, path = heapq.heappop(open_list)
        explored.append(curr)

        if curr == goal:
            return path, explored

        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nx, ny = curr.x + dx, curr.y + dy
            pos = Position(nx, ny)
            if warehouse.is_walkable(nx, ny) and pos not in visited:
                visited.add(pos)
                heapq.heappush(open_list, (heuristic(pos), pos, path + [pos]))
                
    return [], explored
