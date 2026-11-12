# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/slotted-aloha/. The authors are listed in prov/S3TWTY.jsonl.

from fractions import Fraction
import math
import random

from slotted_aloha import (
    best_success_probability,
    poisson_throughput,
    saturated_slotted_aloha,
    slot_outcome,
    slotted_aloha,
    slotted_aloha_stations,
    success_probability,
)


def brute_success(n, p):
    """Sum over all 2^n send patterns of the probability of the patterns with one sender."""
    total = Fraction(0)
    for mask in range(1 << n):
        k = bin(mask).count("1")
        if k == 1:
            total += p ** k * (1 - p) ** (n - k)
    return total


def test_formula_matches_enumeration():
    for n in range(1, 8):
        for p in [Fraction(1, 7), Fraction(1, 3), Fraction(1, 2), Fraction(5, 6)]:
            assert success_probability(n, p) == brute_success(n, p)


def test_exact_small_values():
    assert best_success_probability(2) == Fraction(1, 2)
    assert best_success_probability(3) == Fraction(4, 9)
    assert best_success_probability(4) == Fraction(27, 64)
    assert best_success_probability(5) == Fraction(256, 625)


def test_p_equal_one_over_n_is_best():
    for n in range(2, 9):
        best = best_success_probability(n)
        for k in range(1, 200):
            assert success_probability(n, Fraction(k, 200)) <= best


def test_limit_is_one_over_e_from_above():
    prev = Fraction(1)
    for n in range(2, 60):
        b = best_success_probability(n)
        assert b < prev
        assert float(b) > 1 / math.e
        prev = b
    assert abs(float(best_success_probability(2000)) - 1 / math.e) < 1e-4


def test_poisson_maxima():
    assert abs(poisson_throughput(1.0) - 1 / math.e) < 1e-12
    assert abs(poisson_throughput(0.5, slotted=False) - 1 / (2 * math.e)) < 1e-12
    for g in [0.2, 0.7, 0.99, 1.01, 1.5, 3.0]:
        assert poisson_throughput(g) < 1 / math.e
        assert poisson_throughput(g / 2, slotted=False) < 1 / (2 * math.e) + 1e-15


def test_outcomes():
    assert [slot_outcome(k) for k in range(3)] == ["idle", "success", "collision"]


def test_simulation_agrees_with_formula():
    slots = 60000
    for n, p in [(10, 0.1), (10, 0.2), (5, 0.3)]:
        wins, idle, coll = saturated_slotted_aloha(n, p, slots, random.Random(n * 100 + int(p * 10)))
        s = float(success_probability(n, p))
        sigma = math.sqrt(s * (1 - s) / slots)
        assert abs(sum(wins) / slots - s) < 4 * sigma
        assert sum(wins) + idle + coll == slots
        # symmetric stations get nearly equal shares
        assert max(wins) - min(wins) < 0.15 * max(wins)


def test_station_protocol_delivers_every_frame_once_in_order():
    rng = random.Random(3)
    n = 5
    arrivals = [sorted(rng.sample(range(400), 20)) for _ in range(n)]
    done = slotted_aloha_stations(arrivals, 0.2, 3000, random.Random(11))
    assert len(done) == 20 * n
    slots_used = [t for _, _, t in done]
    assert len(set(slots_used)) == len(slots_used)  # one frame per success slot
    for i in range(n):
        mine = [(a, t) for s, a, t in done if s == i]
        assert [a for a, _ in mine] == arrivals[i]  # FIFO per station
        assert all(t >= a for a, t in mine)


def test_lone_station_never_waits():
    done = slotted_aloha_stations([[0, 3, 7]], 0.5, 10, random.Random(1))
    assert done == [(0, 0, 0), (0, 3, 3), (0, 7, 7)]


def test_fixed_retransmission_probability_is_unstable():
    delivered, trace = slotted_aloha(0.3, 6000, random.Random(7), q_r=0.1, backlog0=50)
    assert trace[-1] > 400
    assert delivered / 6000 < 0.1


def test_pseudo_bayesian_is_stable_below_one_over_e():
    for lam in [0.25, 0.3, 0.35]:
        delivered, trace = slotted_aloha(lam, 20000, random.Random(7), backlog0=50)
        assert max(trace[1000:]) < 100
        assert abs(delivered / 20000 - lam) < 0.02
