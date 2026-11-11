# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/blum-goldwasser-cryptosystem/. The authors are listed in prov/QJYEG7.jsonl.
"""Tests for Blum-Goldwasser encryption.

There is no official test vector for this scheme. The first test checks
Handbook of Applied Cryptography Example 8.57, with the seed fixed. The
larger key uses the primes 2^31 - 1 and 2^61 - 1, both congruent to 3 mod 4.
"""

import random

from blum_goldwasser_cryptosystem import (
    PrivateKey,
    block_size,
    decrypt,
    encrypt,
    from_blocks,
    keygen,
    recover_seed,
    to_blocks,
)

P_BIG, Q_BIG = 2**31 - 1, 2**61 - 1


class FixedSeed(random.Random):
    """Returns r = 399 once, so that x0 = 399^2 mod 272953 = 159201 as in HAC 8.57."""

    def randrange(self, *args, **kwargs):  # type: ignore[override]
        return 399


def test_hac_example_8_57() -> None:
    n, sk = keygen(499, 547)
    assert n == 272953 and (sk.a, sk.b) == (-57, 52)
    assert block_size(n) == 4
    blocks = [0b1001, 0b1100, 0b0001, 0b0000, 0b1100]
    cs, x6 = encrypt(n, blocks, FixedSeed())
    assert cs == [0b0010, 0b0000, 0b1100, 0b1110, 0b0100]
    assert x6 == 139680
    assert pow((499 + 1) // 4, 6, 498) == 463 and pow((547 + 1) // 4, 6, 546) == 337
    assert pow(x6, 463, 499) == 20 and pow(x6, 337, 547) == 24
    assert recover_seed(sk, 5, x6) == 159201
    assert decrypt(sk, cs, x6) == blocks


def test_round_trip_bytes() -> None:
    rng = random.Random(1984)
    n, sk = keygen(P_BIG, Q_BIG)
    h = block_size(n)
    for length in (0, 1, 7, 40):
        msg = bytes(rng.randrange(256) for _ in range(length))
        cs, x_last = encrypt(n, to_blocks(msg, h), rng)
        assert from_blocks(decrypt(sk, cs, x_last), h, length) == msg


def test_probabilistic() -> None:
    rng = random.Random(5)
    n, _ = keygen(P_BIG, Q_BIG)
    blocks = to_blocks(b"same message", block_size(n))
    outs = {tuple(encrypt(n, blocks, rng)[0]) for _ in range(20)}
    assert len(outs) == 20


def test_one_query_chosen_ciphertext_attack() -> None:
    # The attacker flips every block of the challenge and keeps x_{t+1}. The
    # changed ciphertext differs from the challenge, so the oracle answers,
    # and the answer XOR the flips is the message.
    rng = random.Random(58)
    n, sk = keygen(P_BIG, Q_BIG)
    h = block_size(n)
    mask = (1 << h) - 1
    secret = b"attack at dawn"
    cs, x_last = encrypt(n, to_blocks(secret, h), rng)

    def oracle(query: tuple[list[int], int]) -> list[int]:
        assert query != (cs, x_last)
        return decrypt(sk, *query)

    answer = oracle(([c ^ mask for c in cs], x_last))
    assert from_blocks([a ^ mask for a in answer], h, len(secret)) == secret


def test_keygen_rejects_bad_primes() -> None:
    for p, q in ((5, 7), (7, 7), (7, 13)):
        try:
            keygen(p, q)
        except ValueError:
            continue
        raise AssertionError("expected ValueError")


def test_wrong_t_gives_wrong_seed() -> None:
    # The block count t is part of the ciphertext: dropping a block changes
    # the exponent of line L10, and the recovered seed is then a root of the
    # wrong depth.
    rng = random.Random(3)
    n, sk = keygen(P_BIG, Q_BIG)
    blocks = [1, 2, 3, 4]
    cs, x_last = encrypt(n, blocks, rng)
    assert decrypt(sk, cs, x_last) == blocks
    assert decrypt(sk, cs[:-1], x_last) != blocks[:-1]


def test_private_key_type() -> None:
    _, sk = keygen(499, 547)
    assert isinstance(sk, PrivateKey) and sk.a * 499 + sk.b * 547 == 1
