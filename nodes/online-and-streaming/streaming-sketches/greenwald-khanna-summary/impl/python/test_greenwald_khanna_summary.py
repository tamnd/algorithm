# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/greenwald-khanna-summary/. The authors are listed in prov/C80D8X.jsonl.

import bisect
import math
import random

from greenwald_khanna_summary import GKSummary, gk_quantiles


def run_and_check(stream: list, eps: float, check_every: bool = False) -> GKSummary:
    """Feed the stream and check every rank query exactly against the sorted data."""
    s = GKSummary(eps)
    seen: list = []
    for idx, x in enumerate(stream):
        s.insert(x)
        seen.append(x)
        if check_every or idx == len(stream) - 1:
            s.check_invariant()
            check_queries(s, seen, eps)
    return s


def check_queries(s: GKSummary, seen: list, eps: float) -> None:
    n = len(seen)
    data = sorted(seen)
    keys = sorted((x, i + 1) for i, x in enumerate(seen))
    # each stored tuple brackets the true rank of its own item
    for v, arrival, lo, hi in s.rank_bounds():
        true = bisect.bisect_left(keys, (v, arrival)) + 1
        assert lo <= true <= hi
    # every rank query has an answer whose rank range meets [r - eps n, r + eps n]
    for r in range(1, n + 1):
        v = s.query(r)
        low = bisect.bisect_left(data, v) + 1
        high = bisect.bisect_right(data, v)
        assert low <= high
        assert low <= r + eps * n and high >= r - eps * n, (r, v, low, high)


def test_worked_example() -> None:
    stream = [12, 3, 17, 8, 1, 15, 6, 10, 4, 14, 9, 2, 19, 7, 11, 5, 18, 13, 16, 20]
    s = run_and_check(stream, 0.1, check_every=True)
    assert s.ell == 5
    assert [k[0] for k in s.keys] == [4, 8, 12, 13, 17, 19, 20]
    assert s.g == [4, 4, 4, 1, 4, 2, 1]
    assert s.delta == [0, 0, 0, 2, 0, 0, 0]
    assert s.band == [2, 2, 2, 0, 2, 1, 0]
    assert s.query(10) == 12
    assert gk_quantiles(stream, 0.1, [1, 10, 20]) == [1, 12, 20]


def test_small_and_equal() -> None:
    s = GKSummary(0.25)
    s.insert(5)
    assert s.query(1) == 5
    run_and_check([7] * 40, 0.1, check_every=True)
    run_and_check([1, 2], 0.3, check_every=True)


def test_adversarial_orders() -> None:
    n = 400
    for eps in (0.05, 0.1, 0.2):
        orders = [
            list(range(n)),
            list(range(n, 0, -1)),
            [i // 2 if i % 2 == 0 else n - i for i in range(n)],
            [(i * 37) % n for i in range(n)],
            [n // 2 + ((-1) ** i) * (i // 2) for i in range(n)],
            [i % 3 for i in range(n)],
        ]
        for stream in orders:
            run_and_check(stream, eps, check_every=False)


def test_random_streams_every_prefix() -> None:
    rng = random.Random(2001)
    for trial in range(500):
        n = rng.randint(1, 60)
        eps = rng.choice([0.05, 0.1, 0.15, 0.25, 0.4])
        hi = rng.choice([3, 10, 1000])
        stream = [rng.randint(0, hi) for _ in range(n)]
        run_and_check(stream, eps, check_every=(trial % 5 == 0))


def test_space_grows_like_log() -> None:
    rng = random.Random(7)
    for eps in (0.02, 0.05):
        for n in (2000, 6000):
            for stream in (list(range(n)), [rng.random() for _ in range(n)]):
                s = GKSummary(eps)
                for x in stream:
                    s.insert(x)
                s.check_invariant()
                bound = (1 / eps) * math.log2(2 * eps * n) + 2
                assert len(s) <= bound, (eps, n, len(s), bound)
