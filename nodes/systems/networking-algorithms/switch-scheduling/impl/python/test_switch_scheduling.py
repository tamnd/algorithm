# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/switch-scheduling/. The authors are listed in prov/52M6P4.jsonl.

import math
import random
from fractions import Fraction as F

from switch_scheduling import (
    admissible,
    brute_force_max_weight,
    fifo_saturation_throughput,
    max_weight_matching,
    simulate_fifo,
    simulate_voq_max_weight,
)


def test_admissible() -> None:
    assert admissible([[F(1, 2), F(1, 3)], [F(1, 3), F(1, 2)]])
    assert not admissible([[F(1, 2), F(1, 2)], [F(0), F(0)]])  # row sum 1
    assert not admissible([[F(3, 5), F(0)], [F(1, 2), F(0)]])  # column sum > 1


def test_max_weight_matching_against_brute_force() -> None:
    rng = random.Random(3)
    for _ in range(200):
        n = rng.randrange(1, 6)
        w = [[rng.randrange(10) for _ in range(n)] for _ in range(n)]
        m = max_weight_matching(w)
        assert sorted(m) == list(range(n))
        assert sum(w[i][m[i]] for i in range(n)) == brute_force_max_weight(w)


def test_two_by_two_hol_blocking_is_three_quarters() -> None:
    # Exact value: the HOL cells collide with probability 1/2, so (2 + 1)/4.
    assert abs(fifo_saturation_throughput(2, 40000, random.Random(5)) - 0.75) < 0.01


def test_hol_blocking_saturates_near_two_minus_root_two() -> None:
    limit = 2 - math.sqrt(2)  # 0.5858 as N tends to infinity
    t16 = fifo_saturation_throughput(16, 20000, random.Random(1))
    t32 = fifo_saturation_throughput(32, 10000, random.Random(1))
    # Finite N lies a little above the limit (Karol et al. give 0.6184 at N = 8).
    assert limit < t32 < t16 < limit + 0.03


def test_voq_with_max_weight_carries_the_load_fifo_does_not() -> None:
    a, d, left = simulate_fifo(16, 0.95, 2000, random.Random(2))
    assert abs(d / (16 * 2000) - 0.6) < 0.02  # FIFO serves about 0.6 per port
    assert left > 0.3 * a  # and the backlog grows without bound
    a, d, left = simulate_voq_max_weight(16, 0.95, 2000, random.Random(2))
    assert d / a > 0.99  # VOQ with max-weight matching serves the offered load
    assert left < 16 * 16  # and the backlog stays small
