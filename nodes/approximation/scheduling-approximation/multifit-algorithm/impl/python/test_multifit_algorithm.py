# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/multifit-algorithm/. The authors are listed in prov/9QD5G8.jsonl.

import itertools
import random
from fractions import Fraction

from multifit_algorithm import first_fit_decreasing, multifit_algorithm


def brute_opt(p: list[int], m: int) -> int:
    if not p:
        return 0
    best = None
    for rest in itertools.product(range(m), repeat=len(p) - 1):
        load = [0] * m
        for x, i in zip(p, (0,) + rest):
            load[i] += x
        best = max(load) if best is None else min(best, max(load))
    return best


def makespan(p, machine, m):
    load = [0] * m
    for j, i in enumerate(machine):
        load[i] += p[j]
    return max(load)


def test_example() -> None:
    p = [3, 3, 2, 2, 2, 2]
    assert brute_opt(p, 2) == 7
    assert first_fit_decreasing(p, 7, 2) is None
    assert first_fit_decreasing(p, Fraction(799, 100), 2) is None
    assert first_fit_decreasing(p, 8, 2) == [[0, 1, 2], [3, 4, 5]]
    assert [makespan(p, multifit_algorithm(p, 2, k)[0], 2) for k in range(4)] == [14, 10, 8, 8]
    for k in range(0, 12):
        machine, hi = multifit_algorithm(p, 2, k)
        assert 8 <= hi <= 8 + Fraction(7, 2 ** k)
        if k >= 2:
            assert makespan(p, machine, 2) == 8


def test_edges() -> None:
    assert multifit_algorithm([], 3, 5) == ([], 0)
    assert multifit_algorithm([4], 1, 3)[0] == [0]
    machine, _ = multifit_algorithm([5, 1, 1], 3, 10)
    assert makespan([5, 1, 1], machine, 3) == 5
    assert first_fit_decreasing([6], 5, 3) is None


def test_against_brute_force() -> None:
    rng = random.Random(41)
    for _ in range(500):
        m = rng.randrange(1, 4)
        p = [rng.randrange(1, 13) for _ in range(rng.randrange(1, 8))]
        opt = brute_opt(p, m)
        for k in (0, 1, 3, 7):
            machine, hi = multifit_algorithm(p, m, k)
            assert all(0 <= i < m for i in machine)
            alg = makespan(p, machine, m)
            assert alg <= hi
            assert alg <= (Fraction(122, 100) + Fraction(1, 2 ** k)) * opt
            assert alg <= (Fraction(13, 11) + Fraction(1, 2 ** k)) * opt


def test_ffd_succeeds_at_13_11_opt() -> None:
    rng = random.Random(42)
    for _ in range(500):
        m = rng.randrange(1, 4)
        p = [rng.randrange(1, 15) for _ in range(rng.randrange(1, 8))]
        opt = brute_opt(p, m)
        assert first_fit_decreasing(p, Fraction(13, 11) * opt, m) is not None
        assert first_fit_decreasing(p, 2 * Fraction(sum(p), m) + max(p), m) is not None


def test_tight_instance_13_machines() -> None:
    # 13 bins of size 66: (40, 13, 13) x 8, (25, 25, 16) x 3, (25, 24, 17) x 2
    p = [40] * 8 + [25] * 8 + [13] * 16 + [16] * 3 + [24] * 2 + [17] * 2
    assert sum(p) == 13 * 66
    for c in (66, 70, 77, Fraction(7799, 100)):
        assert first_fit_decreasing(p, c, 13) is None
    assert first_fit_decreasing(p, 78, 13) is not None
    for k in (5, 10, 20):
        machine, hi = multifit_algorithm(p, 13, k)
        assert hi >= 78
        assert makespan(p, machine, 13) == 78
