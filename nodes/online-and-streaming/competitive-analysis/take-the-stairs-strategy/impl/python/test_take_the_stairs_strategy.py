# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/take-the-stairs-strategy/. The authors are listed in prov/F0PJDM.jsonl.

import random
from fractions import Fraction

from take_the_stairs_strategy import arrival_time, opt_time, wait_limit, worst_ratio


def test_example_15_45() -> None:
    e, s = 15, 45
    assert wait_limit(e, s) == 30
    assert arrival_time(10, e, s) == 25
    assert opt_time(10, e, s) == 25
    assert arrival_time(30, e, s) == 45
    assert arrival_time(31, e, s) == 75
    assert opt_time(31, e, s) == 45
    assert arrival_time(None, e, s) == 75
    assert Fraction(arrival_time(None, e, s), opt_time(None, e, s)) == Fraction(5, 3)


def test_worst_ratios_of_other_waits() -> None:
    e, s = 15, 45
    table = {0: Fraction(3), 10: Fraction(11, 5), 20: Fraction(13, 7), 30: Fraction(5, 3), 40: Fraction(17, 9), 60: Fraction(7, 3)}
    for w, r in table.items():
        assert worst_ratio(e, s, w) == r


def test_s_minus_e_is_the_best_wait() -> None:
    rng = random.Random(915)
    for _ in range(300):
        s = Fraction(rng.randint(2, 80))
        e = Fraction(rng.randint(1, int(s) - 1))
        best = worst_ratio(e, s, s - e)
        assert best == 2 - e / s
        for _ in range(30):
            w = Fraction(rng.randint(0, 4 * int(s)), rng.randint(1, 4))
            if w != s - e:
                assert worst_ratio(e, s, w) > best


def test_worst_ratio_is_a_true_supremum() -> None:
    rng = random.Random(23)
    for _ in range(200):
        s = Fraction(rng.randint(2, 40))
        e = Fraction(rng.randint(1, int(s) - 1))
        w = Fraction(rng.randint(0, 3 * int(s)), rng.randint(1, 3))
        sup = worst_ratio(e, s, w)
        times = [Fraction(i, 8) for i in range(0, 8 * int(4 * s))] + [None, w, w + Fraction(1, 10**9)]
        seen = max(Fraction(arrival_time(t, e, s, w)) / opt_time(t, e, s) for t in times)
        assert seen <= sup
        assert sup - seen < Fraction(1, 10**6)


def test_strategy_meets_its_bound() -> None:
    rng = random.Random(4)
    for _ in range(2000):
        s = Fraction(rng.randint(1, 100), rng.randint(1, 5))
        e = Fraction(rng.randint(0, 120), rng.randint(1, 5))
        t = None if rng.random() < 0.1 else Fraction(rng.randint(0, 600), rng.randint(1, 7))
        a = arrival_time(t, e, s)
        o = opt_time(t, e, s)
        if e >= s:
            assert a == s and a <= o
        else:
            assert a <= (2 - e / s) * o


def test_bad_input() -> None:
    for e, s in ((-1, 5), (1, 0)):
        try:
            wait_limit(e, s)
        except ValueError:
            continue
        raise AssertionError("expected ValueError")
