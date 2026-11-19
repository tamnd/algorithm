# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dynamic-time-warping/. The authors are listed in prov/JJFMC2.jsonl.

import math
import random

import pytest

from dynamic_time_warping import (
    STEP_PATTERNS,
    dtw,
    dtw_distance,
    is_warping_path,
    path_cost,
    sq_euclidean,
)

PATTERNS = list(STEP_PATTERNS)


def all_paths(n, m):
    """Every monotone warping path from (1, 1) to (n, m)."""
    out = []

    def go(path):
        i, j = path[-1]
        if (i, j) == (n, m):
            out.append(list(path))
            return
        for di, dj in ((1, 1), (1, 0), (0, 1)):
            if i + di <= n and j + dj <= m:
                path.append((i + di, j + dj))
                go(path)
                path.pop()

    go([(1, 1)])
    return out


def test_path_counts_are_delannoy_numbers():
    assert [len(all_paths(k, k)) for k in range(1, 7)] == [1, 3, 13, 63, 321, 1683]
    assert len(all_paths(2, 3)) == 5 and len(all_paths(1, 5)) == 1


@pytest.mark.parametrize("step", PATTERNS)
def test_against_brute_force(step):
    rng = random.Random(10 + PATTERNS.index(step))
    cache = {}
    for _ in range(120):
        n, m = rng.randint(1, 6), rng.randint(1, 6)
        x = [rng.randint(0, 9) for _ in range(n)]
        y = [rng.randint(0, 9) for _ in range(m)]
        if (n, m) not in cache:
            cache[(n, m)] = all_paths(n, m)
        best = min(path_cost(x, y, p, step=step) for p in cache[(n, m)])
        cost, path = dtw(x, y, step=step)
        assert cost == best  # integer inputs: the sums are exact
        assert is_warping_path(path, n, m)
        assert path_cost(x, y, path, step=step) == cost


def test_worked_example():
    x, y = [1, 3, 4, 9, 8], [1, 4, 9, 8]
    cost, path = dtw(x, y)
    assert cost == 1 and path == [(1, 1), (2, 2), (3, 2), (4, 3), (5, 4)]
    assert dtw(x, y, step="symmetric2")[0] == 2
    assert dtw_distance(x, y, step="symmetric2") == pytest.approx(2 / 9)
    assert dtw_distance(x, y, step="asymmetric") == pytest.approx(1 / 5)


def test_not_a_metric():
    a, b, c = [0], [2], [2, 2]
    assert dtw(a, b)[0] == 2 and dtw(b, c)[0] == 0 and dtw(a, c)[0] == 4
    assert dtw(a, c)[0] > dtw(a, b)[0] + dtw(b, c)[0]  # the triangle inequality fails
    # distance 0 between different sequences
    assert dtw([1, 2, 2, 3], [1, 2, 3])[0] == 0


def test_symmetry():
    rng = random.Random(3)
    for _ in range(50):
        x = [rng.randint(0, 9) for _ in range(rng.randint(1, 7))]
        y = [rng.randint(0, 9) for _ in range(rng.randint(1, 7))]
        for step in ("symmetric1", "symmetric2"):
            assert dtw(x, y, step=step)[0] == dtw(y, x, step=step)[0]
    # the asymmetric pattern is not symmetric
    assert dtw([0, 5], [0], step="asymmetric")[0] == 5
    assert dtw([0], [0, 5], step="asymmetric")[0] == 0


def test_identity_and_time_shift():
    x = [math.sin(0.3 * t) for t in range(40)]
    assert dtw(x, x)[0] == 0
    # a slowed copy (each sample twice) is at distance 0
    slow = [v for v in x for _ in range(2)]
    cost, path = dtw(x, slow)
    assert cost == 0
    assert len(path) == len(slow)


def test_tie_rule():
    # all costs 0: every path ties, and the traceback takes diagonals first
    cost, path = dtw([0, 0, 0], [0, 0])
    assert cost == 0 and path == [(1, 1), (2, 1), (3, 2)]


def test_vectors():
    x = [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0)]
    y = [(0.0, 0.0), (2.0, 0.0)]
    cost, path = dtw(x, y, dist=sq_euclidean)
    assert cost == pytest.approx(2.0)
    assert path_cost(x, y, path, dist=sq_euclidean) == pytest.approx(2.0)


def test_empty():
    with pytest.raises(ValueError):
        dtw([], [1])
