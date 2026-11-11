# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/prp-prf-switching-lemma/. The authors are listed in prov/7NPNRH.jsonl.

import random
from fractions import Fraction

from prp_prf_switching_lemma import (
    bellare_rogaway_example,
    best_advantage,
    collision_probability,
    switching_bound,
)


def test_exact_advantage_is_the_collision_probability() -> None:
    # For q <= 2^n, the best adaptive adversary does no better than "output 1 on a collision".
    for n, q in ((1, 1), (1, 2), (2, 1), (2, 2), (2, 3), (2, 4), (3, 2), (3, 3)):
        assert best_advantage(n, q) == collision_probability(n, q)


def test_bound_holds() -> None:
    for n, q in ((1, 1), (1, 2), (1, 3), (2, 2), (2, 3), (2, 4), (2, 5), (3, 2), (3, 3)):
        assert best_advantage(n, q) <= switching_bound(n, q)


def test_bound_is_exact_for_two_queries() -> None:
    for n in (1, 2, 3):
        assert best_advantage(n, 2) == switching_bound(n, 2) == Fraction(1, 2 ** n)


def test_known_values() -> None:
    assert best_advantage(2, 3) == Fraction(5, 8)
    assert best_advantage(2, 4) == Fraction(29, 32)
    assert best_advantage(3, 3) == Fraction(11, 32)
    # More than 2^n queries give no more information than 2^n queries.
    assert best_advantage(2, 5) == best_advantage(2, 4)


def test_collision_probability_against_the_bound_for_larger_n() -> None:
    rng = random.Random(2006)
    for _ in range(50):
        n = rng.randrange(4, 33)
        q = rng.randrange(1, 300)
        assert collision_probability(n, q) <= switching_bound(n, q)


def test_bellare_rogaway_counterexample() -> None:
    # Bellare and Rogaway (2006), Section 2: Pr[A^pi = 1] = 5/12 but Pr[A^rho = 1 | Dist] = 6/13.
    p_pi, p_rho_dist = bellare_rogaway_example()
    assert p_pi == Fraction(5, 12)
    assert p_rho_dist == Fraction(6, 13)
    assert p_pi != p_rho_dist
