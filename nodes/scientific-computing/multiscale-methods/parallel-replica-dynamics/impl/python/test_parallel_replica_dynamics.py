# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/parallel-replica-dynamics/. The authors are listed in prov/6Z28SF.jsonl.
import math
import random

import pytest

from parallel_replica_dynamics import parallel_replica_dynamics

P_B, P_C = 0.15, 0.05


def bernoulli_step(x, rng):
    """From A, go to B with probability P_B and to C with probability P_C per step."""
    if x != "A":
        return x
    u = rng.random()
    if u < P_B:
        return "B"
    if u < P_B + P_C:
        return "C"
    return "A"


def label(x):
    return x


class Script:
    def __init__(self, values):
        self.values = list(values)

    def random(self):
        return self.values.pop(0)


def test_time_accounting_by_hand():
    # n_corr = 1, m = 3. Decorrelation: 1 step, no escape. Dephasing: 1 step
    # per replica, no escape. Parallel stage: step 1 has no escape; at step 2
    # replicas 2 and 3 escape, and replica 2 is the first. t = 1 + 3*1 + 2 = 6.
    rng = Script([0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.0, 0.17])
    x, t, transitions, work, wall = parallel_replica_dynamics("A", bernoulli_step, label, 3, 1, rng, 1)
    assert x == "B"
    assert t == 6.0
    assert transitions == [(6.0, "A", "B")]
    assert work == 1 + 3 + 6
    assert wall == 1 + 1 + 2
    assert rng.values == []


def test_geometric_escape_law_is_kept():
    # With a constant escape probability, the time of the first transition is
    # geometric with mean 1 / (P_B + P_C) = 5 for any m, and the exit is B
    # with probability 0.75.
    rng = random.Random(2)
    times, to_b, work = [], 0, 0
    for _ in range(300):
        _, t, transitions, w, _ = parallel_replica_dynamics("A", bernoulli_step, label, 4, 5, rng, 1)
        assert t == int(t) and t >= 1
        times.append(t)
        to_b += transitions[0][2] == "B"
        work += w
    assert work <= 10000
    n = len(times)
    mean = sum(times) / n
    se = math.sqrt(sum((v - mean) ** 2 for v in times) / (n - 1) / n)
    assert abs(mean - 5.0) < 3.0 * se
    assert abs(to_b / n - 0.75) < 3.0 * math.sqrt(0.75 * 0.25 / n)


KT = 0.5
H = 0.01
SIGMA = math.sqrt(2.0 * KT * H)


def double_well_step(x, rng):
    return x - H * 4.0 * x * (x * x - 1.0) + SIGMA * rng.gauss(0.0, 1.0)


def side(x):
    return x >= 0.0


def test_bookkeeping_on_a_double_well():
    rng = random.Random(5)
    x, t, transitions, work, wall = parallel_replica_dynamics(-1.0, double_well_step, side, 4, 20, rng, 4,
                                                              h=H, max_work=10000)
    assert len(transitions) == 4
    times = [tr[0] for tr in transitions]
    assert times == sorted(times) and times[-1] == pytest.approx(t)
    for (_, a, b), (_, c, _) in zip(transitions, transitions[1:]):
        assert a != b and b == c
    assert transitions[0][1] is False and transitions[-1][2] == side(x)
    assert wall <= work


def test_mean_escape_time_of_a_double_well():
    # Mean first passage time from -1 to 0 for the continuous dynamics: 4.607
    # (quadrature). The Euler steps with h = 0.01 detect the crossing late,
    # which adds about 0.4 (a long serial run gives 5.05). Loose check.
    rng = random.Random(1)
    times, work = [], 0
    while True:
        try:
            _, t, _, w, _ = parallel_replica_dynamics(-1.0, double_well_step, side, 4, 20, rng, 1,
                                                      h=H, max_work=10000 - work)
        except RuntimeError:
            break
        times.append(t)
        work += w
    n = len(times)
    assert n >= 10
    mean = sum(times) / n
    se = math.sqrt(sum((v - mean) ** 2 for v in times) / (n - 1) / n)
    assert abs(mean - 4.607) < 3.0 * se + 0.5


def test_max_work():
    with pytest.raises(RuntimeError):
        parallel_replica_dynamics(-1.0, double_well_step, side, 4, 20, random.Random(1), 100,
                                  h=H, max_work=500)
