# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/random-load-balancing/. The authors are listed in prov/FXC04X.jsonl.

import math
import random

from random_load_balancing import (WeightedPicker, dispatch, queue_lengths, random_server, round_robin,
                                   weighted_dispatch)


class FixedU(random.Random):
    def __init__(self, u: float) -> None:
        super().__init__(0)
        self.u = u

    def random(self) -> float:  # type: ignore[override]
        return self.u


def test_weighted_pick_trace() -> None:
    p = WeightedPicker([1, 2, 3, 4])
    assert p.prefix == [1, 3, 6, 10]
    # u = 10 * 0.47 = 4.7 lies in [3, 6), so server 2.
    assert p.pick(FixedU(0.47)) == 2
    assert p.pick(FixedU(0.0)) == 0
    assert p.pick(FixedU(0.0999)) == 0
    assert p.pick(FixedU(0.1)) == 1
    assert p.pick(FixedU(0.9999999)) == 3


def test_zero_weight_is_never_picked() -> None:
    rng = random.Random(1)
    loads = weighted_dispatch([0, 5, 0, 5], 5000, rng)
    assert loads[0] == 0 and loads[2] == 0 and sum(loads) == 5000


def test_uniform_and_weighted_frequencies() -> None:
    rng = random.Random(2)
    m = 60000
    loads = dispatch(6, m, rng)
    for x in loads:
        assert abs(x - m / 6) < 5 * math.sqrt(m / 6)
    w = [1, 2, 3, 4]
    loads = weighted_dispatch(w, m, rng)
    for wi, x in zip(w, loads):
        mean = m * wi / 10
        assert abs(x - mean) < 5 * math.sqrt(mean)


def test_round_robin_is_exact() -> None:
    assert round_robin(4, 12) == [3, 3, 3, 3]
    assert round_robin(4, 14) == [4, 4, 3, 3]
    for n in range(1, 9):
        for m in range(0, 40):
            loads = round_robin(n, m)
            assert max(loads) - min(loads) <= 1 and sum(loads) == m


def test_max_load_matches_one_choice_bound() -> None:
    rng = random.Random(5)
    n = 1000
    lo = math.log(n) / math.log(math.log(n))
    for _ in range(40):
        mx = max(dispatch(n, n, rng))
        assert lo <= mx < 3 * lo


def test_every_server_is_reachable() -> None:
    rng = random.Random(7)
    seen = {random_server(5, rng) for _ in range(200)}
    assert seen == set(range(5))


def test_queue_length_near_mm1() -> None:
    rng = random.Random(6)
    mean = queue_lengths(20, 0.5, 100000, 10000, rng)
    assert abs(mean - 1.0) < 0.15
