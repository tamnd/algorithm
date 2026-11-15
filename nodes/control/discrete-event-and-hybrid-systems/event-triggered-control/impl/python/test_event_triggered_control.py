# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/event-triggered-control/. The authors are listed in prov/66J2N7.jsonl.

import math
import random
from fractions import Fraction

from ctlmat import add, mul, sub, transpose
from event_triggered_control import lyapunov, min_inter_event_time, sigma_max, simulate_etc

# The example of the page: an unstable plant and u = x_1 - 4 x_2.
A = [[0, 1], [-2, 3]]
B = [[0], [1]]
K = [[-1, 4]]
Q = [[1, 0], [0, 1]]


def test_lyapunov_solution_is_exact():
    p = lyapunov(sub(A, mul(B, K)), Q)
    assert p == [[Fraction(3, 2), Fraction(1, 2)], [Fraction(1, 2), Fraction(1)]]
    acl = sub(A, mul(B, K))
    assert add(mul(transpose(acl), p), mul(p, acl)) == [[-1, 0], [0, -1]]
    # The check value of the area: A = [[0, 1], [-2, -3]] gives P = [[5/4, 1/4], [1/4, 1/4]].
    assert lyapunov([[0, 1], [-2, -3]], Q) == [[Fraction(5, 4), Fraction(1, 4)], [Fraction(1, 4), Fraction(1, 4)]]


def test_threshold_and_bound_of_the_example():
    sb, _ = sigma_max(A, B, K, Q)
    assert abs(sb - 1 / (2 * math.sqrt(21.25))) < 1e-12
    tau = min_inter_event_time(A, B, K, 0.05)
    al, be = (1 + math.sqrt(5)) / 2, math.sqrt(17)
    assert abs(tau - math.log(al * 1.05 / (al + 0.05 * be)) / (al - be)) < 1e-12
    assert abs(tau - 0.028396) < 1e-6


def test_equal_norms_branch():
    # A - B K = -I and B K = I: alpha = beta = 1, so tau* = sigma / (1 + sigma).
    a = [[0.0, 0.0], [0.0, 0.0]]
    b = [[1.0, 0.0], [0.0, 1.0]]
    k = [[1.0, 0.0], [0.0, 1.0]]
    assert abs(min_inter_event_time(a, b, k, 0.2) - 0.2 / 1.2) < 1e-12


def test_events_respect_the_bound_and_state_converges():
    tau = min_inter_event_time(A, B, K, 0.05)
    events, ts, xs = simulate_etc(A, B, K, [1.0, 0.0], 0.05, 10.0, 0.001)
    gaps = [b - a for a, b in zip(events, events[1:])]
    assert len(events) == 218
    assert min(gaps) >= tau - 0.001
    assert math.hypot(*xs[-1]) < 0.004
    # Fewer updates than periodic sampling with the period tau*.
    assert len(events) < 10.0 / tau


def test_bound_on_random_stable_loops():
    rng = random.Random(5)
    for _ in range(6):
        # A - B K = [[a11, 1], [-c1, -c2]] with a11 <= 0.2 and c1, c2 in [1, 3]:
        # its trace is negative and its determinant c1 - a11 c2 >= 0.4, so it is Hurwitz.
        a = [[rng.uniform(-1, 0.2), 1.0], [rng.uniform(-2, 2), rng.uniform(-1, 1)]]
        k = [[a[1][0] + rng.uniform(1, 3), a[1][1] + rng.uniform(1, 3)]]
        acl = sub(a, mul(B, k))
        assert acl[0][0] + acl[1][1] < 0 and acl[0][0] * acl[1][1] - acl[0][1] * acl[1][0] > 0
        sb, p = sigma_max(a, B, k, Q)
        assert p[0][0] > 0 and p[0][0] * p[1][1] - p[0][1] * p[1][0] > 0
        sigma = 0.8 * sb
        tau = min_inter_event_time(a, B, k, sigma)
        x0 = [rng.uniform(-1, 1), rng.uniform(-1, 1)]
        events, _, xs = simulate_etc(a, B, k, x0, sigma, 5.0, 0.001)
        gaps = [q - p for p, q in zip(events, events[1:])]
        assert min(gaps) >= tau - 0.001
        assert math.hypot(*xs[-1]) < math.hypot(*x0)


def test_error_stays_below_threshold_between_events():
    """Between events ||x_hat - x|| < sigma ||x|| at every step, up to the step delay."""
    sigma = 0.05
    events, ts, xs = simulate_etc(A, B, K, [1.0, 0.0], sigma, 3.0, 0.001)
    held = None
    j = 0
    for t, x in zip(ts, xs):
        if j < len(events) and abs(t - events[j]) < 1e-9:
            held = x
            j += 1
            continue
        e = math.hypot(held[0] - x[0], held[1] - x[1])
        assert e < sigma * math.hypot(*x)
