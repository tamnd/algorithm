# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dueling-network/. The authors are listed in prov/P4J42D.jsonl.

"""Dueling network architecture for Q-values.

A shared hidden layer z feeds two heads, a value V(z) and advantages A(z, a),
and the aggregation layer combines them,

    mean:  Q(s, a) = V + A(a) - (1/m) sum_b A(b)     (Wang et al., eq. 9)
    max:   Q(s, a) = V + A(a) - max_b A(b)           (Wang et al., eq. 8)

The network here is tiny: one-hot state, one ReLU layer, linear heads.
dueling_ddqn trains it with the Double DQN target and a replay buffer, as in
the paper. Cost of one forward and backward pass: O(H * (S + m)).
"""

import math
import random


def aggregate(v, adv, kind: str = "mean"):
    """Combine a value v and an advantage list adv into Q-values."""
    if kind == "mean":
        c = sum(adv) / len(adv)  # @line L4
    elif kind == "max":
        c = max(adv)  # @line L4
    elif kind == "sum":
        c = 0 * v  # the naive, unidentifiable aggregation of eq. 7
    else:
        raise ValueError(kind)
    return [v + x - c for x in adv]  # @line L5


def decompose(q, kind: str = "mean"):
    """The unique (V, centred A) that aggregate maps to q, for kind mean or max."""
    if kind == "mean":
        v = sum(q) / len(q)
    elif kind == "max":
        v = max(q)
    else:
        raise ValueError("only mean and max aggregation are identifiable")
    return v, [x - v for x in q]


def argmax(xs) -> int:
    """The first index of a largest entry."""
    best = 0
    for i in range(1, len(xs)):
        if xs[i] > xs[best]:
            best = i
    return best


class DuelingQNet:
    """Shared ReLU layer, a value head and an advantage head, then aggregate."""

    def __init__(self, n_states: int, n_actions: int, hidden: int, rng: random.Random,
                 kind: str = "mean", rescale: float = 1.0 / math.sqrt(2.0)) -> None:
        self.n_states, self.n_actions, self.hidden = n_states, n_actions, hidden
        self.kind, self.rescale = kind, rescale
        a2 = 1.0 / math.sqrt(hidden)
        self.w1 = [[rng.uniform(-1.0, 1.0) for _ in range(n_states)] for _ in range(hidden)]
        self.b1 = [0.0] * hidden
        self.wv = [rng.uniform(-a2, a2) for _ in range(hidden)]
        self.bv = 0.0
        self.wa = [[rng.uniform(-a2, a2) for _ in range(hidden)] for _ in range(n_actions)]
        self.ba = [0.0] * n_actions

    def copy_from(self, other: "DuelingQNet") -> None:
        self.w1 = [list(r) for r in other.w1]
        self.b1 = list(other.b1)
        self.wv = list(other.wv)
        self.bv = other.bv
        self.wa = [list(r) for r in other.wa]
        self.ba = list(other.ba)

    def heads(self, s: int):
        """Return (z, v, adv) for one-hot state s."""
        z = [max(0.0, self.w1[h][s] + self.b1[h]) for h in range(self.hidden)]  # @line L1
        v = sum(w * x for w, x in zip(self.wv, z)) + self.bv  # @line L2
        adv = [sum(w * x for w, x in zip(self.wa[a], z)) + self.ba[a]  # @line L3
               for a in range(self.n_actions)]
        return z, v, adv

    def q(self, s: int) -> list[float]:
        _, v, adv = self.heads(s)
        return aggregate(v, adv, self.kind)  # @line L6

    def grads(self, batch: list[tuple[int, int, float]], loss: str = "huber"):
        """Gradients of the mean loss of y - Q(s, a) over (s, a, y) in batch."""
        H, m = self.hidden, self.n_actions
        g = {"w1": {}, "b1": [0.0] * H, "wv": [0.0] * H, "bv": 0.0,
             "wa": [[0.0] * H for _ in range(m)], "ba": [0.0] * m}
        for s, a, y in batch:
            z, v, adv = self.heads(s)
            qsa = aggregate(v, adv, self.kind)[a]
            d = y - qsa
            if loss == "huber":
                d = max(-1.0, min(1.0, d))
            gq = -d / len(batch)
            # dQ(a)/dA(b) = [a = b] - w(b), w = 1/m (mean) or one-hot argmax (max)
            if self.kind == "mean":
                w = [1.0 / m] * m
            elif self.kind == "max":
                w = [0.0] * m
                w[argmax(adv)] = 1.0
            else:
                w = [0.0] * m
            gadv = [gq * ((1.0 if b == a else 0.0) - w[b]) for b in range(m)]
            g["bv"] += gq
            for b in range(m):
                g["ba"][b] += gadv[b]
            col = g["w1"].setdefault(s, [0.0] * H)
            for h in range(H):
                g["wv"][h] += gq * z[h]
                for b in range(m):
                    g["wa"][b][h] += gadv[b] * z[h]
                if z[h] > 0.0:
                    gz = gq * self.wv[h] + sum(gadv[b] * self.wa[b][h] for b in range(m))
                    gz *= self.rescale
                    col[h] += gz
                    g["b1"][h] += gz
        return g

    def sgd_step(self, batch, lr: float, loss: str = "huber") -> None:
        g = self.grads(batch, loss)
        self.bv -= lr * g["bv"]
        for h in range(self.hidden):
            self.wv[h] -= lr * g["wv"][h]
            self.b1[h] -= lr * g["b1"][h]
        for b in range(self.n_actions):
            self.ba[b] -= lr * g["ba"][b]
            for h in range(self.hidden):
                self.wa[b][h] -= lr * g["wa"][b][h]
        for s, col in g["w1"].items():
            for h in range(self.hidden):
                self.w1[h][s] -= lr * col[h]


def dueling_ddqn(env, n_states: int, n_actions: int, start: int, gamma: float, n_steps: int,
                 capacity: int, batch_size: int, sync_every: int, lr: float, hidden: int,
                 rng: random.Random, kind: str = "mean", eps_end: float = 0.1,
                 eps_steps: int = 1000, warmup: int = 100,
                 max_episode_len: int = 100) -> DuelingQNet:
    """Double DQN with a dueling network on env(s, a) -> (r, s_next, done)."""
    buffer: list[tuple] = []
    nxt = 0
    online = DuelingQNet(n_states, n_actions, hidden, rng, kind)
    target = DuelingQNet(n_states, n_actions, hidden, rng, kind)
    target.copy_from(online)
    s, ep_len = start, 0
    for t in range(1, n_steps + 1):
        eps = 1.0 + min(1.0, t / eps_steps) * (eps_end - 1.0)
        a = rng.randrange(n_actions) if rng.random() < eps else argmax(online.q(s))
        r, s2, done = env(s, a)
        if len(buffer) < capacity:
            buffer.append((s, a, r, s2, done))
        else:
            buffer[nxt] = (s, a, r, s2, done)
        nxt = (nxt + 1) % capacity
        if len(buffer) >= warmup:
            batch = []
            for _ in range(batch_size):
                bs, ba, br, bs2, bd = buffer[rng.randrange(len(buffer))]
                y = br if bd else br + gamma * target.q(bs2)[argmax(online.q(bs2))]
                batch.append((bs, ba, y))
            online.sgd_step(batch, lr)
        if t % sync_every == 0:
            target.copy_from(online)
        ep_len += 1
        if done or ep_len >= max_episode_len:
            s, ep_len = start, 0
        else:
            s = s2
    return online
