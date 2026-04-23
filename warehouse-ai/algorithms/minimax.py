from environment.warehouse_grid import Warehouse, Position
import math

def heuristic(pos: Position, goal: Position):
    return abs(pos.x - goal.x) + abs(pos.y - goal.y)

def get_moves(warehouse: Warehouse, pos: Position):
    moves = []
    for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        nx, ny = pos.x + dx, pos.y + dy
        if warehouse.is_walkable(nx, ny):
            moves.append(Position(nx, ny))
    return moves

def minimax(warehouse: Warehouse, pos: Position, goal: Position, depth: int, alpha: float, beta: float, is_maximizing: bool):
    """
    Minimax with Alpha-Beta Pruning for Grid Navigation.
    Maximizer: Agent (trying to reach goal)
    Minimizer: Adversary (trying to block or distance agent)
    """
    if depth == 0 or pos == goal:
        return -heuristic(pos, goal), pos # Negative because agent wants to minimize distance

    if is_maximizing:
        max_eval = -math.inf
        best_move = pos
        for move in get_moves(warehouse, pos):
            eval, _ = minimax(warehouse, move, goal, depth - 1, alpha, beta, False)
            if eval > max_eval:
                max_eval = eval
                best_move = move
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval, best_move
    else:
        min_eval = math.inf
        best_move = pos
        # In this grid version, the 'adversary' doesn't move the agent, 
        # but we simulate the agent's turn as the minimizer's impact for parity.
        # Alternatively, a real adversary would be another robot.
        for move in get_moves(warehouse, pos):
            eval, _ = minimax(warehouse, move, goal, depth - 1, alpha, beta, True)
            if eval < min_eval:
                min_eval = eval
                best_move = move
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval, best_move

def get_best_move_adversarial(warehouse: Warehouse, start: Position, goal: Position, depth: int = 3):
    _, move = minimax(warehouse, start, goal, depth, -math.inf, math.inf, True)
    return move
