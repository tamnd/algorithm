# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/double-dqn/. The authors are listed in prov/WJ898F.jsonl.

"""Double DQN: DQN whose target selects the next action with the online
network and evaluates it with the target network,

    y = r + gamma * Q_target(s', argmax_a' Q_online(s', a')).

The Q-network is a tiny one-hidden-layer ReLU network on a one-hot state.
A "network" in the target functions is any object with a method q(s) that
returns the list of action values, so the tests can pass exact tables.
Cost per environment step: O(B * H * A) for a minibatch of B, H hidden
units and A actions, one more forward pass per sample than DQN needs.
"""

import math
import random


class QNet:
    """Q(s, .) = W2 relu(W1[:, s] + b1) + b2 for a one-hot state s."""

    def __init__(self, n_states: int, n_actions: int, hidden: int, rng: random.Random) -> None:
        self.n_states, self.n_actions, self.hidden = n_states, n_actions, hidden
        a2 = 1.0 / math.sqrt(hidden)
        self.w1 = [[rng.uniform(-1.0, 1.0) for _ in range(n_states)] for _ in range(hidden)]
        self.b1 = [0.0] * hidden
        self.w2 = [[rng.uniform(-a2, a2) for _ in range(hidden)] for _ in range(n_actions)]
        self.b2 = [0.0] * n_actions

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
        """One SGD step on the mean Huber loss of y - Q(s, a) over (s, a, y) in batch."""
        gw1: dict[int, list[float]] = {}
        gb1 = [0.0] * self.hidden
        gw2 = [[0.0] * self.hidden for _ in range(self.n_actions)]
        gb2 = [0.0] * self.n_actions
        for s, a, y in batch:
            z = self.hidden_of(s)
            qsa = sum(w * x for w, x in zip(self.w2[a], z)) + self.b2[a]
            g = -max(-1.0, min(1.0, y - qsa)) / len(batch)
            gb2[a] += g
            col = gw1.setdefault(s, [0.0] * self.hidden)
            for h in range(self.hidden):
                gw2[a][h] += g * z[h]
                if z[h] > 0.0:
                    col[h] += g * self.w2[a][h]
                    gb1[h] += g * self.w2[a][h]
        for a in range(self.n_actions):
            self.b2[a] -= lr * gb2[a]
            for h in range(self.hidden):
                self.w2[a][h] -= lr * gw2[a][h]
        for s, col in gw1.items():
            for h in range(self.hidden):
                self.w1[h][s] -= lr * col[h]
        for h in range(self.hidden):
            self.b1[h] -= lr * gb1[h]


def argmax(xs) -> int:
    """The first index of a largest entry."""
    best = 0
    for i in range(1, len(xs)):
        if xs[i] > xs[best]:
            best = i
    return best


def dqn_target(r, s2, done: bool, online, target, gamma):
    """The DQN target r + gamma * max_a' Q_target(s2, a'); online is unused."""
    return r if done else r + gamma * max(target.q(s2))


def double_dqn_target(r, s2, done: bool, online, target, gamma):
    """The Double DQN target r + gamma * Q_target(s2, argmax_a' Q_online(s2, a'))."""
    if done:
        return r  # @line L6
    a_star = argmax(online.q(s2))  # @line L6
    return r + gamma * target.q(s2)[a_star]  # @line L7


def double_dqn(env, n_states: int, n_actions: int, start: int, gamma: float, n_steps: int,
               capacity: int, batch_size: int, sync_every: int, lr: float, hidden: int,
               rng: random.Random, eps_end: float = 0.1, eps_steps: int = 1000,
               warmup: int = 100, max_episode_len: int = 100) -> QNet:
    """Train Double DQN on env(s, a) -> (r, s_next, done); return the online network."""
    buffer: list[tuple] = []  # @line L1
    nxt = 0
    online = QNet(n_states, n_actions, hidden, rng)  # @line L1
    target = QNet(n_states, n_actions, hidden, rng)
    target.copy_from(online)  # @line L1
    s, ep_len = start, 0
    for t in range(1, n_steps + 1):  # @line L2
        eps = 1.0 + min(1.0, t / eps_steps) * (eps_end - 1.0)
        a = rng.randrange(n_actions) if rng.random() < eps else argmax(online.q(s))  # @line L3
        r, s2, done = env(s, a)  # @line L4
        if len(buffer) < capacity:  # @line L4
            buffer.append((s, a, r, s2, done))
        else:
            buffer[nxt] = (s, a, r, s2, done)
        nxt = (nxt + 1) % capacity
        if len(buffer) >= warmup:
            mb = [buffer[rng.randrange(len(buffer))] for _ in range(batch_size)]  # @line L5
            batch = [(bs, ba, double_dqn_target(br, bs2, bd, online, target, gamma))
                     for bs, ba, br, bs2, bd in mb]
            online.sgd_step(batch, lr)  # @line L8
        if t % sync_every == 0:  # @line L9
            target.copy_from(online)  # @line L9
        ep_len += 1
        if done or ep_len >= max_episode_len:  # @line L10
            s, ep_len = start, 0
        else:
            s = s2  # @line L10
    return online
