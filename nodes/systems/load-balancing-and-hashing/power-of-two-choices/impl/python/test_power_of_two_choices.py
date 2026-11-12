# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/power-of-two-choices/. The authors are listed in prov/FH6PZB.jsonl.

import itertools
import math
import random
from fractions import Fraction

from power_of_two_choices import (always_go_left, choose, expected_time, greedy, is_fixed_point,
                                  supermarket, supermarket_tail)


class Script(random.Random):
    """A generator that returns the given bin indices in order."""

    def __init__(self, picks: list[int]) -> None:
        super().__init__(0)
        self.picks = list(picks)

    def randrange(self, *args: int) -> int:  # type: ignore[override]
        return self.picks.pop(0)


def test_trace_of_the_page() -> None:
    # 4 bins, 6 balls, samples (0,1) (0,2) (1,2) (3,3) (0,3) (2,1)
    rng = Script([0, 1, 0, 2, 1, 2, 3, 3, 0, 3, 2, 1])
    loads = [0] * 4
    placed = []
    for _ in range(6):
        b = choose(loads, 2, rng)
        loads[b] += 1
        placed.append(b)
    assert placed == [0, 2, 1, 3, 0, 2]
    assert loads == [2, 1, 2, 1]


def test_choice_is_least_loaded_of_samples() -> None:
    rng = random.Random(4)
    for _ in range(300):
        loads = [rng.randrange(5) for _ in range(8)]
        state = rng.getstate()
        b = choose(loads, 3, rng)
        rng.setstate(state)
        samples = [rng.randrange(8) for _ in range(3)]
        assert b in samples and loads[b] == min(loads[s] for s in samples)


def test_probability_of_a_high_bin_exactly() -> None:
    # Pr[the ball joins a bin with load >= i] = (beta / n)^d, by enumeration of all samples.
    loads = [0, 2, 1, 3, 2]
    n = len(loads)
    for d in (1, 2, 3):
        for i in range(4):
            beta = sum(1 for x in loads if x >= i)
            hits = sum(1 for s in itertools.product(range(n), repeat=d)
                       if loads[min(s, key=lambda b: loads[b])] >= i)
            assert Fraction(hits, n ** d) == Fraction(beta, n) ** d


def test_loads_add_up() -> None:
    rng = random.Random(8)
    for d in (1, 2, 3):
        assert sum(greedy(50, 123, d, rng)) == 123
    assert sum(always_go_left(50, 123, 2, rng)) == 123


def test_two_choices_beat_one_choice() -> None:
    rng = random.Random(5)
    n = 20000
    one = max(greedy(n, n, 1, rng))
    two = max(greedy(n, n, 2, rng))
    left = max(always_go_left(n, n, 2, rng))
    assert two <= 4 and left <= 4 and one >= 5
    assert two <= math.log(math.log(n)) / math.log(2) + 2


def test_heavy_case_gap_stays_small() -> None:
    rng = random.Random(6)
    n, mean = 1000, 50
    gap_two = max(greedy(n, mean * n, 2, rng)) - mean
    gap_one = max(greedy(n, mean * n, 1, rng)) - mean
    assert gap_two <= 3 < gap_one


def test_fixed_point_exact() -> None:
    for lam in (Fraction(1, 2), Fraction(9, 10), Fraction(99, 100)):
        for d in (1, 2, 3, 4):
            assert is_fixed_point(lam, d, 6)
    assert supermarket_tail(Fraction(9, 10), 2, 3) == Fraction(9, 10) ** 7


def test_expected_time_values() -> None:
    assert abs(expected_time(0.9, 1) - 10) < 1e-9
    assert abs(expected_time(0.9, 2) - 2.614) < 1e-3
    assert abs(expected_time(0.99, 2) - 5.432) < 1e-3
    assert abs(expected_time(0.99, 3) - 3.858) < 1e-3


def test_supermarket_simulation_near_fixed_point() -> None:
    rng = random.Random(7)
    s = supermarket(100, 0.9, 2, 120000, 20000, rng)
    for i in range(1, 6):
        assert abs(s[i] - float(supermarket_tail(Fraction(9, 10), 2, i))) < 0.03
