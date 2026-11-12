# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/phylogenetic-independent-contrasts/. The authors are listed in prov/VXSG4E.jsonl.

import math
import random
from fractions import Fraction as F

from phylogenetic_independent_contrasts import (
    children_of,
    contrast_weights,
    contrasts,
    regression_through_origin,
    standardized,
)


def random_binary_tree(rng: random.Random, n_tips: int):
    parent, tips = [-1], [0]
    while len(tips) < n_tips:
        t = tips.pop(rng.randrange(len(tips)))
        for _ in range(2):
            parent.append(t)
            tips.append(len(parent) - 1)
    length = [F(0)] + [F(rng.randrange(1, 6), rng.randrange(1, 4)) for _ in parent[1:]]
    return parent, length, sorted(tips)


def bm_covariance(parent, length, tips):
    """C[s][t] = length of the shared part of the root paths of tips s and t."""
    def path(v):
        out = set()
        while parent[v] >= 0:
            out.add(v)
            v = parent[v]
        return out
    paths = [path(t) for t in tips]
    return [[sum(length[e] for e in a & b) for b in paths] for a in paths]


def solve(a, b):
    """Solve a y = b exactly by Gaussian elimination."""
    n = len(a)
    m = [row[:] + [b[i]] for i, row in enumerate(a)]
    for col in range(n):
        piv = next(r for r in range(col, n) if m[r][col] != 0)
        m[col], m[piv] = m[piv], m[col]
        for r in range(n):
            if r != col and m[r][col] != 0:
                f = m[r][col] / m[col][col]
                m[r] = [x - f * y for x, y in zip(m[r], m[col])]
    return [m[i][n] / m[i][i] for i in range(n)]


def quad(u, c, w):
    return sum(u[s] * c[s][t] * w[t] for s in range(len(u)) for t in range(len(w)))


def test_contrasts_are_independent_with_stated_variances() -> None:
    rng = random.Random(51)
    for _ in range(40):
        parent, length, tips = random_binary_tree(rng, rng.randrange(2, 9))
        c = bm_covariance(parent, length, tips)
        rows, root_row, variances, root_var = contrast_weights(parent, length, tips)
        assert len(rows) == len(tips) - 1
        assert sum(root_row) == 1 and all(sum(r) == 0 for r in rows)
        for a, ra in enumerate(rows):
            for b, rb in enumerate(rows):
                assert quad(ra, c, rb) == (variances[a] if a == b else 0)
            assert quad(ra, c, root_row) == 0
        assert quad(root_row, c, root_row) == root_var


def test_root_estimate_and_sum_of_squares_are_gls() -> None:
    rng = random.Random(52)
    for _ in range(40):
        parent, length, tips = random_binary_tree(rng, rng.randrange(2, 9))
        x = {t: F(rng.randrange(-20, 21), rng.randrange(1, 5)) for t in tips}
        xs = [x[t] for t in tips]
        raw, root_value, root_var = contrasts(parent, length, x)
        c = bm_covariance(parent, length, tips)
        ci_x, ci_1 = solve(c, xs), solve(c, [F(1)] * len(tips))
        one_x, one_one = sum(ci_x), sum(ci_1)
        assert root_value == one_x / one_one
        assert root_var == 1 / one_one
        ss = sum(cc * cc / var for _, cc, var in raw)
        assert ss == sum(a * b for a, b in zip(xs, ci_x)) - one_x ** 2 / one_one


def test_regression_through_origin_equals_gls_slope() -> None:
    rng = random.Random(53)
    for _ in range(30):
        parent, length, tips = random_binary_tree(rng, rng.randrange(3, 9))
        x = {t: F(rng.randrange(-20, 21)) for t in tips}
        y = {t: F(rng.randrange(-20, 21)) for t in tips}
        rx, _, _ = contrasts(parent, length, x)
        ry, _, _ = contrasts(parent, length, y)
        if all(cc == 0 for _, cc, _ in rx):
            continue
        # Standardized contrasts of x and y share the variances, so the slope
        # through the origin is sum(cx cy / v) / sum(cx^2 / v), exactly.
        exact = sum(a * b / v for (_, a, v), (_, b, _) in zip(rx, ry)) / sum(a * a / v for _, a, v in rx)
        c = bm_covariance(parent, length, tips)
        xs, ys, ones = [x[t] for t in tips], [y[t] for t in tips], [F(1)] * len(tips)
        ci_1, ci_x, ci_y = solve(c, ones), solve(c, xs), solve(c, ys)
        dot = lambda u, w: sum(a * b for a, b in zip(u, w))
        m = [[dot(ones, ci_1), dot(ones, ci_x)], [dot(xs, ci_1), dot(xs, ci_x)]]
        _, beta = solve(m, [dot(ones, ci_y), dot(xs, ci_y)])
        assert exact == beta
        slope = regression_through_origin(standardized(rx), standardized(ry))
        assert abs(slope - float(beta)) < 1e-9 * (1 + abs(float(beta)))


def test_simulated_standardized_contrasts() -> None:
    rng = random.Random(54)
    parent = [-1, 0, 0, 1, 1, 2, 2, 5, 5, 6, 6]
    length = [0.0, 1.0, 0.5, 0.3, 2.0, 0.7, 1.2, 0.4, 0.4, 1.5, 0.2]
    kids = children_of(parent)
    reps = 20000
    sums = [0.0] * 5
    squares = [0.0] * 5
    cross = 0.0
    for _ in range(reps):
        value = {0: 0.0}
        stack = [0]
        while stack:
            v = stack.pop()
            for ch in kids[v]:
                value[ch] = value[v] + rng.gauss(0.0, math.sqrt(length[ch]))
                stack.append(ch)
        tips = {v: value[v] for v in range(len(parent)) if not kids[v]}
        s = standardized(contrasts(parent, length, tips)[0])
        for i, u in enumerate(s):
            sums[i] += u
            squares[i] += u * u
        cross += s[0] * s[-1]
    for i in range(5):
        assert abs(sums[i] / reps) < 4 / math.sqrt(reps)
        assert abs(squares[i] / reps - 1) < 4 * math.sqrt(2 / reps)
    assert abs(cross / reps) < 4 / math.sqrt(reps)
