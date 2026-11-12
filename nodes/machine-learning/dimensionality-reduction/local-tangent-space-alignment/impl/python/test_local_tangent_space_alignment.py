# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/local-tangent-space-alignment/. The authors are listed in prov/8CGP5G.jsonl.

import math
import random

from local_tangent_space_alignment import alignment_matrix, ltsa


def l_domain(seed, curved=False):
    """A jittered grid on the L-shaped region [0,3]^2 minus (1.5,3]^2, which is not convex.
    The flat version lies in a tilted plane in R^3; the curved version rolls the sheet
    onto a cylinder of radius 2, which keeps all lengths on the sheet."""
    rng = random.Random(seed)
    uv = []
    for a in range(7):
        for b in range(7):
            u, v = 0.5 * a, 0.5 * b
            if u > 1.5 and v > 1.5:
                continue
            uv.append((u + rng.uniform(-0.1, 0.1), v + rng.uniform(-0.1, 0.1)))
    if curved:
        pts = [(2 * math.cos(u / 2), 2 * math.sin(u / 2), v) for u, v in uv]
    else:
        pts = [((3 * u + 4 * v) / 5, (12 * u - 9 * v) / 25, (16 * u - 12 * v) / 25 + 1) for u, v in uv]
    return pts, uv


def residual_of_fit(y, z):
    """Least squares residual of z on the columns [1, y], relative to the spread of z."""
    n, m = len(y), len(y[0])
    q = []
    for col in [[1.0] * n] + [[r[l] for r in y] for l in range(m)]:
        v = col[:]
        for u in q:
            d = sum(a * b for a, b in zip(u, v))
            v = [a - d * b for a, b in zip(v, u)]
        nv = math.sqrt(sum(a * a for a in v))
        if nv > 1e-12:
            q.append([a / nv for a in v])
    r = list(z)
    for u in q:
        d = sum(a * b for a, b in zip(u, r))
        r = [a - d * b for a, b in zip(r, u)]
    mean = sum(z) / n
    return math.sqrt(sum(a * a for a in r) / sum((a - mean) ** 2 for a in z))


def test_alignment_matrix_is_symmetric_with_constant_null_vector():
    pts, _ = l_domain(0)
    b = alignment_matrix(pts, k=6, m=2)
    n = len(pts)
    assert max(abs(b[i][j] - b[j][i]) for i in range(n) for j in range(n)) < 1e-12
    assert max(abs(sum(row)) for row in b) < 1e-9


def test_true_coordinates_in_null_space():
    pts, uv = l_domain(1)
    b = alignment_matrix(pts, k=6, m=2)
    n = len(pts)
    for c in range(2):
        f = [p[c] for p in uv]
        bf = [sum(b[i][j] * f[j] for j in range(n)) for i in range(n)]
        assert max(abs(x) for x in bf) < 1e-9


def test_line_example():
    y, lam = ltsa([(float(i), 0.0) for i in range(5)], k=2, m=1)
    s = 1.0 if y[4][0] > 0 else -1.0
    for i, (v,) in enumerate(y):
        assert abs(s * v - (i - 2) / math.sqrt(10)) < 1e-9
    assert abs(lam[0]) < 1e-12 and lam[1] > 0.1


def test_recovers_nonconvex_flat_sheet():
    pts, uv = l_domain(2)
    y, lam = ltsa(pts, k=6, m=2)
    assert abs(lam[0]) < 1e-9 and abs(lam[1]) < 1e-9 and lam[2] > 1e-3
    for c in range(2):
        assert residual_of_fit(y, [p[c] for p in uv]) < 1e-6
    for a in range(2):
        for b in range(2):
            dot = sum(r[a] * r[b] for r in y)
            assert abs(dot - (1.0 if a == b else 0.0)) < 1e-9


def test_recovers_rolled_sheet_approximately():
    pts, uv = l_domain(3, curved=True)
    y, _ = ltsa(pts, k=6, m=2)
    for c in range(2):
        assert residual_of_fit(y, [p[c] for p in uv]) < 0.05
