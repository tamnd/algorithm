# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kung-algorithm/. The authors are listed in prov/R32A7X.jsonl.

import random
import time
from fractions import Fraction as Fr

from kung_algorithm import kung


def dominates(a, b) -> bool:
    return all(x <= y for x, y in zip(a, b)) and tuple(a) != tuple(b)


def brute(points):
    """Check all pairs."""
    return [i for i, y in enumerate(points) if not any(dominates(z, y) for z in points)]


def test_example() -> None:
    pts = [(2, 9), (3, 6), (4, 7), (5, 4), (7, 3), (8, 5), (9, 1)]
    assert kung(pts) == [0, 1, 3, 4, 6]


def test_example_three_objectives() -> None:
    pts = [(0, 5, 5), (5, 0, 5), (5, 5, 0), (1, 1, 9), (1, 1, 10), (6, 6, 6)]
    assert kung(pts) == [0, 1, 2, 3]


def test_edges() -> None:
    assert kung([]) == []
    assert kung([(1, 2)]) == [0]
    assert kung([(1, 2), (1, 2)]) == [0, 1]
    assert kung([(3,), (1,), (1,), (2,)]) == [1, 2]
    assert kung([(1, 1), (1, 2), (2, 1)]) == [0]
    assert kung([(1, 2), (2, 1)]) == [0, 1]
    # A chain: only the first point survives.
    assert kung([(i, i, i) for i in range(10)]) == [0]
    # An antichain: every point survives.
    assert kung([(i, 9 - i, (i * 7) % 10) for i in range(10)]) == list(range(10))
    # Exact rational entries.
    pts = [(Fr(1, 3), Fr(2, 3)), (Fr(1, 2), Fr(1, 2)), (Fr(2, 3), Fr(2, 3))]
    assert kung(pts) == [0, 1]


def test_random_against_brute_force() -> None:
    rng = random.Random(1975)
    for trial in range(1500):
        p = rng.randint(1, 6)
        n = rng.randint(1, 40)
        hi = rng.choice([1, 2, 3, 5, 10, 100])
        pts = [tuple(rng.randint(0, hi) for _ in range(p)) for _ in range(n)]
        assert kung(pts) == brute(pts), (trial, pts)


def test_random_antichains() -> None:
    # Points on the plane x_1 + ... + x_p = c are pairwise nondominated.
    rng = random.Random(7)
    for _ in range(200):
        p = rng.randint(2, 5)
        n = rng.randint(1, 30)
        pts = []
        for _ in range(n):
            v = [rng.randint(0, 20) for _ in range(p - 1)]
            v.append(100 - sum(v))
            pts.append(tuple(v))
        assert kung(pts) == brute(pts)


def test_medium_against_brute_force() -> None:
    rng = random.Random(3)
    for p in (2, 3, 4, 5):
        pts = [tuple(rng.randint(0, 30) for _ in range(p)) for _ in range(300)]
        assert kung(pts) == brute(pts)


def test_speed() -> None:
    rng = random.Random(42)
    for p in (2, 3, 4, 5):
        pts = [tuple(rng.random() for _ in range(p)) for _ in range(3000)]
        t = time.perf_counter()
        res = kung(pts)
        assert time.perf_counter() - t < 5
        # Spot check: no returned point is dominated by a random sample.
        sample = rng.sample(pts, 200)
        for i in res[:50]:
            assert not any(dominates(z, pts[i]) for z in sample)
