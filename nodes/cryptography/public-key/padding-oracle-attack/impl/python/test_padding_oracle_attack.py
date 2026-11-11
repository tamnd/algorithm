# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/padding-oracle-attack/. The authors are listed in prov/88GNSJ.jsonl.

import random

import pytest
from padding_oracle_attack import (
    BLOCK,
    PaddingError,
    PaddingOracleServer,
    SafeServer,
    attack,
    cbc_decrypt,
    cbc_encrypt,
    pkcs7_pad,
    pkcs7_unpad,
    recover_decrypted_block,
)

# Official vector: NIST SP 800-38A, Appendix F.2.1, CBC-AES128.Encrypt.
NIST_KEY = bytes.fromhex("2b7e151628aed2a6abf7158809cf4f3c")
NIST_IV = bytes.fromhex("000102030405060708090a0b0c0d0e0f")
NIST_PLAINTEXT = bytes.fromhex(
    "6bc1bee22e409f96e93d7e117393172a"
    "ae2d8a571e03ac9c9eb76fac45af8e51"
    "30c81c46a35ce411e5fbc1191a0a52ef"
    "f69f2445df4f9b17ad2b417be66c3710")
NIST_CIPHERTEXT = bytes.fromhex(
    "7649abac8119b246cee98e9b12e9197d"
    "5086cb9b507219ee95db113a917678b2"
    "73bed6b8e3c1743b7116e69e22229516"
    "3ff1caa1681fac09120eca307586e1a7")

KEY = bytes.fromhex("00112233445566778899aabbccddeeff")
IV = bytes.fromhex("0f0e0d0c0b0a09080706050403020100")


def test_cbc_matches_the_nist_vector() -> None:
    """The four blocks of SP 800-38A F.2.1, with the padding block dropped."""
    out = cbc_encrypt(NIST_KEY, NIST_IV, NIST_PLAINTEXT)
    assert out[:BLOCK] == NIST_IV
    assert out[BLOCK:BLOCK + len(NIST_CIPHERTEXT)] == NIST_CIPHERTEXT
    assert cbc_decrypt(NIST_KEY, out) == NIST_PLAINTEXT


def test_pkcs7_padding_round_trip_and_rejections() -> None:
    for length in range(0, 33):
        data = bytes(range(length))
        padded = pkcs7_pad(data)
        assert len(padded) % BLOCK == 0 and len(padded) > length
        assert pkcs7_unpad(padded) == data
    for bad in [bytes(16), bytes(15) + bytes([17]), bytes([2]) * 15 + bytes([3]), b""]:
        with pytest.raises(PaddingError):
            pkcs7_unpad(bad)


def test_cbc_round_trip_on_random_messages() -> None:
    rnd = random.Random(31)
    for _ in range(40):
        message = bytes(rnd.randrange(256) for _ in range(rnd.randrange(0, 40)))
        iv = bytes(rnd.randrange(256) for _ in range(BLOCK))
        assert cbc_decrypt(KEY, cbc_encrypt(KEY, iv, message)) == message


def test_the_attack_recovers_the_plaintext() -> None:
    """Vaudenay's attack, against the local simulated server."""
    secret = b"attack at dawn, bring 32 bytes!!"  # two blocks, so padding is a third
    ciphertext = cbc_encrypt(KEY, IV, secret)
    server = PaddingOracleServer(key=KEY)
    assert attack(server, ciphertext) == secret
    # Three ciphertext blocks of 16 octets: at most 256 queries for each of
    # the 48 positions, and about 128 on average.
    assert server.queries <= 48 * 256 + 48
    assert server.queries >= 48


def test_the_attack_works_for_every_padding_length() -> None:
    """The confirmation step handles the last octet, whatever the real padding is."""
    for length in (1, 16, 17):
        secret = bytes([0x02]) * length  # a plaintext that looks like padding
        ciphertext = cbc_encrypt(KEY, IV, secret)
        server = PaddingOracleServer(key=KEY)
        assert attack(server, ciphertext) == secret


def test_recover_decrypted_block_gives_the_block_cipher_output() -> None:
    """D(block) XOR the previous ciphertext block is the plaintext block."""
    secret = b"one block only!!"
    ciphertext = cbc_encrypt(KEY, IV, secret)
    server = PaddingOracleServer(key=KEY)
    decrypted = recover_decrypted_block(server, ciphertext[BLOCK:2 * BLOCK])
    assert bytes(a ^ b for a, b in zip(decrypted, IV)) == secret


def test_encrypt_then_mac_stops_the_attack() -> None:
    """With the MAC checked first, the bit no longer depends on the padding."""
    server = SafeServer(key=KEY, mac_key=b"mac key for the toy server")
    sealed = server.seal(IV, b"attack at dawn")
    assert server(sealed) is True
    body = bytearray(sealed)
    body[BLOCK] ^= 1
    assert server(bytes(body)) is False
    with pytest.raises(RuntimeError):
        recover_decrypted_block(server, sealed[BLOCK:2 * BLOCK])


def test_the_attacker_never_uses_the_key() -> None:
    """The attack function takes the oracle and the ciphertext, and nothing else."""
    import inspect
    source = inspect.getsource(attack) + inspect.getsource(recover_decrypted_block)
    assert "key" not in source.replace("key and no plaintext", "")
