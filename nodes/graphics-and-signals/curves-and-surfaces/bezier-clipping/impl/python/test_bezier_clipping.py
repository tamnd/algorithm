# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bezier-clipping/. The authors are listed in prov/FFP21G.jsonl.

import random
from fractions import Fraction
from math import comb

from bezier_clipping import bezier_clip_intersect, bezier_clip_roots, clip_range, restrict

EPS = Fraction(1, 2**20)


# Exact polynomial helpers in the power basis (coefficient i is that of t^i).

def trim(p):
    p = list(p)
    while p and p[-1] == 0:
        p.pop()
    return p


def padd(p, q):
    r = [Fraction(0)] * max(len(p), len(q))
    for i, a in enumerate(p):
        r[i] += a
    for i, a in enumerate(q):
        r[i] += a
    return trim(r)


def pmul(p, q):
    if not p or not q:
        return []
    r = [Fraction(0)] * (len(p) + len(q) - 1)
    for i, a in enumerate(p):
        for j, b in enumerate(q):
            r[i + j] += a * b
    return trim(r)


def pscale(p, k):
    return trim([k * a for a in p])


def prem(p, q):
    p = [Fraction(a) for a in p]
    while len(p) >= len(q) and p:
        k = p[-1] / q[-1]
        s = len(p) - len(q)
        for i, b in enumerate(q):
            p[s + i] -= k * b
        p = trim(p)
    return p


def peval(p, t):
    r = Fraction(0)
    for a in reversed(p):
        r = r * t + a
    return r


def bernstein_to_power(c):
    n = len(c) - 1
    p = [Fraction(0)] * (n + 1)
    for i, ci in enumerate(c):
        for k in range(i, n + 1):
            p[k] += ci * (-1) ** (k - i) * comb(n, k) * comb(k, i)
    return trim(p)


def power_to_bernstein(p, n):
    # t^k = sum over i >= k of C(i, k) / C(n, k) B_i^n
    c = [Fraction(0)] * (n + 1)
    for k, a in enumerate(p):
        for i in range(k, n + 1):
            c[i] += a * Fraction(comb(i, k), comb(n, k))
    return c


def sturm_chain(p):
    d = trim([i * a for i, a in enumerate(p)][1:])
    chain = [trim(p), d]
    while chain[-1]:
        r = pscale(prem(chain[-2], chain[-1]), -1)
        if not r:
            break
        chain.append(r)
    return chain


def changes(chain, t):
    signs = [v for v in (peval(q, t) for q in chain) if v != 0]
    return sum(1 for u, v in zip(signs, signs[1:]) if (u > 0) != (v > 0))


def squarefree(p):
    chain = sturm_chain(p)
    return len(chain[-1]) == 1


def isolate(p, width):
    """Isolating intervals (a, b] of the distinct roots of p in (0, 1], plus [0, 0]."""
    chain = sturm_chain(p)
    out = [(Fraction(0), Fraction(0))] if peval(p, 0) == 0 else []
    stack = [(Fraction(0), Fraction(1))]
    while stack:
        a, b = stack.pop()
        k = changes(chain, a) - changes(chain, b)
        if k == 0:
            continue
        if k == 1 and b - a <= width:
            out.append((a, b))
            continue
        m = (a + b) / 2
        stack += [(a, m), (m, b)]
    return sorted(out)


def bern_eval(c, t):
    n = len(c) - 1
    return sum(ci * comb(n, i) * t**i * (1 - t) ** (n - i) for i, ci in enumerate(c))


# Root finding.

def test_example() -> None:
    c = [-1, -1, 3, 2]
    assert clip_range([Fraction(i, 3) for i in range(4)], c, 0, 0) == (Fraction(1, 6), Fraction(5, 9))
    out = bezier_clip_roots([Fraction(x) for x in c])
    assert len(out) == 1
    a, b = out[0]
    assert a <= Fraction(1, 3) <= b and b - a <= EPS


def test_restrict_matches_curve() -> None:
    rng = random.Random(3)
    for _ in range(50):
        c = [Fraction(rng.randint(-9, 9)) for _ in range(rng.randint(1, 6))]
        a = Fraction(rng.randint(0, 50), 64)
        b = a + Fraction(rng.randint(0, 64 - int(a * 64)), 64)
        r = restrict(c, a, b)
        for j in range(5):
            u = Fraction(j, 4)
            assert bern_eval(r, u) == bern_eval(c, a + (b - a) * u)


def test_planted_roots() -> None:
    rng = random.Random(5)
    for _ in range(60):
        roots = set()
        while len(roots) < rng.randint(1, 4):
            roots.add(Fraction(rng.randint(1, 47), 48))
        roots = sorted(roots)
        p = [Fraction(rng.choice([-3, -1, 2, 5]))]
        for r in roots:
            p = pmul(p, [-r, Fraction(1)])
        if rng.random() < 0.5:
            p = pmul(p, [Fraction(1), Fraction(0), Fraction(1)])  # no root in [0, 1]
        out = bezier_clip_roots(power_to_bernstein(p, len(p) - 1))
        assert len(out) == len(roots)
        for (a, b), r in zip(out, roots):
            assert a <= r <= b and b - a <= 2 * EPS


def test_random_against_sturm_and_sampling() -> None:
    rng = random.Random(7)
    tested = 0
    while tested < 60:
        n = rng.randint(1, 6)
        c = [Fraction(rng.randint(-20, 20)) for _ in range(n + 1)]
        p = bernstein_to_power(c)
        if len(p) < 2 or not squarefree(p):
            continue
        tested += 1
        out = bezier_clip_roots(c)
        ref = isolate(p, EPS / 4)
        assert len(out) == len(ref)
        for (a, b), (u, v) in zip(out, ref):
            assert a <= v and u <= b
        # dense exact sampling: each sign change lies in an output interval
        N = 400
        vals = [bern_eval(c, Fraction(k, N)) for k in range(N + 1)]
        for k in range(N):
            if vals[k] * vals[k + 1] < 0:
                lo, hi = Fraction(k, N), Fraction(k + 1, N)
                assert any(a < hi and lo < b for a, b in out)


def test_multiple_roots() -> None:
    half = Fraction(1, 2)
    out = bezier_clip_roots([Fraction(1, 4), Fraction(-1, 4), Fraction(1, 4)])  # (t - 1/2)^2
    assert len(out) == 1 and out[0][0] <= half <= out[0][1]
    third = Fraction(1, 3)
    p = pmul(pmul([-third, 1], [-third, 1]), [-third, 1])
    out = bezier_clip_roots(power_to_bernstein(p, 3))
    assert len(out) == 1 and out[0][0] <= third <= out[0][1]


def test_no_roots_and_end_roots() -> None:
    assert bezier_clip_roots([Fraction(1), Fraction(-1, 2), Fraction(1)]) == []  # 1 - 3t + 3t^2 > 0
    assert bezier_clip_roots([Fraction(2), Fraction(1), Fraction(3)]) == []
    out = bezier_clip_roots([Fraction(0), Fraction(1), Fraction(-1)])
    assert out[0][0] == 0 and len(out) == 2
    try:
        bezier_clip_roots([0, 0, 0])
    except ValueError:
        pass
    else:
        raise AssertionError("the zero polynomial must be rejected")


# Curve against curve.

def curve_power(P):
    return [bernstein_to_power([p[k] for p in P]) for k in range(2)]


def cross(u, v):
    return u[0] * v[1] - u[1] * v[0]


def reference_intersections(P, Q):
    """Exact implicitization of the quadratic Q: lambda1^2 = 4 lambda0 lambda2.

    Return isolating t intervals of P with the parameter s of Q, or None
    when the instance is close to a degenerate case.
    """
    q0, q1, q2 = Q
    D = cross((q1[0] - q0[0], q1[1] - q0[1]), (q2[0] - q0[0], q2[1] - q0[1]))
    if D == 0:
        return None
    x, y = curve_power(P)
    X = (padd(x, [-q0[0]]), padd(y, [-q0[1]]))
    l1 = pscale(padd(pscale(X[0], q2[1] - q0[1]), pscale(X[1], -(q2[0] - q0[0]))), 1 / D)
    l2 = pscale(padd(pscale(X[1], q1[0] - q0[0]), pscale(X[0], -(q1[1] - q0[1]))), 1 / D)
    l0 = padd(padd([Fraction(1)], pscale(l1, -1)), pscale(l2, -1))
    g = padd(pmul(l1, l1), pscale(pmul(l0, l2), -4))
    if len(g) < 2 or not squarefree(g):
        return None
    out = []
    for a, b in isolate(g, EPS / 8):
        sa, sb = (peval(l2, t) + peval(l1, t) / 2 for t in (a, b))
        s = (sa + sb) / 2
        if not (Fraction(-1, 100) <= s <= Fraction(101, 100)):
            continue
        if min(abs(s), abs(1 - s), a, 1 - b) < Fraction(1, 100):
            return None
        out.append(((a, b), (min(sa, sb), max(sa, sb))))
    return out


def test_parabolas() -> None:
    P = [(Fraction(0), Fraction(0)), (Fraction(1), Fraction(2)), (Fraction(2), Fraction(0))]
    Q = [(Fraction(0), Fraction(1)), (Fraction(1), Fraction(-1)), (Fraction(2), Fraction(1))]
    out = bezier_clip_intersect(P, Q)
    assert len(out) == 2
    for (a, b), (c, d) in out:
        # the exact roots satisfy 8 t^2 - 8 t + 1 = 0 and s = t
        assert (8 * a * a - 8 * a + 1) * (8 * b * b - 8 * b + 1) <= 0
        assert max(b, d) - min(a, c) <= 2 * EPS


def test_against_implicit_reference() -> None:
    rng = random.Random(11)
    tested = 0
    with_hits = 0
    while tested < 40:
        P = [(Fraction(rng.randint(-8, 8)), Fraction(rng.randint(-8, 8))) for _ in range(rng.randint(2, 4))]
        Q = [(Fraction(rng.randint(-8, 8)), Fraction(rng.randint(-8, 8))) for _ in range(3)]
        ref = reference_intersections(P, Q)
        if ref is None:
            continue
        tested += 1
        with_hits += bool(ref)
        out = bezier_clip_intersect(P, Q)
        assert len(out) == len(ref)
        for ((a, b), (c, d)), ((u, v), (s0, s1)) in zip(sorted(out), ref):
            assert a <= v + EPS and u - EPS <= b
            assert c - EPS <= s1 and s0 <= d + EPS
    assert with_hits >= 10


def test_line_against_curve() -> None:
    P = [(Fraction(0), Fraction(0)), (Fraction(1), Fraction(2)), (Fraction(2), Fraction(0))]
    L = [(Fraction(-1), Fraction(1, 2)), (Fraction(3), Fraction(1, 2))]
    out = bezier_clip_intersect(P, L)
    assert len(out) == 2
    for (a, b), _ in out:
        # 4 t (1 - t) = 1/2 gives 8 t^2 - 8 t + 1 = 0
        assert (8 * a * a - 8 * a + 1) * (8 * b * b - 8 * b + 1) <= 0


def test_disjoint_and_overlap() -> None:
    P = [(Fraction(0), Fraction(0)), (Fraction(1), Fraction(1)), (Fraction(2), Fraction(0))]
    Q = [(Fraction(0), Fraction(5)), (Fraction(1), Fraction(6)), (Fraction(2), Fraction(5))]
    assert bezier_clip_intersect(P, Q) == []
    try:
        bezier_clip_intersect(P, P, max_steps=500)
    except RuntimeError:
        pass
    else:
        raise AssertionError("overlapping curves must hit the step limit")
