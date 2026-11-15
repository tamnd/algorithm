# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dynamic-mode-decomposition/. The authors are listed in prov/BZWTTE.jsonl.

import cmath
import math
import random

from ctlmat import charpoly, matvec, mul, polyroots, transpose
from dynamic_mode_decomposition import amplitudes, continuous_eigenvalues, dmd, jacobi_svd


def _orbit(A, x0, M):
    out = [list(x0)]
    for _ in range(M):
        out.append(matvec(A, out[-1]))
    return out


def _column(m, k):
    return [row[k] for row in m]


def _wave_snapshots(M, h=0.1, q=32):
    lam = [cmath.exp(complex(-0.1, 2.0) * h), cmath.exp(complex(-0.3, 5.0) * h)]
    grid = [2 * math.pi * i / q for i in range(q)]
    return [[(lam[0] ** k * cmath.exp(1j * g)).real + 0.5 * (lam[1] ** k * cmath.exp(3j * g)).real for g in grid]
            for k in range(M + 1)]


def _x_plus_times(snaps, v):
    # X' X^+ v with X^+ = V S^-1 U^T over the nonzero singular values
    X = transpose(snaps[:-1])
    Xp = transpose(snaps[1:])
    U, s, V = jacobi_svd(X)
    r = sum(1 for t in s if t > 1e-10 * s[0])
    coef = [sum(U[i][k] * v[i] for i in range(len(U))) / s[k] for k in range(r)]
    z = [sum(V[j][k] * coef[k] for k in range(r)) for j in range(len(V))]
    return [sum(Xp[i][j] * z[j] for j in range(len(z))) for i in range(len(Xp))]


def test_full_state_linear_system():
    A = [[0.9, 0.2, 0.0], [-0.2, 0.9, 0.1], [0.0, 0.0, 0.5]]
    snaps = _orbit(A, [1.0, 0.0, 1.0], 6)
    lams, modes, s = dmd(snaps)
    assert len(lams) == 3
    true = polyroots(charpoly(A))
    assert max(abs(a - b) for a, b in zip(lams, true)) < 1e-9
    for k, lam in enumerate(lams):
        phi = _column(modes, k)
        lhs = [sum(A[i][j] * phi[j] for j in range(3)) for i in range(3)]
        assert max(abs(lhs[i] - lam * phi[i]) for i in range(3)) < 1e-9


def test_wave_data_recovers_the_frequencies():
    h = 0.1
    snaps = _wave_snapshots(20, h)
    lams, modes, s = dmd(snaps)
    assert len(lams) == 4
    assert s[4] < 1e-12 * s[0]
    want = sorted([complex(-0.1, 2.0), complex(-0.1, -2.0), complex(-0.3, 5.0), complex(-0.3, -5.0)],
                  key=lambda w: (w.real, w.imag))
    got = sorted(continuous_eigenvalues(lams, h), key=lambda w: (w.real, w.imag))
    assert max(abs(a - b) for a, b in zip(got, want)) < 1e-9
    # every pair is an eigenpair of X' X^+
    for k, lam in enumerate(lams):
        phi = _column(modes, k)
        lhs = _x_plus_times(snaps, phi)
        assert max(abs(a - lam * b) for a, b in zip(lhs, phi)) < 1e-9
    # the modes and amplitudes rebuild every snapshot
    b = amplitudes(modes, snaps[0])
    for k in (0, 7, 20):
        rebuilt = [sum(modes[i][j] * lams[j] ** k * b[j] for j in range(4)) for i in range(len(modes))]
        assert max(abs(a - c) for a, c in zip(rebuilt, snaps[k])) < 1e-9


def test_too_few_snapshots():
    # two snapshot pairs of a three-state system: rank 2, so the result is not
    # the spectrum of A, but each pair is still an eigenpair of X' X^+
    A = [[0.9, 0.2, 0.0], [-0.2, 0.9, 0.1], [0.0, 0.0, 0.5]]
    snaps = _orbit(A, [1.0, 0.0, 1.0], 2)
    lams, modes, s = dmd(snaps)
    assert len(lams) == 2
    true = polyroots(charpoly(A))
    assert max(min(abs(a - b) for b in true) for a in lams) > 1e-3
    for k, lam in enumerate(lams):
        phi = _column(modes, k)
        lhs = _x_plus_times(snaps, phi)
        assert max(abs(a - lam * b) for a, b in zip(lhs, phi)) < 1e-9


def test_noisy_snapshots():
    # measurement: noise with standard deviation 0.05 on every entry, 21 snapshots
    h = 0.1
    snaps = _wave_snapshots(20, h)
    want = [complex(-0.3, -5.0), complex(-0.1, -2.0), complex(-0.1, 2.0), complex(-0.3, 5.0)]
    for seed in (1, 2, 3):
        rng = random.Random(seed)
        noisy = [[v + rng.gauss(0.0, 0.05) for v in row] for row in snaps]
        lams, modes, s = dmd(noisy, r=4)
        got = continuous_eigenvalues(lams, h)
        for w in want:
            best = min(got, key=lambda g: abs(g - w))
            assert abs(best.imag - w.imag) < 0.1
            assert abs(best.real - w.real) < 0.05


def test_rank_above_data_rank_is_rejected():
    snaps = _orbit([[0.5, 0.0], [0.0, 0.5]], [1.0, 1.0], 4)
    try:
        dmd(snaps, r=2)
    except ValueError:
        return
    assert False, "a rank above the rank of X must be rejected"
