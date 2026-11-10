# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hochbaum-shmoys-makespan-ptas/. The authors are listed in prov/AYZTA8.jsonl.

import random
from fractions import Fraction
from itertools import product

from hochbaum_shmoys_makespan_ptas import dual_test, hochbaum_shmoys_makespan_ptas, makespan


def brute_opt(p, m):
    best = sum(p)
    for a in product(range(m), repeat=len(p)):
        if a and a[0] != 0:
            continue
        best = min(best, makespan(p, m, a))
    return best


def test_example() -> None:
    p, m = [7, 7, 6, 6, 5, 4, 4, 3], 3
    assert brute_opt(p, m) == 14
    stats: dict = {}
    s = dual_test(p, m, 14, 3, stats)
    assert s == [0, 0, 1, 1, 1, 2, 2, 2] and makespan(p, m, s) == 17
    assert stats == {"states": 12, "configs": 6, "sizes": 2, "large": 5}
    assert dual_test(p, m, 11, 3) is None
    sched, calls = hochbaum_shmoys_makespan_ptas(p, m, 3)
    assert makespan(p, m, sched) == 17 and calls == 4


def test_dual_contract_against_brute_force() -> None:
    rng = random.Random(1987)
    for _ in range(120):
        n, m, k = rng.randint(1, 7), rng.randint(1, 3), rng.randint(1, 4)
        p = [rng.randint(1, 12) for _ in range(n)]
        opt = brute_opt(p, m)
        for t in range(1, sum(p) + 1):
            s = dual_test(p, m, t, k)
            if s is None:
                assert opt > t
            else:
                assert sorted(set(s)) <= list(range(m)) and len(s) == n
                assert makespan(p, m, s) <= Fraction(k + 1, k) * t


def test_ratio_for_several_eps() -> None:
    rng = random.Random(34)
    for k in (1, 2, 3, 5):
        for _ in range(40):
            n, m = rng.randint(1, 8), rng.randint(1, 3)
            p = [rng.randint(1, 30) for _ in range(n)]
            opt = brute_opt(p, m)
            assert opt >= max(max(p), Fraction(sum(p), m))  # the lower bound of the search
            sched, calls = hochbaum_shmoys_makespan_ptas(p, m, k)
            assert makespan(p, m, sched) <= Fraction(k + 1, k) * opt
            lb = max(max(p), -(-sum(p) // m))
            assert calls <= (lb + 1).bit_length() + 1


def test_state_and_size_bounds() -> None:
    rng = random.Random(5)
    for _ in range(60):
        k = rng.randint(1, 4)
        n, m = rng.randint(1, 10), rng.randint(1, 4)
        p = [rng.randint(1, 40) for _ in range(n)]
        t = rng.randint(max(p), sum(p))
        stats: dict = {}
        dual_test(p, m, t, k, stats)
        if "sizes" not in stats:
            continue
        assert stats["sizes"] <= k * k - k + 1
        assert stats["states"] <= (stats["large"] + 1) ** stats["sizes"]
        for _ in range(1):
            assert stats["configs"] <= (k + 1) ** stats["sizes"]
