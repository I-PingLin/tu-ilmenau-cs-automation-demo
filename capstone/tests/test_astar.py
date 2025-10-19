from cs_capstone.robotics.grid_world import GridWorld
from cs_capstone.robotics.astar import astar


def test_astar_finds_shortest_path():
    grid = GridWorld(5, 5, {(x, 2) for x in range(5) if x != 2}, (0, 0), (4, 4))
    path = astar(grid)
    assert path[0] == (0, 0)
    assert path[-1] == (4, 4)
    # Manhattan distance with a single vertical barrier having a gap -> still 8 steps
    assert len(path) - 1 == 8
