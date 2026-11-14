# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/pht-spline/. The authors are listed in prov/BQ9V8S.jsonl.

import copy
import random
from fractions import Fraction as F

from pht_spline import PHT, ZERO, cell_box


def cubic_bspline(t, x, end):
    """Reference: cubic B-spline on 5 local knots by Cox-de Boor, closed at the domain end."""
    vals = [F(int(t[k] <= x < t[k + 1] or (x == end and t[k] < t[k + 1] == end))) for k in range(4)]
    for d in range(1, 4):
        vals = [
            ((x - t[k]) / (t[k + d] - t[k]) * vals[k] if t[k + d] != t[k] else 0)
            + ((t[k + d + 1] - x) / (t[k + d + 1] - t[k + 1]) * vals[k + 1] if t[k + d + 1] != t[k + 1] else 0)
            for k in range(len(vals) - 1)
        ]
    return vals[0]


def local_knots(u, h, n, c):
    """Local knots of the C^1 cubic B-spline c in {0, 1} of the vertex u with spacing h."""
    lo, hi = max(u - h, F(0)), min(u + h, F(n))
    if u == 0:
        lo = F(0)
    return (lo, lo, u, u, hi) if c == 0 else (lo, u, u, hi, hi)


def tensor_bspline(v, h, n, a, b, x, y):
    return cubic_bspline(local_knots(v[0], h, n, a), x, F(n)) * cubic_bspline(local_knots(v[1], h, n, b), y, F(n))


def example():
    T = PHT(2)
    T.refine([(0, 0, 0)])
    T.refine([(1, 1, 1)])
    return T


def random_mesh(rng, n=2, steps=3):
    T = PHT(n)
    for _ in range(steps):
        finest = sorted(c for c in T.leaves if c[0] == T.K)
        T.refine(rng.sample(finest, min(len(finest), rng.randint(1, 3))))
    return T


def cases():
    rng = random.Random(1)
    yield example()
    for _ in range(2):
        yield random_mesh(rng)


def pts(rng, k, n):
    return [(F(rng.randint(0, 1000 * n), 1000), F(rng.randint(0, 1000 * n), 1000)) for _ in range(k)]


def combine(T, coeffs):
    out = {}
    for key, c in coeffs.items():
        for v, d in T.funcs[key].items():
            out[v] = tuple(a + c * b for a, b in zip(out.get(v, ZERO), d))
    return out


def rank(vectors):
    pivots = {}
    for v in vectors:
        v = {k: x for k, x in v.items() if x}
        while v:
            k = min(v)
            if k not in pivots:
                pivots[k] = v
                break
            p = pivots[k]
            f = v[k] / p[k]
            for kk, x in p.items():
                v[kk] = v.get(kk, F(0)) - f * x
            v = {kk: x for kk, x in v.items() if x}
    return len(pivots)


def brute_dimension(T):
    """dim S(3, 3, 1, 1, T) from all piecewise bicubics with C^1 conditions across each shared edge."""
    cells = sorted(T.leaves)
    idx = {c: k for k, c in enumerate(cells)}
    eqs = []
    for A in cells:
        ax0, ax1, ay0, ay1 = cell_box(A)
        for B in cells:
            bx0, bx1, by0, by1 = cell_box(B)
            if ax1 == bx0 and min(ay1, by1) > max(ay0, by0):
                line, swap = ax1, False
            elif ay1 == by0 and min(ax1, bx1) > max(ax0, bx0):
                line, swap = ay1, True
            else:
                continue
            for q in range(4):
                for deriv in (0, 1):
                    e = {}
                    for p in range(4):
                        w = line**p if deriv == 0 else (p * line ** (p - 1) if p else F(0))
                        k = 4 * q + p if swap else 4 * p + q  # the power p is in the normal direction
                        if w:
                            e[16 * idx[A] + k] = e.get(16 * idx[A] + k, F(0)) + w
                            e[16 * idx[B] + k] = e.get(16 * idx[B] + k, F(0)) - w
                    eqs.append(e)
    return 16 * len(cells) - rank(eqs)


def fit_cubic(vals):
    """Coefficients a0..a3 of the cubic through (k, vals[k-1]), k = 1..4."""
    rows = [[F(k) ** e for e in range(4)] + [vals[k - 1]] for k in range(1, 5)]
    for c in range(4):
        piv = next(r for r in range(c, 4) if rows[r][c])
        rows[c], rows[piv] = rows[piv], rows[c]
        for r in range(4):
            if r != c and rows[r][c]:
                f = rows[r][c] / rows[c][c]
                rows[r] = [a - f * b for a, b in zip(rows[r], rows[c])]
    return [rows[c][4] / rows[c][c] for c in range(4)]


def jumps(T, data, p, axis, d):
    """Jumps of f and of its derivative along `axis` across the line through p.

    The one-sided values f(p +- k d e) for k = 1..4 are fitted by cubics, which
    is exact since f is a cubic on each side; the fits give the one-sided
    limits of f and of the derivative at p.
    """
    e = (1, 0) if axis == 0 else (0, 1)
    R = fit_cubic([T.evaluate(data, p[0] + k * d * e[0], p[1] + k * d * e[1])[0] for k in range(1, 5)])
    L = fit_cubic([T.evaluate(data, p[0] - k * d * e[0], p[1] - k * d * e[1])[0] for k in range(1, 5)])
    return R[0] - L[0], (R[1] + L[1]) / d


def tjunction_probes(T):
    """Points next to each T-junction on the long side and on the stem, with the normal axis."""
    eps = F(1, 2 ** (T.K + 2))
    out = []
    for v, C in sorted(T.tjunctions.items()):
        x0, x1, y0, y1 = cell_box(C)
        if v[0] in (x0, x1):  # the long side is vertical
            out += [((v[0], v[1] + eps), 0), ((v[0], v[1] - eps), 0)]
            stem_x = v[0] - eps if v[0] == x0 else v[0] + eps
            out.append(((stem_x, v[1]), 1))
        else:
            out += [((v[0] + eps, v[1]), 1), ((v[0] - eps, v[1]), 1)]
            stem_y = v[1] - eps if v[1] == y0 else v[1] + eps
            out.append(((v[0], stem_y), 0))
    return out, eps / 8


def test_level_0_basis_is_the_tensor_c1_bicubic_b_splines():
    T = PHT(3)
    assert len(T.funcs) == 4 * 16
    rng = random.Random(2)
    for (v, a, b), data in T.funcs.items():
        for x, y in pts(rng, 4, 3):
            assert T.evaluate(data, x, y)[0] == tensor_bspline(v, F(1), 3, a, b, x, y)


def test_dimension_formula_against_brute_force():
    T = PHT(2)
    dims = [len(T.funcs)]
    T.refine([(0, 0, 0)])
    dims.append(len(T.funcs))
    T.refine([(1, 1, 1)])
    dims.append(len(T.funcs))
    assert dims == [36, 48, 52]
    assert len(T.tjunctions) == 6
    for T in cases():
        n_basis = 4 * (len(T.boundary) + len(T.crossings))
        assert len(T.funcs) == n_basis == brute_dimension(T)


def support_cells(T, data):
    """The leaf cells with a corner where the data are not zero; the function is zero on the others."""
    return [c for c in sorted(T.leaves) if any(p in data for p in T.corners(c).values())]


def grid(c, k):
    x0, x1, y0, y1 = cell_box(c)
    return [(x0 + (x1 - x0) * s / (k + 1), y0 + (y1 - y0) * t / (k + 1)) for s in range(1, k + 1) for t in range(1, k + 1)]


def test_basis_is_linearly_independent():
    # a bicubic on a cell is fixed by its values on a 4 x 4 grid, so the rank of
    # these values is the rank of the functions
    for T in cases():
        vecs = []
        for data in T.funcs.values():
            vecs.append({(c, s): T.cell_values(data, c, x, y)[0] for c in support_cells(T, data) for s, (x, y) in enumerate(grid(c, 4))})
        assert rank(vecs) == len(T.funcs)


def test_partition_of_unity():
    rng = random.Random(3)
    for T in cases():
        total = combine(T, {k: F(1) for k in T.funcs})
        for x, y in pts(rng, 10, T.n):
            assert T.evaluate(total, x, y) == (1, 0, 0, 0)


def test_c1_across_t_junctions_by_finite_differences():
    rng = random.Random(4)
    for T in cases():
        probes, d = tjunction_probes(T)
        assert probes
        spline = combine(T, {k: F(rng.randint(-9, 9)) for k in T.funcs})
        some = rng.sample(sorted(T.funcs), 2)
        for p, axis in probes:
            assert jumps(T, spline, p, axis, d) == (0, 0)
            for key in some:
                assert jumps(T, T.funcs[key], p, axis, d) == (0, 0)


def test_wrong_t_junction_data_breaks_c1():
    T = example()
    spline = combine(T, {k: F(1) for k in T.funcs})
    v, C = sorted(T.tjunctions.items())[0]
    f, fx, fy, fxy = spline[v]
    spline[v] = (f, fx + 1, fy + 1, fxy)
    probes, d = tjunction_probes(T)
    near = [(p, axis) for p, axis in probes if abs(p[0] - v[0]) + abs(p[1] - v[1]) < F(1, 2**T.K)]
    assert any(jumps(T, spline, p, axis, d)[1] != 0 for p, axis in near)


def test_refinement_matches_deng_truncation_formula():
    rng = random.Random(5)
    T0 = PHT(2)
    T = copy.deepcopy(T0)
    new = T.refine([(0, 0, 0), (0, 1, 0)])
    h = F(1, 2)
    for (v0, a0, b0), data in T0.funcs.items():
        dual = {}
        for v in new:
            f, fx, fy, fxy = T0.evaluate(data, v[0], v[1])
            sx = (-(h if v[0] > 0 else F(0)) / 3, (h if v[0] < 2 else F(0)) / 3)
            sy = (-(h if v[1] > 0 else F(0)) / 3, (h if v[1] < 2 else F(0)) / 3)
            for a in (0, 1):
                for b in (0, 1):
                    dual[(v, a, b)] = f + sx[a] * fx + sy[b] * fy + sx[a] * sy[b] * fxy
        for x, y in pts(rng, 6, 2):
            ref = tensor_bspline(v0, F(1), 2, a0, b0, x, y)
            ref -= sum(c * tensor_bspline(v, h, 2, a, b, x, y) for (v, a, b), c in dual.items())
            assert T.evaluate(T.funcs[(v0, a0, b0)], x, y)[0] == ref


def test_refinement_gives_nested_spaces():
    rng = random.Random(6)
    T = PHT(2)
    for _ in range(3):
        old = copy.deepcopy(T)
        spline = combine(old, {k: F(rng.randint(-5, 5)) for k in old.funcs})
        finest = sorted(c for c in T.leaves if c[0] == T.K)
        T.refine(rng.sample(finest, min(2, len(finest))))
        data = {v: old.evaluate(spline, v[0], v[1]) for v in T.basis_vertices}
        again = combine(T, T.coefficients(data))
        for x, y in pts(rng, 8, 2):
            assert T.evaluate(again, x, y)[0] == old.evaluate(spline, x, y)[0]


def test_basis_functions_are_nonnegative_at_samples():
    for T in cases():
        for data in T.funcs.values():
            assert all(T.cell_values(data, c, x, y)[0] >= 0 for c in support_cells(T, data) for x, y in grid(c, 3))
