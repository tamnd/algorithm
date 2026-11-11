# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ecies/. The authors are listed in prov/YWSZYG.jsonl.
"""Tests for ECIES on secp256k1 and on the toy curve of the page.

There are no official test vectors for ECIES: SEC 1 and ISO 18033-2 leave
the KDF, cipher and MAC to the user, and SEC 1 gives no worked example.
The tests check the curve constants, the worked example of the page, the
round trip, the MAC check, the benign malleability without binding, and
the invalid curve leak without validation. Randomness is seeded.
"""

import hashlib
import hmac
import random

import pytest

from ecies import (
    SECP256K1,
    TOY,
    DecryptionError,
    decrypt,
    encode_point,
    encrypt,
    kdf_x963,
    keygen,
    mul,
    neg,
    on_curve,
)


def seeded(seed: int):
    return random.Random(seed).randrange


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


def test_secp256k1_constants() -> None:
    c = SECP256K1
    assert probably_prime(c.p) and probably_prime(c.n)
    assert on_curve(c, c.g)
    assert mul(c, c.n, c.g) is None
    assert mul(c, c.n - 1, c.g) == neg(c, c.g)


def test_toy_example_of_the_page() -> None:
    c = TOY
    assert [mul(c, i, c.g) for i in (1, 2, 7, 10)] == [(5, 1), (6, 3), (0, 6), (7, 11)]
    assert mul(c, 19, c.g) is None
    d, q = keygen(c, rand_below=lambda n: 6)  # d = 7
    assert (d, q) == (7, (0, 6))
    r_bytes, body, tag = encrypt(q, b"hi", c, rand_below=lambda n: 9)  # k = 10
    assert r_bytes.hex() == "04070b"  # R = (7, 11)
    assert mul(c, 10, q) == (16, 4) == mul(c, 7, (7, 11))
    key = kdf_x963(bytes([16]), 34)
    assert key[:2].hex() == "6598"
    assert body.hex() == "0df1"
    assert tag.hex().startswith("50b9bb64")
    assert decrypt(d, (r_bytes, body, tag), c) == b"hi"


def test_kdf_counter_layout() -> None:
    z, info = b"\x01\x02", b"info"
    out = kdf_x963(z, 40, info)
    assert out[:32] == hashlib.sha256(z + b"\x00\x00\x00\x01" + info).digest()
    assert out[32:] == hashlib.sha256(z + b"\x00\x00\x00\x02" + info).digest()[:8]


@pytest.mark.parametrize("bind", [False, True])
def test_round_trip(bind: bool) -> None:
    rb = seeded(2001)
    d, q = keygen(rand_below=rb)
    for m in (b"", b"x", bytes(range(100))):
        ct = encrypt(q, m, rand_below=rb, bind_ephemeral=bind)
        assert decrypt(d, ct, bind_ephemeral=bind) == m


def test_encryption_is_randomized() -> None:
    rb = seeded(3)
    _, q = keygen(rand_below=rb)
    assert encrypt(q, b"same", rand_below=rb) != encrypt(q, b"same", rand_below=rb)


def test_mac_rejects_changes() -> None:
    rb = seeded(4)
    d, q = keygen(rand_below=rb)
    r_bytes, body, tag = encrypt(q, b"attack at dawn", rand_below=rb)
    flipped = bytes([body[0] ^ 1]) + body[1:]
    other_r = encode_point(SECP256K1, mul(SECP256K1, 5, SECP256K1.g))
    for bad in ((r_bytes, flipped, tag), (r_bytes, body, bytes(32)), (other_r, body, tag)):
        with pytest.raises(DecryptionError):
            decrypt(d, bad)


def test_negated_ephemeral_point_without_binding() -> None:
    # The KDF sees only x(Z), and x(d(-R)) = x(dR). So (-R, c, t) is a new
    # ciphertext with the same message: one decryption query wins IND-CCA2.
    c = SECP256K1
    rb = seeded(5)
    d, q = keygen(rand_below=rb)
    wins = 0
    for trial in range(8):
        m0, m1 = b"left", b"rite"
        bit = trial % 2
        r_bytes, body, tag = encrypt(q, (m0, m1)[bit], rand_below=rb)
        r = (int.from_bytes(r_bytes[1:33], "big"), int.from_bytes(r_bytes[33:], "big"))
        query = (encode_point(c, neg(c, r)), body, tag)
        assert query != (r_bytes, body, tag)
        wins += decrypt(d, query) == (m0, m1)[bit]
    assert wins == 8
    r_bytes, body, tag = encrypt(q, b"left", rand_below=rb, bind_ephemeral=True)
    r = (int.from_bytes(r_bytes[1:33], "big"), int.from_bytes(r_bytes[33:], "big"))
    with pytest.raises(DecryptionError):
        decrypt(d, (encode_point(c, neg(c, r)), body, tag), bind_ephemeral=True)


def test_invalid_curve_point_leaks_without_validation() -> None:
    # T = (0, 1) lies on y^2 = x^3 + 1, not on secp256k1, and has order 3.
    # The addition formulas do not use b, so dT is computed on that curve.
    c = SECP256K1
    t = (0, 1)
    assert not on_curve(c, t) and mul(c, 3, t) is None
    z = c.size * b"\x00"  # x(T) = x(-T) = 0
    k = kdf_x963(z, 1 + 32)
    body = b"\x00"
    tag = hmac.new(k[1:], body, hashlib.sha256).digest()
    ct = (encode_point(c, t), body, tag)
    for d in (3 * 12345, 3 * 12345 + 1, 3 * 12345 + 2):
        with pytest.raises(DecryptionError):
            decrypt(d, ct)  # validation stops the attack
        if d % 3 == 0:
            with pytest.raises(DecryptionError):
                decrypt(d, ct, validate=False)
        else:
            assert decrypt(d, ct, validate=False) == k[:1]  # accepted: d mod 3 != 0
