# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gossip-averaging/. The authors are listed in prov/ZSVD30.jsonl.

import functools
import math
import random
from fractions import Fraction

from gossip_averaging import (complete, cycle, exact_run, expected_matrix, lambda2,
                              lambda2_closed_form, predicted_ticks, ticks_to_eps, torus)

EPS = 0.05
RUNS = 200


def graph(kind: str, n: int) -> list[list[int]]:
    if kind == "complete":
        return complete(n)
    if kind == "cycle":
        return cycle(n)
    return torus(math.isqrt(n))


def slow_input(kind: str, n: int) -> list[float]:
    """An input on the slowest eigenvector of W-bar, which is close to the
    worst case in the supremum of the averaging time."""
    if kind == "complete":
        return [1.0] + [0.0] * (n - 1)
    if kind == "cycle":
        return [math.cos(2 * math.pi * i / n) for i in range(n)]
    s = math.isqrt(n)
    return [math.cos(2 * math.pi * (i // s) / s) for i in range(n)]


@functools.lru_cache(maxsize=None)
def samples(kind: str, n: int) -> list[int]:
    rng = random.Random(n)
    adj = graph(kind, n)
    return sorted(ticks_to_eps(adj, slow_input(kind, n), EPS, rng) for _ in range(RUNS))


def test_the_sum_is_kept_exactly() -> None:
    for adj in (complete(6), cycle(9), torus(3)):
        x0 = list(range(len(adj)))
        for seed in range(5):
            x = exact_run(adj, x0, 200, seed)
            assert sum(x) == sum(Fraction(v) for v in x0)


def test_lambda2_of_w_bar_matches_the_closed_form() -> None:
    for kind, n in (("complete", 8), ("complete", 12), ("cycle", 7), ("cycle", 12), ("torus", 9), ("torus", 16)):
        got = lambda2(expected_matrix(graph(kind, n)))
        assert abs(got - lambda2_closed_form(kind, n)) < 1e-9, (kind, n)


def test_averaging_time_lies_in_the_window_of_theorem_3() -> None:
    # T_ave(eps) is the least t with Pr(error at t >= eps) <= eps. The error
    # never grows, so T_ave is the (1 - eps) quantile of the hitting time.
    for kind, n in (("complete", 16), ("complete", 64), ("cycle", 16), ("cycle", 32), ("torus", 16), ("torus", 64)):
        ts = samples(kind, n)
        t_ave = ts[int((1 - EPS) * RUNS) - 1]
        pred = predicted_ticks(lambda2_closed_form(kind, n), EPS)
        assert 0.5 * pred <= t_ave <= 3 * pred, (kind, n, t_ave, pred)


def test_time_scales_like_one_over_the_gap() -> None:
    # complete: n log(1/eps) ticks; cycle: n^3; torus: n^2.
    for kind, small, big in (("complete", 16, 64), ("cycle", 16, 32), ("torus", 16, 64)):
        m_small = sum(samples(kind, small)) / RUNS
        m_big = sum(samples(kind, big)) / RUNS
        want = predicted_ticks(lambda2_closed_form(kind, big), EPS) / predicted_ticks(
            lambda2_closed_form(kind, small), EPS)
        got = m_big / m_small
        assert abs(got / want - 1) < 0.2, (kind, got, want)
    # The exponents themselves: doubling n multiplies the cycle time by about 8.
    r = predicted_ticks(lambda2_closed_form("cycle", 64), EPS) / predicted_ticks(lambda2_closed_form("cycle", 32), EPS)
    assert 7.5 < r < 8.5
