# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/companion-model/. The authors are listed in prov/JH4KPG.jsonl.

import math
import random
from fractions import Fraction as F

import pytest

from companion_model import capacitor_be, capacitor_tr, inductor_be, inductor_tr, transient


def rc_circuit(e_src, r, c):
    # A source e_src with series resistor r, as its Norton form: e_src / r into node 1 and r from 1 to ground.
    return [("I", 0, 1, lambda t: e_src / r), ("R", 1, 0, r), ("C", 1, 0, c)]


def test_single_step_formulas():
    c, h, v0, i0 = F(3), F(1, 2), F(2), F(5)
    g, j = capacitor_be(c, h, v0)
    v1 = F(7)
    assert g * v1 + j == c * (v1 - v0) / h
    g, j = capacitor_tr(c, h, v0, i0)
    i1 = g * v1 + j
    assert (i1 + i0) / 2 == c * (v1 - v0) / h  # the trapezoidal rule for c dv/dt = i
    l = F(4)
    g, j = inductor_be(l, h, i0)
    assert (g * v1 + j - i0) / h == v1 / l
    g, j = inductor_tr(l, h, v0, i0)
    assert (g * v1 + j - i0) / h == (v1 + v0) / (2 * l)


@pytest.mark.parametrize("method", ["be", "tr"])
def test_rc_matches_the_exact_recurrence(method):
    e_src, r, c, h = F(5), F(2), F(3, 4), F(1, 10)
    tau = r * c
    net = rc_circuit(e_src, r, c)
    steps = 12
    cap_i = {2: e_src / r} if method == "tr" else None
    out = transient(net, 1, [F(0), F(0)], h, steps, method, capacitor_currents=cap_i)
    if method == "be":
        rho = 1 / (1 + h / tau)
    else:
        rho = (1 - h / (2 * tau)) / (1 + h / (2 * tau))
    for k, e in enumerate(out):
        assert e[1] == e_src * (1 - rho**k)


def rc_error(method, steps, give_current=True):
    e_src, r, c, t_end = 1.0, 1.0, 1.0, 1.0
    h = t_end / steps
    cap_i = {2: e_src / r} if give_current else None
    out = transient(rc_circuit(e_src, r, c), 1, [0.0, 0.0], h, steps, method, capacitor_currents=cap_i)
    exact = [e_src * (1 - math.exp(-k * h / (r * c))) for k in range(steps + 1)]
    return max(abs(e[1] - x) for e, x in zip(out, exact))


def test_backward_euler_error_falls_like_h():
    errs = [rc_error("be", s) for s in (20, 40, 80, 160, 320)]
    ratios = [a / b for a, b in zip(errs, errs[1:])]
    assert all(1.9 < q < 2.1 for q in ratios), ratios
    assert errs[-1] < 2e-3


def test_trapezoidal_error_falls_like_h_squared():
    errs = [rc_error("tr", s) for s in (20, 40, 80, 160, 320)]
    ratios = [a / b for a, b in zip(errs, errs[1:])]
    assert all(3.9 < q < 4.1 for q in ratios), ratios
    assert errs[-1] < 2e-6


def test_one_backward_euler_start_keeps_second_order():
    errs = [rc_error("tr", s, give_current=False) for s in (20, 40, 80, 160, 320)]
    ratios = [a / b for a, b in zip(errs, errs[1:])]
    assert all(3.5 < q < 4.5 for q in ratios), ratios


def test_rl_current_converges_with_the_right_order():
    # A current source s into node 1, r from 1 to ground and l from 1 to ground: i_L = s (1 - exp(-t r / l)).
    s, r, l = 2.0, 3.0, 1.5
    net = [("I", 0, 1, lambda t: s), ("R", 1, 0, r), ("L", 1, 0, l)]

    def err(method, steps):
        h = 1.0 / steps
        out = transient(net, 1, [0.0, s * r], h, steps, method, inductor_currents={2: 0.0})
        worst = 0.0
        i_l = 0.0
        for k in range(1, steps + 1):
            i_l = s - out[k][1] / r  # KCL at node 1
            worst = max(worst, abs(i_l - s * (1 - math.exp(-k * h * r / l))))
        return worst

    be = [err("be", n) for n in (40, 80, 160, 320)]
    tr = [err("tr", n) for n in (40, 80, 160, 320)]
    assert all(1.8 < a / b < 2.2 for a, b in zip(be, be[1:])), be
    assert all(3.8 < a / b < 4.2 for a, b in zip(tr, tr[1:])), tr


def lc_energy(e, i_l, c, l):
    return (c * e * e + l * i_l * i_l) / 2


def test_trapezoidal_keeps_lc_energy_and_backward_euler_loses_it():
    c, l, h = F(1, 2), F(2), F(1, 5)
    net = [("C", 1, 0, c), ("L", 1, 0, l)]
    for method in ("tr", "be"):
        # e(0) = 1, i_L(0) = 0, so KCL gives i_C(0) = 0.
        out = transient(net, 1, [F(0), F(1)], h, 25, method, inductor_currents={1: F(0)}, capacitor_currents={0: F(0)})
        energies = []
        i_l = F(0)
        v_old = F(1)
        for e in out[1:]:
            v = e[1]
            if method == "tr":
                i_l = i_l + h / (2 * l) * (v + v_old)
            else:
                i_l = i_l + h / l * v
            v_old = v
            energies.append(lc_energy(v, i_l, c, l))
        if method == "tr":
            assert all(en == F(1, 4) for en in energies)
        else:
            assert all(b < a for a, b in zip([F(1, 4)] + energies, energies))


def test_random_linear_circuits_against_a_fine_reference():
    # Random RC ladders: the trapezoidal answer at h and at h/2 must agree to the order h^2.
    rng = random.Random(4242)
    for _ in range(5):
        n = rng.randint(2, 4)
        net = [("I", 0, 1, lambda t: 1.0)]
        for k in range(1, n + 1):
            net.append(("C", k, 0, rng.uniform(0.5, 2.0)))
            net.append(("R", k, 0, rng.uniform(0.5, 2.0)))
            if k < n:
                net.append(("R", k, k + 1, rng.uniform(0.5, 2.0)))
        e0 = [0.0] * (n + 1)
        cap_i = {k: (1.0 if net[k][1] == 1 else 0.0) for k, el in enumerate(net) if el[0] == "C"}
        coarse = transient(net, n, e0, 0.02, 50, "tr", capacitor_currents=cap_i)[-1]
        fine = transient(net, n, e0, 0.01, 100, "tr", capacitor_currents=cap_i)[-1]
        finer = transient(net, n, e0, 0.005, 200, "tr", capacitor_currents=cap_i)[-1]
        d1 = max(abs(a - b) for a, b in zip(coarse, fine))
        d2 = max(abs(a - b) for a, b in zip(fine, finer))
        assert d1 < 1e-3
        assert 3.5 < d1 / d2 < 4.5
