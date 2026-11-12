# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/pool-adjacent-violators/. The authors are listed in prov/9PKVV8.jsonl.

import itertools
import random
from fractions import Fraction as F

from pool_adjacent_violators import blocks, pool_adjacent_violators


def sse(y, w, z):
    return sum(c * (a - b) ** 2 for a, c, b in zip(y, w, z))


def brute_force(y, w):
    """Best fit over all splits into consecutive blocks whose weighted means do not decrease.

    The optimum is constant on intervals, with each value equal to the weighted mean
    of its interval, so it is one of these candidates.
    """
    n = len(y)
    if n == 0:
        return []
    best = None
    for cuts in itertools.product([0, 1], repeat=max(n - 1, 0)):
        bounds = [0] + [i + 1 for i in range(n - 1) if cuts[i]] + [n]
        z = []
        for a, b in zip(bounds, bounds[1:]):
            m = sum(F(w[i]) * y[i] for i in range(a, b)) / sum(w[a:b])
            z.extend([m] * (b - a))
        if all(z[i] <= z[i + 1] for i in range(n - 1)):
            if best is None or sse(y, w, z) < sse(y, w, best):
                best = z
    return best or []


def av(y, w, j, k):
    return sum(F(w[i]) * y[i] for i in range(j, k + 1)) / sum(w[j : k + 1])


def max_min(y, w):
    n = len(y)
    return [max(min(av(y, w, j, k) for k in range(i, n)) for j in range(i + 1)) for i in range(n)]


def min_max(y, w):
    n = len(y)
    return [min(max(av(y, w, j, k) for j in range(i + 1)) for k in range(i, n)) for i in range(n)]


def test_example() -> None:
    y = [4, 5, 7, 2, 3, 8, 6, 9]
    z = pool_adjacent_violators(y)
    assert z == [4, F(17, 4), F(17, 4), F(17, 4), F(17, 4), 7, 7, 9]
    assert sse(y, [1] * 8, z) == F(67, 4)


def test_edges() -> None:
    assert pool_adjacent_violators([]) == []
    assert pool_adjacent_violators([7]) == [7]
    assert pool_adjacent_violators([2, 2, 2]) == [2, 2, 2]
    assert pool_adjacent_violators([1, 2, 3]) == [1, 2, 3]
    assert pool_adjacent_violators([3, 2, 1]) == [2, 2, 2]
    assert pool_adjacent_violators([3, 1], [3, 1]) == [F(5, 2), F(5, 2)]


def test_floats() -> None:
    z = pool_adjacent_violators([1.0, 0.0, 2.5], [1.0, 1.0, 2.0])
    assert all(abs(a - b) < 1e-12 for a, b in zip(z, [0.5, 0.5, 2.5]))


def test_against_brute_force_and_min_max() -> None:
    rng = random.Random(7)
    for _ in range(600):
        n = rng.randrange(0, 8)
        y = [rng.randrange(-5, 6) for _ in range(n)]
        w = [rng.randrange(1, 4) for _ in range(n)]
        z = pool_adjacent_violators(y, w)
        assert all(z[i] <= z[i + 1] for i in range(n - 1))
        assert z == brute_force(y, w)
        assert z == max_min(y, w) == min_max(y, w)


def test_block_conditions() -> None:
    rng = random.Random(11)
    for _ in range(500):
        n = rng.randrange(1, 12)
        y = [rng.randrange(-9, 10) for _ in range(n)]
        w = [rng.randrange(1, 5) for _ in range(n)]
        z = pool_adjacent_violators(y, w)
        for a, b in blocks(z):
            # The value is the weighted mean, and each prefix of the block has partial sum >= 0.
            run = 0
            for i in range(a, b):
                run += w[i] * (y[i] - z[i])
                assert run >= 0
            assert run == 0


def test_linear_number_of_merges_on_decreasing_input() -> None:
    n = 2000
    z = pool_adjacent_violators(list(range(n, 0, -1)))
    assert z == [F(n + 1, 2)] * n
