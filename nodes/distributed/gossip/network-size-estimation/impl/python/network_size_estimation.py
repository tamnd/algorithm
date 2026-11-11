# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/network-size-estimation/. The authors are listed in prov/RJGWTH.jsonl.

"""Five ways to estimate the number of nodes n of a network by gossip or by
random walks, in a seeded simulator.

  averaging_count:  push-pull averaging with one node at 1 and the rest at 0;
                    every node estimates 1 / a_i.
  kmin_uniform:     every node draws U_i uniform on (0, 1); gossip keeps the
                    k smallest values; (k - 1) / U_(k) is unbiased for n.
  exp_minima:       every node draws k independent Exp(1) values; gossip
                    keeps the minimum of each coordinate; with S the sum of
                    the k minima, (k - 1) / S is unbiased for n.
  random_tour:      a simple random walk from node i back to i, adding
                    1 / d_j at each visit; d_i times the sum is unbiased.
  sample_collide:   uniform samples from a continuous time random walk;
                    with C the number of samples up to the l-th repeat,
                    C^2 / (2 l) estimates n.
  hyperloglog:      every node puts its own id in an m register HyperLogLog
                    sketch; gossip merges sketches by register maximum.
"""

import hashlib
import heapq
import math
import random


# ---------------------------------------------------------------- graphs

def random_graph(n: int, d: int, seed: int) -> list[list[int]]:
    """A connected undirected graph: a random Hamiltonian cycle plus d - 2
    random chords per node, so the degrees vary."""
    rng = random.Random(seed)
    order = list(range(n))
    rng.shuffle(order)
    nb = [set() for _ in range(n)]
    for k in range(n):
        a, b = order[k], order[(k + 1) % n]
        nb[a].add(b)
        nb[b].add(a)
    for a in range(n):
        for _ in range(d - 2):
            b = rng.randrange(n)
            if b != a:
                nb[a].add(b)
                nb[b].add(a)
    return [sorted(s) for s in nb]


def push_pull_round(state: list, merge, rng: random.Random) -> None:
    """One cycle of GETPAIR_DISTR over a uniform peer sampling service:
    every node, in random order, exchanges with a uniform random peer and
    both keep merge(own, other)."""
    n = len(state)
    order = list(range(n))
    rng.shuffle(order)
    for i in order:
        j = rng.randrange(n - 1)
        j = j if j < i else j + 1
        state[i] = state[j] = merge(state[i], state[j])


# ---------------------------------------------------------------- gossip

def averaging_count(n: int, cycles: int, seed: int) -> list[float]:
    rng = random.Random(seed)
    a = [0.0] * n
    a[rng.randrange(n)] = 1.0
    for _ in range(cycles):
        push_pull_round(a, lambda u, v: (u + v) / 2, rng)
    return [1 / v if v > 0 else math.inf for v in a]


def kmin_uniform(n: int, k: int, cycles: int, seed: int) -> list[float]:
    rng = random.Random(seed)
    sets = [(rng.random(),) for _ in range(n)]
    merge = lambda u, v: tuple(sorted(set(u) | set(v))[:k])
    for _ in range(cycles):
        push_pull_round(sets, merge, rng)
    return [(k - 1) / s[k - 1] if len(s) == k else float(len(s)) for s in sets]


def kmin_direct(n: int, k: int, rng: random.Random) -> float:
    """The value that kmin_uniform converges to, computed centrally."""
    return (k - 1) / heapq.nsmallest(k, (rng.random() for _ in range(n)))[-1]


def exp_direct(n: int, k: int, rng: random.Random) -> float:
    """The value that exp_minima converges to: each coordinate minimum of n
    Exp(1) values is Exp(n), drawn here directly."""
    return (k - 1) / sum(rng.expovariate(n) for _ in range(k))


def exp_minima(n: int, k: int, cycles: int, seed: int) -> list[float]:
    rng = random.Random(seed)
    vec = [tuple(rng.expovariate(1.0) for _ in range(k)) for _ in range(n)]
    merge = lambda u, v: tuple(min(p, q) for p, q in zip(u, v))
    for _ in range(cycles):
        push_pull_round(vec, merge, rng)
    return [(k - 1) / sum(v) for v in vec]


# ---------------------------------------------------------------- random walks

def random_tour(adj: list[list[int]], start: int, rng: random.Random) -> float:
    """Massoulie, Le Merrer, Kermarrec and Ganesh: one tour from start."""
    total = 1 / len(adj[start])
    v = rng.choice(adj[start])
    while v != start:
        total += 1 / len(adj[v])
        v = rng.choice(adj[v])
    return len(adj[start]) * total


def ctrw_sample(adj: list[list[int]], start: int, timer: float, rng: random.Random) -> int:
    """A continuous time random walk that stays an Exp(d_v) time at v and
    then moves to a uniform neighbour. Its stationary law is uniform, so the
    node where the timer runs out is close to a uniform sample."""
    v = start
    t = timer
    while True:
        t -= rng.expovariate(len(adj[v]))
        if t <= 0:
            return v
        v = rng.choice(adj[v])


def sample_collide(adj: list[list[int]], l: int, timer: float, seed: int, uniform: bool = False) -> float:
    rng = random.Random(seed)
    n = len(adj)
    seen = set()
    c = 0
    repeats = 0
    while repeats < l:
        v = rng.randrange(n) if uniform else ctrw_sample(adj, 0, timer, rng)
        c += 1
        if v in seen:
            repeats += 1
        seen.add(v)
    return c * c / (2 * l)


# ---------------------------------------------------------------- HyperLogLog

def _hash64(node: int, salt: int) -> int:
    h = hashlib.blake2b(f"{salt}:{node}".encode(), digest_size=8).digest()
    return int.from_bytes(h, "big")


def hll_add(reg: list[int], item: int, salt: int) -> None:
    m = len(reg)
    b = m.bit_length() - 1
    h = _hash64(item, salt)
    j = h >> (64 - b)
    rest = (h << b) & ((1 << 64) - 1)
    rank = 64 - b + 1 if rest == 0 else (64 - rest.bit_length()) + 1
    reg[j] = max(reg[j], rank)


def hll_estimate(reg: list[int]) -> float:
    m = len(reg)
    alpha = 0.7213 / (1 + 1.079 / m)
    e = alpha * m * m / sum(2.0 ** -r for r in reg)
    zeros = reg.count(0)
    if e <= 2.5 * m and zeros:
        return m * math.log(m / zeros)
    return e


def hyperloglog(n: int, m: int, cycles: int, seed: int) -> list[float]:
    rng = random.Random(seed)
    sk = []
    for v in range(n):
        reg = [0] * m
        hll_add(reg, v, seed)
        sk.append(tuple(reg))
    merge = lambda u, w: tuple(max(p, q) for p, q in zip(u, w))
    for _ in range(cycles):
        push_pull_round(sk, merge, rng)
    return [hll_estimate(list(s)) for s in sk]
