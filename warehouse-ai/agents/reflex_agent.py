from environment.warehouse_grid import Position, Warehouse

class ReflexAgent:
    """A Simple Reflex Agent that moves towards the target based on coordinate comparison."""
    def __init__(self, pos: Position):
        self.pos = pos

    def get_action(self, warehouse: Warehouse, goal: Position):
        # Move on X then Y or vice versa solely based on current percept
        if self.pos.x < goal.x and warehouse.is_walkable(self.pos.x + 1, self.pos.y):
            return Position(self.pos.x + 1, self.pos.y)
        elif self.pos.x > goal.x and warehouse.is_walkable(self.pos.x - 1, self.pos.y):
            return Position(self.pos.x - 1, self.pos.y)
        elif self.pos.y < goal.y and warehouse.is_walkable(self.pos.x, self.pos.y + 1):
            return Position(self.pos.x, self.pos.y + 1)
        elif self.pos.y > goal.y and warehouse.is_walkable(self.pos.x, self.pos.y - 1):
            return Position(self.pos.x, self.pos.y - 1)
        return self.pos
