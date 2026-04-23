from environment.warehouse_grid import Position, Warehouse
from algorithms.astar import a_star_search

class GoalBasedAgent:
    """An agent that plans a path to the goal using a search algorithm."""
    def __init__(self, pos: Position):
        self.pos = pos
        self.planned_path = []

    def get_action(self, warehouse: Warehouse, goal: Position):
        if not self.planned_path:
            self.planned_path, _ = a_star_search(warehouse, self.pos, goal)
            if self.planned_path:
                self.planned_path.pop(0) # Current pos
        
        if self.planned_path:
            return self.planned_path.pop(0)
        return self.pos
