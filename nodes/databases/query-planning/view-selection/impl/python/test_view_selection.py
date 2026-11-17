# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/view-selection/. The authors are listed in prov/QEVP9Z.jsonl.

import random
from fractions import Fraction
from itertools import combinations

from view_selection import Lattice, cube, greedy, greedy_ratio_bound, optimal

M = 10 ** 6


def name(views, v):
    return "".join(sorted(views[v])) or "none"


def test_cube_example():
    size = {frozenset("psc"): 6 * M, frozenset("pc"): 6 * M, frozenset("ps"): 8 * 10 ** 5,
            frozenset("sc"): 6 * M, frozenset("p"): 2 * 10 ** 5, frozenset("s"): 10 ** 4,
            frozenset("c"): 10 ** 5, frozenset(): 1}
    lat, views = cube("psc", size)
    assert lat.total_cost([]) == 48 * M
    S, gains = greedy(lat, 3)
    assert [name(views, v) for v in S] == ["ps", "c", "s"]
    assert gains == [20_800_000, 6_600_000, 880_000]
    assert lat.total_cost(S) == 19_720_000
    assert optimal(lat, 3)[0] == sum(gains)


def hand_lattice():
    # views: 0 T (top), 1 M, 2 A, 3 B, 4 L1, 5 L2, 6 L3, 7 L4
    anc = [set(), {0}, {0}, {0}, {0, 1, 2}, {0, 1, 2}, {0, 1, 3}, {0, 1, 3}]
    return Lattice([100, 50, 40, 40, 40, 40, 40, 40], [frozenset(a) for a in anc], 0)


def test_greedy_can_be_suboptimal():
    lat = hand_lattice()
    S, gains = greedy(lat, 2)
    assert S == [1, 2] and gains == [250, 80]
    best, sets = optimal(lat, 2)
    assert best == 360 and sets == (2, 3)
    assert Fraction(sum(gains), best) == Fraction(11, 12) >= greedy_ratio_bound(2) == Fraction(3, 4)


def random_cube(rng):
    dims = "abcd"[:rng.randrange(2, 5)]
    n_rows = rng.choice([100, 1000, 5000])
    dom = {x: rng.randrange(1, 30) for x in dims}
    size = {}
    for r in range(len(dims) + 1):
        for c in combinations(dims, r):
            p = 1
            for x in c:
                p *= dom[x]
            size[frozenset(c)] = min(n_rows, p)
    size[frozenset(dims)] = n_rows
    lat, _ = cube(dims, size)
    if rng.random() < 0.5:
        lat.freq = [Fraction(rng.randrange(1, 5)) for _ in range(lat.m)]
    return lat


def random_poset(rng):
    m = rng.randrange(2, 10)
    anc = [frozenset()]
    for w in range(1, m):
        parents = [p for p in range(w) if rng.random() < 0.4] or [0]
        a = set()
        for p in parents:
            a |= anc[p] | {p}
        anc.append(frozenset(a))
    size = [1000] + [rng.randrange(1, 1000) for _ in range(m - 1)]
    freq = [rng.randrange(0, 4) for _ in range(m)]
    return Lattice(size, anc, 0, freq)


def test_greedy_bound_against_brute_force():
    rng = random.Random(1996)
    checks = 0
    for t in range(600):
        lat = random_cube(rng) if t % 2 else random_poset(rng)
        k = rng.randrange(1, 5)
        S, gains = greedy(lat, k)
        got = lat.benefit(S)
        assert got == sum(gains)
        best, _ = optimal(lat, k)
        assert got <= best
        assert got >= greedy_ratio_bound(k) * best
        checks += 1
    assert checks >= 500


def test_benefit_is_monotone_and_submodular():
    rng = random.Random(3)
    for _ in range(200):
        lat = random_poset(rng)
        cand = [v for v in range(lat.m) if v != lat.top]
        A = {v for v in cand if rng.random() < 0.3}
        B = A | {v for v in cand if rng.random() < 0.3}
        for v in cand:
            if v in B:
                continue
            gain_a = lat.benefit(A | {v}) - lat.benefit(A)
            gain_b = lat.benefit(B | {v}) - lat.benefit(B)
            assert gain_a >= gain_b >= 0


def test_bound_values():
    assert greedy_ratio_bound(1) == 1
    assert greedy_ratio_bound(2) == Fraction(3, 4)
    assert greedy_ratio_bound(3) == Fraction(19, 27)
    assert all(greedy_ratio_bound(k) > Fraction(632, 1000) for k in range(1, 40))
