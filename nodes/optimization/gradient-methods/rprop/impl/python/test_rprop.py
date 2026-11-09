# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/rprop/. The authors are listed in prov/TRX7X7.jsonl.

import math
import random

from rprop import rprop


def test_example_trace() -> None:
    # f(x) = (x - 1)^2 from x = 0 with the default factors and delta_min = 0.
    xs = rprop(lambda t, x: [2 * (x[0] - 1)], [0.0], 14, delta_min=0.0)
    want = [0.0, 0.1, 0.22, 0.364, 0.5368, 0.74416, 0.992992, 1.29159, 1.29159, 1.142291, 0.963132, 0.963132,
            1.052712, 1.052712, 1.007922]
    for x, w in zip(xs, want):
        assert abs(x[0] - w) <= 5e-6


def test_only_the_signs_matter() -> None:
    # Multiplying each gradient coordinate by any positive factor, different at every call, gives the same iterates.
    def g(x: list[float]) -> list[float]:
        return [4 * (x[0] - 0.3) ** 3 + (x[0] - 0.3), math.tanh(x[1] + 2.0)]

    base = rprop(lambda t, x: g(x), [5.0, 5.0], 200)
    for seed in range(10):
        r = random.Random(seed)
        scaled = rprop(lambda t, x: [gi * 10 ** r.uniform(-6, 6) for gi in g(x)], [5.0, 5.0], 200)
        assert scaled == base


def test_moves_are_zero_or_a_step_in_range() -> None:
    r = random.Random(4)
    gs = [[r.gauss(0, 1) for _ in range(3)] for _ in range(500)]
    lo, hi = 1e-3, 2.0
    xs = rprop(lambda t, x: gs[t], [0.0, 0.0, 0.0], 500, delta0=0.5, delta_min=lo, delta_max=hi)
    for a, b in zip(xs, xs[1:]):
        for p, q in zip(a, b):
            assert p == q or lo * (1 - 1e-12) <= abs(q - p) <= hi * (1 + 1e-12)


def test_separable_linear_convergence_every_iterate() -> None:
    # f(x) = sum_i h_i(x_i) with h_i' of the sign of x_i - z_i. With delta_min = 0, eta_minus eta_plus < 1 and
    # eta_minus (1 + eta_plus) >= 1: after the first sign change t_1, with s_1 the last move before it,
    # |x_t,i - z_i| <= s_1 (eta_minus eta_plus)^floor((t - t_1) / 3) for every t >= t_1.
    shapes = [
        lambda u: u,
        lambda u: u**3,
        lambda u: math.tanh(u),
        lambda u: math.copysign(math.sqrt(abs(u)), u),
        lambda u: math.exp(u) - 1,
    ]
    for seed in range(30):
        r = random.Random(seed)
        d = 4
        z = [r.uniform(-10, 10) for _ in range(d)]
        k = [r.randrange(len(shapes)) for _ in range(d)]
        c = [10 ** r.uniform(-3, 3) for _ in range(d)]
        ep = r.uniform(1.05, 1.6)
        em = r.uniform(1 / (1 + ep), 1 / ep * 0.999)
        x0 = [r.uniform(-20, 20) for _ in range(d)]
        iters = 400
        xs = rprop(
            lambda t, x: [c[i] * shapes[k[i]](x[i] - z[i]) for i in range(d)], x0, iters,
            delta0=10 ** r.uniform(-3, 0), eta_plus=ep, eta_minus=em, delta_min=0.0,
        )
        q = em * ep
        for i in range(d):
            moves = [xs[t + 1][i] - xs[t][i] for t in range(iters)]
            # iteration t (0-based) has a sign change when it does not move after having moved
            first, s1 = None, 0.0
            for t in range(1, iters):
                if moves[t] == 0.0 and moves[t - 1] != 0.0:
                    first, s1 = t, abs(moves[t - 1])
                    break
            if first is None:
                assert xs[-1][i] == z[i] or all(m != 0.0 for m in moves)
                continue
            for t in range(first, iters + 1):
                err = abs(xs[t][i] - z[i])
                assert err <= s1 * q ** ((t - first) // 3) * (1 + 1e-9) + 1e-12


def test_zero_iterations() -> None:
    assert rprop(lambda t, x: x, [1.0], 0) == [[1.0]]
