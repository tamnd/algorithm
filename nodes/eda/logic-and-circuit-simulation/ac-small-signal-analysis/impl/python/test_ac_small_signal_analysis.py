# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ac-small-signal-analysis/. The authors are listed in prov/ZS7YDS.jsonl.

import cmath
import math
import random

import sim3dense
from ac_small_signal_analysis import (
    Netlist,
    ac_analysis,
    bode,
    dc_operating_point,
    decade_sweep,
    unit,
)

# Level-1 MOSFET parameters: K (transconductance), VT (threshold) and LAM
# (channel-length modulation) are fitted model parameters, as is the overlap
# capacitance CGD; these are typical teaching values.
K, VT, LAM = 200e-6, 0.5, 0.05
VDD, RD, CL, CGD, VG = 1.8, 50e3, 100e-15, 5e-15, 0.8


def cs_amp(vg=VG):
    net = Netlist(3)  # node 1 supply, 2 drain (output), 3 gate (input)
    net.vsource(1, 0, VDD)
    net.vsource(3, 0, vg, 1.0)
    net.resistor(1, 2, RD)
    net.mosfet("n", 2, 3, 0, K, VT, LAM)
    net.capacitor(3, 2, CGD)
    net.capacitor(2, 0, CL)
    return net


def test_rc_lowpass():
    r, c = 1e3, 1e-9
    net = Netlist(2)
    net.vsource(1, 0, 0.0, 1.0)
    net.resistor(1, 2, r)
    net.capacitor(2, 0, c)
    ws = decade_sweep(1.0, 1e9, 5)
    assert len(ws) == 46
    _, H = ac_analysis(net, ws, unit(net, 2))
    for w, h in zip(ws, H):
        assert abs(h - 1 / (1 + 1j * w * r * c)) < 1e-12
    _, (h,) = ac_analysis(net, [1 / (r * c)], unit(net, 2))
    db, ph = bode(h)
    assert abs(db + 10 * math.log10(2)) < 1e-9 and abs(ph + 45) < 1e-9


def series_rlc(r, l, c):
    net = Netlist(3)
    net.vsource(1, 0, 0.0, 1.0)
    net.resistor(1, 2, r)
    net.inductor(2, 3, l)
    net.capacitor(3, 0, c)
    return net


def test_series_rlc_and_the_time_domain_identity():
    r, l, c = 10.0, 1e-6, 1e-9
    net = series_rlc(r, l, c)
    w0 = 1 / math.sqrt(l * c)
    ws = [w0 * 10 ** (k / 10) for k in range(-20, 21)]
    _, H = ac_analysis(net, ws, unit(net, 3))
    for w, h in zip(ws, H):
        assert abs(h - 1 / (1 - w * w * l * c + 1j * w * r * c)) < 1e-9 * abs(h)
    # at resonance the gain is the quality factor (1/R) sqrt(L/C)
    assert abs(abs(H[20]) - math.sqrt(l / c) / r) < 1e-9
    # Re(X e^{jwt}) solves G x + C x' = Re(b e^{jwt}) at every t
    x0 = dc_operating_point(net)
    _, G, _, C = net.evaluate(x0)
    b = net.sources(1)
    w = 0.7 * w0
    Y = [[G[i][j] + 1j * w * C[i][j] for j in range(5)] for i in range(5)]
    X = sim3dense.solve(Y, [complex(v) for v in b])
    rng = random.Random(71)
    for _ in range(20):
        t = rng.uniform(0, 10 / w)
        x = [(xi * cmath.exp(1j * w * t)).real for xi in X]
        dx = [(1j * w * xi * cmath.exp(1j * w * t)).real for xi in X]
        lhs = [sum(G[i][j] * x[j] + C[i][j] * dx[j] for j in range(5)) for i in range(5)]
        rhs = [(bi * cmath.exp(1j * w * t)).real for bi in b]
        assert max(abs(p - q) for p, q in zip(lhs, rhs)) < 1e-9


def test_common_source_amplifier_against_hand_analysis():
    net = cs_amp()
    ws = decade_sweep(1e3, 1e11, 4)
    x0, H = ac_analysis(net, ws, unit(net, 2))
    # DC point in closed form: (K/2) vov^2 (1 + LAM vds) RD = VDD - vds
    vov = VG - VT
    a = K / 2 * vov**2 * RD
    vds = (VDD - a) / (1 + a * LAM)
    assert abs(x0[1] - vds) < 1e-12
    gm = K * vov * (1 + LAM * vds)
    gds = K / 2 * vov**2 * LAM
    for w, h in zip(ws, H):
        hand = -(gm - 1j * w * CGD) / (1 / RD + gds + 1j * w * (CL + CGD))
        assert abs(h - hand) < 1e-12 * abs(hand)
    assert abs(H[0] + gm / (1 / RD + gds)) < 2e-4  # at 1 kHz, far below the pole
    assert abs(H[-1] - CGD / (CL + CGD)) < 1e-3  # feedthrough of the gate-drain capacitance


def test_zero_frequency_is_the_dc_gain():
    _, (h0,) = ac_analysis(cs_amp(), [0.0], unit(cs_amp(), 2))
    d = 1e-6
    fd = (dc_operating_point(cs_amp(VG + d))[1] - dc_operating_point(cs_amp(VG - d))[1]) / (2 * d)
    assert abs(h0.imag) == 0
    assert abs(h0.real - fd) < 1e-7 * abs(fd)


def test_random_rc_networks_against_nodal_admittance():
    rng = random.Random(72)
    for _ in range(30):
        n = rng.randint(2, 7)
        net = Netlist(n)
        Y = lambda w: [[0j] * n for _ in range(n)]
        edges = []
        for _ in range(2 * n):
            p, q = rng.sample(range(n + 1), 2)
            g, c = rng.uniform(0.1, 2), rng.uniform(0.1, 2)
            net.resistor(p, q, 1 / g)
            net.capacitor(p, q, c)
            edges.append((p, q, g, c))
        for i in range(1, n + 1):
            net.resistor(i, 0, 10.0)
            edges.append((i, 0, 0.1, 0.0))
        net.isource(0, 1, 0.0, 1.0)  # inject 1 A (phasor) into node 1
        w = rng.uniform(0.1, 10)
        Ym = Y(w)
        for p, q, g, c in edges:
            y = g + 1j * w * c
            for a, b2, s in ((p, p, 1), (q, q, 1), (p, q, -1), (q, p, -1)):
                if a and b2:
                    Ym[a - 1][b2 - 1] += s * y
        inj = [0j] * n
        inj[0] = 1
        ref = sim3dense.solve(Ym, inj)
        for node in range(1, n + 1):
            _, (h,) = ac_analysis(net, [w], unit(net, node))
            assert abs(h - ref[node - 1]) < 1e-10 * (1 + abs(ref[node - 1]))


def transient_fundamental(net, x0, eps, w, periods, m):
    """Trapezoidal transient with the AC sources scaled by eps cos(wt); the
    complex amplitude of the output's fundamental over the last period, over eps."""
    b, u0 = net.sources(1), net.sources(0)
    h = 2 * math.pi / w / m

    def u(t):
        return [a + eps * bb * math.cos(w * t) for a, bb in zip(u0, b)]

    x = list(x0)
    f, _, q, _ = net.evaluate(x)
    acc = 0j
    for k in range(periods * m):
        un, un1 = u(k * h), u((k + 1) * h)
        y = list(x)
        for _ in range(30):
            f1, g1, q1, c1 = net.evaluate(y)
            r = [q1[i] - q[i] + h / 2 * (f1[i] - un1[i] + f[i] - un[i]) for i in range(len(y))]
            jac = [[c1[i][j] + h / 2 * g1[i][j] for j in range(len(y))] for i in range(len(y))]
            dy = sim3dense.solve(jac, [-v for v in r])
            y = [a + d for a, d in zip(y, dy)]
            if max(abs(d) for d in dy) < 1e-13:
                break
        x = y
        f, _, q, _ = net.evaluate(x)
        if k + 1 > (periods - 1) * m:
            acc += x[1] * cmath.exp(-1j * w * (k + 1) * h)
    return 2 * acc / m / eps


def test_small_sinusoid_transient_matches_ac():
    net = cs_amp()
    w = 2 * math.pi * 31e6  # near the pole
    x0, (H,) = ac_analysis(net, [w], unit(net, 2))
    e100 = abs(transient_fundamental(net, x0, 1e-3, w, 8, 100) - H) / abs(H)
    t4 = transient_fundamental(net, x0, 1e-4, w, 8, 200)
    t3 = transient_fundamental(net, x0, 1e-3, w, 8, 200)
    t2 = transient_fundamental(net, x0, 1e-2, w, 8, 200)
    e200 = abs(t3 - H) / abs(H)
    assert e200 < 1e-4
    assert 3.5 < e100 / e200 < 4.5  # the trapezoidal error, second order in the step
    # the nonlinear part of the response grows like the square of the amplitude
    d3, d2 = abs(t3 - t4) / abs(H), abs(t2 - t4) / abs(H)
    assert 60 < d2 / d3 < 140
