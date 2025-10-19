from cs_capstone.robotics.grid_world import GridWorld
from cs_capstone.robotics.astar import astar
from cs_capstone.ml.q_learning import GridWorldEnv, QLearningAgent


def test_q_learning_learns_reasonable_policy():
    grid = GridWorld(5, 5, {(x, 2) for x in range(5) if x != 2}, (0, 0), (4, 4))
    env = GridWorldEnv(grid, max_steps=200, seed=123)
    agent = QLearningAgent(env, alpha=0.5, gamma=0.95, epsilon=0.1, seed=123)
    agent.train(episodes=800, max_steps_per_episode=200)

    astar_path = astar(grid)
    optimal_len = len(astar_path) - 1

    env.reset()
    path = agent.derive_greedy_path(start=grid.start, max_steps=100)

    assert path[-1] == grid.goal
    # Allow some slack over optimal
    assert (len(path) - 1) <= (optimal_len + 4)
