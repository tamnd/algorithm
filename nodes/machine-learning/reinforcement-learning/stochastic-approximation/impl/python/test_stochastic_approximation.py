# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/stochastic-approximation/. The authors are listed in prov/TVB7PM.jsonl.

import math
import random
from fractions import Fraction

from stochastic_approximation import (
    gaussian_noise_sampler,
    linear_field,
    ode_times,
    rotation_ode_solution,
    stochastic_approximation,
)

A = [[1.0, 1.0], [-1.0, 1.0]]
B = [2.0, 0.0]
X_STAR = [1.0, 1.0]
X0 = [3.0, -1.0]
STEP = lambda n: 1.0 / (n + 2)  # noqa: E731


def test_root_of_example_field() -> None:
    h = linear_field(A, B)
    assert h(X_STAR) == [0.0, 0.0]


def test_noiseless_iteration_is_euler_method() -> None:
    h = linear_field(A, B)
    xs = stochastic_approximation(lambda x, r: h(x), X0, STEP, 3, random.Random(0))
    assert xs[1] == [3.0, 1.0]
    assert all(abs(u - v) < 1e-12 for u, v in zip(xs[2], [7 / 3, 5 / 3]))


def test_running_mean_is_stochastic_approximation() -> None:
    # h(x) = E[Z] - x with steps 1/(n+1) gives the sample mean exactly.
    data = [Fraction(v) for v in (3, -1, 4, 1, -5, 9, 2, 6)]
    it = iter(data)
    xs = stochastic_approximation(lambda x, r: [next(it) - x[0]], [Fraction(0)], lambda n: Fraction(1, n + 1), len(data), random.Random(0))
    # The code works in floats; the same recursion in Fractions equals each prefix mean exactly.
    x = Fraction(0)
    for n, z in enumerate(data):
        x = x + Fraction(1, n + 1) * (z - x)
        assert x == sum(data[: n + 1]) / (n + 1)
    assert abs(xs[-1][0] - float(sum(data) / len(data))) < 1e-12


def test_converges_to_root_with_noise() -> None:
    samp = gaussian_noise_sampler(linear_field(A, B), 1.0)
    dists = []
    for seed in range(40):
        xs = stochastic_approximation(samp, X0, STEP, 4000, random.Random(seed))
        dists.append(math.dist(xs[-1], X_STAR))
    # E|x_n - x*| is about 0.06 at n = 4000; the mean of 40 runs stays well below 0.15.
    assert sum(dists) / len(dists) < 0.15
    assert max(dists) < 0.4


def test_iterates_track_the_ode_on_a_window() -> None:
    # ODE method: the iterates from step m on stay near the ODE solution started at x_m,
    # over a window of ODE time T = 1, and the gap shrinks as m grows.
    samp = gaussian_noise_sampler(linear_field(A, B), 1.0)
    ts = ode_times(STEP, 60000)

    def window_gap(m: int, seed: int) -> float:
        xs = stochastic_approximation(samp, X0, STEP, m, random.Random(seed))
        xm, k, gap = xs[-1], m, 0.0
        rng = random.Random(seed + 1000)
        x = list(xm)
        while ts[k] - ts[m] <= 1.0:
            ode = rotation_ode_solution(X_STAR, xm, ts[k] - ts[m])
            gap = max(gap, math.dist(x, ode))
            y = samp(x, rng)
            x = [xi + STEP(k) * yi for xi, yi in zip(x, y)]
            k += 1
        return gap

    early = sum(window_gap(20, s) for s in range(20)) / 20
    late = sum(window_gap(2000, s) for s in range(20)) / 20
    assert late < early / 3
    assert late < 0.1


def test_ode_solution_solves_the_ode() -> None:
    h = linear_field(A, B)
    t, dt = 0.7, 1e-6
    x = rotation_ode_solution(X_STAR, X0, t)
    x2 = rotation_ode_solution(X_STAR, X0, t + dt)
    deriv = [(u - v) / dt for u, v in zip(x2, x)]
    assert all(abs(u - v) < 1e-4 for u, v in zip(deriv, h(x)))
