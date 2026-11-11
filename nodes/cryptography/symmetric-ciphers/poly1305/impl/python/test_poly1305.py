# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/poly1305/. The authors are listed in prov/T94CVM.jsonl.

import random

import pytest

from poly1305 import CLAMP, P, clamp, poly1305_mac, poly1305_verify

IETF_TEXT = (
    b"Any submission to the IETF intended by the Contributor for publication as all or part of an "
    b"IETF Internet-Draft or RFC and any statement made within the context of an IETF activity is "
    b'considered an "IETF Contribution". Such statements include oral statements in IETF sessions, '
    b"as well as written and electronic communications made at any time or place, which are addressed to"
)
JABBERWOCKY = (
    b"'Twas brillig, and the slithy toves\nDid gyre and gimble in the wabe:\n"
    b"All mimsy were the borogoves,\nAnd the mome raths outgrabe."
)


def test_rfc8439_section_2_5_2() -> None:
    # RFC 8439, Section 2.5.2, "Poly1305 Example and Test Vector".
    key = bytes.fromhex("85d6be7857556d337f4452fe42d506a80103808afb0db2fd4abff6af4149f51b")
    msg = b"Cryptographic Forum Research Group"
    assert clamp(int.from_bytes(key[:16], "little")) == 0x806D5400E52447C036D555408BED685
    assert int.from_bytes(key[16:], "little") == 0x1BF54941AFF6BF4AFDB20DFB8A800301
    assert poly1305_mac(key, msg).hex() == "a8061dc1305136c6c22b8baf0c0127a9"


@pytest.mark.parametrize(
    "key, msg, tag",
    [
        # RFC 8439, Appendix A.3, Test Vectors #1 to #4.
        ("00" * 32, "00" * 64, "00" * 16),
        ("00" * 16 + "36e5f6b5c5e06070f0efca96227a863e", IETF_TEXT.hex(), "36e5f6b5c5e06070f0efca96227a863e"),
        ("36e5f6b5c5e06070f0efca96227a863e" + "00" * 16, IETF_TEXT.hex(), "f3477e7cd95417af89a6b8794c310cf0"),
        (
            "1c9240a5eb55d38af333888604f6b5f0473917c1402b80099dca5cbc207075c0",
            JABBERWOCKY.hex(),
            "4541669a7eaaee61e708dc7cbcc5eb62",
        ),
        # Appendix A.3, Test Vectors #5 to #11 (key = R || S), the reduction edge cases.
        ("02" + "00" * 31, "ff" * 16, "03" + "00" * 15),
        ("02" + "00" * 15 + "ff" * 16, "02" + "00" * 15, "03" + "00" * 15),
        ("01" + "00" * 31, "ff" * 16 + "f0" + "ff" * 15 + "11" + "00" * 15, "05" + "00" * 15),
        ("01" + "00" * 31, "ff" * 16 + "fb" + "fe" * 15 + "01" * 16, "00" * 16),
        ("02" + "00" * 31, "fd" + "ff" * 15, "fa" + "ff" * 15),
        (
            "01" + "00" * 7 + "04" + "00" * 7 + "00" * 16,
            "e33594d7505e43b900000000000000003394d7505e4379cd01000000000000000000000000000000000000000000000001000000000000000000000000000000",
            "14000000000000005500000000000000",
        ),
        (
            "01" + "00" * 7 + "04" + "00" * 7 + "00" * 16,
            "e33594d7505e43b900000000000000003394d7505e4379cd010000000000000000000000000000000000000000000000",
            "13000000000000000000000000000000",
        ),
    ],
)
def test_rfc8439_appendix_a3(key: str, msg: str, tag: str) -> None:
    assert len(IETF_TEXT) == 375 and len(JABBERWOCKY) == 127
    assert poly1305_mac(bytes.fromhex(key), bytes.fromhex(msg)).hex() == tag


def test_clamp_mask() -> None:
    # Bytes 3, 7, 11, 15 keep only the low 4 bits; bytes 4, 8, 12 lose the low 2 bits.
    m = CLAMP.to_bytes(16, "little")
    assert [m[i] for i in (3, 7, 11, 15)] == [0x0F] * 4
    assert [m[i] for i in (4, 8, 12)] == [0xFC] * 3
    assert bin(CLAMP).count("1") == 106


def test_one_changed_bit_is_rejected() -> None:
    rng = random.Random(8439)
    key = rng.randbytes(32)
    msg = rng.randbytes(100)
    t = poly1305_mac(key, msg)
    assert poly1305_verify(key, msg, t)
    for bit in range(0, 800, 11):
        m2 = bytearray(msg)
        m2[bit // 8] ^= 1 << (bit % 8)
        assert not poly1305_verify(key, bytes(m2), t)
    for bit in range(128):
        t2 = bytearray(t)
        t2[bit // 8] ^= 1 << (bit % 8)
        assert not poly1305_verify(key, msg, bytes(t2))


def recover_key_from_two_tags(m1: bytes, t1: bytes, m2: bytes, t2: bytes) -> list[tuple[int, int]]:
    """The attack: two 16-byte messages tagged under one key (r, s) give r and s.

    With c = LE(m || 01) and a = c * r mod p, the tag is (a + s) mod 2^128. So
    a1 - a2 = (t1 - t2) + j * 2^128 for some j with |j| <= 4, and r = (a1 - a2) / (c1 - c2) mod p.
    """
    c1 = int.from_bytes(m1 + b"\x01", "little")
    c2 = int.from_bytes(m2 + b"\x01", "little")
    T1, T2 = int.from_bytes(t1, "little"), int.from_bytes(t2, "little")
    inv = pow((c1 - c2) % P, -1, P)
    found = []
    for j in range(-4, 5):
        r = (T1 - T2 + j * (1 << 128)) * inv % P
        if clamp(r) != r:  # a real r passed the clamp, so it has 106 free bits only
            continue
        s = (T1 - c1 * r % P) % (1 << 128)
        if (c2 * r % P + s) % (1 << 128) == T2:
            found.append((r, s))
    return found


def test_key_reuse_lets_an_attacker_forge() -> None:
    rng = random.Random(2005)
    for _ in range(50):
        key = rng.randbytes(32)  # used twice: the mistake
        m1, m2 = b"transfer 100 EUR", b"transfer 200 EUR"
        t1, t2 = poly1305_mac(key, m1), poly1305_mac(key, m2)
        candidates = recover_key_from_two_tags(m1, t1, m2, t2)
        r_true = clamp(int.from_bytes(key[:16], "little"))
        s_true = int.from_bytes(key[16:], "little")
        assert (r_true, s_true) in candidates and len(candidates) <= 9
        # These two messages differ in one byte, so c1 - c2 = -2^72 and the candidates for
        # different j differ by multiples of 2^56; several can pass the clamp. The attacker
        # sends one forgery per candidate, at most 9 tries, and one of them is accepted.
        target = b"transfer 999999 EUR to the attacker, approved"
        tries = [poly1305_mac(r.to_bytes(16, "little") + s.to_bytes(16, "little"), target) for r, s in candidates]
        assert any(poly1305_verify(key, target, t) for t in tries)


def test_key_reuse_random_messages_give_one_candidate() -> None:
    # For unstructured messages a false candidate passes the clamp with probability about 2^-24.
    rng = random.Random(613)
    for _ in range(50):
        key = rng.randbytes(32)
        m1, m2 = rng.randbytes(16), rng.randbytes(16)
        candidates = recover_key_from_two_tags(m1, poly1305_mac(key, m1), m2, poly1305_mac(key, m2))
        assert len(candidates) == 1
        r, s = candidates[0]
        forged_key = r.to_bytes(16, "little") + s.to_bytes(16, "little")
        target = rng.randbytes(77)
        assert poly1305_verify(key, target, poly1305_mac(forged_key, target))


def test_weak_key_r_zero() -> None:
    # Appendix A.3 notes that r = 0 makes the tag equal to s for every message.
    key = bytes(16) + bytes(range(16))
    assert poly1305_mac(key, b"a") == poly1305_mac(key, b"b") == bytes(range(16))


def test_p_is_2_130_minus_5() -> None:
    assert P == 0x3FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFB
    # A Fermat test as a sanity check (Bernstein proves primality with Pocklington's theorem).
    for a in (2, 3, 5, 7, 11):
        assert pow(a, P - 1, P) == 1
