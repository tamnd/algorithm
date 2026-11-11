# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ed25519/. The authors are listed in prov/2THJ4W.jsonl.

import hashlib

from ed25519 import (
    B,
    IDENTITY,
    L,
    decode,
    encode,
    expand_secret,
    point_equal,
    point_mul,
    public_key,
    sign,
    sha512_int,
    sign_with_torsion_key,
    torsion_point_of_order_8,
    verify,
)

# RFC 8032, Section 7.1, TEST 1, TEST 2 and TEST 3, copied by hand.
VECTORS = [
    (
        "9d61b19deffd5a60ba844af492ec2cc44449c5697b326919703bac031cae7f60",
        "d75a980182b10ab7d54bfed3c964073a0ee172f3daa62325af021a68f707511a",
        "",
        "e5564300c360ac729086e2cc806e828a84877f1eb8e5d974d873e065224901555fb8821590a33bacc61e39701cf9b46bd25bf5f0595bbe24655141438e7a100b",
    ),
    (
        "4ccd089b28ff96da9db6c346ec114e0f5b8a319f35aba624da8cf6ed4fb8a6fb",
        "3d4017c3e843895a92b70aa74d1b7ebc9c982ccf2ec4968cc0cd55f12af4660c",
        "72",
        "92a009a9f0d4cab8720e820b5f642540a2b27b5416503f8fb3762223ebdb69da085ac1e43e15996e458f3613d0f11d8c387b2eaeb4302aeeb00d291612bb0c00",
    ),
    (
        "c5aa8df43f9f837bedb7442f31dcb7b166d38535076f094b85ce3a2e0b4458f7",
        "fc51cd8e6218a1a38da47ed00230f0580816ed13ba3303ac5deb911548908025",
        "af82",
        "6291d657deec24024827e69c3abe01a30ce548a284743a445e3680d7db5ac3ac18ff9b538d16f290ae67f760984dc6594a7c15e9716ed28dc027beceea1ec40a",
    ),
]


def test_base_point() -> None:
    assert encode(B).hex() == "58" + "66" * 31
    assert point_equal(point_mul(L, B), IDENTITY)


def test_rfc8032_vectors() -> None:
    for sk_hex, pk_hex, msg_hex, sig_hex in VECTORS:
        sk, msg = bytes.fromhex(sk_hex), bytes.fromhex(msg_hex)
        assert public_key(sk).hex() == pk_hex
        assert sign(sk, msg).hex() == sig_hex
        pk, sig = bytes.fromhex(pk_hex), bytes.fromhex(sig_hex)
        for cof in (True, False):
            assert verify(pk, msg, sig, cofactored=cof)
            assert not verify(pk, msg + b"x", sig, cofactored=cof)
            bad = bytearray(sig)
            bad[40] ^= 1
            assert not verify(pk, msg, bytes(bad), cofactored=cof)


def test_deterministic() -> None:
    sk = bytes(range(32))
    assert sign(sk, b"abc") == sign(sk, b"abc")
    assert sign(sk, b"abc")[:32] != sign(sk, b"abd")[:32]


def test_non_canonical_s_is_rejected() -> None:
    sk, pk_hex, msg_hex, sig_hex = VECTORS[0]
    sig = bytes.fromhex(sig_hex)
    s = int.from_bytes(sig[32:], "little")
    twin = sig[:32] + (s + L).to_bytes(32, "little")
    # s + L passes the group equation, so only the check S < L stops this second signature.
    assert not verify(bytes.fromhex(pk_hex), b"", twin)


def test_encoding_round_trip() -> None:
    p = point_mul(123456789, B)
    assert point_equal(decode(encode(p)), p)
    assert decode(b"\xff" * 32) is None  # y >= p


def test_cofactored_and_cofactorless_disagree() -> None:
    t = torsion_point_of_order_8()
    assert point_equal(point_mul(8, t), IDENTITY)
    a, prefix = expand_secret(bytes(32))
    agree = disagree = 0
    for i in range(16):
        msg = b"message %d" % i
        pk, sig = sign_with_torsion_key(a, prefix, t, msg)
        k = sha512_int(sig[:32], pk, msg) % L
        assert verify(pk, msg, sig, cofactored=True)
        plain = verify(pk, msg, sig, cofactored=False)
        assert plain == (k % 8 == 0)
        agree += plain
        disagree += not plain
    assert disagree >= 8  # about 7 in 8 messages split the two verifiers


def test_sha512_from_hashlib() -> None:
    assert sha512_int(b"") == int.from_bytes(hashlib.sha512(b"").digest(), "little")
