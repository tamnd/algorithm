# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/parametric-continuity/. The authors are listed in prov/WGBTZC.jsonl.

import random
from fractions import Fraction as F
from math import comb, inf

from parametric_continuity import (
    bezier_to_power,
    continuity_order,
    derivative_at,
    g1_beta,
    g2_betas,
)


def rand_vec(rng, d, lo=-5, hi=5):
    return tuple(F(rng.randint(lo, hi), rng.randint(1, 3)) for _ in range(d))


def rand_seg(rng, deg, d):
    return [rand_vec(rng, d) for _ in range(deg + 1)]


def taylor_order(A, B, ha, hb):
    """Reference: the first index where B(s/hb) - A(1 + s/ha) has a nonzero s^k coefficient, minus 1."""
    top = max(len(A), len(B))
    d = len(A[0])
    for k in range(top):
        bk = B[k] if k < len(B) else (F(0),) * d
        ak = [F(0)] * d
        for i in range(k, len(A)):
            ak = [x + comb(i, k) * y for x, y in zip(ak, A[i])]
        diff = [x / hb ** k - y / ha ** k for x, y in zip(bk, ak)]
        if any(v != 0 for v in diff):
            return k - 1
    return inf


def poly_mul(p, q):
    out = [F(0)] * (len(p) + len(q) - 1)
    for i, a in enumerate(p):
        for j, b in enumerate(q):
            out[i + j] += a * b
    return out


def compose(seg, phi):
    """The segment seg(phi(s)) for a scalar polynomial phi given by its coefficients."""
    d = len(seg[0])
    res = [[F(0)] for _ in range(d)]
    for c in reversed(seg):
        res = [poly_mul(r, phi) for r in res]
        for k in range(d):
            res[k][0] += c[k]
    n = max(len(r) for r in res)
    return [tuple(res[k][i] if i < len(res[k]) else F(0) for k in range(d)) for i in range(n)]


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def curvature_vector(seg, u):
    """kappa N = (|C'|^2 C'' - (C'.C'') C') / |C'|^4, rational in the coefficients."""
    c1 = derivative_at(seg, u, 1)
    c2 = derivative_at(seg, u, 2)
    s = dot(c1, c1)
    return tuple((s * b - dot(c1, c2) * a) / (s * s) for a, b in zip(c1, c2))


def with_jets(A, jets, extra):
    """A segment B starting at the given derivative values (local, h = 1), then free terms."""
    B = []
    f = 1
    for j, v in enumerate(jets):
        if j:
            f *= j
        B.append(tuple(x / f for x in v))
    return B + extra


def test_derivative_against_expansion():
    rng = random.Random(1)
    for _ in range(100):
        seg = rand_seg(rng, rng.randint(0, 5), 2)
        u = F(rng.randint(-4, 4), rng.randint(1, 4))
        for j in range(len(seg) + 1):
            ref = [F(0), F(0)]
            for i in range(j, len(seg)):
                f = 1
                for r in range(i - j + 1, i + 1):
                    f *= r
                ref = [x + f * c * u ** (i - j) for x, c in zip(ref, seg[i])]
            assert derivative_at(seg, u, j) == tuple(ref)


def test_continuity_order_against_taylor_shift():
    rng = random.Random(2)
    seen = set()
    for _ in range(300):
        d = rng.choice((2, 3))
        A = rand_seg(rng, rng.randint(1, 4), d)
        ha = F(rng.randint(1, 4), rng.randint(1, 3))
        hb = F(rng.randint(1, 4), rng.randint(1, 3))
        k = rng.randint(-1, 3)
        one = F(1)
        jets = [derivative_at(A, one, j, ha) for j in range(k + 1)]
        # scale global derivatives back to the local parameter of B
        jets = [tuple(x * hb ** j for x in v) for j, v in enumerate(jets)]
        B = with_jets(A, jets, rand_seg(rng, rng.randint(0, 2), d))
        got = continuity_order(A, B, ha, hb)
        assert got == taylor_order(A, B, ha, hb)
        assert got >= k
        seen.add(got)
    assert {-1, 0, 1, 2}.issubset(seen)


def test_one_polynomial_is_c_infinity():
    rng = random.Random(3)
    for _ in range(50):
        P = rand_seg(rng, 3, 2)
        # P on [0, 2] cut at 1: A(u) = P(u), B(u) = P(1 + u)
        B = compose(P, [F(1), F(1)])
        assert continuity_order(P, B) == inf


def test_g1_and_g2_by_construction():
    rng = random.Random(4)
    for _ in range(200):
        d = rng.choice((2, 3))
        A = rand_seg(rng, 3, d)
        a1 = derivative_at(A, F(1), 1)
        if all(x == 0 for x in a1):
            continue
        b1 = F(rng.randint(1, 6), rng.randint(1, 4))
        b2 = F(rng.randint(-5, 5), rng.randint(1, 3))
        a2 = derivative_at(A, F(1), 2)
        jets = [derivative_at(A, F(1), 0), tuple(b1 * x for x in a1),
                tuple(b1 * b1 * y + b2 * x for x, y in zip(a1, a2))]
        B = with_jets(A, jets, [rand_vec(rng, d)])
        assert g1_beta(A, B) == b1
        assert g2_betas(A, B) == (b1, b2)
        # same unit tangent and same curvature vector at the joint
        assert curvature_vector(A, F(1)) == curvature_vector(B, F(0))
        # the reparametrization u = s / b1 - b2 s^2 / (2 b1^3) makes the joint C^2
        Bs = compose(B, [F(0), 1 / b1, -b2 / (2 * b1 ** 3)])
        assert continuity_order(A, Bs) >= 2
        # C^1 exactly when beta1 = 1, C^2 exactly when also beta2 = 0
        assert (continuity_order(A, B) >= 1) == (b1 == 1)
        assert (continuity_order(A, B) >= 2) == (b1 == 1 and b2 == 0)


def test_g2_fails_when_curvature_jumps():
    rng = random.Random(5)
    count = 0
    for _ in range(200):
        A = rand_seg(rng, 3, 2)
        a1 = derivative_at(A, F(1), 1)
        if all(x == 0 for x in a1):
            continue
        b1 = F(rng.randint(1, 5))
        a2 = derivative_at(A, F(1), 2)
        normal = (-a1[1], a1[0])
        e = F(rng.randint(1, 4))
        jets = [derivative_at(A, F(1), 0), tuple(b1 * x for x in a1),
                tuple(b1 * b1 * y + e * z for y, z in zip(a2, normal))]
        B = with_jets(A, jets, [])
        assert g1_beta(A, B) == b1
        assert g2_betas(A, B) is None
        assert curvature_vector(A, F(1)) != curvature_vector(B, F(0))
        count += 1
    assert count > 100


def test_g1_fails():
    # a corner, a reversed tangent and a zero velocity
    A = [(F(0), F(0)), (F(1), F(0))]
    assert g1_beta(A, [(F(1), F(0)), (F(1), F(1))]) is None
    assert g1_beta(A, [(F(1), F(0)), (F(-2), F(0))]) is None
    assert g1_beta(A, [(F(1), F(0)), (F(0), F(0)), (F(1), F(0))]) is None
    assert g1_beta(A, [(F(2), F(0)), (F(1), F(0))]) is None


def test_page_example_c1_not_g1():
    # A(t) = (-(1 - t)^2, 0), B(t) = (0, t^2)
    A = [(F(-1), F(0)), (F(2), F(0)), (F(-1), F(0))]
    B = [(F(0), F(0)), (F(0), F(0)), (F(0), F(1))]
    assert continuity_order(A, B) == 1
    assert g1_beta(A, B) is None


def test_bezier_joint_conditions():
    rng = random.Random(6)
    for _ in range(100):
        a = [rand_vec(rng, 2) for _ in range(4)]
        if a[3] == a[2]:
            continue
        beta = F(rng.randint(1, 5), rng.randint(1, 3))
        b1 = tuple(x + beta * (x - y) for x, y in zip(a[3], a[2]))
        b = [a[3], b1, rand_vec(rng, 2), rand_vec(rng, 2)]
        A, B = bezier_to_power(a), bezier_to_power(b)
        # the power form reproduces the end points and the end tangents 3 (P1 - P0)
        assert derivative_at(A, F(0), 0) == a[0] and derivative_at(A, F(1), 0) == a[3]
        assert derivative_at(B, F(0), 1) == tuple(3 * (x - y) for x, y in zip(b[1], b[0]))
        assert g1_beta(A, B) == beta
        assert (continuity_order(A, B) >= 1) == (beta == 1)


def test_page_g2_example():
    # A(t) = (t, t^2), and B starts at (1, 1) with beta1 = 2, beta2 = 1
    A = [(F(0), F(0)), (F(1), F(0)), (F(0), F(1))]
    B = [(F(1), F(1)), (F(2), F(4)), (F(1, 2), F(5))]
    assert continuity_order(A, B) == 0
    assert g2_betas(A, B) == (2, 1)
    assert curvature_vector(A, F(1)) == curvature_vector(B, F(0)) == (F(-4, 25), F(2, 25))
    assert continuity_order(A, compose(B, [F(0), F(1, 2), F(-1, 16)])) >= 2
    # no choice of knot intervals makes it C^2, since beta2 != 0
    assert continuity_order(A, B, 1, F(2)) == 1


def test_page_bezier_example():
    a = [(F(0), F(0)), (F(1), F(1)), (F(2), F(1)), (F(3), F(0))]
    b = [(F(3), F(0)), (F(5), F(-2)), (F(6), F(0)), (F(7), F(2))]
    A, B = bezier_to_power(a), bezier_to_power(b)
    assert continuity_order(A, B) == 0
    assert g1_beta(A, B) == 2
    # knot intervals 1 and 2 turn the same joint into C^1
    assert continuity_order(A, B, 1, F(2)) >= 1
