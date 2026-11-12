# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/curve-intersection/. The authors are listed in prov/9E0B9K.jsonl.

import random
from fractions import Fraction
from math import comb

from curve_intersection import box, intersect_by_subdivision, split_half

F = Fraction
EPS = F(1, 2**16)


def trim(p):
    p = list(p)
    while p and p[-1] == 0:
        p.pop()
    return p


def padd(p, q):
    r = [F(0)] * max(len(p), len(q))
    for i, a in enumerate(p):
        r[i] += a
    for i, a in enumerate(q):
        r[i] += a
    return trim(r)


def pmul(p, q):
    if not p or not q:
        return []
    r = [F(0)] * (len(p) + len(q) - 1)
    for i, a in enumerate(p):
        for j, b in enumerate(q):
            r[i + j] += a * b
    return trim(r)


def pscale(p, k):
    return trim([k * a for a in p])


def peval(p, t):
    r = F(0)
    for a in reversed(p):
        r = r * t + a
    return r


def prem(p, q):
    p = list(p)
    while len(p) >= len(q) and p:
        k = p[-1] / q[-1]
        s = len(p) - len(q)
        for i, b in enumerate(q):
            p[s + i] -= k * b
        p = trim(p)
    return p


def sturm_chain(p):
    chain = [trim(p), trim([i * a for i, a in enumerate(p)][1:])]
    while True:
        r = pscale(prem(chain[-2], chain[-1]), -1)
        if not r:
            return chain
        chain.append(r)


def changes(chain, t):
    s = [v for v in (peval(q, t) for q in chain) if v != 0]
    return sum(1 for u, v in zip(s, s[1:]) if (u > 0) != (v > 0))


def isolate(p, width):
    chain = sturm_chain(p)
    if len(chain[-1]) != 1:
        return None  # not squarefree
    out = [(F(0), F(0))] if peval(p, 0) == 0 else []
    stack = [(F(0), F(1))]
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


def bernstein_to_power(c):
    n = len(c) - 1
    p = [F(0)] * (n + 1)
    for i, ci in enumerate(c):
        for k in range(i, n + 1):
            p[k] += ci * (-1) ** (k - i) * comb(n, k) * comb(k, i)
    return trim(p)


def point(P, t):
    n = len(P) - 1
    return tuple(sum(p[k] * comb(n, i) * t**i * (1 - t) ** (n - i) for i, p in enumerate(P)) for k in range(2))


def cross(u, v):
    return u[0] * v[1] - u[1] * v[0]


def implicit_reference(P, Q):
    """Exact reference for a quadratic Q, by its implicit equation.

    With the barycentric coordinates l0, l1, l2 of the triangle Q0 Q1 Q2,
    the parabola is l1^2 = 4 l0 l2, and its parameter is s = l2 + l1 / 2.
    Return a list of (t interval, s interval), or None near a degenerate case.
    """
    q0, q1, q2 = Q
    D = cross((q1[0] - q0[0], q1[1] - q0[1]), (q2[0] - q0[0], q2[1] - q0[1]))
    if D == 0:
        return None
    x = padd(bernstein_to_power([p[0] for p in P]), [-q0[0]])
    y = padd(bernstein_to_power([p[1] for p in P]), [-q0[1]])
    l1 = pscale(padd(pscale(x, q2[1] - q0[1]), pscale(y, -(q2[0] - q0[0]))), 1 / D)
    l2 = pscale(padd(pscale(y, q1[0] - q0[0]), pscale(x, -(q1[1] - q0[1]))), 1 / D)
    l0 = padd(padd([F(1)], pscale(l1, -1)), pscale(l2, -1))
    g = padd(pmul(l1, l1), pscale(pmul(l0, l2), -4))
    if len(g) < 2:
        return None
    iso = isolate(g, EPS / 8)
    if iso is None:
        return None
    out = []
    for a, b in iso:
        sa, sb = (peval(l2, t) + peval(l1, t) / 2 for t in (a, b))
        s = (sa + sb) / 2
        if not (F(-1, 100) <= s <= F(101, 100)):
            continue
        if min(abs(s), abs(1 - s), a, 1 - b) < F(1, 100):
            return None
        out.append(((a, b), (min(sa, sb), max(sa, sb))))
    return out


def polyline_crossings(P, Q, N):
    """Proper crossings of the polylines through N + 1 exact curve samples."""
    ps = [point(P, F(k, N)) for k in range(N + 1)]
    qs = [point(Q, F(k, N)) for k in range(N + 1)]
    hits = []
    for i in range(N):
        a, b = ps[i], ps[i + 1]
        for j in range(N):
            c, d = qs[j], qs[j + 1]
            o1 = cross((b[0] - a[0], b[1] - a[1]), (c[0] - a[0], c[1] - a[1]))
            o2 = cross((b[0] - a[0], b[1] - a[1]), (d[0] - a[0], d[1] - a[1]))
            o3 = cross((d[0] - c[0], d[1] - c[1]), (a[0] - c[0], a[1] - c[1]))
            o4 = cross((d[0] - c[0], d[1] - c[1]), (b[0] - c[0], b[1] - c[1]))
            if o1 * o2 < 0 and o3 * o4 < 0:
                hits.append((F(2 * i + 1, 2 * N), F(2 * j + 1, 2 * N)))
    return hits


def test_split_and_box() -> None:
    P = [(F(0), F(0)), (F(1), F(2)), (F(3), F(2)), (F(4), F(0))]
    left, right = split_half(P)
    for k in range(5):
        u = F(k, 4)
        assert point(left, u) == point(P, u / 2)
        assert point(right, u) == point(P, (1 + u) / 2)
    assert box(P) == (0, 4, 0, 2)


def test_parabolas() -> None:
    P = [(F(0), F(0)), (F(1), F(2)), (F(2), F(0))]
    Q = [(F(0), F(1)), (F(1), F(-1)), (F(2), F(1))]
    out = intersect_by_subdivision(P, Q)
    assert len(out) == 2
    for (a, b), (c, d) in out:
        # the exact parameters are the roots of 8 t^2 - 8 t + 1 with s = t
        assert (8 * a * a - 8 * a + 1) * (8 * b * b - 8 * b + 1) <= 0
        assert (8 * c * c - 8 * c + 1) * (8 * d * d - 8 * d + 1) <= 0
        assert b - a <= 4 * EPS


def test_against_implicit_reference_and_sampling() -> None:
    rng = random.Random(21)
    tested = hits = 0
    while tested < 25:
        P = [(F(rng.randint(-8, 8)), F(rng.randint(-8, 8))) for _ in range(rng.randint(2, 4))]
        Q = [(F(rng.randint(-8, 8)), F(rng.randint(-8, 8))) for _ in range(3)]
        ref = implicit_reference(P, Q)
        if ref is None:
            continue
        tested += 1
        hits += bool(ref)
        out = intersect_by_subdivision(P, Q)
        assert len(out) == len(ref)
        for ((a, b), (c, d)), ((u, v), (s0, s1)) in zip(out, ref):
            assert a <= v + EPS and u - EPS <= b
            assert c - EPS <= s1 and s0 <= d + EPS
        # dense exact sampling: each polyline crossing is near an output box
        N = 48
        for t, s in polyline_crossings(P, Q, N):
            assert any(a - F(2, N) <= t <= b + F(2, N) and c - F(2, N) <= s <= d + F(2, N) for (a, b), (c, d) in out)
    assert hits >= 8


def test_disjoint_touching_and_overlap() -> None:
    P = [(F(0), F(0)), (F(1), F(1)), (F(2), F(0))]
    assert intersect_by_subdivision(P, [(F(0), F(3)), (F(2), F(3))]) == []
    # the line y = 1/2 touches the top of the parabola y = 2 t (1 - t) at t = 1/2
    out = intersect_by_subdivision(P, [(F(0), F(1, 2)), (F(2), F(1, 2))])
    assert len(out) == 1 and out[0][0][0] <= F(1, 2) <= out[0][0][1]
    try:
        intersect_by_subdivision(P, P, max_pairs=3000)
    except RuntimeError:
        pass
    else:
        raise AssertionError("overlapping curves must hit the pair limit")
