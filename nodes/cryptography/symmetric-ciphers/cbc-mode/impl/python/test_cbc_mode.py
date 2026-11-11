# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cbc-mode/. The authors are listed in prov/AAD84Q.jsonl.

import random

import pytest

from aes import AES
from cbc_mode import cbc_decrypt, cbc_encrypt, pkcs7_pad, pkcs7_unpad

KEY = bytes.fromhex("2b7e151628aed2a6abf7158809cf4f3c")
IV = bytes.fromhex("000102030405060708090a0b0c0d0e0f")
PT = bytes.fromhex(
    "6bc1bee22e409f96e93d7e117393172a"
    "ae2d8a571e03ac9c9eb76fac45af8e51"
    "30c81c46a35ce411e5fbc1191a0a52ef"
    "f69f2445df4f9b17ad2b417be66c3710"
)


def rand_bytes(rng: random.Random, n: int) -> bytes:
    return bytes(rng.randrange(256) for _ in range(n))


def test_aes_fips197_appendix_c() -> None:
    # FIPS 197, Appendix C.1 (AES-128).
    a = AES(bytes.fromhex("000102030405060708090a0b0c0d0e0f"))
    assert a.encrypt_block(bytes.fromhex("00112233445566778899aabbccddeeff")).hex() == "69c4e0d86a7b0430d8cdb78070b4c55a"


def test_sp800_38a_f21_f22_cbc_aes128() -> None:
    # SP 800-38A, Appendix F.2.1 (CBC-AES128.Encrypt) and F.2.2 (CBC-AES128.Decrypt).
    ct = bytes.fromhex(
        "7649abac8119b246cee98e9b12e9197d"
        "5086cb9b507219ee95db113a917678b2"
        "73bed6b8e3c1743b7116e69e22229516"
        "3ff1caa1681fac09120eca307586e1a7"
    )
    a = AES(KEY)
    assert cbc_encrypt(a, IV, PT) == ct
    assert cbc_decrypt(a, IV, ct) == PT


def test_round_trip_and_errors() -> None:
    rng = random.Random(11)
    a = AES(rand_bytes(rng, 16))
    for n in range(0, 50, 7):
        iv, p = rand_bytes(rng, 16), rand_bytes(rng, n)
        assert pkcs7_unpad(cbc_decrypt(a, iv, cbc_encrypt(a, iv, pkcs7_pad(p)))) == p
    with pytest.raises(ValueError):
        cbc_encrypt(a, bytes(15), bytes(16))
    with pytest.raises(ValueError):
        cbc_decrypt(a, bytes(16), bytes(17))


def test_random_iv_hides_repeats() -> None:
    rng = random.Random(5)
    a = AES(KEY)
    p = bytes(64)
    c1 = cbc_encrypt(a, rand_bytes(rng, 16), p)
    c2 = cbc_encrypt(a, rand_bytes(rng, 16), p)
    assert c1 != c2
    assert len({c1[i : i + 16] for i in range(0, 64, 16)}) == 4


def test_bit_flip_propagation() -> None:
    # A flip in C[1] garbles P[1] and flips the same bit of P[2]; P[3] and P[4] are intact.
    a = AES(KEY)
    c = bytearray(cbc_encrypt(a, IV, PT))
    c[5] ^= 0x10
    p = cbc_decrypt(a, IV, bytes(c))
    assert p[:16] != PT[:16]
    assert p[16:32] == PT[16:21] + bytes([PT[21] ^ 0x10]) + PT[22:32]
    assert p[32:] == PT[32:]


def test_predictable_iv_attack() -> None:
    # TLS 1.0 style chaining: the IV of a record is the last ciphertext block of the previous one.
    a = AES(bytes(range(16)))
    state = {"iv": IV}

    def encrypt_record(p: bytes) -> tuple[bytes, bytes]:
        iv = state["iv"]
        c = cbc_encrypt(a, iv, p)
        state["iv"] = c[-16:]
        return iv, c

    secret = b"vote: candidate2"
    iv_v, c_v = encrypt_record(secret)  # the victim record; the attacker sees iv_v and c_v
    found = None
    for guess in (b"vote: candidate1", b"vote: candidate2", b"vote: candidate3"):
        next_iv = state["iv"]  # predictable: it is the last block on the wire
        probe = bytes(x ^ y ^ z for x, y, z in zip(next_iv, iv_v, guess))
        _, c = encrypt_record(probe)
        if c[:16] == c_v[:16]:
            found = guess
    assert found == secret


def padding_oracle_attack(oracle, iv: bytes, ct: bytes) -> bytes:
    """Vaudenay's attack: recover the padded plaintext from a padding oracle only."""
    blocks = [iv] + [ct[i : i + 16] for i in range(0, len(ct), 16)]
    out = bytearray()
    for prev, cur in zip(blocks, blocks[1:]):
        inter = bytearray(16)  # inter = D_K(cur), found byte by byte from the right
        for pos in range(15, -1, -1):
            pad = 16 - pos
            for g in range(256):
                forged = bytearray(16)
                for j in range(pos + 1, 16):
                    forged[j] = inter[j] ^ pad
                forged[pos] = g
                if not oracle(bytes(forged) + cur):
                    continue
                if pos == 15:  # rule out a valid pad of 02 02 (or longer) by chance
                    forged[14] ^= 0xFF
                    if not oracle(bytes(forged) + cur):
                        continue
                inter[pos] = g ^ pad
                break
            else:
                raise AssertionError("no valid padding found")
        out += bytes(x ^ y for x, y in zip(inter, prev))
    return bytes(out)


def test_padding_oracle_recovers_plaintext() -> None:
    rng = random.Random(2002)
    key = rand_bytes(rng, 16)
    a = AES(key)
    calls = [0]

    def oracle(data: bytes) -> bool:  # the local server: decrypt, then report only padding validity
        calls[0] += 1
        try:
            pkcs7_unpad(cbc_decrypt(a, data[:16], data[16:]))
            return True
        except ValueError:
            return False

    secret = b"PIN=4921; meet at gate 7"
    iv = rand_bytes(rng, 16)
    ct = cbc_encrypt(a, iv, pkcs7_pad(secret))
    recovered = padding_oracle_attack(oracle, iv, ct)
    assert pkcs7_unpad(recovered) == secret
    assert calls[0] <= 256 * 32 + 8  # at most 256 guesses per byte, plus a few checks


def test_pkcs7_strict() -> None:
    assert pkcs7_pad(b"") == bytes([16]) * 16
    assert pkcs7_unpad(b"A" * 15 + b"\x01") == b"A" * 15
    for bad in (b"A" * 15 + b"\x00", b"A" * 14 + b"\x01\x02", b"A" * 15 + b"\x11", b"A" * 16):
        with pytest.raises(ValueError):
            pkcs7_unpad(bad)
