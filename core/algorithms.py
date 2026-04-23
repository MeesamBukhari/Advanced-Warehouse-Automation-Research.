import heapq
from typing import List, Tuple, Dict, Optional, Callable
from .warehouse import Warehouse, Position, CellType

class Node:
    def __init__(self, pos: Position, parent: Optional['Node'] = None, g: float = 0, h: float = 0):
        self.pos = pos
        self.parent = parent
        self.g = g  # Cost from start to this node
        self.h = h  # Estimated cost from this node to goal
        self.f = g + h

    def __lt__(self, other):
        return self.f < other.f

def get_neighbors(warehouse: Warehouse, pos: Position) -> List[Position]:
    neighbors = []
    # 4-way movement (up, down, left, right)
    for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        nx, ny = pos.x + dx, pos.y + dy
        if warehouse.is_walkable(nx, ny):
            neighbors.append(Position(nx, ny))
    return neighbors

def reconstruct_path(node: Node) -> List[Position]:
    path = []
    curr = node
    while curr:
        path.append(curr.pos)
        curr = curr.parent
    return path[::-1]

def bfs(warehouse: Warehouse, start: Position, goal: Position) -> Tuple[List[Position], List[Position]]:
    """Returns (path, explored_nodes)"""
    queue = [Node(start)]
    visited = {start}
    explored = []

    while queue:
        curr = queue.pop(0)
        explored.append(curr.pos)

        if curr.pos == goal:
            return reconstruct_path(curr), explored

        for neighbor in get_neighbors(warehouse, curr.pos):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(Node(neighbor, curr))
    
    return [], explored

def ucs(warehouse: Warehouse, start: Position, goal: Position) -> Tuple[List[Position], List[Position]]:
    """Uniform Cost Search (Dijkstra's with uniform weights)"""
    return a_star(warehouse, start, goal, lambda p1, p2: 0)

def a_star(warehouse: Warehouse, start: Position, goal: Position, heuristic: Optional[Callable[[Position, Position], float]] = None) -> Tuple[List[Position], List[Position]]:
    if heuristic is None:
        # Manhattan Distance
        heuristic = lambda p1, p2: abs(p1.x - p2.x) + abs(p1.y - p2.y)

    open_list = []
    heapq.heappush(open_list, Node(start, g=0, h=heuristic(start, goal)))
    closed_set = {} # pos -> g_score
    explored = []

    while open_list:
        curr = heapq.heappop(open_list)
        
        if curr.pos in closed_set and closed_set[curr.pos] <= curr.g:
            continue
            
        closed_set[curr.pos] = curr.g
        explored.append(curr.pos)

        if curr.pos == goal:
            return reconstruct_path(curr), explored

        for neighbor in get_neighbors(warehouse, curr.pos):
            g_score = curr.g + 1 # Uniform cost
            if neighbor not in closed_set or g_score < closed_set[neighbor]:
                h_score = heuristic(neighbor, goal)
                heapq.heappush(open_list, Node(neighbor, curr, g=g_score, h=h_score))
                
    return [], explored
