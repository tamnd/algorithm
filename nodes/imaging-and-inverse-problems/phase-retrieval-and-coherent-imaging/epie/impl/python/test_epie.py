# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/epie/. The authors are listed in prov/RV95GV.jsonl.

import cmath
import math
import random

from epie import data_error, epie, exit_wave, forward_amplitudes, modulus_replace, patch
from imgkit import dft2, idft2


def rand_obj(rng, n1, n2):
    return [[rng.uniform(0.6, 1.0) * cmath.exp(1j * rng.uniform(-1.2, 1.2)) for _ in range(n2)] for _ in range(n1)]


def gauss_probe(m1, m2):
    ca, cb = (m1 - 1) / 2, (m2 - 1) / 2
    return [
        [math.exp(-((a - ca) ** 2 + (b - cb) ** 2) / 8.0) * cmath.exp(0.3j * ((a - ca) ** 2 + (b - cb) ** 2)) for b in range(m2)]
        for a in range(m1)
    ]


def max_diff(a, b):
    return max(abs(x - y) for ra, rb in zip(a, b) for x, y in zip(ra, rb))


def aligned_error(est, true, rows, cols):
    """Max error of est against true on a region, after the best global phase."""
    num = sum(est[i][j].conjugate() * true[i][j] for i in rows for j in cols)
    g = num / abs(num)
    return max(abs(est[i][j] * g - true[i][j]) for i in rows for j in cols)


def test_forward_matches_direct_dft():
    rng = random.Random(1)
    obj, probe = rand_obj(rng, 6, 7), gauss_probe(3, 4)
    pos = (2, 1)
    amps = forward_amplitudes(obj, probe, [pos])[0]
    for k in range(3):
        for l in range(4):
            s = sum(
                probe[a][b] * obj[2 + a][1 + b] * cmath.exp(-2j * math.pi * (a * k / 3 + b * l / 4))
                for a in range(3)
                for b in range(4)
            )
            assert abs(abs(s) - amps[k][l]) < 1e-12


def test_modulus_replacement_is_nearest_point():
    rng = random.Random(2)
    spec = [[complex(rng.gauss(0, 1), rng.gauss(0, 1)) for _ in range(4)] for _ in range(4)]
    amp = [[rng.uniform(0, 2) for _ in range(4)] for _ in range(4)]
    best = modulus_replace(spec, amp)
    for i in range(4):
        for j in range(4):
            assert abs(abs(best[i][j]) - amp[i][j]) < 1e-12
            d = abs(best[i][j] - spec[i][j])
            assert abs(d - abs(abs(spec[i][j]) - amp[i][j])) < 1e-12
            for _ in range(20):
                z = amp[i][j] * cmath.exp(1j * rng.uniform(-math.pi, math.pi))
                assert d <= abs(z - spec[i][j]) + 1e-12
    assert modulus_replace([[0j]], [[1.5]]) == [[1.5 + 0j]]


def test_true_pair_is_fixed_point():
    rng = random.Random(3)
    obj, probe = rand_obj(rng, 8, 8), gauss_probe(4, 4)
    pos = [(r, c) for r in (0, 2, 4) for c in (0, 2, 4)]
    amps = forward_amplitudes(obj, probe, pos)
    o, p = epie(amps, pos, obj, probe, 3)
    assert max_diff(o, obj) < 1e-12
    assert max_diff(p, probe) < 1e-12
    assert data_error(amps, pos, o, p) < 1e-24


def test_one_step_matches_the_update_formulas():
    rng = random.Random(4)
    obj, probe = rand_obj(rng, 4, 8), gauss_probe(4, 4)
    pos = [(0, 3)]
    amps = [[[rng.uniform(0.2, 3.0) for _ in range(4)] for _ in range(4)]]
    psi = exit_wave(obj, probe, pos[0])
    psi2 = idft2(modulus_replace(dft2(psi), amps[0]))
    o_old = patch(obj, pos[0], 4, 4)
    pmax = max(abs(v) ** 2 for row in probe for v in row)
    omax = max(abs(v) ** 2 for row in o_old for v in row)
    for alpha, beta in ((1.0, 1.0), (0.5, 0.2), (2.0, 1.0)):
        o, p = epie(amps, pos, obj, probe, 1, alpha=alpha, beta=beta)
        for a in range(4):
            for b in range(4):
                d = psi2[a][b] - psi[a][b]
                want_o = o_old[a][b] + alpha * probe[a][b].conjugate() / pmax * d
                want_p = probe[a][b] + beta * o_old[a][b].conjugate() / omax * d
                assert abs(o[a][3 + b] - want_o) < 1e-12
                assert abs(p[a][b] - want_p) < 1e-12
        # Pixels outside the window do not change.
        assert all(o[a][b] == obj[a][b] for a in range(4) for b in range(3))
        assert all(o[a][7] == obj[a][7] for a in range(4))


def test_object_step_shrinks_the_residual_per_pixel():
    rng = random.Random(5)
    obj, probe = rand_obj(rng, 4, 4), gauss_probe(4, 4)
    pos = [(0, 0)]
    amps = [[[rng.uniform(0.2, 3.0) for _ in range(4)] for _ in range(4)]]
    psi = exit_wave(obj, probe, pos[0])
    psi2 = idft2(modulus_replace(dft2(psi), amps[0]))
    pmax = max(abs(v) ** 2 for row in probe for v in row)
    for alpha in (0.1, 0.7, 1.0, 1.5, 2.0):
        o, _ = epie(amps, pos, obj, probe, 1, alpha=alpha, update_probe=False)
        new = exit_wave(o, probe, pos[0])
        for a in range(4):
            for b in range(4):
                before = abs(psi[a][b] - psi2[a][b])
                after = abs(new[a][b] - psi2[a][b])
                factor = abs(1 - alpha * abs(probe[a][b]) ** 2 / pmax)
                assert abs(after - factor * before) < 1e-12
                assert after <= before + 1e-12


def test_ambiguities_leave_the_data_unchanged():
    rng = random.Random(6)
    obj, probe = rand_obj(rng, 8, 10), gauss_probe(4, 4)
    pos = [(r, c) for r in (0, 2, 4) for c in (0, 3, 6)]
    amps = forward_amplitudes(obj, probe, pos)
    c = 1.7 * cmath.exp(0.4j)
    o2 = [[c * v for v in row] for row in obj]
    p2 = [[v / c for v in row] for row in probe]
    assert data_error(amps, pos, o2, p2) < 1e-24
    # A phase ramp on the object and the opposite ramp on the probe.
    kx, ky = 0.37, -0.21
    o3 = [[v * cmath.exp(1j * (kx * j + ky * i)) for j, v in enumerate(row)] for i, row in enumerate(obj)]
    p3 = [[v * cmath.exp(-1j * (kx * b + ky * a)) for b, v in enumerate(row)] for a, row in enumerate(probe)]
    assert data_error(amps, pos, o3, p3) < 1e-24


def test_known_probe_recovers_the_object():
    rng = random.Random(1)
    obj, probe = rand_obj(rng, 12, 12), gauss_probe(8, 8)
    pos = [(r, c) for r in (0, 2, 4) for c in (0, 2, 4)]
    amps = forward_amplitudes(obj, probe, pos)
    start = [[1 + 0j] * 12 for _ in range(12)]
    o1, _ = epie(amps, pos, start, probe, 1, update_probe=False, seed=2)
    o, _ = epie(amps, pos, start, probe, 60, update_probe=False, seed=2)
    assert data_error(amps, pos, o, probe) < 1e-3 < data_error(amps, pos, o1, probe)
    inner = range(2, 10)
    assert aligned_error(o, obj, inner, inner) < 0.15 < aligned_error(o1, obj, inner, inner)


def test_joint_recovery_lowers_the_data_error():
    rng = random.Random(1)
    obj, probe = rand_obj(rng, 1, 40), gauss_probe(1, 8)
    pos = [(0, c) for c in range(33)]
    amps = forward_amplitudes(obj, probe, pos)
    start = [[1 + 0j] * 40]
    guess = [[abs(v) for v in probe[0]]]  # the right modulus, no phase
    o1, p1 = epie(amps, pos, start, guess, 1, seed=2)
    o, p = epie(amps, pos, start, guess, 150, seed=2)
    e1, e = data_error(amps, pos, o1, p1), data_error(amps, pos, o, p)
    assert e < 0.02 * e1
    assert e < 1e-2


def test_same_seed_same_result():
    rng = random.Random(7)
    obj, probe = rand_obj(rng, 1, 16), gauss_probe(1, 4)
    pos = [(0, c) for c in range(0, 13, 2)]
    amps = forward_amplitudes(obj, probe, pos)
    start = [[1 + 0j] * 16]
    a = epie(amps, pos, start, probe, 5, seed=11)
    b = epie(amps, pos, start, probe, 5, seed=11)
    assert a == b
