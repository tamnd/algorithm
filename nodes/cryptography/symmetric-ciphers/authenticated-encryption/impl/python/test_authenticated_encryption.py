# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/authenticated-encryption/. The authors are listed in prov/NRR0YJ.jsonl.

import random

import pytest

from aes import AES
from authenticated_encryption import (
    InvalidCiphertext,
    cmac,
    eam_encrypt,
    etm_decrypt,
    etm_encrypt,
    mte_decrypt,
    mte_encrypt,
)

RNG = random.Random(2000)
KE, KM = RNG.randbytes(16), RNG.randbytes(16)


def test_aes_fips197_appendix_c1() -> None:
    # FIPS 197, Appendix C.1, AES-128.
    key = bytes(range(16))
    pt = bytes.fromhex("00112233445566778899aabbccddeeff")
    assert AES(key).encrypt_block(pt).hex() == "69c4e0d86a7b0430d8cdb78070b4c55a"


def test_cmac_rfc4493_examples() -> None:
    # RFC 4493, Section 4, Examples 1 and 2, to check the inline CMAC used as the MAC.
    key = bytes.fromhex("2b7e151628aed2a6abf7158809cf4f3c")
    assert cmac(key, b"").hex() == "bb1d6929e95937287fa37d129b756746"
    m = bytes.fromhex("6bc1bee22e409f96e93d7e117393172a")
    assert cmac(key, m).hex() == "070a16b46b4d4144f79bdd9dd04a287c"


@pytest.mark.parametrize("n", [0, 1, 15, 16, 17, 100])
def test_etm_round_trip(n: int) -> None:
    nonce, ad, p = RNG.randbytes(12), RNG.randbytes(n % 7), RNG.randbytes(n)
    ct = etm_encrypt(KE, KM, nonce, ad, p)
    assert len(ct) == n + 16
    assert etm_decrypt(KE, KM, nonce, ad, ct) == p


def test_etm_rejects_one_changed_bit_anywhere() -> None:
    nonce, ad, p = RNG.randbytes(12), b"header", RNG.randbytes(40)
    ct = etm_encrypt(KE, KM, nonce, ad, p)
    for bit in range(len(ct) * 8):
        bad = bytearray(ct)
        bad[bit // 8] ^= 1 << (bit % 8)
        with pytest.raises(InvalidCiphertext):
            etm_decrypt(KE, KM, nonce, ad, bytes(bad))
    for bit in range(len(ad) * 8):
        bad_ad = bytearray(ad)
        bad_ad[bit // 8] ^= 1 << (bit % 8)
        with pytest.raises(InvalidCiphertext):
            etm_decrypt(KE, KM, nonce, bytes(bad_ad), ct)
    for bit in range(96):
        bad_n = bytearray(nonce)
        bad_n[bit // 8] ^= 1 << (bit % 8)
        with pytest.raises(InvalidCiphertext):
            etm_decrypt(KE, KM, bytes(bad_n), ad, ct)


def test_etm_moving_bytes_between_ad_and_ciphertext_is_rejected() -> None:
    # The lengths at the end of the MAC input stop this shift.
    nonce = RNG.randbytes(12)
    ct = etm_encrypt(KE, KM, nonce, b"ab", b"cdef")
    c, t = ct[:-16], ct[-16:]
    with pytest.raises(InvalidCiphertext):
        etm_decrypt(KE, KM, nonce, b"ab" + c[:1], c[1:] + t)


def test_mac_then_encrypt_counterexample_breaks_int_ctxt() -> None:
    # Bellare and Namprempre: MtE with an IND-CPA scheme whose last byte is ignored. A changed
    # last byte gives a new ciphertext that decrypts to the same message, so INT-CTXT fails.
    nonce, p = RNG.randbytes(12), b"move 5 EUR"
    ct = mte_encrypt(KE, KM, nonce, p)
    forged = ct[:-1] + bytes([ct[-1] ^ 0x5A])
    assert forged != ct
    assert mte_decrypt(KE, KM, nonce, forged) == p


def test_mac_then_encrypt_counterexample_breaks_ind_cca() -> None:
    # The IND-CCA game: the adversary may not ask for the challenge ciphertext to be decrypted,
    # but it may ask for the changed one, which reveals the hidden bit every time.
    wins = 0
    for _ in range(20):
        b = RNG.randrange(2)
        m0, m1 = b"attack at dawn!!", b"attack at dusk!!"
        nonce = RNG.randbytes(12)
        challenge = mte_encrypt(KE, KM, nonce, (m0, m1)[b])

        def decryption_oracle(n: bytes, c: bytes) -> bytes:
            assert (n, c) != (nonce, challenge)
            return mte_decrypt(KE, KM, n, c)

        guess = int(decryption_oracle(nonce, challenge[:-1] + b"\x01") == m1)
        wins += guess == b
    assert wins == 20


def test_the_same_trick_fails_against_encrypt_then_mac() -> None:
    nonce = RNG.randbytes(12)
    ct = etm_encrypt(KE, KM, nonce, b"", b"move 5 EUR")
    with pytest.raises(InvalidCiphertext):
        etm_decrypt(KE, KM, nonce, b"", ct[:-1] + bytes([ct[-1] ^ 0x5A]))


def test_encrypt_and_mac_is_not_ind_cpa() -> None:
    # The tag CMAC(km, P) is deterministic, so equal plaintexts give equal tags even under fresh
    # nonces. The adversary asks for E(m0), then the challenge on (m0, m1), and compares tags.
    wins = 0
    for _ in range(20):
        b = RNG.randrange(2)
        m0, m1 = b"yes", b"no!"
        seen = eam_encrypt(KE, KM, RNG.randbytes(12), m0)
        challenge = eam_encrypt(KE, KM, RNG.randbytes(12), (m0, m1)[b])
        guess = 0 if challenge[-16:] == seen[-16:] else 1
        wins += guess == b
    assert wins == 20


def test_etm_tags_differ_for_equal_plaintexts() -> None:
    a = etm_encrypt(KE, KM, RNG.randbytes(12), b"", b"yes")
    b = etm_encrypt(KE, KM, RNG.randbytes(12), b"", b"yes")
    assert a[-16:] != b[-16:]
