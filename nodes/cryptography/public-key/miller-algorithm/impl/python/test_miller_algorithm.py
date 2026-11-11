# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/miller-algorithm/. The authors are listed in prov/7N5369.jsonl.
#
# The toy curves are not standard curves, so there are no official test vectors. The tests check
# the worked example of the page on p = 59, bilinearity and non-degeneracy of the reduced Tate and
# Weil pairings, and that the fast and naive final exponentiations and the versions with and
# without denominators agree, with fixed seeds. The curves are NOT secure.

import random

import miller_algorithm as m

P59 = 59


def tiny():
    C = m.Curve(P59, 1, 0, 5)
    P = C.point(25, 29)
    return C, P, C.distortion(P)


def test_worked_example_p59() -> None:
    C, P, Q = tiny()
    F = C.F
    assert [C.mul(k, P) for k in range(1, 6)] == [
        ((25, 0), (29, 0)), ((35, 0), (28, 0)), ((35, 0), (31, 0)), ((25, 0), (30, 0)), None]
    assert Q == ((34, 0), (0, 29)) and C.on_curve(Q)
    # r = 5 = 101 in binary: doubling, then doubling and addition.
    assert C.slope(P, P) == (12, 0)
    assert C.line(P, P, Q) == (40, 29) and C.vertical(C.mul(2, P), Q) == (58, 0)
    f1 = F.div(C.line(P, P, Q), (58, 0))
    assert f1 == (19, 30)
    P2 = C.mul(2, P)
    assert C.slope(P2, P2) == (53, 0)
    assert C.line(P2, P2, Q) == (25, 29) and C.vertical(C.mul(4, P), Q) == (9, 0)
    f2 = F.div(F.mul(F.mul(f1, f1), (25, 29)), (9, 0))
    assert f2 == (28, 27)
    P4 = C.mul(4, P)
    assert C.slope(P4, P) is None and C.line(P4, P, Q) == (9, 0)  # vertical, since 4P = -P
    f3 = F.mul(f2, (9, 0))
    assert f3 == (16, 7) == C.miller(P, Q, 5)
    assert C.miller(P, Q, 5, denominators=False) == (26, 4)
    assert (59 * 59 - 1) // 5 == 696
    assert F.pow((16, 7), 696) == (42, 40) == F.pow((26, 4), 696)
    assert C.tate(P, Q) == C.tate(P, Q, fast=False) == (42, 40)
    z = (42, 40)
    assert [F.pow(z, k) for k in range(1, 6)] == [(42, 40), (46, 56), (46, 3), (42, 19), (1, 0)]
    assert C.weil(P, Q) == (46, 56)


def test_tiny_bilinearity_all_pairs() -> None:
    C, P, Q = tiny()
    F = C.F
    z, w = C.tate(P, Q), C.weil(P, Q)
    for a in range(1, 5):
        for b in range(1, 5):
            A, B = C.mul(a, P), C.mul(b, Q)
            assert C.tate(A, B) == F.pow(z, a * b) == C.tate(A, B, fast=False)
            assert C.weil(A, B) == F.pow(w, a * b)


def test_general_coefficients_y2_x3_plus_1() -> None:
    # y^2 = x^3 + 1 over F_59 (59 = 2 mod 3) is supersingular with 60 points; the distortion map is
    # (x, y) -> (zeta x, y) for a primitive cube root of unity zeta in F_59^2.
    C = m.Curve(P59, 0, 1, 5)
    F = C.F
    s = next(t for t in range(59) if t * t % 59 == 3)
    zeta = F.mul(F.e(-1, s), F.inv(F.e(2)))
    assert zeta != (1, 0) and F.pow(zeta, 3) == (1, 0)
    pts = [C.point(x, y) for x in range(59) for y in range(59) if (y * y - x**3 - 1) % 59 == 0]
    assert len(pts) + 1 == 60
    P = next(T for T in (C.mul(12, U) for U in pts) if T is not None)
    Q = (F.mul(zeta, P[0]), P[1])
    assert C.on_curve(Q)
    z = C.tate(P, Q)
    assert z != (1, 0) and F.pow(z, 5) == (1, 0)
    assert z == C.tate(P, Q, fast=False)
    # Here x_Q is not in F_p, so dropping the vertical lines gives a wrong value.
    assert C.final_exponentiation(C.miller(P, Q, 5, denominators=False)) != z
    for a in range(1, 5):
        for b in range(1, 5):
            assert C.tate(C.mul(a, P), C.mul(b, Q)) == F.pow(z, a * b)


def toy():
    # The 128-bit toy curve y^2 = x^3 + x of the bilinear pairing page.
    p = 170141183460469232340429858148299309287
    r = 9223372036854775837
    C = m.Curve(p, 1, 0, r)
    x = 2
    while True:
        rhs = (x**3 + x) % p
        if pow(rhs, (p - 1) // 2, p) == 1:
            P = C.mul((p + 1) // r, C.point(x, pow(rhs, (p + 1) // 4, p)))
            if P is not None:
                return C, P
        x += 1


def test_toy_tate_bilinear_and_non_degenerate() -> None:
    C, P = toy()
    F = C.F
    assert C.mul(C.r, P) is None
    Q = C.distortion(P)
    z = C.tate(P, Q)
    assert z != (1, 0) and F.pow(z, C.r) == (1, 0)
    assert z == C.tate(P, Q, fast=False)
    rng = random.Random(1986)
    for _ in range(3):
        a, b = rng.randrange(1, C.r), rng.randrange(1, C.r)
        assert C.tate(C.mul(a, P), C.mul(b, Q)) == F.pow(z, a * b % C.r)


def test_toy_weil_alternating_and_bilinear() -> None:
    C, P = toy()
    F = C.F
    Q = C.distortion(P)
    w = C.weil(P, Q)
    assert w != (1, 0) and F.pow(w, C.r) == (1, 0)
    assert C.weil(Q, P) == F.inv(w)  # antisymmetric
    a = random.Random(2004).randrange(1, C.r)
    assert C.weil(C.mul(a, P), Q) == F.pow(w, a)


def test_without_distortion_the_tate_value_is_1() -> None:
    C, P = toy()
    assert C.tate(P, C.mul(7, P)) == (1, 0)
