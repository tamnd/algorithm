# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/package-merge/. The authors are listed in prov/Y4RNV8.jsonl.

import heapq
import random
from fractions import Fraction
from functools import lru_cache
from itertools import combinations_with_replacement

import pytest

from package_merge import cost, package_merge


def kraft(lengths) -> Fraction:
    return sum((Fraction(1, 2**l) for l in lengths), Fraction(0))


def exact_cost(weights, limit) -> float:
    """Level-by-level dynamic program over weights in non-increasing order."""
    ws = sorted(weights, reverse=True)
    n = len(ws)
    prefix = [0]
    for x in ws:
        prefix.append(prefix[-1] + x)

    @lru_cache(maxsize=None)
    def best(d, i, a):
        result = float("inf")
        for k in range(min(a, n - i) + 1):
            here = d * (prefix[i + k] - prefix[i])
            if i + k == n:
                result = min(result, here)
            elif d < limit:
                nxt = min(2 * (a - k), n - i - k)
                if nxt > 0:
                    result = min(result, here + best(d + 1, i + k, nxt))
        return result

    return best(0, 0, 1)


def brute_cost(weights, limit) -> float:
    ws = sorted(weights, reverse=True)
    n = len(ws)
    best = None
    for ls in combinations_with_replacement(range(1, limit + 1), n):
        if kraft(ls) <= 1:
            c = sum(a * b for a, b in zip(ws, ls))
            best = c if best is None else min(best, c)
    return best


def huffman_cost(weights) -> float:
    h = list(weights)
    heapq.heapify(h)
    total = 0
    while len(h) > 1:
        a = heapq.heappop(h)
        b = heapq.heappop(h)
        total += a + b
        heapq.heappush(h, a + b)
    return total


def min_limit(n: int) -> int:
    return (n - 1).bit_length()  # ceil(log2 n)


def test_moffat_figure_6() -> None:
    # Moffat (2019), Section 4.1 and Figure 6.
    w = [20, 17, 6, 3, 2, 2, 2, 1, 1, 1]
    assert sorted(package_merge(w, 5)) == [2, 2, 3, 4, 4, 4, 4, 4, 5, 5]
    assert cost(w, package_merge(w, 5)) == 142
    assert sorted(package_merge(w, 4)) == [2, 2, 4, 4, 4, 4, 4, 4, 4, 4]
    assert cost(w, package_merge(w, 4)) == 146
    assert cost(w, package_merge(w, 9)) == 140
    with pytest.raises(ValueError):
        package_merge(w, 3)


def test_against_brute_force() -> None:
    rng = random.Random(41)
    for _ in range(150):
        n = rng.randint(2, 7)
        limit = rng.randint(min_limit(n), 6)
        w = [rng.randint(1, 40) for _ in range(n)]
        l = package_merge(w, limit)
        assert max(l) <= limit and kraft(l) == 1
        assert cost(w, l) == brute_cost(w, limit)


def test_against_dynamic_program() -> None:
    rng = random.Random(42)
    for _ in range(120):
        n = rng.randint(2, 30)
        w = [int(1 + 500 * rng.random() ** 5) for _ in range(n)]
        for limit in {min_limit(n), min_limit(n) + 1, rng.randint(min_limit(n), n)}:
            l = package_merge(w, limit)
            assert max(l) <= limit and kraft(l) == 1
            assert cost(w, l) == exact_cost(w, limit)


def test_tightest_limit() -> None:
    # L = ceil(log2 n) is the smallest feasible limit. For n = 2^k it
    # forces the flat code with all lengths k.
    rng = random.Random(43)
    for n in range(2, 40):
        w = [int(1 + 100 * rng.random() ** 4) for _ in range(n)]
        l = package_merge(w, min_limit(n))
        assert max(l) <= min_limit(n)
        assert cost(w, l) == exact_cost(w, min_limit(n))
        if n & (n - 1) == 0:
            assert set(l) == {min_limit(n)}


def test_large_limit_gives_huffman_cost() -> None:
    rng = random.Random(44)
    for _ in range(80):
        n = rng.randint(2, 40)
        w = [rng.randint(0, 100) for _ in range(n)]
        assert cost(w, package_merge(w, n - 1)) == huffman_cost(w)


def test_fibonacci_weights() -> None:
    fib = [1, 1]
    while len(fib) < 12:
        fib.append(fib[-1] + fib[-2])
    for limit in range(4, 12):
        assert cost(fib, package_merge(fib, limit)) == exact_cost(fib, limit)
