# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/integral-cryptanalysis/. The authors are listed in prov/9XG8MF.jsonl.

import random

from integral_cryptanalysis import (
    MC,
    encrypt,
    gf16_mul,
    lambda_set,
    mix_columns,
    recover_last_round_key,
    shift_rows,
    shift_rows_inv,
    xor_sum,
)


def _keys(rng: random.Random, n: int) -> list[list[int]]:
    return [[rng.randrange(16) for _ in range(16)] for _ in range(n)]


def test_mix_columns_is_invertible() -> None:
    # The 4x4 matrix over GF(2^4) has full rank: MixColumns is a bijection on a column.
    images = set()
    for v in range(1 << 16):
        col = [(v >> (4 * i)) & 0xF for i in range(4)]
        images.add(tuple(mix_columns(col + [0] * 12)[:4]))
    assert len(images) == 1 << 16
    assert gf16_mul(2, 8) == 3  # x * x^3 = x^4 = x + 1


def test_shift_rows_inverse() -> None:
    s = list(range(16))
    assert shift_rows_inv(shift_rows(s)) == s
    assert shift_rows(s)[0:4] == [0, 5, 10, 15]  # column 0 after ShiftRows, as in AES


def test_three_rounds_are_balanced() -> None:
    rng = random.Random(1)
    for _ in range(50):
        keys = _keys(rng, 4)
        cts = [encrypt(p, keys, last_mix=True) for p in lambda_set(rng, rng.randrange(16))]
        assert xor_sum(cts) == [0] * 16


def test_four_rounds_are_not_balanced() -> None:
    rng = random.Random(2)
    unbalanced = 0
    for _ in range(50):
        keys = _keys(rng, 5)
        cts = [encrypt(p, keys, last_mix=True) for p in lambda_set(rng)]
        unbalanced += xor_sum(cts) != [0] * 16
    assert unbalanced >= 45


def test_key_recovery_on_four_rounds() -> None:
    rng = random.Random(3)
    for _ in range(20):
        keys = _keys(rng, 5)
        k4, used = recover_last_round_key(lambda p: encrypt(p, keys), rng)
        assert k4 == keys[4]
        assert used <= 5  # at most 5 * 16 = 80 chosen plaintexts


def test_matrix_rows() -> None:
    assert MC[0] == [2, 3, 1, 1]
