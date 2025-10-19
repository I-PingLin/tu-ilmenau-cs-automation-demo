import heapq
from typing import Dict, Tuple, List, Optional

from .grid_world import GridWorld, Coord


def heuristic(a: Coord, b: Coord) -> float:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def astar(grid: GridWorld, start: Optional[Coord] = None, goal: Optional[Coord] = None) -> List[Coord]:
    if start is None:
        start = grid.start
    if goal is None:
        goal = grid.goal

    frontier: List[Tuple[float, Coord]] = []
    heapq.heappush(frontier, (0.0, start))

    came_from: Dict[Coord, Optional[Coord]] = {start: None}
    cost_so_far: Dict[Coord, float] = {start: 0.0}

    while frontier:
        _, current = heapq.heappop(frontier)
        if current == goal:
            break

        for nxt in grid.neighbors(current):
            new_cost = cost_so_far[current] + grid.cost(current, nxt)
            if nxt not in cost_so_far or new_cost < cost_so_far[nxt]:
                cost_so_far[nxt] = new_cost
                priority = new_cost + heuristic(nxt, goal)
                heapq.heappush(frontier, (priority, nxt))
                came_from[nxt] = current

    if goal not in came_from:
        return []

    path: List[Coord] = []
    cur: Optional[Coord] = goal
    while cur is not None:
        path.append(cur)
        cur = came_from[cur]
    path.reverse()
    return path
