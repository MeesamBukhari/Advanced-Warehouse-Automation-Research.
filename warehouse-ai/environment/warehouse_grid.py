import enum
from dataclasses import dataclass
from typing import List, Tuple, Optional, Set

class CellType(enum.Enum):
    EMPTY = 0
    SHELF = 1
    OBSTACLE = 2
    ROBOT = 3
    ITEM = 4
    PATH = 5
    EXPLORED = 6

@dataclass
class Position:
    x: int
    y: int

    def to_tuple(self) -> Tuple[int, int]:
        return (self.x, self.y)

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        if not isinstance(other, Position):
            return False
        return self.x == other.x and self.y == other.y

class Warehouse:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.grid = [[CellType.EMPTY for _ in range(width)] for _ in range(height)]
        self.robot_pos: Optional[Position] = None
        self.items: List[Position] = []

    def set_cell(self, x: int, y: int, cell_type: CellType):
        if 0 <= x < self.width and 0 <= y < self.height:
            if cell_type == CellType.ROBOT:
                if self.robot_pos:
                    self.grid[self.robot_pos.y][self.robot_pos.x] = CellType.EMPTY
                self.robot_pos = Position(x, y)
            elif cell_type == CellType.ITEM:
                self.items.append(Position(x, y))
            
            self.grid[y][x] = cell_type

    def get_cell(self, x: int, y: int) -> CellType:
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.grid[y][x]
        return CellType.OBSTACLE

    def is_walkable(self, x: int, y: int) -> bool:
        cell = self.get_cell(x, y)
        return cell in [CellType.EMPTY, CellType.ITEM, CellType.PATH, CellType.EXPLORED]

    def reset_grid_effects(self):
        for y in range(self.height):
            for x in range(self.width):
                if self.grid[y][x] in [CellType.PATH, CellType.EXPLORED]:
                    self.grid[y][x] = CellType.EMPTY
