# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kinetic-monte-carlo/. The authors are listed in prov/SFQPD9.jsonl.
import math
import random

import pytest

from kinetic_monte_carlo import arrhenius_rate, kinetic_monte_carlo, select_event


class FixedRng:
    """Returns the given numbers in order, so that a run can be checked by hand."""

    def __init__(self, values):
        self.values = list(values)

    def random(self):
        return self.values.pop(0)


def two_state(k_ab, k_ba):
    return lambda x: [(k_ab, "B")] if x == "A" else [(k_ba, "A")]


def test_select_event():
    rates = [1.0, 2.0, 3.0]
    assert select_event(rates, 0.0) == 0
    assert select_event(rates, 0.999) == 0
    assert select_event(rates, 1.0) == 1
    assert select_event(rates, 2.999) == 1
    assert select_event(rates, 3.0) == 2
    assert select_event(rates, 5.999) == 2
    assert select_event([1.0, 0.0], 1.0) == 0


def test_trace_by_hand():
    # The page example: k_AB = 1, k_BA = 3. Each step uses (u1, 1 - u2).
    u = [(0.5, 0.5), (0.2, 0.9), (0.7, 0.3), (0.1, 0.6)]
    flat = [v for a, b in u for v in (a, 1.0 - b)]
    x, t, path, avg = kinetic_monte_carlo(
        "A", two_state(1.0, 3.0), 10.0, FixedRng(flat + [0.5, 0.5]),
        observe=lambda s: 1.0 if s == "A" else 0.0, max_steps=4)
    times = [p[0] for p in path]
    states = [p[1] for p in path]
    assert states == ["A", "B", "A", "B", "A"]
    expect = [0.0]
    for (u1, u2), rate in zip(u, [1.0, 3.0, 1.0, 3.0]):
        expect.append(expect[-1] - math.log(u2) / rate)
    assert times == pytest.approx(expect, abs=1e-12)
    assert times[1:] == pytest.approx([0.693147, 0.728268, 1.932241, 2.102515], abs=1e-6)
    in_a = (times[1] - times[0]) + (times[3] - times[2])
    assert avg == pytest.approx(in_a / times[-1], abs=1e-12)


def test_two_state_time_fraction():
    rng = random.Random(1)
    k_ab, k_ba = 1.0, 3.0
    _, t, path, frac = kinetic_monte_carlo(
        "A", two_state(k_ab, k_ba), 2500.0, rng,
        observe=lambda s: 1.0 if s == "A" else 0.0)
    assert t == 2500.0
    assert len(path) < 10000
    assert frac == pytest.approx(k_ba / (k_ab + k_ba), abs=0.02)


def test_residence_time_and_choice():
    rng = random.Random(2)
    rates = [1.0, 2.0, 3.0]
    n = 6000
    waits, counts = [], [0, 0, 0]
    for _ in range(n):
        _, _, path, _ = kinetic_monte_carlo(
            0, lambda s: [(k, j + 1) for j, k in enumerate(rates)] if s == 0 else [],
            1e9, rng)
        waits.append(path[1][0])
        counts[path[1][1] - 1] += 1
    mean = sum(waits) / n
    var = sum((w - mean) ** 2 for w in waits) / (n - 1)
    total = sum(rates)
    # Exponential law with rate 6: mean 1/6, standard deviation 1/6.
    assert abs(mean - 1 / total) < 4 * (1 / total) / math.sqrt(n)
    assert var == pytest.approx(1 / total ** 2, rel=0.1)
    for j, k in enumerate(rates):
        p = k / total
        assert abs(counts[j] / n - p) < 4 * math.sqrt(p * (1 - p) / n)


def test_random_walk_mean_square_displacement():
    rng = random.Random(3)
    k, t_end, walkers = 1.0, 5.0, 500
    hop = lambda x: [(k, x - 1), (k, x + 1)]
    sq = [kinetic_monte_carlo(0, hop, t_end, rng)[0] ** 2 for _ in range(walkers)]
    mean = sum(sq) / walkers
    # <x^2> = 2 k t; x is the difference of two Poisson(5) counts, so Var(x^2) = 210.
    assert abs(mean - 2 * k * t_end) < 4 * math.sqrt(210 / walkers)


def expm_times_vector(q, p0, t, terms=60):
    """p0 exp(Q t) by the Taylor series, for a small generator Q and a small t."""
    n = len(p0)
    out = list(p0)
    term = list(p0)
    for m in range(1, terms):
        term = [sum(term[i] * q[i][j] for i in range(n)) * t / m for j in range(n)]
        out = [a + b for a, b in zip(out, term)]
    return out


def test_three_state_chain_against_master_equation():
    # 0 <-> 1 <-> 2 with rates 2, 1 (from 1 to 0 and to 2) and 0.5 back.
    k = {(0, 1): 2.0, (1, 0): 1.0, (1, 2): 1.0, (2, 1): 0.5}
    events = lambda x: [(r, j) for (i, j), r in k.items() if i == x]
    q = [[0.0] * 3 for _ in range(3)]
    for (i, j), r in k.items():
        q[i][j] += r
        q[i][i] -= r
    t_end = 0.7
    p_exact = expm_times_vector(q, [1.0, 0.0, 0.0], t_end)
    assert sum(p_exact) == pytest.approx(1.0, abs=1e-12)
    rng = random.Random(4)
    n = 3000
    counts = [0, 0, 0]
    for _ in range(n):
        counts[kinetic_monte_carlo(0, events, t_end, rng)[0]] += 1
    for j in range(3):
        p = p_exact[j]
        assert abs(counts[j] / n - p) < 4 * math.sqrt(p * (1 - p) / n)


def test_absorbing_state_stops():
    x, t, path, _ = kinetic_monte_carlo("A", lambda s: [(1.0, "B")] if s == "A" else [],
                                        100.0, random.Random(5))
    assert x == "B" and len(path) == 2 and t == path[-1][0] < 100.0


def test_arrhenius_rate():
    kT = 8.617333262e-5 * 300.0
    assert arrhenius_rate(1e13, 0.5, kT) == pytest.approx(1e13 * math.exp(-0.5 / kT))
    assert arrhenius_rate(1e13, 0.5, kT) == pytest.approx(3.98e4, rel=0.01)
