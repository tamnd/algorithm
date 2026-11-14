# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/circuit-noise-analysis/. The authors are listed in prov/P2C0RA.jsonl.

import math
import random

import sim3dense
from circuit_noise_analysis import (
    BOLTZMANN,
    CHARGE,
    Netlist,
    noise_analysis,
    noise_direct,
    transfer,
    unit,
)

KT = BOLTZMANN * 300.0

# Level-1 MOSFET: K, VT and LAM are fitted model parameters, and so are the
# flicker coefficients KF and AF. COX_L2 = Cox Leff^2 for Cox = 8.6 mF/m^2 and
# Leff = 1 um is a geometry value. These are typical teaching values.
K, VT, LAM = 200e-6, 0.5, 0.05
KF, AF, COX_L2 = 1e-28, 1.0, 8.6e-15
VDD, RD, CL, CGD, VG = 1.8, 50e3, 100e-15, 5e-15, 0.8


def cs_amp(kf=KF):
    net = Netlist(3)  # node 1 supply, 2 drain (output), 3 gate (input)
    net.vsource(1, 0, VDD)
    net.vsource(3, 0, VG, 1.0)
    net.resistor(1, 2, RD)
    net.mosfet("n", 2, 3, 0, K, VT, LAM, kf, AF, COX_L2)
    net.capacitor(3, 2, CGD)
    net.capacitor(2, 0, CL)
    return net


def test_divider_is_the_thermal_noise_of_the_parallel_resistance():
    for r1, r2 in ((1e3, 1e3), (1e3, 3e3), (47e3, 2.2e3)):
        net = Netlist(2)
        net.vsource(1, 0, 1.0)
        net.resistor(1, 2, r1)
        net.resistor(2, 0, r2)
        _, (s,), (share,) = noise_analysis(net, [1e3], unit(net, 2))
        rp = r1 * r2 / (r1 + r2)
        assert abs(s - 4 * KT * rp) < 1e-12 * s
        # each resistor contributes 4kT/R_i times (R1 || R2)^2
        assert abs(share["R1 thermal"] - 4 * KT / r1 * rp * rp) < 1e-12 * s
        assert abs(share["R2 thermal"] - 4 * KT / r2 * rp * rp) < 1e-12 * s


def test_rc_total_noise_is_kt_over_c_for_every_r():
    c = 1e-12
    for r in (1e2, 1e4, 1e6):
        net = Netlist(2)
        net.vsource(1, 0, 0.0)
        net.resistor(1, 2, r)
        net.capacitor(2, 0, c)
        fc = 1 / (2 * math.pi * r * c)
        # f = fc tan(theta) maps [0, inf) onto [0, pi/2); midpoint rule
        m = 64
        thetas = [(i + 0.5) * (math.pi / 2) / m for i in range(m)]
        _, dens, _ = noise_analysis(net, [fc * math.tan(t) for t in thetas], unit(net, 2))
        total = sum(s * fc / math.cos(t) ** 2 for s, t in zip(dens, thetas)) * (math.pi / 2) / m
        assert abs(total - KT / c) < 1e-9 * KT / c


def test_common_source_amplifier_against_hand_analysis():
    net = cs_amp()
    fs = [10 ** (k / 4) for k in range(0, 45)]
    x0, dens, parts = noise_analysis(net, fs, unit(net, 2))
    vov = VG - VT
    a = K / 2 * vov**2 * RD
    vds = (VDD - a) / (1 + a * LAM)
    assert abs(x0[1] - vds) < 1e-12
    gm = K * vov * (1 + LAM * vds)
    gds = K / 2 * vov**2 * LAM
    idd = K / 2 * vov**2 * (1 + LAM * vds)
    white = 4 * KT / RD + 8 / 3 * KT * gm
    for f, s in zip(fs, dens):
        w = 2 * math.pi * f
        z2 = 1 / abs(1 / RD + gds + 1j * w * (CL + CGD)) ** 2
        hand = (white + KF * idd ** AF / (f * COX_L2)) * z2
        assert abs(s - hand) < 1e-12 * hand
    # at the flicker corner the flicker share is one half of the device noise
    corner = KF * idd / (COX_L2 * white)
    _, (s,), (share,) = noise_analysis(net, [corner], unit(net, 2))
    assert abs(share["M3 flicker"] / s - 0.5) < 1e-12
    # input-referred white noise is the output noise over the gain squared
    _, (s,), _ = noise_analysis(cs_amp(0.0), [1e3], unit(net, 2))
    (h,) = transfer(cs_amp(0.0), [1e3], unit(net, 2))
    assert abs(s / abs(h) ** 2 - white / gm**2) < 1e-6 * white / gm**2


def test_diode_shot_noise():
    for ib in (1e-6, 1e-4, 1e-3):
        net = Netlist(1)
        net.isource(0, 1, ib)  # bias current into the anode
        net.diode(1, 0, 1e-14)  # the saturation current is a fitted value
        x0, (s,), _ = noise_analysis(net, [1e4], unit(net, 1))
        nvt = KT / CHARGE
        gd = 1e-14 * math.exp(x0[0] / nvt) / nvt
        assert abs(s - 2 * CHARGE * ib / gd**2) < 1e-9 * s
        # gd is close to ib / VT, so the density is close to 2 q VT^2 / ib
        assert abs(s / (2 * CHARGE * nvt**2 / ib) - 1) < 1e-7


def random_network(rng, n):
    net = Netlist(n)
    for _ in range(2 * n):
        p, q = rng.sample(range(n + 1), 2)
        net.resistor(p, q, rng.uniform(0.5, 10))
        net.capacitor(p, q, rng.uniform(0.1, 2))
    for i in range(1, n + 1):
        net.resistor(i, 0, 20.0)
    for _ in range(n):
        p, q, c, d = rng.sample(range(n + 1), 4)
        net.vccs(p, q, c, d, rng.uniform(-1.0, 1.0))
    p, q = rng.sample(range(1, n + 1), 2)
    net.inductor(p, q, rng.uniform(0.1, 2))
    net.vsource(1, 0, 0.0)
    return net


def test_adjoint_equals_direct_summation_on_random_networks():
    rng = random.Random(81)
    wrong = 0
    for _ in range(40):
        n = rng.randint(3, 7)
        net = random_network(rng, n)
        out = [0.0] * net.size
        out[rng.randrange(1, n)] = 1.0
        fs = [rng.uniform(0.001, 1.0) for _ in range(3)]
        _, adj, _ = noise_analysis(net, fs, out)
        ref = noise_direct(net, fs, out)
        for a, b in zip(adj, ref):
            assert abs(a - b) <= 1e-10 * b
        # solving with Y instead of its transpose gives wrong gains when Y is not symmetric
        _, G, _, C = net.evaluate([0.0] * net.size)
        w = 2 * math.pi * fs[0]
        y = [[complex(G[i][j], w * C[i][j]) for j in range(net.size)] for i in range(net.size)]
        z = sim3dense.solve(y, [complex(o) for o in out])
        bad = 0.0
        for _, p, q, s in net.noise_sources([0.0] * net.size):
            h = (z[q - 1] if q else 0) - (z[p - 1] if p else 0)
            bad += abs(h) ** 2 * s(fs[0])
        if abs(bad - ref[0]) > 1e-3 * ref[0]:
            wrong += 1
    assert wrong >= 30
