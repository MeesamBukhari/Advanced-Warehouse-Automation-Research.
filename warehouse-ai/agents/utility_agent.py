from environment.warehouse_grid import Position, Warehouse
from algorithms.astar import a_star_search

class UtilityBasedAgent:
    """An agent that chooses the goal with the highest utility (lowest path cost)."""
    def __init__(self, pos: Position):
        self.pos = pos
        self.planned_path = []

    def get_action(self, warehouse: Warehouse):
        if not self.planned_path and warehouse.items:
            # Find closest item
            best_goal = None
            shortest_path = None
            
            for item in warehouse.items:
                path, _ = a_star_search(warehouse, self.pos, item)
                if path and (shortest_path is None or len(path) < len(shortest_path)):
                    shortest_path = path
                    best_goal = item
            
            if shortest_path:
                self.planned_path = shortest_path
                self.planned_path.pop(0) # Current pos
        
        if self.planned_path:
            return self.planned_path.pop(0)
        return self.pos
