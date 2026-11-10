# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dual-approximation/. The authors are listed in prov/DPDS4B.jsonl.

import random
from itertools import combinations, product

from dual_approximation import (dual_search, kcenter_dual_approximation, kcenter_two_dual,
                                makespan_dual_approximation, makespan_two_dual)


def loads(p, m, machine):
    load = [0] * m
    for j, i in enumerate(machine):
        load[i] += p[j]
    return load


def brute_makespan(p, m):
    return min(max(loads(p, m, a)) for a in product(range(m), repeat=len(p)))


def radius(dist, centers):
    return max(min(dist[v][c] for c in centers) for v in range(len(dist)))


def brute_kcenter(dist, k):
    n = len(dist)
    return min(radius(dist, c) for c in combinations(range(n), min(k, n)))


def random_metric(rng, n):
    pts = [(rng.randint(0, 20), rng.randint(0, 20)) for _ in range(n)]
    return [[abs(a[0] - b[0]) + abs(a[1] - b[1]) for b in pts] for a in pts]


def test_example() -> None:
    p, m = [5, 4, 3, 3, 3], 2
    assert brute_makespan(p, m) == 9
    assert makespan_two_dual(p, m, 8) is None  # 18 > 2 * 8
    machine, target, calls = makespan_dual_approximation(p, m)
    assert target == 9 and max(loads(p, m, machine)) == 10 and calls == 4
    x = [0, 1, 2, 10, 11, 20]
    dist = [[abs(a - b) for b in x] for a in x]
    assert brute_kcenter(dist, 2) == 9
    assert kcenter_two_dual(dist, 2, 2) is None
    centers, target, calls = kcenter_dual_approximation(dist, 2)
    assert centers == [0, 5] and target == 8 and radius(dist, centers) == 10 and calls == 5


def test_makespan_contract_and_ratio() -> None:
    rng = random.Random(1987)
    for _ in range(150):
        n, m = rng.randint(1, 7), rng.randint(1, 3)
        p = [rng.randint(1, 15) for _ in range(n)]
        opt = brute_makespan(p, m)
        for t in range(1, sum(p) + 1):
            s = makespan_two_dual(p, m, t)
            if s is None:
                assert opt > t
            else:
                assert max(loads(p, m, s)) <= 2 * t
        machine, target, _ = makespan_dual_approximation(p, m)
        assert target <= opt
        assert max(loads(p, m, machine)) <= 2 * opt


def test_kcenter_contract_and_ratio() -> None:
    rng = random.Random(1985)
    for _ in range(150):
        n, k = rng.randint(1, 8), rng.randint(1, 3)
        dist = random_metric(rng, n)
        opt = brute_kcenter(dist, k)
        for r in sorted({d for row in dist for d in row}):
            c = kcenter_two_dual(dist, k, r)
            if c is None:
                assert opt > r
            else:
                assert len(c) <= k and radius(dist, c) <= 2 * r
        centers, target, _ = kcenter_dual_approximation(dist, k)
        assert target <= opt and radius(dist, centers) <= 2 * opt


def test_call_count() -> None:
    for size in range(1, 70):
        cand = list(range(size))
        for opt in range(size):
            _, target, calls = dual_search(cand, lambda t: t if t >= opt else None)
            assert target == opt
            assert calls <= 1 + (size).bit_length()
