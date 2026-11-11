# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/rsa-pkcs1-v1-5-encryption/. The authors are listed in prov/GMTEEK.jsonl.

import random

import pytest
from rsa_pkcs1_v1_5_encryption import (
    DecryptionError,
    SimulatedOracle,
    bleichenbacher_attack,
    decrypt,
    eme_pkcs1_v1_5_decode,
    eme_pkcs1_v1_5_encode,
    encrypt,
    i2osp,
    nonzero_from_random,
    os2ip,
    toy_key,
)

# Toy primes of 125 binary digits each, drawn once with random.Random(424242)
# and a Miller-Rabin test. The product has 249 binary digits, so the modulus
# is 32 octets long and sits a little above the byte boundary: n / B = 387.
# A conforming value is then about 387 times more common than for a byte
# aligned modulus, so Bleichenbacher's attack below needs about a thousand
# queries instead of about a million. The key is far too small for real use.
P = 20049945685769410886995031361227698861
Q = 34144336936972862972314898450181336227
KEY = toy_key(P, Q)


def padder(seed: int):
    rnd = random.Random(seed)
    return lambda count: nonzero_from_random(rnd, count)


def test_toy_key_shape() -> None:
    assert KEY.n.bit_length() == 249
    assert KEY.k == 32
    assert KEY.n >> (8 * (KEY.k - 2)) == 387
    assert KEY.e * KEY.d % ((P - 1) * (Q - 1) // 2) == 1


def test_encoding_follows_rfc_8017_section_7_2_1() -> None:
    message = b"toy key"
    em = eme_pkcs1_v1_5_encode(message, 32, padder(1))
    assert len(em) == 32
    assert em[0] == 0x00 and em[1] == 0x02
    ps = em[2:32 - len(message) - 1]
    assert len(ps) == 32 - len(message) - 3
    assert len(ps) >= 8
    assert 0 not in ps
    assert em[32 - len(message) - 1] == 0x00
    assert em[32 - len(message):] == message
    assert eme_pkcs1_v1_5_decode(em) == message


def test_longest_and_shortest_messages() -> None:
    longest = bytes(range(1, 22))  # k - 11 = 21 octets
    em = eme_pkcs1_v1_5_encode(longest, 32, padder(2))
    assert len(em) == 32
    assert eme_pkcs1_v1_5_decode(em) == longest
    empty = eme_pkcs1_v1_5_encode(b"", 32, padder(3))
    assert eme_pkcs1_v1_5_decode(empty) == b""
    with pytest.raises(ValueError):
        eme_pkcs1_v1_5_encode(bytes(22), 32, padder(4))


def test_round_trip_on_random_messages() -> None:
    rnd = random.Random(5)
    pad = lambda count: nonzero_from_random(rnd, count)
    for _ in range(100):
        length = rnd.randrange(0, 22)
        message = bytes(rnd.randrange(256) for _ in range(length))
        ciphertext = encrypt(KEY.n, KEY.e, message, pad)
        assert len(ciphertext) == KEY.k
        assert decrypt(KEY.n, KEY.d, ciphertext) == message


def test_encryption_is_randomized() -> None:
    pad = padder(6)
    message = b"same message"
    seen = {encrypt(KEY.n, KEY.e, message, pad) for _ in range(50)}
    assert len(seen) == 50


def test_decode_rejects_bad_encodings() -> None:
    bad = [
        b"\x00\x01" + b"\xaa" * 26 + b"\x00" + b"msg",       # wrong second octet
        b"\x01\x02" + b"\xaa" * 26 + b"\x00" + b"msg",       # wrong first octet
        b"\x00\x02" + b"\xaa" * 29 + b"\x01",                # no zero separator
        b"\x00\x02" + b"\xaa" * 6 + b"\x00" + b"\xbb" * 23,  # padding below 8 octets
    ]
    for em in bad:
        assert len(em) == 32
        with pytest.raises(DecryptionError):
            eme_pkcs1_v1_5_decode(em)


def test_decrypt_rejects_wrong_length_and_random_ciphertexts() -> None:
    with pytest.raises(DecryptionError):
        decrypt(KEY.n, KEY.d, b"\x00" * 31)
    rnd = random.Random(7)
    failures = 0
    for _ in range(40):
        ciphertext = i2osp(rnd.randrange(KEY.n), KEY.k)
        try:
            decrypt(KEY.n, KEY.d, ciphertext)
        except DecryptionError:
            failures += 1
    assert failures == 40  # a random ciphertext almost never has valid padding


def test_bleichenbacher_attack_recovers_the_message() -> None:
    """The million message attack, on a toy key and a local oracle."""
    message = b"toy key"
    ciphertext = encrypt(KEY.n, KEY.e, message, padder(8))
    oracle = SimulatedOracle(n=KEY.n, d=KEY.d)
    trace = []
    recovered = bleichenbacher_attack(KEY.n, KEY.e, ciphertext, oracle, trace)
    assert recovered == i2osp(pow(os2ip(ciphertext), KEY.d, KEY.n), KEY.k)
    assert eme_pkcs1_v1_5_decode(recovered) == message
    assert oracle.queries < 4000
    widths = [width for _, _, _, width in trace]
    assert widths == sorted(widths, reverse=True)  # the interval never grows
    assert widths[-1] == 1


def test_a_stricter_oracle_answers_yes_less_often() -> None:
    """The weak oracle needs only the 0x00 0x02 prefix, so it says yes more often.

    The attack works with either answer, because both imply 2B <= m < 3B. A
    stricter server slows the attack down but does not stop it.
    """
    weak = SimulatedOracle(n=KEY.n, d=KEY.d)
    strict = SimulatedOracle(n=KEY.n, d=KEY.d, strict=True)
    ciphertext = os2ip(encrypt(KEY.n, KEY.e, b"toy key", padder(9)))
    assert weak(ciphertext) and strict(ciphertext)
    weak_yes = strict_yes = 0
    for s in range(2, 400):
        probe = ciphertext * pow(s, KEY.e, KEY.n) % KEY.n
        weak_yes += weak(probe)
        strict_yes += strict(probe)
    assert weak_yes >= strict_yes
    assert weak_yes >= 1  # the weak oracle says yes about once every 387 probes


def test_attack_needs_a_conforming_ciphertext() -> None:
    oracle = SimulatedOracle(n=KEY.n, d=KEY.d)
    with pytest.raises(ValueError):
        bleichenbacher_attack(KEY.n, KEY.e, i2osp(2, KEY.k), oracle, None)
