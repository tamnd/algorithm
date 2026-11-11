# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/x25519/. The authors are listed in prov/J2GJN1.jsonl.

import random

import pytest

from x25519 import (
    P,
    cswap,
    decode_scalar,
    decode_u_coordinate,
    ladder_step,
    public_key,
    x25519,
    x25519_shared,
)

H = bytes.fromhex

# RFC 7748 Section 5.2, the two X25519 test vectors, copied by hand.
VECTORS = [
    (
        "a546e36bf0527c9d3b16154b82465edd62144c0ac1fc5a18506a2244ba449ac4",
        "e6db6867583030db3594c1a424b15f7c726624ec26b3353b10a903a6d0ab1c4c",
        "c3da55379de9c6908e94ea4df28d084f32eccf03491c71f754b4075577a28552",
    ),
    (
        "4b66e9d4d1b4673c5ad22691957d6af5c11b6421e0ea01d42ca4169e7918ba0d",
        "e5210f12786811d3f4b7959d0538ae2c31dbe7106fc03c3efc4cd549c715a493",
        "95cbde9476e8907d7aade45cb4b873f88b595a68799fa152e6f8f7647aac7957",
    ),
]

# RFC 7748 Section 5.2, the input values written in base 10 (copied by hand).
SCALAR_1_DEC = 31029842492115040904895560451863089656472772604678260265531221036453811406496
U_1_DEC = 34426434033919594451155107781188821651316167215306631574996226621102155684838
SCALAR_2_DEC = 35156891815674817266734212754503633747128614016119564763269015315466259359304
U_2_DEC = 8883857351183929894090759386610649319417338800022198945255395922347792736741

# RFC 7748 Section 5.2, the iterated test (k = u = 9 at the start).
ITER_1 = "422c8e7a6227d7bca1350b3e2bb7279f7897b87bb6854b783c60e80311ae3079"
ITER_1000 = "684cf59ba83309552800ef566f2f4d3c1c3887c49360e3875f2eb94d99532c51"
# The 1,000,000 iteration value of the RFC
# (7c3911e0ab2586fd864497297e575e6f3bc601c0883c30df5f4dd2d24f665424)
# takes hours in pure Python, so it is not run here.

# RFC 7748 Section 6.1, the Alice and Bob example.
ALICE_PRIV = "77076d0a7318a57d3c16c17251b26645df4c2f87ebc0992ab177fba51db92c2a"
ALICE_PUB = "8520f0098930a754748b7ddcb43ef75a0dbf3a0d26381af4eba4a98eaa9b4e6a"
BOB_PRIV = "5dab087e624a8a4b79e17f8b83800ee66f3bb1292618b6fd1c2f8b27ff88e0eb"
BOB_PUB = "de9edb7d7b7dc1b4d35b61c2ece435373f8343c85b78674dadfc7e146f882b4f"
SHARED = "4a5d9d5ba4ce2de1728e3bf480350f25e07e21c947d19e3376f09b3c1e161742"

# RFC 8448 Section 3 (TLS 1.3 traces, simple 1-RTT handshake): the client and
# server ephemeral X25519 key pairs and the (EC)DHE shared secret, which is the
# IKM of the "handshake" extract step.
TLS_CLIENT_PRIV = "49af42ba7f7994852d713ef2784bcbcaa7911de26adc5642cb634540e7ea5005"
TLS_CLIENT_PUB = "99381de560e4bd43d23d8e435a7dbafeb3c06e51c13cae4d5413691e529aaf2c"
TLS_SERVER_PRIV = "b1580eeadf6dd589b8ef4f2d5652578cc810e9980191ec8d058308cea216a21e"
TLS_SERVER_PUB = "c9828876112095fe66762bdbf7c672e156d6cc253b833df1dd69b1b04e751f0f"
TLS_SHARED = "8bd4054fb55b9d63fdfbacf9f04b9f0d35e6d63f537563efd46272900f89492d"


@pytest.mark.parametrize("k,u,out", VECTORS)
def test_rfc7748_section_5_2_vectors(k: str, u: str, out: str) -> None:
    assert x25519(H(k), H(u)).hex() == out


def test_rfc7748_decimal_forms() -> None:
    # The RFC gives the clamped scalar and the masked u-coordinate in base 10.
    assert decode_scalar(H(VECTORS[0][0])) == SCALAR_1_DEC
    assert decode_u_coordinate(H(VECTORS[0][1])) == U_1_DEC
    assert decode_scalar(H(VECTORS[1][0])) == SCALAR_2_DEC
    # The second u-coordinate has its top bit set; masking it gives the decimal value.
    assert H(VECTORS[1][1])[31] & 0x80
    assert decode_u_coordinate(H(VECTORS[1][1])) == U_2_DEC


def test_rfc7748_iterated_1_and_1000() -> None:
    k = u = (9).to_bytes(32, "little")
    for i in range(1, 1001):
        k, u = x25519(k, u), k
        if i == 1:
            assert k.hex() == ITER_1
    assert k.hex() == ITER_1000


def test_rfc7748_section_6_1_alice_and_bob() -> None:
    a, b = H(ALICE_PRIV), H(BOB_PRIV)
    assert public_key(a).hex() == ALICE_PUB
    assert public_key(b).hex() == BOB_PUB
    assert x25519_shared(a, H(BOB_PUB)).hex() == SHARED
    assert x25519_shared(b, H(ALICE_PUB)).hex() == SHARED


def test_rfc8448_tls13_trace() -> None:
    c, s = H(TLS_CLIENT_PRIV), H(TLS_SERVER_PRIV)
    assert public_key(c).hex() == TLS_CLIENT_PUB
    assert public_key(s).hex() == TLS_SERVER_PUB
    assert x25519_shared(c, H(TLS_SERVER_PUB)).hex() == TLS_SHARED
    assert x25519_shared(s, H(TLS_CLIENT_PUB)).hex() == TLS_SHARED


def test_random_agreement() -> None:
    rng = random.Random(7748)
    for _ in range(20):
        a = rng.randbytes(32)
        b = rng.randbytes(32)
        assert x25519(a, public_key(b)) == x25519(b, public_key(a))


def test_clamping() -> None:
    rng = random.Random(25519)
    for _ in range(200):
        k = decode_scalar(rng.randbytes(32))
        assert k % 8 == 0
        assert 2**254 <= k < 2**255
    # Two scalars that differ only in the clamped bits give the same output.
    k1 = bytes(32)
    k2 = bytes([7]) + bytes(30) + bytes([0xC0])
    u = public_key(H(ALICE_PRIV))
    assert x25519(k1, u) == x25519(k2, u)


def test_cswap() -> None:
    assert cswap(0, 5, 9) == (5, 9)
    assert cswap(1, 5, 9) == (9, 5)


def test_top_bit_of_u_is_ignored_and_non_canonical_u_is_reduced() -> None:
    k = H(ALICE_PRIV)
    u = bytearray(H(BOB_PUB))
    u_high = bytearray(u)
    u_high[31] |= 0x80
    assert x25519(k, bytes(u_high)) == x25519(k, bytes(u))
    # u + p fits in 255 bits for small u; it must act as u.
    small = 9
    assert x25519(k, (small + P).to_bytes(32, "little")) == x25519(k, small.to_bytes(32, "little"))


def _ladder_unclamped(n: int, u: int) -> tuple[int, int]:
    """[n](u:1) on the x-line, without clamping; returns (X:Z) projectively."""
    x2, z2, x3, z3, swap = 1, 0, u, 1, 0
    for t in range(n.bit_length() - 1, -1, -1):
        bit = (n >> t) & 1
        swap ^= bit
        x2, x3 = cswap(swap, x2, x3)
        z2, z3 = cswap(swap, z2, z3)
        swap = bit
        x2, z2, x3, z3 = ladder_step(u, x2, z2, x3, z3)
    x2, x3 = cswap(swap, x2, x3)
    z2, z3 = cswap(swap, z2, z3)
    return x2, z2


ORDER_8_U = [
    325606250916557431795983626356110631294008115727848805560023387167927233504,
    39382357235489614581723060781553021112529911719440698176882885853963445705823,
]


def test_small_order_points_give_all_zero() -> None:
    # u = 0 has order 2 and u = 1 has order 4; the two values below have order 8.
    for u in ORDER_8_U:
        assert _ladder_unclamped(8, u)[1] == 0
        assert _ladder_unclamped(4, u)[1] != 0
    assert _ladder_unclamped(2, 0)[1] == 0
    assert _ladder_unclamped(4, 1)[1] == 0 and _ladder_unclamped(2, 1)[1] != 0
    rng = random.Random(8)
    for u in [0, 1, *ORDER_8_U, P - 1, P, P + 1]:
        enc = u.to_bytes(32, "little")
        for _ in range(3):
            k = rng.randbytes(32)
            assert x25519(k, enc) == bytes(32)
            with pytest.raises(ValueError):
                x25519_shared(k, enc)


def test_twist_points_are_accepted() -> None:
    # u = 2: 8 + 4 * 486662 + 2 is not a square mod p, so u = 2 is on the twist.
    rhs = (2**3 + 486662 * 4 + 2) % P
    assert pow(rhs, (P - 1) // 2, P) == P - 1
    out = x25519(H(ALICE_PRIV), (2).to_bytes(32, "little"))
    assert len(out) == 32 and out != bytes(32)


def test_bad_lengths() -> None:
    with pytest.raises(ValueError):
        x25519(bytes(31), bytes(32))
    with pytest.raises(ValueError):
        x25519(bytes(32), bytes(33))
