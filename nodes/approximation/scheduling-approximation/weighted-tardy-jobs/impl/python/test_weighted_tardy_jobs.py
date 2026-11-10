# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/weighted-tardy-jobs/. The authors are listed in prov/44W58E.jsonl.

import itertools
import random
from fractions import Fraction

from weighted_tardy_jobs import fptas, is_feasible, late_weight, lawler_moore


def brute_force(p, d, w):
    n = len(p)
    best = None
    for mask in range(1 << n):
        on = [j for j in range(n) if mask >> j & 1]
        if is_feasible(p, d, on):
            v = sum(w[j] for j in range(n) if not mask >> j & 1)
            if best is None or v < best:
                best = v
    return best


def check_solution(p, d, w, on_time, late, value):
    assert sorted(on_time + late) == list(range(len(p)))
    assert is_feasible(p, d, on_time)
    # A job of the late list may still finish on time when it runs after the
    # on-time jobs, so the schedule is never worse than the returned value.
    assert value == sum(w[j] for j in late)
    assert late_weight(p, d, w, on_time + late) <= value


def test_page_example() -> None:
    p = [3, 2, 4, 1, 3, 2]
    d = [4, 5, 6, 8, 9, 10]
    w = [5, 4, 7, 2, 6, 3]
    on_time, late, value = lawler_moore(p, d, w)
    check_solution(p, d, w, on_time, late, value)
    assert value == 9 == brute_force(p, d, w)
    assert min(late_weight(p, d, w, o) for o in itertools.permutations(range(6))) == 9


def test_lawler_moore_against_brute_force() -> None:
    rng = random.Random(61)
    for _ in range(300):
        n = rng.randint(1, 9)
        p = [rng.randint(0, 6) for _ in range(n)]
        d = [rng.randint(-1, 4 * n) for _ in range(n)]
        w = [rng.randint(0, 20) for _ in range(n)]
        on_time, late, value = lawler_moore(p, d, w)
        check_solution(p, d, w, on_time, late, value)
        assert value == brute_force(p, d, w)


def test_fptas_ratio() -> None:
    rng = random.Random(62)
    for eps in (Fraction(1), Fraction(1, 2), Fraction(1, 4), Fraction(1, 10)):
        for _ in range(120):
            n = rng.randint(1, 8)
            p = [rng.randint(1, 8) for _ in range(n)]
            d = [rng.randint(0, 4 * n) for _ in range(n)]
            w = [rng.randint(1, 1000) for _ in range(n)]
            on_time, late, value = fptas(p, d, w, eps)
            check_solution(p, d, w, on_time, late, value)
            opt = brute_force(p, d, w)
            assert opt <= value <= (1 + eps) * opt


def test_fptas_zero_and_bounds() -> None:
    assert fptas([1, 2], [5, 5], [3, 4], Fraction(1, 2)) == ([0, 1], [], 0)
    rng = random.Random(63)
    for _ in range(200):
        n = rng.randint(1, 8)
        p = [rng.randint(1, 8) for _ in range(n)]
        d = [rng.randint(0, 3 * n) for _ in range(n)]
        w = [rng.randint(1, 50) for _ in range(n)]
        if is_feasible(p, d, range(n)):
            continue
        tstar = max(x for x in w if not is_feasible(p, d, [j for j in range(n) if w[j] >= x]))
        opt = brute_force(p, d, w)
        assert tstar <= opt <= n * tstar


def test_complement_approximation_is_not_enough() -> None:
    # Keeping job 0 alone has 90 percent of the best on-time weight but 100 times the late weight.
    p, d, w = [10, 1, 10], [11, 11, 11], [900, 99, 1]
    best_on_time = sum(w) - brute_force(p, d, w)
    assert best_on_time == 999 and brute_force(p, d, w) == 1
    assert 900 >= Fraction(9, 10) * best_on_time
    assert late_weight(p, d, w, [0, 2, 1]) == 100
    assert fptas(p, d, w, Fraction(1, 10))[2] == 1


def test_edges() -> None:
    assert lawler_moore([], [], []) == ([], [], 0)
    assert fptas([], [], [], 1) == ([], [], 0)
    assert lawler_moore([3], [2], [5]) == ([], [0], 5)
