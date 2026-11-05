# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/simrank/. The authors are listed in prov/G0C81F.jsonl.

import itertools
import random
from fractions import Fraction

from simrank import rounds_for, simrank


def exact(n: int, arcs: list[tuple[int, int]], c: Fraction) -> list[list[Fraction]]:
    """Solve the SimRank equations of the definition exactly, as one linear system."""
    into: list[list[int]] = [[] for _ in range(n)]
    for u, v in arcs:
        into[v].append(u)
    idx = {p: t for t, p in enumerate(itertools.product(range(n), repeat=2))}
    size = len(idx)
    m = [[Fraction(0)] * (size + 1) for _ in range(size)]
    for (a, b), t in idx.items():
        m[t][t] += 1
        if a == b:
            m[t][size] = Fraction(1)
        elif into[a] and into[b]:
            w = c / (len(into[a]) * len(into[b]))
            for i in into[a]:
                for j in into[b]:
                    m[t][idx[(i, j)]] -= w
    for col in range(size):
        piv = next(r for r in range(col, size) if m[r][col] != 0)
        m[col], m[piv] = m[piv], m[col]
        p = m[col][col]
        m[col] = [x / p for x in m[col]]
        for r in range(size):
            if r != col and m[r][col] != 0:
                f = m[r][col]
                m[r] = [x - f * y for x, y in zip(m[r], m[col])]
    return [[m[idx[(a, b)]][size] for b in range(n)] for a in range(n)]


def test_university_example() -> None:
    arcs = [(0, 1), (0, 2), (1, 3), (3, 0), (2, 4), (4, 2)]
    s = exact(5, arcs, Fraction(4, 5))
    assert s[1][2] == Fraction(6250, 15113)
    assert s[3][4] == Fraction(5000, 15113)
    assert s[0][2] == Fraction(2000, 15113)
    assert s[0][1] == 0
    r = simrank(5, arcs, 0.8, 60)
    for a in range(5):
        for b in range(5):
            assert abs(r[a][b] - float(s[a][b])) < 1e-5
    assert round(r[1][2], 3) == 0.414
    assert round(r[3][4], 3) == 0.331


def test_edge_cases() -> None:
    assert simrank(0, [], 0.8, 5) == []
    assert simrank(1, [], 0.8, 5) == [[1.0]]
    assert simrank(2, [], 0.8, 5) == [[1.0, 0.0], [0.0, 1.0]]
    # two vertices with the same single in-neighbour
    assert simrank(3, [(0, 1), (0, 2)], 0.5, 3)[1][2] == 0.5
    # zero rounds gives the identity
    assert simrank(3, [(0, 1), (0, 2)], 0.5, 0)[1][2] == 0.0
    # self-loop: vertex 0 is its own in-neighbour
    r = simrank(2, [(0, 0), (0, 1)], 0.5, 40)
    assert abs(r[0][1] - 0.5) < 1e-12
    for bad in ((0.0, 1), (1.0, 1), (0.5, -1)):
        try:
            simrank(2, [], bad[0], bad[1])
        except ValueError:
            pass
        else:
            raise AssertionError("expected ValueError")
    assert rounds_for(0.5, 0.5) == 0
    assert rounds_for(0.25, 0.5) == 1
    assert rounds_for(0.2, 0.5) == 2
    assert rounds_for(1e-4, 0.8) == 41


def test_random_against_definition() -> None:
    rng = random.Random(20021)
    for _ in range(500):
        n = rng.randint(1, 4)
        p = rng.random()
        arcs = [(u, v) for u in range(n) for v in range(n) if rng.random() < p]
        c = Fraction(rng.randint(1, 9), 10)
        k = rng.randint(0, 6)
        s = exact(n, arcs, c)
        r = simrank(n, arcs, float(c), k)
        bound = float(c) ** (k + 1)
        for a in range(n):
            for b in range(n):
                err = float(s[a][b]) - r[a][b]
                assert -1e-12 <= err <= bound + 1e-12
                assert abs(r[a][b] - r[b][a]) < 1e-12
                assert 0.0 <= r[a][b] <= 1.0
