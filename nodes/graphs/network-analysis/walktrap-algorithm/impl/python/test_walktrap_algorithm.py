# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/walktrap-algorithm/. The authors are listed in prov/78KW1X.jsonl.

import itertools
import random
from fractions import Fraction

from walktrap_algorithm import modularity, walktrap


def oracle(n, edges, t):
    """Walktrap from the definitions, in exact arithmetic.

    Each merge joins the two adjacent communities whose union increases
    sigma = (1/n) sum over communities C and i in C of r(i, C)^2 the least,
    with sigma computed from scratch; ties go to the smallest pair of ids.
    """
    a = [[Fraction(0)] * n for _ in range(n)]
    for i in range(n):
        a[i][i] = Fraction(1)
    for e in edges:
        u, v = e[0], e[1]
        w = Fraction(e[2]) if len(e) == 3 else Fraction(1)
        a[u][v] += w
        a[v][u] += w
    d = [sum(row) for row in a]
    p = [[a[i][j] / d[i] for j in range(n)] for i in range(n)]
    pt = [[Fraction(int(i == j)) for j in range(n)] for i in range(n)]
    for _ in range(t):
        pt = [[sum(pt[i][k] * p[k][j] for k in range(n)) for j in range(n)] for i in range(n)]

    def r2(row1, row2):
        return sum((row1[k] - row2[k]) ** 2 / d[k] for k in range(n))

    def mean_row(c):
        return [sum(pt[i][k] for i in c) / len(c) for k in range(n)]

    def sigma(comms):
        total = Fraction(0)
        for c in comms.values():
            m = mean_row(c)
            total += sum(r2(pt[i], m) for i in c)
        return total / n

    comms = {i: [i] for i in range(n)}
    seq = [sorted(sorted(c) for c in comms.values())]
    merges = []
    while True:
        cand = []
        for x, y in itertools.combinations(sorted(comms), 2):
            if any(a[i][j] and i != j for i in comms[x] for j in comms[y]):
                trial = {k: v for k, v in comms.items() if k not in (x, y)}
                trial[-1] = comms[x] + comms[y]
                cand.append((sigma(trial) - sigma(comms), x, y))
        if not cand:
            break
        ds, x, y = min(cand)
        merges.append((x, y, ds))
        comms[n + len(merges) - 1] = comms.pop(x) + comms.pop(y)
        seq.append(sorted(sorted(c) for c in comms.values()))
    wedges = [(e[0], e[1], float(e[2]) if len(e) == 3 else 1.0) for e in edges]
    best = max(range(len(seq)), key=lambda k: (round(modularity(n, wedges, seq[k]), 9), -k))
    return seq[best], merges


def test_worked_example() -> None:
    edges = [(0, 1), (0, 2), (1, 2), (3, 4), (3, 5), (4, 5), (2, 3)]
    parts, merges = walktrap(6, edges, 2)
    assert parts == [[0, 1, 2], [3, 4, 5]]
    assert [(x, y) for x, y, _ in merges] == [(0, 1), (4, 5), (2, 6), (3, 7), (8, 9)]
    _, exact = oracle(6, edges, 2)
    for (_, _, got), (_, _, want) in zip(merges, exact):
        assert abs(got - float(want)) < 1e-12
    assert abs(modularity(6, [(u, v, 1.0) for u, v in edges], parts) - 5 / 14) < 1e-12


def test_edge_cases() -> None:
    assert walktrap(0, []) == ([], [])
    assert walktrap(1, []) == ([[0]], [])
    assert walktrap(3, []) == ([[0], [1], [2]], [])
    parts, merges = walktrap(4, [(0, 1), (2, 3)], 3)
    assert parts == [[0, 1], [2, 3]] and len(merges) == 2
    for bad in ([(0, 0)], [(0, 9)], [(0, 1, -1.0)]):
        try:
            walktrap(2, bad)
        except ValueError:
            pass
        else:
            raise AssertionError("expected ValueError")
    try:
        walktrap(2, [(0, 1)], 0)
    except ValueError:
        pass
    else:
        raise AssertionError("expected ValueError")


def test_random_against_definition() -> None:
    rng = random.Random(2005)
    for _ in range(500):
        n = rng.randint(1, 6)
        prob = rng.random()
        weighted = rng.random() < 0.3
        edges = []
        for u in range(n):
            for v in range(u + 1, n):
                if rng.random() < prob:
                    edges.append((u, v, rng.randint(1, 3)) if weighted else (u, v))
        t = rng.randint(1, 3)
        parts, merges = walktrap(n, edges, t)
        want_parts, want_merges = oracle(n, edges, t)
        assert [(x, y) for x, y, _ in merges] == [(x, y) for x, y, _ in want_merges]
        for (_, _, got), (_, _, want) in zip(merges, want_merges):
            assert abs(got - float(want)) < 1e-9
        assert parts == want_parts
