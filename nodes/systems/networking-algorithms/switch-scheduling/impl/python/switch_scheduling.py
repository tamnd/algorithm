# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/switch-scheduling/. The authors are listed in prov/52M6P4.jsonl.

"""Discrete-time models of an N x N crossbar switch with fixed-size cells.

Time is slotted. In each slot every input sends at most one cell and every
output receives at most one cell, so the set of (input, output) pairs that
transfer a cell is a matching. Two input-queue disciplines are modeled:

* FIFO input queues: only the head-of-line (HOL) cell of an input may be sent.
* Virtual output queues (VOQs): input i keeps one queue per output j, and the
  scheduler picks a matching with the maximum total queue length.
"""

import random
from fractions import Fraction
from itertools import permutations


def admissible(rates: list[list[Fraction]]) -> bool:
    """True when every row sum and every column sum of the rate matrix is < 1."""
    n = len(rates)
    rows = all(sum(rates[i]) < 1 for i in range(n))
    cols = all(sum(rates[i][j] for i in range(n)) < 1 for j in range(n))
    return rows and cols


def max_weight_matching(w: list[list[int]]) -> list[int]:
    """Return match[i] = output of input i in a perfect matching of maximum weight.

    The Hungarian method on the cost -w, in O(n^3) time. Pairs with weight 0
    may be in the result; the caller skips them.
    """
    n = len(w)
    inf = float("inf")
    u = [0] * (n + 1)
    v = [0] * (n + 1)
    p = [0] * (n + 1)  # p[j] = row matched to column j (1-based), 0 if none
    way = [0] * (n + 1)
    for i in range(1, n + 1):
        p[0] = i
        j0 = 0
        minv = [inf] * (n + 1)
        used = [False] * (n + 1)
        while True:
            used[j0] = True
            i0 = p[j0]
            delta = inf
            j1 = 0
            for j in range(1, n + 1):
                if not used[j]:
                    cur = -w[i0 - 1][j - 1] - u[i0] - v[j]
                    if cur < minv[j]:
                        minv[j] = cur
                        way[j] = j0
                    if minv[j] < delta:
                        delta = minv[j]
                        j1 = j
            for j in range(n + 1):
                if used[j]:
                    u[p[j]] += delta
                    v[j] -= delta
                else:
                    minv[j] -= delta
            j0 = j1
            if p[j0] == 0:
                break
        while True:
            j1 = way[j0]
            p[j0] = p[j1]
            j0 = j1
            if j0 == 0:
                break
    match = [0] * n
    for j in range(1, n + 1):
        match[p[j] - 1] = j - 1
    return match


def brute_force_max_weight(w: list[list[int]]) -> int:
    """The largest weight of a perfect matching, by trying all n! of them."""
    n = len(w)
    return max(sum(w[i][s[i]] for i in range(n)) for s in permutations(range(n)))


def fifo_saturation_throughput(n: int, slots: int, rng: random.Random, warmup: int = 1000) -> float:
    """Throughput per port of FIFO input queueing when every input is always backlogged.

    Each HOL cell has a uniform random output. Each output serves one of the
    HOL cells that want it, chosen uniformly at random. A served cell is
    replaced by a new cell with a new uniform random output; a blocked cell
    stays. Returns the cells served per output per slot after the warm-up.
    """
    head = [rng.randrange(n) for _ in range(n)]
    served = 0
    for t in range(warmup + slots):
        want: dict[int, list[int]] = {}
        for i in range(n):
            want.setdefault(head[i], []).append(i)
        for j, inputs in want.items():
            winner = inputs[rng.randrange(len(inputs))]
            head[winner] = rng.randrange(n)
            if t >= warmup:
                served += 1
    return served / (n * slots)


def simulate_fifo(n: int, load: float, slots: int, rng: random.Random) -> tuple[int, int, int]:
    """FIFO input queues under Bernoulli(load) arrivals with uniform outputs.

    Returns (arrivals, departures, cells left in the queues at the end).
    """
    queues: list[list[int]] = [[] for _ in range(n)]
    arrivals = departures = 0
    for _ in range(slots):
        want: dict[int, list[int]] = {}
        for i in range(n):
            if queues[i]:
                want.setdefault(queues[i][0], []).append(i)
        for j, inputs in want.items():
            winner = inputs[rng.randrange(len(inputs))]
            queues[winner].pop(0)
            departures += 1
        for i in range(n):
            if rng.random() < load:
                queues[i].append(rng.randrange(n))
                arrivals += 1
    return arrivals, departures, sum(len(q) for q in queues)


def simulate_voq_max_weight(n: int, load: float, slots: int, rng: random.Random) -> tuple[int, int, int]:
    """VOQs with a maximum-weight matching (weight = queue length) in each slot.

    The arrival process is the same as in simulate_fifo. Returns
    (arrivals, departures, cells left in the queues at the end).
    """
    q = [[0] * n for _ in range(n)]
    arrivals = departures = 0
    for _ in range(slots):
        match = max_weight_matching(q)
        for i in range(n):
            j = match[i]
            if q[i][j] > 0:
                q[i][j] -= 1
                departures += 1
        for i in range(n):
            if rng.random() < load:
                q[i][rng.randrange(n)] += 1
                arrivals += 1
    return arrivals, departures, sum(map(sum, q))
