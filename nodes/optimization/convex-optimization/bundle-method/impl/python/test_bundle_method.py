# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bundle-method/. The authors are listed in prov/M2Z5AG.jsonl.

import itertools
import math
import random
from fractions import Fraction

from bundle_method import dot, proximal_bundle


def sub(u, v):
    return [p - q for p, q in zip(u, v)]


def gauss(m, r):
    k = len(r)
    t = [list(row) + [r[i]] for i, row in enumerate(m)]
    for col in range(k):
        piv = next((i for i in range(col, k) if t[i][col] != 0), None)
        if piv is None:
            return None
        t[col], t[piv] = t[piv], t[col]
        for i in range(k):
            if i != col and t[i][col] != 0:
                f = t[i][col] / t[col][col]
                t[i] = [p - f * q for p, q in zip(t[i], t[col])]
    return [t[i][k] / t[i][i] for i in range(k)]


def pwl_min(pieces, lo, hi):
    """(f*, x*) for f = max_i a_i^T x + b_i on a box, by enumeration of the vertices of {(x, t)}."""
    n = len(lo)
    rows = [(list(a) + [Fraction(-1)], -b) for a, b in pieces]
    for j in range(n):
        e = [Fraction(int(i == j)) for i in range(n)]
        rows.append(([-v for v in e] + [Fraction(0)], -lo[j]))
        rows.append((e + [Fraction(0)], hi[j]))
    best = None
    for s in itertools.combinations(rows, n + 1):
        p = gauss([r for r, _ in s], [h for _, h in s])
        if p is None or any(dot(r, p) > h for r, h in rows):
            continue
        if best is None or p[n] < best[0]:
            best = (p[n], p[:n])
    return best


def pwl_oracle(pieces):
    def oracle(x):
        vals = [dot(a, x) + b for a, b in pieces]
        i = vals.index(max(vals))
        return vals[i], list(pieces[i][0])

    return oracle


def check_run(res, f, t, kappa, g2, fstar, xstar, rng):
    """Exact checks of the lemmas of the proof. g2 bounds the squared norm of every subgradient."""
    a_const = (1 - kappa) ** 2 / (8 * t * g2)
    hist = res.history
    for k, s in enumerate(hist):
        c, fc, ha, ga, v = s["center"], s["fc"], s["ha"], s["ga"], s["v"]
        e = fc - ha  # linearization error of the aggregate cut at the center
        assert e >= 0 and v == e + t * dot(ga, ga)
        # the aggregate cut is a minorant of f
        for z in [xstar, s["y"]] + [[Fraction(rng.randint(-6, 6), 2) for _ in c] for _ in range(2)]:
            assert ha + dot(ga, sub(z, c)) <= f(z)
        # optimality certificate: f(c) - f* <= e + ||g_a|| ||x* - c||
        lhs = fc - fstar - e
        assert lhs <= 0 or lhs * lhs <= dot(ga, ga) * dot(sub(xstar, c), sub(xstar, c))
        if "serious" not in s:
            continue
        if s["serious"]:
            assert hist[k + 1]["fc"] <= fc - kappa * v if k + 1 < len(hist) else True
        elif k + 1 < len(hist):
            w0 = e + t * dot(ga, ga) / 2
            nxt = hist[k + 1]
            w1 = nxt["fc"] - nxt["ha"] + t * dot(nxt["ga"], nxt["ga"]) / 2
            q = dot(sub(s["gy"], ga), sub(s["gy"], ga))
            gain = (1 - kappa) * v / 2 if t * q <= (1 - kappa) * v else ((1 - kappa) * v) ** 2 / (2 * t * q)
            assert w1 <= w0 - gain
            assert w1 * (1 + a_const * w0) <= w0  # 1/W grows by at least a per null step


def test_page_example() -> None:
    # f(x) = max(-x, 2x - 3), x0 = 4, t = 1, kappa = 1/2; x* = 1, f* = -1
    pieces = [([Fraction(-1)], Fraction(0)), ([Fraction(2)], Fraction(-3))]
    f = lambda x: max(dot(a, x) + b for a, b in pieces)
    res = proximal_bundle(pwl_oracle(pieces), [Fraction(4)], Fraction(1), Fraction(1, 2))
    got = [(s["center"][0], s["lam"], s["ha"], s["ga"][0], s["y"][0], s["v"], s.get("serious")) for s in res.history]
    assert got == [
        (4, 1, 5, 2, 2, 4, True),
        (2, 1, 1, 2, 0, 4, False),
        (2, Fraction(2, 3), 0, 1, 1, 2, True),
        (1, 1, -1, -1, 2, 1, False),
        (1, Fraction(2, 3), -1, 0, 1, 0, None),
    ]
    assert res.x == [1] and res.fx == -1
    check_run(res, f, Fraction(1), Fraction(1, 2), Fraction(4), Fraction(-1), [Fraction(1)], random.Random(1))


def test_random_polyhedral() -> None:
    rng = random.Random(12)
    for _ in range(500):
        n = rng.randint(1, 2)
        pieces = [([Fraction(rng.randint(-2, 2)) for _ in range(n)], Fraction(rng.randint(-3, 3))) for _ in range(rng.randint(1, 3))]
        c = [Fraction(rng.randint(-2, 2)) for _ in range(n)]
        w, b0 = Fraction(3), Fraction(rng.randint(-3, 0))
        for j in range(n):  # +-w (x_j - c_j) + b0 make f coercive
            for sgn in (1, -1):
                a = [Fraction(sgn) * w if i == j else Fraction(0) for i in range(n)]
                pieces.append((a, b0 - sgn * w * c[j]))
        f = lambda x: max(dot(a, x) + b for a, b in pieces)
        r = (f(c) - b0) / w + 1  # f > f(c) outside the box |x - c| <= r
        fstar, xstar = pwl_min(pieces, [ci - r for ci in c], [ci + r for ci in c])
        g2 = max(dot(a, a) for a, _ in pieces)
        t = Fraction(rng.choice([1, 2, 4]), 2)
        kappa = Fraction(rng.choice([1, 2, 3]), 4)
        x0 = [Fraction(rng.randint(-4, 4)) for _ in range(n)]
        res = proximal_bundle(pwl_oracle(pieces), x0, t, kappa, max_iter=10)
        assert f(res.x) == res.fx and res.fx <= f(x0)
        check_run(res, f, t, kappa, g2, fstar, xstar, rng)


def test_float_convergence() -> None:
    # f(x) = |x1 - 1| + 2 |x2 + 1/2| has f* = 0 at (1, -1/2)
    def oracle(x):
        s1 = 1.0 if x[0] >= 1 else -1.0
        s2 = 1.0 if x[1] >= -0.5 else -1.0
        return abs(x[0] - 1) + 2 * abs(x[1] + 0.5), [s1, 2 * s2]

    eps = 1e-10
    res = proximal_bundle(oracle, [3.0, 2.0], 1.0, 0.5, eps=eps, max_iter=2000)
    assert res.history[-1]["v"] <= eps
    dist = math.hypot(res.x[0] - 1, res.x[1] + 0.5)
    assert res.fx <= eps + math.sqrt(eps) * dist + 1e-12
