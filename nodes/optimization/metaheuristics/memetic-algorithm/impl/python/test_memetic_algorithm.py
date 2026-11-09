# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/memetic-algorithm/. The authors are listed in prov/P2XYTJ.jsonl.

import math
import random

from memetic_algorithm import (
    canonical,
    is_two_opt_optimal,
    memetic_algorithm,
    order_crossover,
    tour_length,
    two_opt,
    two_opt_delta,
)


def instance(n: int, seed: int) -> list[list[float]]:
    r = random.Random(seed)
    pts = [(r.random(), r.random()) for _ in range(n)]
    return [[math.dist(p, q) for q in pts] for p in pts]


def held_karp(d: list[list[float]]) -> float:
    """The optimal tour length by dynamic programming over subsets, O(2^n n^2)."""
    n = len(d)
    inf = float("inf")
    dp = [[inf] * n for _ in range(1 << n)]
    dp[1][0] = 0.0
    for s in range(1, 1 << n, 2):
        for j in range(n):
            if dp[s][j] == inf:
                continue
            for k in range(1, n):
                if not s & (1 << k):
                    t = s | (1 << k)
                    dp[t][k] = min(dp[t][k], dp[s][j] + d[j][k])
    return min(dp[(1 << n) - 1][j] + d[j][0] for j in range(1, n))


def test_order_crossover_example_and_permutations() -> None:
    a = [1, 2, 3, 4, 5, 6, 7, 8]
    b = [3, 7, 5, 1, 6, 8, 2, 4]
    assert order_crossover(a, b, 2, 4) == [1, 6, 3, 4, 5, 8, 2, 7]
    rng = random.Random(1)
    for _ in range(500):
        n = rng.randrange(4, 12)
        a, b = rng.sample(range(n), n), rng.sample(range(n), n)
        i, j = sorted(rng.sample(range(n), 2))
        c = order_crossover(a, b, i, j)
        assert sorted(c) == list(range(n))
        assert c[i : j + 1] == a[i : j + 1]
        rest = [x for x in c[j + 1 :] + c[:i]]
        assert rest == [x for x in b[j + 1 :] + b[: j + 1] if x not in a[i : j + 1]]


def test_two_opt_delta_is_exact() -> None:
    rng = random.Random(2)
    d = instance(10, 2)
    for _ in range(300):
        t = rng.sample(range(10), 10)
        i = rng.randrange(0, 8)
        j = rng.randrange(i + 2, 10 if i > 0 else 9)
        u = t[: i + 1] + t[i + 1 : j + 1][::-1] + t[j + 1 :]
        assert math.isclose(tour_length(d, u) - tour_length(d, t), two_opt_delta(d, t, i, j), abs_tol=1e-12)


def test_two_opt_returns_a_local_optimum() -> None:
    rng = random.Random(3)
    for n in (5, 9, 15):
        d = instance(n, n)
        for _ in range(30):
            t = rng.sample(range(n), n)
            u = two_opt(d, t)
            assert sorted(u) == list(range(n))
            assert tour_length(d, u) <= tour_length(d, t) + 1e-12
            assert is_two_opt_optimal(d, u)


def test_canonical_identifies_the_same_cycle() -> None:
    t = [3, 0, 4, 1, 2]
    rotations = [t[k:] + t[:k] for k in range(5)]
    forms = {canonical(r) for r in rotations} | {canonical(r[::-1]) for r in rotations}
    assert forms == {(0, 3, 2, 1, 4)}
    assert canonical([0, 1, 2, 3, 4]) != canonical([0, 2, 1, 3, 4])


def test_population_invariants() -> None:
    d = instance(13, 10)
    seen = []

    def check(s, pop, lengths):
        assert len(pop) == 6
        for t, length in zip(pop, lengths):
            assert sorted(t) == list(range(13))
            assert math.isclose(length, tour_length(d, t))
            assert is_two_opt_optimal(d, t)
        seen.append(sorted(lengths))

    memetic_algorithm(d, 6, 80, 0.2, random.Random(4), check)
    for prev, cur in zip(seen, seen[1:]):
        # Replace-worst: the sorted lengths never get worse in any rank.
        assert all(c <= p + 1e-12 for p, c in zip(prev, cur))
        changed = sum(1 for p, c in zip(prev, cur) if p != c) > 0
        if changed:
            assert sum(cur) < sum(prev)


def test_replacement_never_adds_a_duplicate() -> None:
    d = instance(12, 16)
    counts = []

    def check(s, pop, lengths):
        counts.append(len({canonical(t) for t in pop}))

    memetic_algorithm(d, 5, 80, 0.2, random.Random(5), check)
    # The number of distinct tours never falls, since a child enters only if it is new.
    assert all(b >= a for a, b in zip(counts, counts[1:]))


def test_fixed_seed_reaches_the_optimum_from_a_worse_start() -> None:
    for n, inst, seed in ((12, 10, 1), (13, 10, 0)):
        d = instance(n, inst)
        opt = held_karp(d)
        tour, length, hist = memetic_algorithm(d, 4, 100, 0.2, random.Random(seed))
        assert hist[0] > opt + 1e-9
        assert sorted(tour) == list(range(n))
        assert math.isclose(length, opt, rel_tol=1e-12)
        assert all(hist[k + 1] <= hist[k] for k in range(len(hist) - 1))
