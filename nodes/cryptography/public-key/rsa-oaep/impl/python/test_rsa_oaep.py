# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/rsa-oaep/. The authors are listed in prov/60YSZW.jsonl.

import hashlib
import math
import random

import pytest
from rsa_oaep import (
    DecryptionError,
    decrypt,
    eme_oaep_decode,
    eme_oaep_encode,
    encrypt,
    max_message_length,
    mgf1,
    os2ip,
)

# Official test vectors: PKCS #1 v2.1 test vector file oaep-vect.txt, from the
# archive pkcs-1v2-1-vec.zip of RSA Laboratories. Key 1 has 1024 binary digits,
# the hash and the mask generation function are SHA-1, and the label is empty.
N = os2ip(bytes.fromhex(
    "a8b3b284af8eb50b387034a860f146c4919f318763cd6c5598c8ae4811a1e0ab"
    "c4c7e0b082d693a5e7fced675cf4668512772c0cbc64a742c6c630f533c8cc72"
    "f62ae833c40bf25842e984bb78bdbf97c0107d55bdb662f5c4e0fab9845cb514"
    "8ef7392dd3aaff93ae1e6b667bb3d4247616d4f5ba10d4cfd226de88d39f16fb"))
E = 0x010001
D = os2ip(bytes.fromhex(
    "53339cfdb79fc8466a655c7316aca85c55fd8f6dd898fdaf119517ef4f52e8fd"
    "8e258df93fee180fa0e4ab29693cd83b152a553d4ac4d1812b8b9fa5af0e7f55"
    "fe7304df41570926f3311f15c4d65a732c483116ee3d3d2d0af3549ad9bf7cbf"
    "b78ad884f84d5beb04724dc7369b31def37d0cf539e9cfcdd3de653729ead5d1"))
P = os2ip(bytes.fromhex(
    "d32737e7267ffe1341b2d5c0d150a81b586fb3132bed2f8d5262864a9cb9f30a"
    "f38be448598d413a172efb802c21acf1c11c520c2f26a471dcad212eac7ca39d"))
Q = os2ip(bytes.fromhex(
    "cc8853d1d54da630fac004f471f281c7b8982d8224a490edbeb33d3e3d5cc93c"
    "4765703d1dd791642f1f116a0dd852be2419b2af72bfe9a030e860b0288b5d77"))

# Example 1.1 of the same file.
VECTOR_1_1 = {
    "message": "6628194e12073db03ba94cda9ef9532397d50dba79b987004afefe34",
    "seed": "18b776ea21069d69776a33e96bad48e1dda0a5ef",
    "ciphertext": (
        "354fe67b4a126d5d35fe36c777791a3f7ba13def484e2d3908aff722fad468fb"
        "21696de95d0be911c2d3174f8afcc201035f7b6d8e69402de5451618c21a535f"
        "a9d7bfc5b8dd9fc243f8cf927db31322d6e881eaa91a996170e657a05a266426"
        "d98c88003f8477c1227094a0d9fa1e8c4024309ce1ecccb5210035d47ac72e8a"),
}

# Example 1.2 of the same file.
VECTOR_1_2 = {
    "message": "750c4047f547e8e41411856523298ac9bae245efaf1397fbe56f9dd5",
    "seed": "0cc742ce4a9b7f32f951bcb251efd925fe4fe35f",
    "ciphertext": (
        "640db1acc58e0568fe5407e5f9b701dff8c3c91e716c536fc7fcec6cb5b71c11"
        "65988d4a279e1577d730fc7a29932e3f00c81515236d8d8e31017a7a09df4352"
        "d904cdeb79aa583adcc31ea698a4c05283daba9089be5491f67c1a4ee48dc74b"
        "bbe6643aef846679b4cb395a352d5ed115912df696ffe0702932946d71492b44"),
}


def test_the_vector_key_is_consistent() -> None:
    assert N.bit_length() == 1024
    assert P * Q == N
    lam = (P - 1) * (Q - 1) // math.gcd(P - 1, Q - 1)
    assert pow(E, -1, lam) == D
    assert E * D % lam == 1


@pytest.mark.parametrize("vector", [VECTOR_1_1, VECTOR_1_2])
def test_official_oaep_vectors_sha1(vector) -> None:
    """Encryption with the given seed gives the given ciphertext."""
    message = bytes.fromhex(vector["message"])
    seed = bytes.fromhex(vector["seed"])
    expected = bytes.fromhex(vector["ciphertext"])
    got = encrypt(N, E, message, b"", "sha1", seed)
    assert got == expected
    assert decrypt(N, D, expected, b"", "sha1") == message


def test_encoding_shape_of_vector_1_1() -> None:
    """EM = 0x00 || maskedSeed || maskedDB, and DB starts with the label hash."""
    message = bytes.fromhex(VECTOR_1_1["message"])
    em = eme_oaep_encode(message, 128, b"", "sha1", bytes.fromhex(VECTOR_1_1["seed"]))
    assert len(em) == 128
    assert em[0] == 0x00
    assert eme_oaep_decode(em, b"", "sha1") == message
    assert max_message_length(N, "sha1") == 128 - 40 - 2


def test_mgf1_length_and_prefix_property() -> None:
    """A longer mask starts with the shorter mask, because the counter grows."""
    seed = b"seed for the mask"
    short = mgf1(seed, 20, "sha1")
    long = mgf1(seed, 100, "sha1")
    assert len(short) == 20 and len(long) == 100
    assert long.startswith(short)
    assert long[:20] == hashlib.sha1(seed + b"\x00\x00\x00\x00").digest()
    assert long[20:40] == hashlib.sha1(seed + b"\x00\x00\x00\x01").digest()
    assert mgf1(seed, 32, "sha256")[:32] == hashlib.sha256(seed + b"\x00\x00\x00\x00").digest()


def test_round_trip_with_sha256_and_a_label() -> None:
    """No official vector uses SHA-256, so this is a round trip check only."""
    rnd = random.Random(11)
    limit = max_message_length(N, "sha256")
    assert limit == 128 - 64 - 2
    for _ in range(20):
        length = rnd.randrange(0, limit + 1)
        message = bytes(rnd.randrange(256) for _ in range(length))
        label = bytes(rnd.randrange(256) for _ in range(rnd.randrange(0, 8)))
        seed = bytes(rnd.randrange(256) for _ in range(32))
        ciphertext = encrypt(N, E, message, label, "sha256", seed)
        assert decrypt(N, D, ciphertext, label, "sha256") == message


def test_encryption_is_randomized() -> None:
    message = b"the same message twice"
    seen = {encrypt(N, E, message, b"", "sha1") for _ in range(20)}
    assert len(seen) == 20


def test_the_wrong_label_fails() -> None:
    ciphertext = encrypt(N, E, b"bound to a label", b"label A", "sha1")
    assert decrypt(N, D, ciphertext, b"label A", "sha1") == b"bound to a label"
    with pytest.raises(DecryptionError):
        decrypt(N, D, ciphertext, b"label B", "sha1")


def test_the_wrong_hash_fails() -> None:
    ciphertext = encrypt(N, E, b"hash agility", b"", "sha1")
    with pytest.raises(DecryptionError):
        decrypt(N, D, ciphertext, b"", "sha256")


def test_a_changed_ciphertext_fails() -> None:
    """One flipped octet gives a decryption error, not a changed message."""
    rnd = random.Random(12)
    ciphertext = bytearray(encrypt(N, E, b"integrity", b"", "sha1"))
    failures = 0
    for _ in range(20):
        copy = bytearray(ciphertext)
        index = rnd.randrange(1, len(copy))
        copy[index] ^= 1 << rnd.randrange(8)
        try:
            decrypt(N, D, bytes(copy), b"", "sha1")
        except DecryptionError:
            failures += 1
    assert failures == 20


def test_too_long_messages_and_short_moduli_are_rejected() -> None:
    with pytest.raises(ValueError):
        encrypt(N, E, bytes(max_message_length(N, "sha1") + 1), b"", "sha1")
    with pytest.raises(ValueError):
        eme_oaep_encode(b"", 41, b"", "sha1")  # k < 2hLen + 2
    with pytest.raises(DecryptionError):
        decrypt(N, D, bytes(127), b"", "sha1")  # wrong ciphertext length


def test_decode_rejects_the_three_failures() -> None:
    """A nonzero first octet, a wrong label hash and a missing 0x01 all fail."""
    message = b"three ways to fail"
    good = bytearray(eme_oaep_encode(message, 128, b"", "sha1", bytes(20)))
    assert eme_oaep_decode(bytes(good), b"", "sha1") == message
    with_y = bytearray(good)
    with_y[0] = 1
    for broken in (with_y, bytearray(good[:1] + good[1:21] + bytes(107)),
                   bytearray(good[:-1] + bytes([good[-1] ^ 0xff]))):
        with pytest.raises(DecryptionError):
            eme_oaep_decode(bytes(broken), b"", "sha1")
