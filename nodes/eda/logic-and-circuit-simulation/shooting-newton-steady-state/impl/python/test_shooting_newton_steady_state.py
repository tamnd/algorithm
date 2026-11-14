# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/shooting-newton-steady-state/. The authors are listed in prov/FS9DNT.jsonl.

import cmath
import math
import random

import sim3dense
from shooting_newton_steady_state import Netlist, period_map, shooting, transient_until_periodic

F0 = 1e6
W = 2 * math.pi * F0
T = 1 / F0

# Diode parameters: the saturation current IS and the emission coefficient N
# are fitted model parameters (typical values for a small silicon diode).
IS, N = 1e-14, 1.0


def rectifier():
    """2 V, 1 MHz source behind 1 kOhm (Norton form), diode, 100 kOhm || 1 nF load."""
    net = Netlist(2)
    net.isource(0, 1, lambda t: 2e-3 * math.sin(W * t))
    net.resistor(1, 0, 1e3)
    net.capacitor(1, 0, 10e-12)
    net.diode(1, 2, IS, N)
    net.resistor(2, 0, 100e3)
    net.capacitor(2, 0, 1e-9)
    return net


def parallel_rlc(r=200.0, l=10e-6, c=2e-9):
    """1 mA cosine source into R, L and C in parallel; unknowns e1 and the L current."""
    net = Netlist(1)
    net.isource(0, 1, lambda t: 1e-3 * math.cos(W * t))
    net.resistor(1, 0, r)
    net.inductor(1, 0, l)
    net.capacitor(1, 0, c)
    return net, r, l, c


def phasor(r, l, c, s):
    """Node voltage phasor of parallel_rlc for the complex frequency s (source phasor 1 mA)."""
    return 1e-3 / (1 / r + 1 / (s * l) + s * c)


def test_linear_trapezoidal_is_exact_for_the_discrete_map_in_one_newton_step():
    net, r, l, c = parallel_rlc()
    for S in (40, 80, 160):
        h = T / S
        x, it, hist, states = shooting(net, T, S, method="trap")
        assert it == 2  # the first step solves the affine problem
        # the trapezoidal recurrence has the periodic solution of the frequency
        # s_d = j (2/h) tan(w h / 2), the warped frequency of the bilinear map
        sd = 2j / h * math.tan(W * h / 2)
        v = phasor(r, l, c, sd)
        for k in range(S + 1):
            assert abs(states[k][0] - (v * cmath.exp(1j * W * k * h)).real) < 1e-12


def test_linear_backward_euler_matches_its_discrete_phasor():
    net = Netlist(2)  # voltage source with an algebraic row, R, C
    net.vsource(1, 0, lambda t: math.cos(W * t))
    net.resistor(1, 2, 1e3)
    net.capacitor(2, 0, 100e-12)
    S = 64
    h = T / S
    x, it, _, states = shooting(net, T, S, method="be")
    assert it == 2
    z = cmath.exp(1j * W * h)
    sd = (1 - 1 / z) / h  # backward Euler: (x_k - x_{k-1}) / h
    v2 = 1 / (1 + sd * 1e3 * 100e-12)
    for k in range(S + 1):
        assert abs(states[k][1] - (v2 * cmath.exp(1j * W * k * h)).real) < 1e-12


def test_error_against_the_analytic_steady_state_is_second_order():
    net, r, l, c = parallel_rlc()
    exact = phasor(r, l, c, 1j * W)
    errs = []
    for S in (40, 80, 160):
        x, _, _, _ = shooting(net, T, S, method="trap")
        errs.append(abs(x[0] - exact.real))
    # measured ratios: about 4 per halving of the step
    assert 3.8 < errs[0] / errs[1] < 4.2 and 3.8 < errs[1] / errs[2] < 4.2


def test_monodromy_matches_finite_differences():
    rng = random.Random(61)
    net = rectifier()
    for _ in range(3):
        x0 = [rng.uniform(-0.5, 0.5), rng.uniform(0.5, 1.5)]
        _, Phi, _ = period_map(net, x0, T, 50)
        eps = 1e-6
        for b in range(2):
            xp, xm = list(x0), list(x0)
            xp[b] += eps
            xm[b] -= eps
            fp, _, _ = period_map(net, xp, T, 50, sensitivity=False)
            fm, _, _ = period_map(net, xm, T, 50, sensitivity=False)
            for a in range(2):
                fd = (fp[a] - fm[a]) / (2 * eps)
                assert abs(fd - Phi[a][b]) < 1e-6 * (1 + abs(Phi[a][b]))


def test_rectifier_agrees_with_a_long_transient_and_converges_quadratically():
    net = rectifier()
    S = 100
    x, it, hist, _ = shooting(net, T, S)
    xt, periods = transient_until_periodic(net, T, S, tol=1e-9)
    # measured: 7 Newton iterations against 155 periods of plain transient
    assert it <= 8 and periods > 100
    # the transient stops 1e-9 per period from its limit, which is about 1e-8 away
    assert max(abs(a - b) for a, b in zip(x, xt)) < 2e-8
    # quadratic convergence: each residual is at most about the square of the last
    tail = [h for h in hist if h < 1e-2]
    for a, b in zip(tail, tail[1:]):
        assert b < 50 * a * a + 1e-14


def test_trapezoidal_rule_makes_algebraic_rows_singular_for_even_step_counts():
    net = Netlist(2)
    net.vsource(1, 0, lambda t: math.cos(W * t))
    net.resistor(1, 2, 1e3)
    net.capacitor(2, 0, 100e-12)
    x0 = [0.3, 0.1, -1e-4]
    _, G, _, _ = net.evaluate(x0)
    row = G[2]  # the source row e_1 = v(t) has no charge term
    for S, sign in ((64, 1.0), (65, -1.0)):
        _, Phi, _ = period_map(net, x0, T, S, method="trap")
        # proved: row^T Phi = (-1)^S row^T, so row^T (Phi - I) is 0 or -2 row^T
        prod = [sum(row[a] * (Phi[a][b] - (a == b)) for a in range(3)) for b in range(3)]
        target = [0.0 if sign > 0 else -2 * v for v in row]
        assert max(abs(p - t) for p, t in zip(prod, target)) < 1e-9
    _, Phi, _ = period_map(net, x0, T, 64, method="be")
    prod = [sum(row[a] * (Phi[a][b] - (a == b)) for a in range(3)) for b in range(3)]
    assert max(abs(p + v) for p, v in zip(prod, row)) < 1e-9  # backward Euler: row^T Phi = 0
    try:
        sim3dense.solve([[Phi[a][b] - (a == b) for b in range(3)] for a in range(3)], [1.0, 0.0, 0.0])
    except sim3dense.SingularMatrixError:
        raise AssertionError("backward Euler should give a nonsingular Newton matrix")
