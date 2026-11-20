# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/low-rank-plus-sparse-mri/. The authors are listed in prov/FVJ0PD.jsonl.

import math
import random

from imgkit import disk_phantom
from imgla import svd
from low_rank_plus_sparse_mri import (
    encode,
    encode_adjoint,
    l_plus_s,
    nuclear_norm,
    objective,
    soft,
    svt,
    temporal_ft,
    temporal_ift,
)


def rand_series(rng, nt, npix):
    return [[complex(rng.gauss(0, 1), rng.gauss(0, 1)) for _ in range(npix)] for _ in range(nt)]


def rand_masks(rng, nt, npix, p=0.5):
    return [[1 if rng.random() < p else 0 for _ in range(npix)] for _ in range(nt)]


def two_coils(rng, npix):
    """Two coil maps with |c_1|^2 + |c_2|^2 = 1 at every pixel."""
    c1, c2 = [], []
    for _ in range(npix):
        a = complex(rng.gauss(0, 1), rng.gauss(0, 1))
        b = complex(rng.gauss(0, 1), rng.gauss(0, 1))
        s = math.sqrt(abs(a) ** 2 + abs(b) ** 2)
        c1.append(a / s)
        c2.append(b / s)
    return [c1, c2]


def inner(u, v):
    return sum(a.conjugate() * b for fu, fv in zip(u, v) for a, b in zip(fu, fv))


def inner3(u, v):
    return sum(inner(a, b) for a, b in zip(u, v))


def sq_dist(u, v):
    return sum(abs(a - b) ** 2 for fu, fv in zip(u, v) for a, b in zip(fu, fv))


def rel_err(u, v):
    return math.sqrt(sq_dist(u, v) / sum(abs(b) ** 2 for fv in v for b in fv))


def embed(c):
    """The real matrix [[Re C, -Im C], [Im C, Re C]]."""
    top = [[v.real for v in row] + [-v.imag for v in row] for row in c]
    bot = [[v.imag for v in row] + [v.real for v in row] for row in c]
    return top + bot


def test_encode_adjoint():
    rng = random.Random(1)
    n1, n2, nt = 4, 4, 3
    x = rand_series(rng, nt, n1 * n2)
    masks = rand_masks(rng, nt, n1 * n2)
    for coils in (None, two_coils(rng, n1 * n2)):
        nc = 1 if coils is None else 2
        y = [[[complex(rng.gauss(0, 1), rng.gauss(0, 1)) * m for m in masks[t]] for _ in range(nc)] for t in range(nt)]
        lhs = inner3(encode(x, masks, n1, n2, coils), y)
        rhs = inner(x, encode_adjoint(y, masks, n1, n2, coils))
        assert abs(lhs - rhs) < 1e-10 * abs(lhs)


def test_encoding_norm_at_most_one():
    rng = random.Random(2)
    n1, n2, nt = 4, 4, 3
    coils = two_coils(rng, n1 * n2)
    full = [[1] * (n1 * n2) for _ in range(nt)]
    for _ in range(3):
        x = rand_series(rng, nt, n1 * n2)
        nx = inner(x, x).real
        ex = encode(x, rand_masks(rng, nt, n1 * n2), n1, n2, coils)
        assert sum(inner(e, e).real for e in ex) <= nx * (1 + 1e-12)
        ex = encode(x, full, n1, n2, coils)
        assert abs(sum(inner(e, e).real for e in ex) - nx) < 1e-10 * nx


def test_temporal_transform_is_unitary():
    rng = random.Random(3)
    x = rand_series(rng, 6, 5)
    tx = temporal_ft(x)
    assert abs(inner(tx, tx).real - inner(x, x).real) < 1e-10 * inner(x, x).real
    assert sq_dist(temporal_ift(tx), x) < 1e-20 * inner(x, x).real
    const = [[2.0 + 1j] * 5 for _ in range(6)]
    tc = temporal_ft(const)
    assert all(abs(v) < 1e-12 for frame in tc[1:] for v in frame)


def test_svt_matches_real_svd():
    rng = random.Random(4)
    x = rand_series(rng, 4, 7)
    casorati = [[x[t][p] for t in range(4)] for p in range(7)]
    u, s, v = svd(embed(casorati))
    assert abs(nuclear_norm(x) - sum(s) / 2) < 1e-10
    for tau in (0.0, 0.5, s[2], 2.0):
        low = svt(x, tau)
        shr = [max(si - tau, 0.0) for si in s]
        e = [[sum(u[i][k] * shr[k] * v[j][k] for k in range(len(s))) for j in range(len(v))] for i in range(len(u))]
        got = embed([[low[t][p] for t in range(4)] for p in range(7)])
        assert max(abs(got[i][j] - e[i][j]) for i in range(14) for j in range(8)) < 1e-9


def test_soft_threshold():
    assert soft(3 + 4j, 1.0) == (3 + 4j) * 0.8
    assert soft(0.5j, 1.0) == 0j
    assert soft(0j, 0.0) == 0j


def test_full_sampling_known_answers():
    rng = random.Random(5)
    n1, n2, nt = 4, 4, 4
    x = rand_series(rng, nt, n1 * n2)
    full = [[1] * (n1 * n2) for _ in range(nt)]
    d = encode(x, full, n1, n2)
    low, sparse = l_plus_s(d, full, n1, n2, 0.7, 1e9, 1.0, 3)
    assert sq_dist(low, svt(x, 0.7)) < 1e-18 and sq_dist(sparse, [[0j] * 16] * nt) == 0
    low, sparse = l_plus_s(d, full, n1, n2, 1e9, 0.4, 1.0, 3)
    want = temporal_ift([[soft(v, 0.4) for v in frame] for frame in temporal_ft(x)])
    assert sq_dist(sparse, want) < 1e-18 and nuclear_norm(low) < 1e-12


def test_sufficient_decrease():
    rng = random.Random(6)
    n1, n2, nt = 4, 4, 4
    coils = two_coils(rng, n1 * n2)
    x = rand_series(rng, nt, n1 * n2)
    masks = rand_masks(rng, nt, n1 * n2)
    d = encode(x, masks, n1, n2, coils)
    for step in (0.5, 0.9):
        prev = None
        for k in range(7):
            low, sparse = l_plus_s(d, masks, n1, n2, 0.3, 0.1, step, k, coils)
            f = objective(low, sparse, d, masks, n1, n2, 0.3, 0.1, coils)
            if prev is not None:
                change = sq_dist(low, prev[0]) + sq_dist(sparse, prev[1])
                assert f <= prev[2] - (1 / step - 1) * change + 1e-10
            prev = (low, sparse, f)


def test_boundary_step_is_monotone():
    rng = random.Random(7)
    n1, n2, nt = 4, 4, 4
    x = rand_series(rng, nt, n1 * n2)
    masks = rand_masks(rng, nt, n1 * n2)
    d = encode(x, masks, n1, n2)
    hist = []
    l_plus_s(d, masks, n1, n2, 0.2, 0.05, 1.0, 15, None, hist)
    assert all(b <= a + 1e-10 for a, b in zip(hist, hist[1:]))


def test_beats_zero_filling_on_a_dynamic_phantom():
    n1 = n2 = nt = 8
    bg = [v for row in disk_phantom(8, 0.8) for v in row]
    curve = [1.0, 1.4, 1.7, 1.8, 1.7, 1.5, 1.3, 1.2]
    x = []
    for t in range(nt):
        f = [complex(v) * curve[t] for v in bg]
        f[27] += 0.5 * math.cos(2 * math.pi * t / nt)
        f[28] += 0.5 * math.sin(2 * math.pi * 2 * t / nt)
        f[36] += 0.5 * math.cos(2 * math.pi * 3 * t / nt)
        x.append(f)
    rng = random.Random(1)
    masks = []
    for t in range(nt):
        rows = {0}
        while len(rows) < 3:
            rows.add(rng.randrange(n1))
        masks.append([1 if i in rows else 0 for i in range(n1) for _ in range(n2)])
    d = encode(x, masks, n1, n2)
    zero_filled = rel_err(encode_adjoint(d, masks, n1, n2), x)
    low, sparse = l_plus_s(d, masks, n1, n2, 0.3, 0.1, 0.9, 40)
    rec = [[a + b for a, b in zip(fl, fs)] for fl, fs in zip(low, sparse)]
    assert zero_filled > 0.4
    assert rel_err(rec, x) < 0.6 * zero_filled
