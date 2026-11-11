# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bilinear-pairing/. The authors are listed in prov/VJKYK9.jsonl.
#
# The toy curve is not a standard curve, so there are no official test vectors. The tests check
# the worked example of the page and the defining properties (bilinearity, non-degeneracy,
# symmetry, values of order r) with fixed seeds. The curves are NOT secure.

import random

import bilinear_pairing as bp


def test_tiny_worked_example() -> None:
    C = bp.TINY
    assert C.points_of_order_r() == [(5, 3), (5, 8)]
    G = C.generator()
    assert G == (5, 3) and C.mul(2, G) == (5, 8) and C.mul(3, G) is None
    assert C.distortion(G) == ((6, 0), (0, 3))
    assert C.miller(G, G) == (10, 3)  # the tangent line at G, evaluated at psi(G)
    f = C.miller(G, G)
    g = C.f2_mul((f[0], -f[1] % 11), C.f2_inv(f))
    assert g == (8, 5)  # f^(p - 1)
    assert C.f2_pow(g, 4) == (5, 3)
    w = C.pairing(G, G)
    assert w == (5, 3)
    assert C.f2_mul(w, w) == (5, 8) == C.pairing(G, C.mul(2, G)) == C.pairing(C.mul(2, G), G)
    assert C.f2_pow(w, 3) == (1, 0)
    assert C.pairing(C.mul(2, G), C.mul(2, G)) == C.f2_pow(w, 4) == w


def test_toy_curve_parameters() -> None:
    C = bp.TOY
    assert C.p.bit_length() == 128 and C.p % 4 == 3
    assert (C.p + 1) % C.r == 0 and C.r > 2**63
    assert (C.p * C.p - 1) % C.r == 0 and (C.p - 1) % C.r != 0  # embedding degree 2
    G = C.generator()
    assert C.on_curve(G) and G is not None and C.mul(C.r, G) is None


def test_non_degenerate_and_order_r() -> None:
    C = bp.TOY
    G = C.generator()
    z = C.pairing(G, G)
    assert z != (1, 0)
    assert C.f2_pow(z, C.r) == (1, 0)


def test_bilinearity() -> None:
    C = bp.TOY
    G = C.generator()
    z = C.pairing(G, G)
    rng = random.Random(2001)
    for _ in range(4):
        a, b = rng.randrange(1, C.r), rng.randrange(1, C.r)
        A, B = C.mul(a, G), C.mul(b, G)
        assert C.pairing(A, B) == C.f2_pow(z, a * b % C.r)
        assert C.pairing(A, B) == C.pairing(B, A)  # symmetric (Type 1)
    P1, P2, Q = (C.mul(rng.randrange(1, C.r), G) for _ in range(3))
    assert C.pairing(C.add(P1, P2), Q) == C.f2_mul(C.pairing(P1, Q), C.pairing(P2, Q))
    assert C.pairing(Q, C.add(P1, P2)) == C.f2_mul(C.pairing(Q, P1), C.pairing(Q, P2))


def test_without_distortion_the_pairing_degenerates() -> None:
    # On G1 x G1 itself (no distortion map) the reduced Tate pairing of P with a multiple of P is 1.
    # The tiny curve shows it: the line values then lie in F_p, and f^(p - 1) = 1.
    C = bp.TINY
    G = (5, 3)
    xt, yt = G
    lam = (3 * xt * xt + 1) * pow(2 * yt, 9, 11) % 11
    line_at_G2 = (C.mul(2, G)[1] - yt - lam * (C.mul(2, G)[0] - xt)) % 11
    assert pow(line_at_G2, 10, 11) == 1


def test_mov_style_transfer() -> None:
    # The pairing moves a discrete logarithm in G1 to one in GT: e(xG, G) = e(G, G)^x.
    C = bp.TOY
    G = C.generator()
    x = 123456789
    assert C.pairing(C.mul(x, G), G) == C.f2_pow(C.pairing(G, G), x)


def test_hash_to_g1() -> None:
    C = bp.TOY
    Q = C.hash_to_g1(b"alice@example.com")
    assert C.on_curve(Q) and C.mul(C.r, Q) is None
    assert Q == C.hash_to_g1(b"alice@example.com") != C.hash_to_g1(b"bob@example.com")
