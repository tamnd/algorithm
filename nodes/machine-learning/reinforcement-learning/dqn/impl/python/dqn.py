# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dqn/. The authors are listed in prov/5J3KX3.jsonl.

"""Deep Q-network (DQN) with a tiny multilayer perceptron, in pure Python.

The Q-network maps a state (one-hot coded) through one hidden ReLU layer to
one output per action. DQN keeps a replay buffer of the last `capacity`
transitions, an online network theta and a target network theta_minus that
is copied from theta every C steps. Each step does epsilon-greedy acting,
stores the transition, samples a minibatch and takes one SGD step on the
Huber loss of y - Q(s, a), with y = r + gamma * max_a' Q_target(s', a').

Cost per environment step: O(B * H * A) arithmetic operations for a
minibatch of B, H hidden units and A actions (the one-hot input makes the
first layer O(H)). Memory: O(capacity) transitions and O(S H + H A)
parameters. There is no convergence guarantee.
"""

import math
import random


class QNet:
    """Q(s, .) = W2 relu(W1[:, s] + b1) + b2 for a one-hot state s."""

    def __init__(self, n_states: int, n_actions: int, hidden: int, rng: random.Random) -> None:
        self.n_states, self.n_actions, self.hidden = n_states, n_actions, hidden
        a1 = 1.0  # the input is one-hot, so each hidden unit sees one weight
        a2 = 1.0 / math.sqrt(hidden)
        self.w1 = [[rng.uniform(-a1, a1) for _ in range(n_states)] for _ in range(hidden)]
        self.b1 = [0.0] * hidden
        self.w2 = [[rng.uniform(-a2, a2) for _ in range(hidden)] for _ in range(n_actions)]
        self.b2 = [0.0] * n_actions

    def params(self) -> list[float]:
        out = [x for row in self.w1 for x in row] + list(self.b1)
        out += [x for row in self.w2 for x in row] + list(self.b2)
        return out

    def copy_from(self, other: "QNet") -> None:
        self.w1 = [list(r) for r in other.w1]
        self.b1 = list(other.b1)
        self.w2 = [list(r) for r in other.w2]
        self.b2 = list(other.b2)

    def hidden_of(self, s: int) -> list[float]:
        return [max(0.0, self.w1[h][s] + self.b1[h]) for h in range(self.hidden)]

    def q(self, s: int) -> list[float]:
        z = self.hidden_of(s)
        return [sum(w * x for w, x in zip(self.w2[a], z)) + self.b2[a] for a in range(self.n_actions)]

    def sgd_step(self, batch: list[tuple[int, int, float]], lr: float) -> None:
        """One SGD step on the mean of huber(y - Q(s, a)) over (s, a, y) in batch."""
        gw1 = {}
        gb1 = [0.0] * self.hidden
        gw2 = [[0.0] * self.hidden for _ in range(self.n_actions)]
        gb2 = [0.0] * self.n_actions
        scale = 1.0 / len(batch)
        for s, a, y in batch:
            z = self.hidden_of(s)
            qsa = sum(w * x for w, x in zip(self.w2[a], z)) + self.b2[a]
            g = -huber_grad(y - qsa) * scale  # d loss / d Q(s, a)
            gb2[a] += g
            col = gw1.setdefault(s, [0.0] * self.hidden)
            for h in range(self.hidden):
                gw2[a][h] += g * z[h]
                if z[h] > 0.0:
                    gh = g * self.w2[a][h]
                    col[h] += gh
                    gb1[h] += gh
        for a in range(self.n_actions):
            self.b2[a] -= lr * gb2[a]
            for h in range(self.hidden):
                self.w2[a][h] -= lr * gw2[a][h]
        for s, col in gw1.items():
            for h in range(self.hidden):
                self.w1[h][s] -= lr * col[h]
        for h in range(self.hidden):
            self.b1[h] -= lr * gb1[h]


def huber_grad(delta: float, kappa: float = 1.0) -> float:
    """Derivative of the Huber loss at delta: delta clipped to [-kappa, kappa]."""
    return max(-kappa, min(kappa, delta))


def dqn_target(r: float, s2: int, done: bool, target: QNet, gamma: float) -> float:
    """y = r for a terminal transition, else r + gamma * max_a' Q_target(s2, a')."""
    return r if done else r + gamma * max(target.q(s2))


def argmax(xs: list[float]) -> int:
    return max(range(len(xs)), key=lambda i: xs[i])


def dqn(env, n_states: int, n_actions: int, start: int, gamma: float, n_steps: int,
        capacity: int, batch_size: int, sync_every: int, lr: float, hidden: int,
        rng: random.Random, eps_start: float = 1.0, eps_end: float = 0.1,
        eps_steps: int = 1000, warmup: int = 100, max_episode_len: int = 100,
        trace: list | None = None) -> QNet:
    """Train DQN on env(s, a) -> (r, s_next, done) and return the online network.

    If trace is a list, (t, target parameters, online parameters) is appended
    after each step.
    """
    buffer: list[tuple] = []  # @line L1
    nxt = 0
    online = QNet(n_states, n_actions, hidden, rng)  # @line L1
    target = QNet(n_states, n_actions, hidden, rng)
    target.copy_from(online)  # @line L1
    s, ep_len = start, 0
    for t in range(1, n_steps + 1):  # @line L2
        frac = min(1.0, t / eps_steps)
        eps = eps_start + frac * (eps_end - eps_start)
        if rng.random() < eps:  # @line L3
            a = rng.randrange(n_actions)
        else:
            a = argmax(online.q(s))  # @line L3
        r, s2, done = env(s, a)  # @line L4
        if len(buffer) < capacity:  # @line L4
            buffer.append((s, a, r, s2, done))
        else:
            buffer[nxt] = (s, a, r, s2, done)
        nxt = (nxt + 1) % capacity
        if len(buffer) >= warmup:
            mb = [buffer[rng.randrange(len(buffer))] for _ in range(batch_size)]  # @line L5
            batch = [(bs, ba, dqn_target(br, bs2, bd, target, gamma))  # @line L6
                     for bs, ba, br, bs2, bd in mb]
            online.sgd_step(batch, lr)  # @line L7
        if t % sync_every == 0:  # @line L8
            target.copy_from(online)  # @line L8
        ep_len += 1
        if done or ep_len >= max_episode_len:  # @line L9
            s, ep_len = start, 0
        else:
            s = s2  # @line L9
        if trace is not None:
            trace.append((t, target.params(), online.params()))
    return online
