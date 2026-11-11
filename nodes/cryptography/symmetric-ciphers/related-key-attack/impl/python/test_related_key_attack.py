# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/related-key-attack/. The authors are listed in prov/3PCPX9.jsonl.

import random

from related_key_attack import F, F_INV, ROUNDS, encrypt, recover_key, rotate_key, subkeys


def test_f_is_a_bijection() -> None:
    assert sorted(F) == list(range(1 << 16))
    assert all(F_INV[F[x]] == x for x in range(0, 1 << 16, 7))


def test_rotated_key_shifts_subkeys() -> None:
    key = [0x1111, 0x2222, 0x3333, 0x4444]
    assert subkeys(rotate_key(key, 1))[:-1] == subkeys(key)[1:]


def test_slid_relation_holds() -> None:
    # E_K*(F_w0(P)) = F_w0(E_K(P)) for every P.
    rng = random.Random(1)
    key = [rng.getrandbits(16) for _ in range(4)]
    star = rotate_key(key, 1)

    def one_round(x: int) -> int:
        left, right = x >> 16, x & 0xFFFF
        return (right << 16) | (left ^ F[right ^ key[0]])

    for _ in range(50):
        p = rng.getrandbits(32)
        assert encrypt(one_round(p), star) == one_round(encrypt(p, key))


def test_recover_full_key() -> None:
    # m = 512 queries per key and step: about m^2 / 2^16 = 4 slid pairs.
    rng = random.Random(2)
    for _ in range(3):
        key = [rng.getrandbits(16) for _ in range(4)]
        queries = [0]

        def oracle(j: int, p: int) -> int:
            queries[0] += 1
            return encrypt(p, rotate_key(key, j))

        assert recover_key(oracle, 512, rng) == key
        assert queries[0] <= 4 * 2 * 512 * 2  # a retry is allowed once per word
        assert ROUNDS == 32
