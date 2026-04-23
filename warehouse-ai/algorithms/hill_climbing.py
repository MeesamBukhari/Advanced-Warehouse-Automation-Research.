from typing import List, Tuple, Optional
from environment.warehouse_grid import Warehouse, Position

def hill_climbing_search(warehouse: Warehouse, start: Position, goal: Position):
    heuristic = lambda p: abs(p.x - goal.x) + abs(p.y - goal.y)
    curr = start
    path = [curr]
    explored = [curr]

    while curr != goal:
        neighbors = []
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nx, ny = curr.x + dx, curr.y + dy
            if warehouse.is_walkable(nx, ny):
                neighbors.append(Position(nx, ny))
        
        if not neighbors: break
        
        # Select best neighbor
        best_neighbor = min(neighbors, key=lambda n: heuristic(n))
        
        if heuristic(best_neighbor) >= heuristic(curr):
            # Local optimum reached or plateau
            break
            
        curr = best_neighbor
        path.append(curr)
        explored.append(curr)
        
    return path, explored
