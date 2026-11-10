# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/marzullo-algorithm/. The authors are listed in prov/61GKS9.jsonl.

import random

from marzullo_algorithm import brute_force, depth_at, marzullo, marzullo_with_faults, ntp_select


def test_page_example() -> None:
    iv = [(10, 14), (11, 15), (9, 12), (16, 18)]
    assert marzullo(iv) == (3, 11, 12)
    assert marzullo_with_faults(iv, 1) == (11, 12)
    assert marzullo_with_faults(iv, 0) is None


def test_edges() -> None:
    assert marzullo([]) == (0, None, None)
    assert marzullo([(3, 3)]) == (1, 3, 3)
    assert marzullo([(1, 2), (2, 3)]) == (2, 2, 2)  # closed intervals that touch meet
    assert marzullo([(1, 2), (3, 4)]) == (1, 1, 2)
    assert marzullo([(0, 10), (0, 10), (0, 10)]) == (3, 0, 10)


def test_against_brute_force() -> None:
    rng = random.Random(3)
    for _ in range(2000):
        k = rng.randrange(1, 9)
        iv = []
        for _ in range(k):
            a = rng.randrange(0, 20)
            iv.append((a, a + rng.randrange(0, 8)))
        best, a, b = marzullo(iv)
        bb, where = brute_force(iv)
        assert best == bb and a == where
        assert a <= b
        # Each point of [a, b] lies in exactly `best` intervals.
        for x in [a, b, (a + b) / 2]:
            assert depth_at(iv, x) == best
        # Just right of b the depth drops, or b is the right end of everything.
        assert depth_at(iv, b + 0.5) < best


def test_ntp_select_page_example() -> None:
    cands = [(0.010, 0.004), (0.012, 0.003), (0.011, 0.005), (0.050, 0.002)]
    l, u, f = ntp_select(cands)
    assert f == 1 and abs(l - 0.009) < 1e-12 and abs(u - 0.014) < 1e-12


def test_ntp_select_keeps_the_truth() -> None:
    rng = random.Random(11)
    hits = 0
    for _ in range(500):
        m = rng.randrange(3, 10)
        k = rng.randrange(0, (m + 1) // 2)  # k < m / 2 falsetickers
        cands = [(rng.uniform(-1, 1), rng.uniform(3, 5)) for _ in range(m - k)]
        for j in range(k):
            cands.append((100.0 * (j + 1) * rng.choice([-1, 1]), rng.uniform(0.1, 1)))
        rng.shuffle(cands)
        res = ntp_select(cands)
        assert res is not None
        l, u, f = res
        assert f == k and l <= 0 <= u
        hits += 1
    assert hits == 500


def test_ntp_select_fails_without_majority() -> None:
    cands = [(0.0, 1.0), (10.0, 1.0), (20.0, 1.0), (30.0, 1.0)]
    assert ntp_select(cands) is None
