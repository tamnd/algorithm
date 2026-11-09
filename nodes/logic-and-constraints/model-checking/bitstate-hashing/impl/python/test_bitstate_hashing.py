# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bitstate-hashing/. The authors are listed in prov/0JT58E.jsonl.

import random

from bitstate_hashing import bitstate_hashing, exact_search, hashes, no_collision_bound


def random_graph(rng, n):
    succ = {v: [rng.randrange(n) for _ in range(rng.randint(0, 3))] for v in range(n)}
    return lambda v: succ[v]


def counters(n, k):
    """n counters mod k that move one at a time: k^n states."""

    def succ(s):
        for i in range(n):
            t = list(s)
            t[i] = (t[i] + 1) % k
            yield tuple(t)

    return succ


def test_example() -> None:
    succ = counters(3, 4)
    exact = exact_search((0, 0, 0), succ)
    assert len(exact) == 64
    big = bitstate_hashing((0, 0, 0), succ, m=1 << 16, k=2)
    assert set(big) == exact and len(big) == 64
    small = bitstate_hashing((0, 0, 0), succ, m=64, k=1)
    assert set(small) <= exact and len(small) < 64


def test_large_table_equals_exact() -> None:
    rng = random.Random(1988)
    for trial in range(600):
        n = rng.randint(1, 60)
        succ = random_graph(rng, n)
        init = rng.randrange(n)
        exact = exact_search(init, succ)
        got = bitstate_hashing(init, succ, m=1 << 20, k=rng.randint(1, 3), salt=bytes([trial % 256]))
        assert set(got) == exact
        assert len(got) == len(exact)  # no state is explored twice


def test_small_table_is_sound() -> None:
    rng = random.Random(1998)
    missed = 0
    for trial in range(600):
        n = rng.randint(5, 80)
        succ = random_graph(rng, n)
        exact = exact_search(0, succ)
        got = bitstate_hashing(0, succ, m=rng.randint(8, 64), k=rng.randint(1, 3), salt=bytes([trial % 256]))
        assert set(got) <= exact
        assert len(got) == len(set(got))
        missed += len(exact) - len(got)
    assert missed > 0


def test_hash_positions() -> None:
    hs = hashes((1, 2), 100, 5, b"x")
    assert len(hs) == 5 and all(0 <= h < 100 for h in hs)
    assert hs == hashes((1, 2), 100, 5, b"x")
    assert hs != hashes((1, 2), 100, 5, b"y")


def test_coverage_meets_the_bound() -> None:
    # 81 states; over many salts the share of complete searches is at least the bound.
    succ = counters(4, 3)
    exact = exact_search((0, 0, 0, 0), succ)
    n = len(exact)
    for m, k in ((1 << 14, 1), (1 << 12, 2), (1 << 12, 3)):
        bound = no_collision_bound(n, m, k)
        assert 0.5 < bound < 1
        trials = 400
        full = sum(
            len(bitstate_hashing((0, 0, 0, 0), succ, m, k, salt=t.to_bytes(2, "little"))) == n
            for t in range(trials)
        )
        assert full / trials >= bound - 0.05


def test_bound_formula() -> None:
    assert no_collision_bound(1, 10, 1) == 1.0
    assert abs(no_collision_bound(30, 4096, 1) - (1 - 30 * 29 / (2 * 4096))) < 1e-12
