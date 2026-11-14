# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/source-stepping/. The authors are listed in prov/QF22WC.jsonl.

import math
import random
from fractions import Fraction as F

import pytest

from source_stepping import NewtonFailure, newton, residual, source_stepping

IS, VT = 1e-14, 0.025852


def diode_circuit(e, r=1000.0):
    # A source e at node 1, a resistor r from node 1 to node 2 and a diode from node 2 to ground.
    return [("V", 1, 0, e), ("R", 1, 2, r), ("D", 2, 0, IS, VT)]


def safe_exp(u):
    return math.inf if u > 700 else math.exp(u)


def bisect(f, lo, hi):
    # f is increasing with f(lo) < 0 < f(hi).
    for _ in range(200):
        mid = (lo + hi) / 2
        if mid in (lo, hi):
            break
        if f(mid) < 0:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def diode_voltage_by_bisection(e, r=1000.0):
    return bisect(lambda v: IS * (safe_exp(v / VT) - 1) - (e - v) / r, 0.0, e)


def test_plain_newton_from_zero_overflows_and_source_stepping_does_not():
    net = diode_circuit(20.0)
    with pytest.raises(NewtonFailure) as info:
        newton(net, 2, [0.0, 0.0, 0.0], 1.0, max_iter=1000)
    assert isinstance(info.value.__cause__, OverflowError)
    x, stats = source_stepping(net, 2)
    v = diode_voltage_by_bisection(20.0)
    assert abs(x[1] - v) < 1e-9
    assert abs(x[2] + (20.0 - v) / 1000.0) < 1e-12  # the source current, from + through the source to -
    assert stats["path"][-1][0] == 1


def test_plain_newton_from_zero_is_slow_at_five_volts():
    net = diode_circuit(5.0)
    with pytest.raises(NewtonFailure):
        newton(net, 2, [0.0, 0.0, 0.0], 1.0, max_iter=100)
    x_plain, its = newton(net, 2, [0.0, 0.0, 0.0], 1.0, max_iter=1000)
    assert its > 150  # about (5 - 0.69) / VT steps of size VT down the exponential
    x, stats = source_stepping(net, 2)
    assert stats["iterations"] < its
    v = diode_voltage_by_bisection(5.0)
    assert abs(x[1] - v) < 1e-9 and abs(x_plain[1] - v) < 1e-9
    assert abs(x[1] - 0.69254) < 1e-5


def test_homotopy_end_points():
    net = diode_circuit(20.0) + [("I", 0, 2, 1e-3)]
    # At lam = 0 every source is off and x = 0 solves the circuit exactly.
    assert residual(net, 2, [0.0, 0.0, 0.0], 0) == [0.0, 0.0, 0.0]
    x, stats = source_stepping(net, 2)
    # At lam = 1 the circuit is the given one.
    assert max(abs(v) for v in residual(net, 2, x, 1)) < 1e-12
    lams = [lam for lam, _ in stats["path"]]
    assert lams[0] == 0 and lams[-1] == 1 and lams == sorted(lams)


def test_linear_circuit_path_is_exact_and_proportional():
    # 10 V at node 1, 2 ohm from 1 to 2, 8 ohm from 2 to ground: e = (10, 8), source current -1.
    net = [("V", 1, 0, F(10)), ("R", 1, 2, F(2)), ("R", 2, 0, F(8))]
    x, stats = source_stepping(net, 2, first_step=F(1, 4))
    assert x == [10, 8, -1]
    assert [lam for lam, _ in stats["path"]] == [0, F(1, 4), F(3, 4), 1]
    for lam, xs in stats["path"]:
        assert xs == [lam * 10, lam * 8, -lam]


def test_no_operating_point_is_reported():
    # The source pulls 1 mA out of the anode, so the diode would need a reverse current of 1 mA.
    net = [("I", 1, 0, 1e-3), ("D", 1, 0, IS, VT)]
    with pytest.raises(NewtonFailure):
        source_stepping(net, 1)


def random_diode_network(rng, n):
    net = []
    for k in range(1, n + 1):
        net.append(("R", k, 0, rng.uniform(100.0, 10000.0)))
        net.append(("I", 0, k, rng.uniform(0.0, 0.01)))
        if k < n:
            net.append(("R", k, k + 1, rng.uniform(100.0, 10000.0)))
        p, q = (k, rng.randint(0, n)) if rng.random() < 0.5 else (rng.randint(0, n), k)
        if p != q:
            net.append(("D", p, q, IS, VT))
    return net


def gauss_seidel(net, n):
    # Nonlinear Gauss-Seidel: solve the KCL of one node at a time by bisection.
    # Every element is monotone, so the current leaving node k increases with e_k.
    e = [0.0] * (n + 1)
    at = {k: [el for el in net if k in (el[1], el[2])] for k in range(1, n + 1)}

    def leaving(k, ek):
        old, e[k] = e[k], ek
        s = 0.0
        for el in at[k]:
            kind, p, q = el[0], el[1], el[2]
            if kind == "R":
                i = (e[p] - e[q]) / el[3]
            elif kind == "I":
                i = el[3]
            else:
                i = el[3] * (safe_exp((e[p] - e[q]) / el[4]) - 1)
            s += i if p == k else -i
        e[k] = old
        return s

    for _ in range(5000):
        change = 0.0
        for k in range(1, n + 1):
            lo, hi = -1.0, 1.0
            while leaving(k, lo) > 0:
                lo *= 2
            while leaving(k, hi) < 0:
                hi *= 2
            v = bisect(lambda u: leaving(k, u), lo, hi)
            change = max(change, abs(v - e[k]))
            e[k] = v
        if change < 1e-14:
            break
    return e[1:]


def test_random_monotone_circuits_against_gauss_seidel():
    rng = random.Random(20240611)
    hard = 0
    for _ in range(8):
        n = rng.randint(2, 4)
        net = random_diode_network(rng, n)
        try:
            newton(net, n, [0.0] * n, 1.0, max_iter=50)
        except NewtonFailure:
            hard += 1
        x, _ = source_stepping(net, n)
        ref = gauss_seidel(net, n)
        # Gauss-Seidel converges slowly when diodes couple the nodes strongly, so it only gives about 7 digits.
        assert max(abs(a - b) for a, b in zip(x, ref)) < 1e-6
        assert max(abs(v) for v in residual(net, n, x, 1)) < 1e-12
    assert hard > 0  # some of these circuits defeat plain Newton from zero
