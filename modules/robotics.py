from typing import List, Tuple, Optional
import random
import heapq
import numpy as np
import matplotlib.pyplot as plt

Coord = Tuple[int, int]


def generate_grid(rows: int, cols: int, obstacle_prob: float = 0.2, seed: int = 42) -> np.ndarray:
    rng = random.Random(seed)
    grid = np.zeros((rows, cols), dtype=np.uint8)
    for r in range(rows):
        for c in range(cols):
            if rng.random() < obstacle_prob:
                grid[r, c] = 1  # obstacle
    return grid


def neighbors(pos: Coord, grid: np.ndarray) -> List[Coord]:
    r, c = pos
    steps = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    result = []
    for dr, dc in steps:
        nr, nc = r + dr, c + dc
        if 0 <= nr < grid.shape[0] and 0 <= nc < grid.shape[1] and grid[nr, nc] == 0:
            result.append((nr, nc))
    return result


def heuristic(a: Coord, b: Coord) -> float:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def a_star(grid: np.ndarray, start: Coord, goal: Coord) -> Optional[List[Coord]]:
    if grid[start] == 1 or grid[goal] == 1:
        return None
    open_set = []
    heapq.heappush(open_set, (0 + heuristic(start, goal), 0, start))
    came_from = {start: None}
    g_score = {start: 0}
    while open_set:
        _, cost, current = heapq.heappop(open_set)
        if current == goal:
            path = []
            while current is not None:
                path.append(current)
                current = came_from[current]
            path.reverse()
            return path
        for nb in neighbors(current, grid):
            tentative = g_score[current] + 1
            if tentative < g_score.get(nb, float("inf")):
                g_score[nb] = tentative
                came_from[nb] = current
                f = tentative + heuristic(nb, goal)
                heapq.heappush(open_set, (f, tentative, nb))
    return None


def visualize_grid_path(grid: np.ndarray, path: Optional[List[Coord]], start: Coord, goal: Coord):
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.imshow(grid, cmap="gray_r")
    ax.scatter([start[1]], [start[0]], c="green", s=80, label="Start")
    ax.scatter([goal[1]], [goal[0]], c="blue", s=80, label="Goal")
    if path:
        ys = [p[0] for p in path]
        xs = [p[1] for p in path]
        ax.plot(xs, ys, c="red", linewidth=2, label="Path")
    ax.set_xticks([])
    ax.set_yticks([])
    ax.legend(loc="upper right")
    fig.tight_layout()
    return fig
