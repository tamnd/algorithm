# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gossip-aggregation/. The authors are listed in prov/2FN2GA.jsonl.

"""Push-pull gossip aggregation (Jelasity, Montresor and Babaoglu 2005).

A cycle is a sequence of atomic push-pull exchanges. In an exchange of the
pair (i, j) both nodes apply UPDATE to their two values; for averaging,
UPDATE(a, b) = (a + b) / 2. The three pair selectors of the paper:

  pm:    two random perfect matchings per cycle, so every node is in
         exactly two exchanges (GETPAIR_PM);
  rand:  n pairs drawn uniformly at random (GETPAIR_RAND);
  distr: every node starts one exchange with a uniform random peer, in a
         random order (GETPAIR_DISTR, the practical protocol).

The simulator is synchronous and seeded. count_with_epochs adds epochs,
restarts and churn: nodes leave during an epoch and take their value with
them, new nodes join and wait for the next epoch.
"""

import math
import random
from typing import Callable


def pairs(kind: str, n: int, rng: random.Random) -> list[tuple[int, int]]:
    if kind == "pm":
        out = []
        for _ in range(2):
            perm = list(range(n))
            rng.shuffle(perm)
            out.extend((perm[k], perm[k + 1]) for k in range(0, n - 1, 2))
        return out
    if kind == "rand":
        out = []
        for _ in range(n):
            i = rng.randrange(n)
            j = rng.randrange(n - 1)
            out.append((i, j if j < i else j + 1))
        return out
    order = list(range(n))
    rng.shuffle(order)
    out = []
    for i in order:
        j = rng.randrange(n - 1)
        out.append((i, j if j < i else j + 1))
    return out


def run_cycle(x: list[float], kind: str, rng: random.Random,
              update: Callable[[float, float], float] = lambda a, b: (a + b) / 2) -> None:
    for i, j in pairs(kind, len(x), rng):
        x[i] = x[j] = update(x[i], x[j])


def variance(x: list[float]) -> float:
    m = sum(x) / len(x)
    return sum((v - m) ** 2 for v in x) / (len(x) - 1)


def convergence_factor(kind: str, n: int, cycles: int, seeds: int) -> float:
    """The geometric mean over cycles and seeds of sigma^2_{i+1} / sigma^2_i,
    from uniform random initial values."""
    logs = []
    for seed in range(seeds):
        rng = random.Random(seed)
        x = [rng.random() for _ in range(n)]
        prev = variance(x)
        for _ in range(cycles):
            run_cycle(x, kind, rng)
            cur = variance(x)
            logs.append(math.log(cur / prev))
            prev = cur
    return math.exp(sum(logs) / len(logs))


def aggregate(x: list[float], what: str, cycles: int, seed: int) -> list[float]:
    """Each node's estimate of max, min, mean, the geometric mean or the
    variance after the given number of cycles of GETPAIR_DISTR."""
    rng = random.Random(seed)
    if what in ("max", "min"):
        y = list(x)
        run = max if what == "max" else min
        for _ in range(cycles):
            run_cycle(y, "distr", rng, lambda a, b: run(a, b))
        return y
    if what == "mean":
        y = list(x)
        for _ in range(cycles):
            run_cycle(y, "distr", rng)
        return y
    if what == "geometric":
        y = [math.log(v) for v in x]
        for _ in range(cycles):
            run_cycle(y, "distr", rng)
        return [math.exp(v) for v in y]
    # variance: average x and x^2 side by side with the same exchanges
    a, b = list(x), [v * v for v in x]
    for _ in range(cycles):
        for i, j in pairs("distr", len(x), rng):
            a[i] = a[j] = (a[i] + a[j]) / 2
            b[i] = b[j] = (b[i] + b[j]) / 2
    return [q - p * p for p, q in zip(a, b)]


def count_with_epochs(n0: int, epochs: int, gamma: int, churn: float, seed: int) -> list[tuple[int, float, float]]:
    """COUNT with restarts. At the start of each epoch one random member is
    the leader with value 1, the others start at 0, and gamma cycles of
    push-pull averaging run among the members. In each cycle a fraction
    churn of the members crash (their values are lost) and as many new
    nodes join; joiners wait for the next epoch. Returns, per epoch, the
    size at the start, the size at the end, and the median estimate 1/x."""
    rng = random.Random(seed)
    alive = n0
    out = []
    for _ in range(epochs):
        size_start = alive
        members = [0.0] * alive
        members[rng.randrange(alive)] = 1.0
        waiting = 0
        for _ in range(gamma):
            k = len(members)
            for i, j in pairs("distr", k, rng):
                members[i] = members[j] = (members[i] + members[j]) / 2
            leave = sum(1 for _ in range(k) if rng.random() < churn)
            for _ in range(leave):
                members.pop(rng.randrange(len(members)))
            waiting += leave
        est = sorted(1.0 / v if v > 0 else float("inf") for v in members)
        alive = len(members) + waiting
        out.append((size_start, len(members), est[len(est) // 2]))
    return out
