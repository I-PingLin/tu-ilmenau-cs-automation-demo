from dataclasses import dataclass
from typing import Set, Tuple, List
import numpy as np


Coord = Tuple[int, int]


@dataclass
class GridWorld:
    width: int
    height: int
    obstacles: Set[Coord]
    start: Coord
    goal: Coord

    def in_bounds(self, p: Coord) -> bool:
        x, y = p
        return 0 <= x < self.width and 0 <= y < self.height

    def passable(self, p: Coord) -> bool:
        return p not in self.obstacles

    def neighbors(self, p: Coord) -> List[Coord]:
        x, y = p
        candidates = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
        return [c for c in candidates if self.in_bounds(c) and self.passable(c)]

    def cost(self, a: Coord, b: Coord) -> float:
        return 1.0

    def to_numpy(self) -> np.ndarray:
        grid = np.zeros((self.height, self.width), dtype=np.uint8)
        for (x, y) in self.obstacles:
            grid[y, x] = 1
        return grid
