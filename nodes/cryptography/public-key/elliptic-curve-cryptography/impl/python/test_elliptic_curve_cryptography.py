# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/elliptic-curve-cryptography/. The authors are listed in prov/HTEPPM.jsonl.
"""Tests for the elliptic curve group code.

Official vector: the P-256 key pair of RFC 6979 Appendix A.2.5 (private
key x and public key U = xG), and the value r of the signature with SHA-256
on the message "sample" in the same appendix, which is x(kG) mod n for the
nonce k given there. The other tests check the group laws on the toy curve
and the worked examples of the page.
"""

import itertools
import random

from elliptic_curve_cryptography import (
    P256,
    TOY,
    add,
    compress,
    decompress,
    is_nonsingular,
    ladder,
    neg,
    on_curve,
)

# RFC 6979 Appendix A.2.5 (ECDSA, 256 bits, prime field).
RFC6979_X = 0xC9AFA9D845BA75166B5C215767B1D6934E50C3DB36E89B127B8A622B120F6721
RFC6979_UX = 0x60FED4BA255A9D31C961EB74C6356D68C049B8923B61FA6CE669622E60F29FB6
RFC6979_UY = 0x7903FE1008B8BC99A41AE9E95628BC64F2F1B20C2D7E9F5177A3C294D4462299
# With SHA-256, message = "sample":
RFC6979_K = 0xA6E3C57DD01ABE90086538398355DD4C3B17AA873382B0F24D6129493D8AAD60
RFC6979_R = 0xEFD48B2AACB6A8FD1140DD9CD45E81D69D2C877B56AAF991C34D0EA84EAF3716


def probably_prime(n: int) -> bool:
    d, s = n - 1, 0
    while d % 2 == 0:
        d, s = d // 2, s + 1
    for a in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


def slow_mul(c, k, pt):
    acc = None
    for bit in bin(k)[2:]:
        acc = add(c, acc, acc)
        if bit == "1":
            acc = add(c, acc, pt)
    return acc


def test_p256_parameters() -> None:
    c = P256
    assert probably_prime(c.p) and probably_prime(c.n)
    assert is_nonsingular(c) and on_curve(c, c.g)
    assert ladder(c, c.n, c.g) is None
    assert ladder(c, c.n - 1, c.g) == neg(c, c.g)
    assert abs(c.n * c.h - (c.p + 1)) <= 2 * (c.p ** 0.5 + 1)  # the Hasse bound


def test_rfc6979_a25_key_pair() -> None:
    u = ladder(P256, RFC6979_X, P256.g)
    assert u == (RFC6979_UX, RFC6979_UY)
    assert on_curve(P256, u)


def test_rfc6979_a25_signature_r() -> None:
    kg = ladder(P256, RFC6979_K, P256.g)
    assert kg[0] % P256.n == RFC6979_R


def test_compression_round_trip() -> None:
    u = (RFC6979_UX, RFC6979_UY)
    data = compress(P256, u)
    assert data[0] == 3 and len(data) == 33  # U_y is odd
    assert decompress(P256, data) == u
    assert decompress(P256, compress(P256, neg(P256, u))) == neg(P256, u)


def test_ladder_matches_affine_on_p256() -> None:
    rng = random.Random(1985)
    for _ in range(3):
        k = rng.randrange(1, P256.n)
        assert ladder(P256, k, P256.g) == slow_mul(P256, k, P256.g)


def test_toy_curve_group() -> None:
    c = TOY
    points = [None] + [(x, y) for x in range(17) for y in range(17) if on_curve(c, (x, y))]
    assert len(points) == 19 and is_nonsingular(c)
    assert add(c, c.g, c.g) == (6, 3) and add(c, c.g, (6, 3)) == (10, 6)
    multiples = [ladder(c, k, c.g) for k in range(19)]
    assert sorted(multiples, key=str) == sorted(points, key=str)  # G generates the group
    for p1, p2 in itertools.product(points, repeat=2):
        assert add(c, p1, p2) == add(c, p2, p1)
        assert on_curve(c, add(c, p1, p2))
    for p1, p2, p3 in itertools.product(points, repeat=3):
        assert add(c, add(c, p1, p2), p3) == add(c, p1, add(c, p2, p3))


def test_toy_ecdh_and_discrete_log() -> None:
    c = TOY
    a_pub, b_pub = ladder(c, 3, c.g), ladder(c, 7, c.g)
    assert (a_pub, b_pub) == ((10, 6), (0, 6))
    assert ladder(c, 3, b_pub) == ladder(c, 7, a_pub) == (6, 3)
    # Brute force: the discrete log of (0, 6) is found by trying all 19 scalars.
    assert [k for k in range(19) if ladder(c, k, c.g) == (0, 6)] == [7]
