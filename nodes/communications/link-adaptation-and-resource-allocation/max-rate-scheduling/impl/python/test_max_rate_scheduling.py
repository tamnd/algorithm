# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/max-rate-scheduling/. The authors are listed in prov/ZZJV41.jsonl.

import math
import random

import pytest

from cbb import undb, wilson
from max_rate_scheduling import (
    brute_force_slot,
    expected_max_rate,
    expected_of_max,
    harmonic,
    max_rate_schedule,
    max_rate_slot,
    slot_total,
    win_probability,
)

# The page example: 3 users, 6 slots, one resource per slot. PAGE[t][k][0] is the rate of user k in slot t.
TABLE = [
    [2.1, 3.4, 1.2, 4.0, 2.5, 0.8],
    [3.0, 1.1, 2.6, 2.2, 3.3, 2.9],
    [0.9, 1.0, 1.9, 0.7, 1.2, 1.5],
]
PAGE = [[[TABLE[k][t]] for k in range(3)] for t in range(6)]


def e1(z: float) -> float:
    """The exponential integral E1(z) = integral from z to infinity of e^(-u) / u du, by its power series."""
    s, term = 0.0, 1.0
    for n in range(1, 200):
        term *= -z / n
        s += term / n
        if abs(term) < 1e-18:
            break
    return -0.5772156649015329 - math.log(z) - s


def closed_form_rate(k: int, snr: float) -> float:
    """E[log2(1 + snr X)] = (1 / ln 2) sum_m (-1)^(m+1) C(k, m) e^(m / snr) E1(m / snr), fine for small k."""
    return sum((-1) ** (m + 1) * math.comb(k, m) * math.exp(m / snr) * e1(m / snr) for m in range(1, k + 1)) / math.log(2.0)


def test_page_example() -> None:
    choices, served = max_rate_schedule(PAGE)
    assert [c[0] for c in choices] == [1, 0, 1, 0, 1, 1]
    assert served == pytest.approx([7.4, 11.8, 0.0], abs=1e-12)
    assert sum(served) == pytest.approx(19.2, abs=1e-12)
    round_robin = sum(TABLE[t % 3][t] for t in range(6))
    assert round_robin == pytest.approx(13.9, abs=1e-12)


def test_ties_go_to_the_smallest_index() -> None:
    assert max_rate_slot([[1.0, 2.0], [1.0, 2.0], [0.5, 2.0]]) == [0, 0]
    assert max_rate_slot([[0.0], [0.0]]) == [0]
    assert max_rate_slot([[1.0, 0.0], [3.0, 0.0], [3.0, 5.0]]) == [1, 2]


def test_bad_input() -> None:
    with pytest.raises(ValueError):
        max_rate_slot([])
    with pytest.raises(ValueError):
        max_rate_slot([[1.0, 2.0], [1.0]])


def test_equals_brute_force() -> None:
    rng = random.Random(41)
    for _ in range(300):
        k, n = rng.randint(1, 4), rng.randint(1, 4)
        rates = [[rng.choice([0.0, 0.5, 1.0, 1.5, rng.random() * 3]) for _ in range(n)] for _ in range(k)]
        best, first = brute_force_slot(rates)
        choice = max_rate_slot(rates)
        assert slot_total(rates, choice) == pytest.approx(best, abs=1e-12)
        # itertools.product runs in lexicographic order, so the first best assignment is the smallest-index one
        assert choice == first


def test_beats_every_other_scheduler_over_time() -> None:
    rng = random.Random(7)
    slots = [[[rng.expovariate(1.0) for _ in range(3)] for _ in range(4)] for _ in range(200)]
    _, served = max_rate_schedule(slots)
    for _ in range(50):
        other = sum(slot_total(r, [rng.randrange(4) for _ in range(3)]) for r in slots)
        assert other <= sum(served) + 1e-9


def test_win_probability_closed_form() -> None:
    for k in range(1, 7):
        for i in range(k):
            assert win_probability([1.0] * k, i) == pytest.approx(1.0 / k, abs=1e-12)
    means = [1.0, 2.0, 4.0]
    p = [win_probability(means, i) for i in range(3)]
    assert sum(p) == pytest.approx(1.0, abs=1e-12)
    # two users: P(user 0 wins) = m0 / (m0 + m1)
    assert win_probability([1.0, 3.0], 0) == pytest.approx(0.25, abs=1e-12)
    assert p == pytest.approx([11 / 105, 30 / 105, 64 / 105], abs=1e-12)


def test_win_probability_by_simulation() -> None:
    rng = random.Random(2024)
    means = [1.0, 2.0, 4.0]
    trials = 20000
    wins = [0, 0, 0]
    for _ in range(trials):
        g = [[rng.expovariate(1.0 / m)] for m in means]
        wins[max_rate_slot(g)[0]] += 1
    for i in range(3):
        lo, hi = wilson(wins[i], trials)
        assert lo <= win_probability(means, i) <= hi


def test_mean_of_the_best_gain_is_harmonic() -> None:
    for k in (1, 2, 3, 8, 16, 64):
        assert expected_of_max(k, lambda x: 1.0) == pytest.approx(harmonic(k), abs=1e-9)


def test_rate_against_closed_forms() -> None:
    # e E1(1) = 0.596347362323194 nats for one user at snr = 1
    assert expected_max_rate(1, 1.0) == pytest.approx(0.596347362323194 / math.log(2.0), abs=1e-9)
    for snr in (1.0, 10.0):
        for k in (1, 2, 3, 4):
            assert expected_max_rate(k, snr) == pytest.approx(closed_form_rate(k, snr), abs=1e-8)


def test_page_rate_table() -> None:
    snr = undb(10.0)
    table = {1: 2.9065, 2: 3.6586, 4: 4.2427, 8: 4.6865, 16: 5.0340, 64: 5.5520}
    prev = 0.0
    for k, v in table.items():
        c = expected_max_rate(k, snr)
        assert c == pytest.approx(v, abs=6e-5)
        assert c > prev
        prev = c


def test_rate_by_simulation() -> None:
    rng = random.Random(99)
    snr, k, trials = 10.0, 8, 20000
    xs = [math.log2(1 + snr * max(rng.expovariate(1.0) for _ in range(k))) for _ in range(trials)]
    mean = sum(xs) / trials
    var = sum((x - mean) ** 2 for x in xs) / (trials - 1)
    assert abs(mean - expected_max_rate(k, snr)) <= 4.5 * math.sqrt(var / trials)
