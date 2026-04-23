from environment.warehouse_grid import Position, Warehouse

class ModelBasedAgent:
    """An agent that maintains an internal state (visited cells) to avoid loops."""
    def __init__(self, pos: Position):
        self.pos = pos
        self.visited = {pos}

    def get_action(self, warehouse: Warehouse, goal: Position):
        possible_moves = []
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nx, ny = self.pos.x + dx, self.pos.y + dy
            if warehouse.is_walkable(nx, ny):
                possible_moves.append(Position(nx, ny))
        
        # Prefer unvisited cells closer to goal
        unvisited = [m for m in possible_moves if m not in self.visited]
        if not unvisited:
            # If all are visited, just move towards goal
            unvisited = possible_moves
            
        if not unvisited: return self.pos
        
        best_move = min(unvisited, key=lambda m: abs(m.x - goal.x) + abs(m.y - goal.y))
        self.visited.add(best_move)
        return best_move
