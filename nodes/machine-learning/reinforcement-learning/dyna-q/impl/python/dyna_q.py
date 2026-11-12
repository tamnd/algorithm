# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dyna-q/. The authors are listed in prov/DC1KQ2.jsonl.

"""Tabular Dyna-Q (Sutton 1990; Sutton and Barto 2018, Section 8.2).

Each real step does one Q-learning update, stores the observed transition in
a deterministic table model, and then does n planning updates on transitions
drawn from the model. An environment has a start state and a method
step(s, a) -> (r, s2, terminal).
"""

import random


class DynaQ:
    def __init__(self, n_states, n_actions, alpha, gamma, epsilon, n_planning, seed=0, q0=0.0):
        """q0 is the initial value of every Q(s, a); an optimistic q0 makes the agent try every action."""
        self.k, self.alpha, self.gamma = n_actions, alpha, gamma
        self.epsilon, self.n = epsilon, n_planning
        self.rng = random.Random(seed)
        self.Q = [[q0] * n_actions for _ in range(n_states)]  # @line L1
        self.model = {}  # (s, a) -> (r, s2, terminal)
        self.seen = {}  # s -> list of the actions tried in s, in first-seen order
        self.states = []  # the states in self.seen, in first-seen order

    def greedy(self, s):
        q = self.Q[s]
        best = max(q)
        return self.rng.choice([a for a in range(self.k) if q[a] == best])

    def act(self, s):
        if self.rng.random() < self.epsilon:
            return self.rng.randrange(self.k)
        return self.greedy(s)

    def update(self, s, a, r, s2, terminal):
        target = r if terminal else r + self.gamma * max(self.Q[s2])
        self.Q[s][a] += self.alpha * (target - self.Q[s][a])

    def step(self, env, s):
        """One real step from state s, then n planning steps. Return (s2, terminal)."""
        a = self.act(s)  # @line L4
        r, s2, terminal = env.step(s, a)  # @line L5
        self.update(s, a, r, s2, terminal)  # @line L6
        if (s, a) not in self.model:
            if s not in self.seen:
                self.states.append(s)
                self.seen[s] = []
            self.seen[s].append(a)
        self.model[(s, a)] = (r, s2, terminal)  # @line L7
        for _ in range(self.n):  # @line L8
            ps = self.rng.choice(self.states)  # @line L9
            pa = self.rng.choice(self.seen[ps])
            pr, ps2, pterm = self.model[(ps, pa)]  # @line L10
            self.update(ps, pa, pr, ps2, pterm)  # @line L11
        return s2, terminal

    def run(self, env, steps):
        """Act for the given number of real steps, restarting episodes at env.start. Return episode lengths."""
        lengths, s, t = [], env.start, 0
        for _ in range(steps):  # @line L2
            s, terminal = self.step(env, s)  # @line L3
            t += 1
            if terminal:
                lengths.append(t)
                s, t = env.start, 0
        return lengths


class Maze:
    """The Dyna maze of Sutton and Barto (Example 8.1): 6 x 9 cells, reward 1 at the goal."""

    ROWS, COLS = 6, 9
    WALLS = {(1, 2), (2, 2), (3, 2), (4, 5), (0, 7), (1, 7), (2, 7)}
    MOVES = ((-1, 0), (1, 0), (0, -1), (0, 1))  # up, down, left, right

    def __init__(self):
        self.start = 2 * self.COLS + 0
        self.goal = 0 * self.COLS + 8

    def step(self, s, a):
        r, c = divmod(s, self.COLS)
        nr, nc = r + self.MOVES[a][0], c + self.MOVES[a][1]
        if not (0 <= nr < self.ROWS and 0 <= nc < self.COLS) or (nr, nc) in self.WALLS:
            nr, nc = r, c
        s2 = nr * self.COLS + nc
        return (1.0, s2, True) if s2 == self.goal else (0.0, s2, False)


def greedy_path_length(agent, env, cap=200):
    """Steps of the greedy policy (first maximizer) from env.start to a terminal state, or None."""
    s = env.start
    for t in range(1, cap + 1):
        q = agent.Q[s]
        _, s, terminal = env.step(s, q.index(max(q)))
        if terminal:
            return t
    return None
