# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tr-bdf2/. The authors are listed in prov/W1B2JC.jsonl.

import cmath
import math
import random

from tr_bdf2 import (
    GAMMA,
    backward_euler_step,
    error_constant,
    stability_function,
    tr_bdf2_adaptive,
    tr_bdf2_fixed,
    tr_bdf2_step,
    trapezoidal_step,
)


class Scalar:
    """y' = lam y + s(t), written as f(y) + dq/dt = u with q = y, f = -lam y."""

    def __init__(self, lam, s=lambda t: 0.0):
        self.lam, self.s = lam, s

    def f(self, x):
        return [-self.lam * x[0]]

    def G(self, x):
        return [[-self.lam]]

    def q(self, x):
        return [x[0]]

    def C(self, x):
        return [[1.0]]

    def u(self, t):
        return [self.s(t)]


class RC:
    """Node voltage v of a capacitor C to ground, fed through R from a source vs(t)."""

    def __init__(self, r, c, vs):
        self.r, self.c, self.vs = r, c, vs

    def f(self, x):
        return [x[0] / self.r]

    def G(self, x):
        return [[1 / self.r]]

    def q(self, x):
        return [self.c * x[0]]

    def C(self, x):
        return [[self.c]]

    def u(self, t):
        return [self.vs(t) / self.r]


class SeriesRLC:
    """MNA of a source V at node 1, R from 1 to 2, L from 2 to 3, C from 3 to ground.

    x = (e1, e2, e3, jV, jL). The matrix C is singular: an index-1 DAE.
    """

    def __init__(self, r, l, c, v):
        self.r, self.l, self.c, self.v = r, l, c, v

    def f(self, x):
        e1, e2, e3, jv, jl = x
        g = 1 / self.r
        return [g * (e1 - e2) + jv, g * (e2 - e1) + jl, -jl, e1, e2 - e3]

    def G(self, x):
        g = 1 / self.r
        return [
            [g, -g, 0, 1, 0],
            [-g, g, 0, 0, 1],
            [0, 0, 0, 0, -1],
            [1, 0, 0, 0, 0],
            [0, 1, -1, 0, 0],
        ]

    def q(self, x):
        return [0.0, 0.0, self.c * x[2], 0.0, -self.l * x[4]]

    def C(self, x):
        m = [[0.0] * 5 for _ in range(5)]
        m[2][2] = self.c
        m[4][4] = -self.l
        return m

    def u(self, t):
        return [0.0, 0.0, 0.0, self.v(t), 0.0]


class Rectifier:
    """Half-wave rectifier: source at node 1, diode from 1 to 2, R and C from 2 to ground.

    x = (e1, e2, jV). Diode i = IS (exp(v / VT) - 1); IS and the emission
    coefficient inside VT are fitted model parameters (typical values here).
    The exponential is continued linearly above 40 VT, as SPICE-like codes do.
    """

    IS, VT = 1e-14, 0.025875

    def __init__(self, r, c, amp, freq):
        self.r, self.c, self.amp, self.freq = r, c, amp, freq

    def _diode(self, v):
        vmax = 40 * self.VT
        if v <= vmax:
            e = math.exp(v / self.VT)
            return self.IS * (e - 1), self.IS * e / self.VT
        e = math.exp(vmax / self.VT)
        return self.IS * (e * (1 + (v - vmax) / self.VT) - 1), self.IS * e / self.VT

    def f(self, x):
        e1, e2, jv = x
        i, _ = self._diode(e1 - e2)
        return [i + jv, -i + e2 / self.r, e1]

    def G(self, x):
        e1, e2, _ = x
        _, g = self._diode(e1 - e2)
        return [[g, -g, 1], [-g, g + 1 / self.r, 0], [1, 0, 0]]

    def q(self, x):
        return [0.0, self.c * x[1], 0.0]

    def C(self, x):
        return [[0.0, 0.0, 0.0], [0.0, self.c, 0.0], [0.0, 0.0, 0.0]]

    def u(self, t):
        return [0.0, 0.0, self.amp * math.sin(2 * math.pi * self.freq * t)]


def test_gamma_makes_stage_matrices_equal():
    g = GAMMA
    d = (1 - g) / (2 - g)
    assert abs(d - g / 2) < 1e-15
    a = 1 / (g * (2 - g))
    b = (1 - g) ** 2 / (g * (2 - g))
    assert abs(a - b - 1) < 1e-14  # consistency
    assert abs(a + b - math.sqrt(2)) < 1e-14


def test_stability_function_closed_form_and_step():
    c = (2 - math.sqrt(2)) / 2
    rng = random.Random(41)
    for _ in range(200):
        z = complex(rng.uniform(-50, 5), rng.uniform(-50, 50))
        closed = (1 + (math.sqrt(2) - 1) * z) / (1 - c * z) ** 2
        assert abs(stability_function(z) - closed) < 1e-12 * max(1, abs(closed))
    for z in (-0.5, -3.0, -10.0, -1000.0):
        y1, _, _ = tr_bdf2_step(Scalar(z), 0.0, [1.0], 1.0)
        assert abs(y1[0] - stability_function(z)) < 1e-12


def test_l_stability():
    for k in range(-400, 401):
        y = k / 4
        assert abs(stability_function(complex(0, y))) <= 1 + 1e-14
    # R(z) -> 0 like 2 (sqrt 2 + 1) / z as z -> -infinity
    for z in (-1e6, -1e9):
        assert abs(z * stability_function(z) - 2 * (math.sqrt(2) + 1)) < 1e-4
    # |R(iy)|^2 = (1 + s) / (1 + s/2)^2 with s = (3 - 2 sqrt 2) y^2
    for y in (0.3, 1.0, 7.0, 100.0):
        s = (3 - 2 * math.sqrt(2)) * y * y
        assert abs(abs(stability_function(complex(0, y))) ** 2 - (1 + s) / (1 + s / 2) ** 2) < 1e-12


def test_second_order_on_taylor_series():
    # R(z) - e^z = -k z^3 + O(z^4), with the error constant k
    k = error_constant()
    assert abs(k - (-(3 * math.sqrt(2) - 4) / 6)) < 1e-15
    for z in (1e-2, 5e-3):
        lead = (stability_function(z) - math.exp(z)) / z**3
        assert abs(lead + k) < 0.05 * abs(k)


def rc_error(steps):
    ckt = RC(1.0, 1.0, lambda t: 1.0)
    out = tr_bdf2_fixed(ckt, [0.0], 0.0, 1.0, steps)
    return abs(out[-1][1][0] - (1 - math.exp(-1.0)))


def rlc_exact(t):
    alpha, wd = 0.5, math.sqrt(0.75)
    return 1 - math.exp(-alpha * t) * (math.cos(wd * t) + alpha / wd * math.sin(wd * t))


def rlc_error(steps):
    ckt = SeriesRLC(1.0, 1.0, 1.0, lambda t: 1.0)
    out = tr_bdf2_fixed(ckt, [1.0, 1.0, 0.0, 0.0, 0.0], 0.0, 5.0, steps)
    return max(abs(x[2] - rlc_exact(t)) for t, x in out)


def test_order_two_on_rc_and_rlc():
    e = [rc_error(s) for s in (10, 20, 40, 80)]
    ratios = [e[i] / e[i + 1] for i in range(3)]
    assert all(3.7 < r < 4.3 for r in ratios), ratios
    e = [rlc_error(s) for s in (50, 100, 200, 400)]
    ratios = [e[i] / e[i + 1] for i in range(3)]
    assert all(3.7 < r < 4.3 for r in ratios), ratios


def test_stiff_damping_versus_trapezoidal_ringing():
    # RC = 1 ms, h = 10 ms: h lambda = -10. The capacitor starts at 1 V, the source is 0.
    ckt = RC(1e-3, 1.0, lambda t: 0.0)
    x_tr, x_tb, x_be = [1.0], [1.0], [1.0]
    trap, trbdf, be = [], [], []
    for n in range(10):
        x_tr = trapezoidal_step(ckt, n * 0.01, x_tr, 0.01)
        x_tb, _, _ = tr_bdf2_step(ckt, n * 0.01, x_tb, 0.01)
        x_be = backward_euler_step(ckt, n * 0.01, x_be, 0.01)
        trap.append(x_tr[0])
        trbdf.append(x_tb[0])
        be.append(x_be[0])
    for n, v in enumerate(trap, 1):
        assert abs(v - (-2 / 3) ** n) < 1e-12
    assert abs(trbdf[0] - stability_function(-10.0)) < 1e-12
    assert abs(trap[4]) > 0.13 and abs(trbdf[4]) < 4e-4 and abs(be[4]) < 1e-5


def test_error_estimate_matches_true_error():
    ckt = Scalar(-1.0)
    for h in (0.1, 0.05, 0.025):
        y1, _, est = tr_bdf2_step(ckt, 0.0, [1.0], h)
        true = math.exp(-h) - y1[0]
        assert abs(est[0] / true - 1) < 0.1


def test_adaptive_rc_and_rectifier():
    ckt = RC(1.0, 1.0, lambda t: math.sin(3 * t))
    out, rej = tr_bdf2_adaptive(ckt, [0.0], 0.0, 4.0, 1e-3, rtol=1e-6, atol=1e-8)

    def exact(t):  # v' = sin 3t - v, v(0) = 0
        return (math.sin(3 * t) - 3 * math.cos(3 * t) + 3 * math.exp(-t)) / 10

    assert max(abs(x[0] - exact(t)) for t, x in out) < 2e-5
    assert len(out) < 600
    # the step count grows by about 10^(1/3) per decade of tolerance (local error h^3)
    n3 = len(tr_bdf2_adaptive(ckt, [0.0], 0.0, 4.0, 1e-3, rtol=1e-3, atol=1e-8)[0])
    n6 = len(out)
    assert 5 < n6 / n3 < 12

    rect = Rectifier(1e3, 1e-4, 5.0, 50.0)
    x0 = [0.0, 0.0, 0.0]
    out, rej = tr_bdf2_adaptive(rect, x0, 0.0, 0.04, 1e-5, rtol=1e-4, atol=1e-10)
    ref = tr_bdf2_fixed(rect, x0, 0.0, 0.04, 4000)
    assert abs(out[-1][1][1] - ref[-1][1][1]) < 2e-3
    assert len(out) < 200
    peak = max(x[1] for _, x in ref)
    assert 4.2 < peak < 4.4  # about one diode drop below 5 V
