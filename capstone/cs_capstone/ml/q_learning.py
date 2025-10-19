from typing import Tuple, List, Optional
import random
import numpy as np

from ..robotics.grid_world import GridWorld, Coord


class GridWorldEnv:
    def __init__(
        self,
        grid: GridWorld,
        step_penalty: float = -1.0,
        goal_reward: float = 100.0,
        invalid_penalty: float = -5.0,
        max_steps: Optional[int] = None,
        seed: int = 42,
    ) -> None:
        self.grid = grid
        self.step_penalty = step_penalty
        self.goal_reward = goal_reward
        self.invalid_penalty = invalid_penalty
        self.max_steps = max_steps or (grid.width * grid.height * 4)
        self.rng = random.Random(seed)
        self.reset()

    def reset(self) -> Coord:
        self.state: Coord = self.grid.start
        self.steps = 0
        return self.state

    def step(self, action: int) -> Tuple[Coord, float, bool, dict]:
        x, y = self.state
        # up, right, down, left in (dx, dy)
        moves = [(0, -1), (1, 0), (0, 1), (-1, 0)]
        dx, dy = moves[action]
        new = (x + dx, y + dy)

        reward = self.step_penalty
        if not self.grid.in_bounds(new) or not self.grid.passable(new):
            reward += self.invalid_penalty
            new = self.state
        else:
            self.state = new

        self.steps += 1
        done = False
        if self.state == self.grid.goal:
            reward += self.goal_reward
            done = True
        if self.steps >= self.max_steps:
            done = True

        return self.state, float(reward), done, {}

    @property
    def action_space_n(self) -> int:
        return 4

    @property
    def observation_space_shape(self) -> Tuple[int, int]:
        return (self.grid.width, self.grid.height)


class QLearningAgent:
    def __init__(self, env: GridWorldEnv, alpha: float = 0.5, gamma: float = 0.95, epsilon: float = 0.1, seed: int = 123) -> None:
        self.env = env
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.rng = random.Random(seed)
        W, H = env.grid.width, env.grid.height
        self.Q = np.zeros((W, H, env.action_space_n), dtype=np.float32)

    def choose_action(self, state: Coord) -> int:
        if self.rng.random() < self.epsilon:
            return self.rng.randrange(self.env.action_space_n)
        x, y = state
        qvalues = self.Q[x, y, :]
        maxq = float(np.max(qvalues))
        best_actions = [i for i, q in enumerate(qvalues) if float(q) == maxq]
        return self.rng.choice(best_actions)

    def learn(self, state: Coord, action: int, reward: float, next_state: Coord) -> None:
        x, y = state
        nx, ny = next_state
        best_next = float(np.max(self.Q[nx, ny, :]))
        td_target = reward + self.gamma * best_next
        td_error = td_target - float(self.Q[x, y, action])
        self.Q[x, y, action] = float(self.Q[x, y, action]) + self.alpha * td_error

    def train(self, episodes: int = 800, max_steps_per_episode: int = 200) -> np.ndarray:
        for _ in range(episodes):
            s = self.env.reset()
            for _ in range(max_steps_per_episode):
                a = self.choose_action(s)
                s2, r, done, _ = self.env.step(a)
                self.learn(s, a, r, s2)
                s = s2
                if done:
                    break
        return self.Q

    def derive_greedy_path(self, start: Optional[Coord] = None, max_steps: int = 500) -> List[Coord]:
        if start is None:
            start = self.env.grid.start
        # reset env and force start
        self.env.reset()
        self.env.state = start
        s = start
        path: List[Coord] = [s]
        for _ in range(max_steps):
            x, y = s
            q = self.Q[x, y, :]
            a = int(np.argmax(q))
            s2, _, done, _ = self.env.step(a)
            if s2 == s:
                # try other actions by descending Q
                for a2 in list(np.argsort(q)[::-1]):
                    s2, _, _, _ = self.env.step(int(a2))
                    if s2 != s:
                        break
                if s2 == s:
                    break
            path.append(s2)
            s = s2
            if s == self.env.grid.goal or done:
                break
        return path
