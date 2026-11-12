# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/pinwheel-scheduling/. The authors are listed in prov/TDMAY5.jsonl.

import itertools
import random
from fractions import Fraction

from pinwheel_scheduling import is_valid_cyclic, pinwheel_schedule


def density(a: list[int]) -> Fraction:
    return sum(Fraction(1, x) for x in a)


def test_known_schedulable() -> None:
    for a in ([3, 3, 3], [2, 4, 8, 8], [3, 4, 5, 8], [2, 4, 4], [1], [2, 2]):
        s = pinwheel_schedule(a)
        assert s is not None and is_valid_cyclic(a, s)
    assert density([2, 4, 8, 8]) == 1


def test_tight_instances() -> None:
    # Lowering any period of these makes them unschedulable.
    for a in ([3, 3, 3], [2, 4, 8, 8], [3, 4, 5, 8]):
        for i in range(len(a)):
            if a[i] > 1:
                b = a[:i] + [a[i] - 1] + a[i + 1:]
                assert pinwheel_schedule(b) is None
    assert density([3, 3, 5, 8]) < 1 and pinwheel_schedule([3, 3, 5, 8]) is None


def test_two_three_m_is_never_schedulable() -> None:
    for m in range(2, 16):
        assert pinwheel_schedule([2, 3, m]) is None
    assert density([2, 3, 6]) == 1


def test_density_above_one() -> None:
    assert pinwheel_schedule([2, 2, 3]) is None
    assert pinwheel_schedule([1, 5]) is None


def brute_cyclic(a: list[int], max_len: int) -> bool:
    for m in range(1, max_len + 1):
        for cyc in itertools.product(range(len(a)), repeat=m):
            if is_valid_cyclic(a, list(cyc)):
                return True
    return False


def test_against_brute_force_and_bounds() -> None:
    rng = random.Random(6)
    yes = no = 0
    for _ in range(250):
        a = sorted(rng.randint(2, 9) for _ in range(rng.randint(1, 4)))
        s = pinwheel_schedule(a)
        if s is not None:
            yes += 1
            assert is_valid_cyclic(a, s)
        else:
            no += 1
            assert not brute_cyclic(a, 7)
        if density(a) <= Fraction(5, 6):
            assert s is not None
        if len(set(a)) <= 2 and density(a) <= 1:
            assert s is not None
        if len(a) <= 3 and max(a) <= 5:
            assert (s is not None) == brute_cyclic(a, 8)
    assert yes > 50 and no > 20


def test_errors() -> None:
    for bad in ([], [0, 2]):
        try:
            pinwheel_schedule(bad)
        except ValueError:
            pass
        else:
            raise AssertionError("bad input accepted")
