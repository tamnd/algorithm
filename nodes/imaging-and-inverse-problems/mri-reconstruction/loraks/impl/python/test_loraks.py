# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/loraks/. The authors are listed in prov/HJ4N14.jsonl.

import cmath
import math
import random

from imgla import adjoint_gap, svd
from loraks import (
    c_adjoint,
    c_matrix,
    coverage,
    disk_offsets,
    line_offsets,
    loraks,
    low_rank_projector,
    objective,
    rank_r_approx,
)


def kspace_line(x):
    """Centered unitary DFT of a 1D signal: frequencies -n/2, ..., n/2 - 1."""
    n = len(x)
    return [
        sum(x[j] * cmath.exp(-2j * math.pi * f * j / n) for j in range(n)) / math.sqrt(n)
        for f in range(-n // 2, n // 2)
    ]


def kspace_grid(img):
    """Centered unitary 2D DFT of a small square image."""
    n = len(img)
    return [
        [
            sum(
                img[p][q] * cmath.exp(-2j * math.pi * (a * p + b * q) / n)
                for p in range(n)
                for q in range(n)
                if img[p][q] != 0
            )
            / n
            for b in range(-n // 2, n // 2)
        ]
        for a in range(-n // 2, n // 2)
    ]


def three_spikes(n=32):
    x = [0j] * n
    x[5] = 1.0
    x[6] = 0.7 - 0.3j
    x[20] = -0.5 + 0.2j
    return x


def random_mask(n, seed, p=0.4):
    rng = random.Random(seed)
    return [[1 if abs(f) <= 2 or rng.random() < p else 0 for f in range(-n // 2, n // 2)]]


def rel_err(u, v):
    num = sum(abs(a - b) ** 2 for ra, rb in zip(u, v) for a, b in zip(ra, rb))
    den = sum(abs(b) ** 2 for rb in v for b in rb)
    return math.sqrt(num / den)


def embed(c):
    """The real matrix [[Re C, -Im C], [Im C, Re C]]."""
    top = [[v.real for v in row] + [-v.imag for v in row] for row in c]
    bot = [[v.imag for v in row] + [v.real for v in row] for row in c]
    return top + bot


def test_rank_equals_support_size_1d():
    k = [kspace_line(three_spikes())]
    c = c_matrix(k, line_offsets(4))
    assert len(c) == 24 and len(c[0]) == 9
    _, s2 = low_rank_projector(c, 3)
    assert s2[2] > 1e-2 * s2[0]
    assert all(v <= 1e-12 * s2[0] for v in s2[3:])


def test_rank_at_most_support_size_2d():
    img = [[0j] * 8 for _ in range(8)]
    img[1][2] = 1.0
    img[4][4] = 0.5j
    img[6][1] = -0.8
    c = c_matrix(kspace_grid(img), disk_offsets(2))
    assert len(c) == 16 and len(c[0]) == 13
    _, s2 = low_rank_projector(c, 3)
    assert s2[2] > 1e-2 * s2[0]
    assert all(v <= 1e-12 * s2[0] for v in s2[3:])


def test_adjoint_and_coverage():
    rng = random.Random(3)
    off = disk_offsets(1.5)
    n1, n2 = 6, 7
    x = [[complex(rng.gauss(0, 1), rng.gauss(0, 1)) for _ in range(n2)] for _ in range(n1)]
    rows = len(c_matrix(x, off))
    y = [[complex(rng.gauss(0, 1), rng.gauss(0, 1)) for _ in off] for _ in range(rows)]
    gap = adjoint_gap(lambda v: c_matrix(v, off), lambda v: c_adjoint(v, n1, n2, off), x, y)
    assert gap < 1e-12
    ones = [[1.0] * n2 for _ in range(n1)]
    back = c_adjoint(c_matrix(ones, off), n1, n2, off)
    cnt = coverage(n1, n2, off)
    assert all(back[a][b] == cnt[a][b] for a in range(n1) for b in range(n2))


def test_rank_r_approx_matches_real_svd():
    rng = random.Random(5)
    c = [[complex(rng.gauss(0, 1), rng.gauss(0, 1)) for _ in range(5)] for _ in range(8)]
    for r in (1, 2, 3):
        low, tail = rank_r_approx(c, r)
        u, s, v = svd(embed(c))
        # Each singular value of C appears twice in the embedding.
        trunc = [
            [sum(u[i][t] * s[t] * v[j][t] for t in range(2 * r)) for j in range(len(v))]
            for i in range(len(u))
        ]
        e = embed(low)
        assert max(abs(e[i][j] - trunc[i][j]) for i in range(len(e)) for j in range(len(e[0]))) < 1e-10
        assert abs(tail - sum(t * t for t in s[2 * r:]) / 2) < 1e-10
        resid = sum(abs(a - b) ** 2 for ra, rb in zip(c, low) for a, b in zip(ra, rb))
        assert abs(resid - tail) < 1e-10


def test_exact_kspace_is_a_fixed_point():
    k = [kspace_line(three_spikes())]
    mask = [[1] * 32]
    out = loraks(k, mask, line_offsets(3), 3, None, 2)
    assert rel_err(out, k) < 1e-12
    out = loraks(k, mask, line_offsets(3), 3, 0.5, 2)
    assert rel_err(out, k) < 1e-6


def test_hard_constraint_monotone_and_recovers():
    k = [kspace_line(three_spikes())]
    mask = random_mask(32, 1)
    assert sum(mask[0]) == 16
    hist = []
    out = loraks(k, mask, line_offsets(4), 3, None, 100, hist)
    for a, b in zip(hist, hist[1:]):
        assert b <= a + 1e-12 * hist[0]
    assert all(out[0][j] == k[0][j] for j in range(32) if mask[0][j])
    assert rel_err(out, k) < 1e-6


def test_penalized_objective_does_not_increase():
    k = [kspace_line(three_spikes())]
    mask = random_mask(32, 2)
    for lam in (0.3, 3.0):
        hist = []
        out = loraks(k, mask, line_offsets(3), 3, lam, 30, hist)
        for a, b in zip(hist, hist[1:]):
            assert b <= a + 1e-12 * hist[0]
        final = objective(out, k, mask, line_offsets(3), 3, lam)
        assert final <= hist[-1] + 1e-12 * hist[0]
