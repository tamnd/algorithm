# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dyadic-intervals/. The authors are listed in prov/G0NHYJ.jsonl.

import bisect
import random

from dyadic_intervals import DyadicCounts, decompose, interval, prefix_decompose


def maximal_dyadic(a: int, b: int, levels: int) -> list[tuple[int, int]]:
    """Oracle: every dyadic interval inside [a, b] whose parent is not inside."""
    out = []
    for j in range(levels + 1):
        for k in range(1 << (levels - j)):
            lo, hi = interval(j, k)
            if a <= lo and hi <= b:
                if j == levels:
                    out.append((j, k))
                else:
                    plo, phi = interval(j + 1, k >> 1)
                    if not (a <= plo and phi <= b):
                        out.append((j, k))
    out.sort(key=lambda p: interval(*p)[0])
    return out


def test_worked_example() -> None:
    assert [interval(j, k) for j, k in decompose(3, 12, 4)] == [(3, 3), (4, 7), (8, 11), (12, 12)]
    assert [interval(j, k) for j, k in decompose(1, 14, 4)] == [
        (1, 1), (2, 3), (4, 7), (8, 11), (12, 13), (14, 14)]
    assert decompose(0, 15, 4) == [(4, 0)]
    assert [interval(j, k) for j, k in prefix_decompose(12, 4)] == [(0, 7), (8, 11), (12, 12)]


def test_all_ranges_small_universes() -> None:
    for levels in range(0, 7):
        u = 1 << levels
        worst = 0
        for a in range(u):
            for b in range(a, u):
                parts = decompose(a, b, levels)
                assert parts == maximal_dyadic(a, b, levels)
                covered = []
                for j, k in parts:
                    lo, hi = interval(j, k)
                    covered.extend(range(lo, hi + 1))
                assert covered == list(range(a, b + 1))  # disjoint, in order, exact
                assert len(parts) <= max(1, 2 * levels)
                worst = max(worst, len(parts))
                if a == 0:
                    pre = prefix_decompose(b, levels)
                    assert len(pre) <= levels + 1
                    assert sorted(pre, key=lambda p: p[1] << p[0]) == parts
        if levels >= 2:
            assert worst == 2 * levels - 2


def test_counts_and_quantiles() -> None:
    rng = random.Random(5)
    for trial in range(500):
        levels = rng.randint(1, 6)
        u = 1 << levels
        d = DyadicCounts(levels)
        data = []
        for _ in range(rng.randint(1, 40)):
            x = rng.randrange(u)
            d.update(x)
            data.append(x)
        if trial % 3 == 0 and len(data) > 1:  # a turnstile deletion
            x = data.pop(rng.randrange(len(data)))
            d.update(x, -1)
        d.check_invariant()
        data.sort()
        a = rng.randrange(u)
        b = rng.randrange(a, u)
        assert d.range_count(a, b) == bisect.bisect_right(data, b) - bisect.bisect_left(data, a)
        for r in range(1, len(data) + 1):
            assert d.quantile(r) == data[r - 1]
