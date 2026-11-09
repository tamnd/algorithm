# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/igd-indicator/. The authors are listed in prov/4MNQFD.jsonl.

import math
import random

from igd_indicator import delta_p, gd, igd, igd_plus

R = [(0, 10), (10, 0)]


def weakly_dominates_set(a, b):
    return all(any(all(u <= v for u, v in zip(x, y)) for x in a) for y in b)


def test_hand_values() -> None:
    ref = [(0, 4), (2, 2), (4, 0)]
    a = [(1, 3), (4, 1)]
    # distances from (0,4): sqrt(2), sqrt(25); from (2,2): sqrt(2), sqrt(5); from (4,0): sqrt(18), 1
    assert math.isclose(igd(a, ref), (2 * math.sqrt(2) + 1) / 3)
    assert math.isclose(gd(a, ref), (math.sqrt(2) + 1) / 2)
    # d+: (0,4) -> (1,3) gives (1,0) -> 1; (2,2) -> (1,3) gives (0,1) -> 1; (4,0) -> (4,1) gives (0,1) -> 1
    assert math.isclose(igd_plus(a, ref), 1)
    assert math.isclose(delta_p(a, ref), max(gd(a, ref), igd(a, ref)))


def test_igd_is_not_pareto_compliant() -> None:
    a = [(0, 10)]
    b = [(0, 11), (10, 11)]
    assert weakly_dominates_set(a, b) and not weakly_dominates_set(b, a)  # a is better than b
    assert math.isclose(igd(a, R), math.sqrt(200) / 2)
    assert igd(b, R) == 6
    assert igd(b, R) < igd(a, R)  # yet IGD prefers b
    assert igd_plus(a, R) == 5 and igd_plus(b, R) == 6  # IGD+ orders them correctly


def test_igd_plus_is_weakly_compliant() -> None:
    rng = random.Random(2)
    for _ in range(2000):
        p = rng.randint(2, 4)
        ref = [tuple(rng.randint(0, 9) for _ in range(p)) for _ in range(rng.randint(1, 6))]
        a = [tuple(rng.randint(0, 9) for _ in range(p)) for _ in range(rng.randint(1, 5))]
        b = [tuple(u + rng.randint(0, 3) for u in rng.choice(a)) for _ in range(rng.randint(1, 5))]
        assert weakly_dominates_set(a, b)
        assert igd_plus(a, ref) <= igd_plus(b, ref) + 1e-12


def test_igd_plus_not_strict_and_zero_cases() -> None:
    a = [(0, 10), (10, 0), (5, 5)]
    b = [(0, 10), (10, 0)]
    assert weakly_dominates_set(a, b) and not weakly_dominates_set(b, a)
    assert igd(a, R) == igd(b, R) == 0 and igd_plus(a, R) == igd_plus(b, R) == 0
    # a single point of the front has GD 0, whatever the rest of the front
    assert gd([(0, 10)], R) == 0 and igd([(0, 10)], R) > 0
