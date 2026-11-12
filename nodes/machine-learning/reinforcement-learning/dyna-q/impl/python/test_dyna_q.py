# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dyna-q/. The authors are listed in prov/DC1KQ2.jsonl.

import random
from collections import deque

from dyna_q import DynaQ, Maze, greedy_path_length


def bfs_shortest(env):
    """Independent oracle: the length of the shortest path from start to goal."""
    dist, todo = {env.start: 0}, deque([env.start])
    while todo:
        s = todo.popleft()
        for a in range(4):
            _, t, term = env.step(s, a)
            if term:
                return dist[s] + 1
            if t not in dist:
                dist[t] = dist[s] + 1
                todo.append(t)
    return None


def first_optimal(n_planning, seed, cap=30000):
    """Real steps until the greedy policy, checked at the end of each episode, takes a shortest path."""
    env = Maze()
    best = bfs_shortest(env)
    agent = DynaQ(54, 4, 1.0, 0.95, 0.1, n_planning, seed, q0=1.0)
    s = env.start
    for t in range(1, cap + 1):
        s, term = agent.step(env, s)
        if term:
            s = env.start
            if greedy_path_length(agent, env) == best:
                return t
    return cap + 1


def test_maze_oracle():
    assert bfs_shortest(Maze()) == 14


def test_more_planning_needs_fewer_real_steps():
    seeds = range(5)
    t0 = [first_optimal(0, s) for s in seeds]
    t5 = [first_optimal(5, s) for s in seeds]
    t50 = [first_optimal(50, s) for s in seeds]
    assert max(t50) <= 30000 and max(t0) <= 30000
    for a, b, c in zip(t0, t5, t50):
        assert c < b < a
    assert sorted(t50)[2] * 3 < sorted(t0)[2]


class TableEnv:
    def __init__(self, T):
        self.T, self.start = T, 0

    def step(self, s, a):
        return self.T[s][a]


def optimal_q(T, gamma):
    """Independent oracle: Q* of a deterministic MDP by repeated Bellman backups."""
    Q = [[0.0] * len(row) for row in T]
    for _ in range(3000):
        Q = [[r + (0.0 if term else gamma * max(Q[t])) for r, t, term in row] for row in T]
    return Q


def test_random_deterministic_mdps_reach_q_star():
    rng = random.Random(81)
    for case in range(500):
        n, k = rng.randint(1, 4), rng.randint(1, 3)
        T = [[(float(rng.randint(-3, 3)), rng.randrange(n), rng.random() < 0.2) for _ in range(k)] for _ in range(n)]
        gamma = rng.choice([0.0, 0.5, 0.8])
        agent = DynaQ(n, k, 0.5, gamma, 1.0, 40, seed=case, q0=rng.uniform(-5, 5))
        env, s = TableEnv(T), 0
        for _ in range(300):
            s2, term = agent.step(env, s)
            s = rng.randrange(n) if term or rng.random() < 0.3 else s2  # random restarts reach every state
        Qs = optimal_q(T, gamma)
        for s in range(n):
            for a in range(k):
                assert (s, a) in agent.model
                assert agent.model[(s, a)] == T[s][a]
                assert abs(agent.Q[s][a] - Qs[s][a]) < 1e-6


def test_no_planning_changes_one_entry():
    env = Maze()
    agent = DynaQ(54, 4, 0.5, 0.9, 0.3, 0, seed=3, q0=0.25)
    s = env.start
    for _ in range(2000):
        before = [row[:] for row in agent.Q]
        s2, term = agent.step(env, s)
        diff = [(i, j) for i in range(54) for j in range(4) if agent.Q[i][j] != before[i][j]]
        assert len(diff) <= 1 and all(i == s for i, _ in diff)
        s = env.start if term else s2


def test_run_returns_episode_lengths():
    env = Maze()
    agent = DynaQ(54, 4, 1.0, 0.95, 0.1, 20, seed=1, q0=1.0)
    lengths = agent.run(env, 3000)
    assert lengths and min(lengths) >= 14 and lengths[-1] <= 20
