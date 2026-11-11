# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hill-cipher/. The authors are listed in prov/G0FB2K.jsonl.

import math
import random

import pytest

from hill_cipher import (
    count_keys,
    det,
    det_mod,
    hill_decrypt,
    hill_encrypt,
    inverse_mod,
    is_valid_key,
    known_plaintext_attack,
    mat_mul,
)

K2 = [[11, 3], [8, 7]]
K3 = [[6, 24, 1], [13, 16, 10], [20, 17, 15]]


def random_key(rng: random.Random, n: int) -> list[list[int]]:
    while True:
        k = [[rng.randrange(26) for _ in range(n)] for _ in range(n)]
        if math.gcd(det_mod(k), 26) == 1:
            return k


def oracle_encrypt(text: str, k: list[list[int]]) -> str:
    """Matrix product written another way: c = sum over j of p_j times column j of K."""
    n = len(k)
    t = "".join(ch for ch in text.upper() if ch.isalpha())
    t += "X" * (-len(t) % n)
    out = []
    for s in range(0, len(t), n):
        acc = [0] * n
        for j, ch in enumerate(t[s : s + n]):
            for i in range(n):
                acc[i] += (ord(ch) - 65) * k[i][j]
        out.extend(chr(65 + x % 26) for x in acc)
    return "".join(out)


def test_examples() -> None:
    assert hill_encrypt("ACT", K3) == "POH"
    assert hill_encrypt("CAT", K3) == "FIN"
    assert inverse_mod(K3) == [[8, 5, 10], [21, 8, 21], [21, 12, 8]]
    assert hill_encrypt("july", K2) == "DELW"
    assert hill_decrypt("DELW", K2) == "JULY"
    assert hill_encrypt("HELP", K2) == "LGKL"


def test_padding_and_bad_keys() -> None:
    assert hill_encrypt("", K2) == ""
    assert hill_decrypt(hill_encrypt("ABC", K2), K2) == "ABCX"
    for bad in ([[2, 0], [0, 1]], [[13, 0], [0, 1]], [[1, 2], [2, 4]]):
        assert not is_valid_key(bad)
        with pytest.raises(ValueError):
            hill_encrypt("HELLO", bad)


def test_determinant_against_formula() -> None:
    rng = random.Random(3)
    for _ in range(500):
        a = [[rng.randrange(-30, 30) for _ in range(3)] for _ in range(3)]
        expansion = (
            a[0][0] * (a[1][1] * a[2][2] - a[1][2] * a[2][1])
            - a[0][1] * (a[1][0] * a[2][2] - a[1][2] * a[2][0])
            + a[0][2] * (a[1][0] * a[2][1] - a[1][1] * a[2][0])
        )
        assert det(a) == expansion


def test_round_trip_and_oracle() -> None:
    rng = random.Random(7)
    for _ in range(600):
        n = rng.randint(1, 4)
        k = random_key(rng, n)
        p = "".join(rng.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ") for _ in range(n * rng.randint(0, 6)))
        c = hill_encrypt(p, k)
        assert c == oracle_encrypt(p, k)
        assert hill_decrypt(c, k) == p
        ident = [[int(i == j) for j in range(n)] for i in range(n)]
        assert mat_mul(k, inverse_mod(k)) == ident


def test_singular_key_is_not_injective() -> None:
    # det = 2 * 7 - 4 * 3 = 2 is even, so 13 times a kernel vector mod 2 collides with 0.
    k = [[2, 4], [3, 7]]
    v = [13 * x for x in (0, 1)]
    assert [(k[i][0] * v[0] + k[i][1] * v[1]) % 26 for i in range(2)] == [0, 13]
    k = [[2, 4], [1, 7]]  # det = 10, even
    assert any(
        [(k[0][0] * x + k[0][1] * y) % 26, (k[1][0] * x + k[1][1] * y) % 26] == [0, 0]
        for x in range(26)
        for y in range(26)
        if (x, y) != (0, 0)
    )


def test_count_of_2x2_keys() -> None:
    brute = sum(
        math.gcd((a * d - b * c) % 26, 26) == 1
        for a in range(26)
        for b in range(26)
        for c in range(26)
        for d in range(26)
    )
    assert brute == count_keys(2) == 157248 == 6 * 168 * 156
    assert count_keys(3) == 1634038189056


def test_known_plaintext_attack_example() -> None:
    assert known_plaintext_attack("HELP", "LGKL", 2) == K2
    # WEST: the plaintext matrix has determinant 8, which is even, so two
    # different keys fit the pair, and the attack must say so.
    assert known_plaintext_attack("WEST", hill_encrypt("WEST", K2), 2) is None
    fits = [
        [[a, b], [c, d]]
        for a in range(26)
        for b in range(26)
        for c in range(26)
        for d in range(26)
        if math.gcd((a * d - b * c) % 26, 26) == 1 and hill_encrypt("WEST", [[a, b], [c, d]]) == "UWVR"
    ]
    assert len(fits) == 2 and K2 in fits
    # One more block that is independent modulo 2 fixes the key.
    assert known_plaintext_attack("WESTWARD", hill_encrypt("WESTWARD", K2), 2) == K2


def spans(blocks: list[list[int]], p: int) -> bool:
    """Oracle for n = 2: the blocks span GF(p)^2 unless a nonzero v is orthogonal to all."""
    return not any(
        all((v0 * b[0] + v1 * b[1]) % p == 0 for b in blocks) for v0 in range(p) for v1 in range(p) if (v0, v1) != (0, 0)
    )


def test_known_plaintext_attack_random_2x2() -> None:
    # The attack answers exactly when the plaintext blocks span both
    # (Z_2)^2 and (Z_13)^2, and then its answer is the key.
    rng = random.Random(11)
    recovered = 0
    for _ in range(500):
        k = random_key(rng, 2)
        blocks = [[rng.randrange(26), rng.randrange(26)] for _ in range(rng.randint(1, 4))]
        p = "".join(chr(65 + x) for b in blocks for x in b)
        got = known_plaintext_attack(p, hill_encrypt(p, k), 2)
        assert (got is not None) == (spans(blocks, 2) and spans(blocks, 13))
        if got is not None:
            assert got == k
            recovered += 1
    assert recovered >= 200


def test_known_plaintext_attack_random_larger() -> None:
    rng = random.Random(12)
    recovered = 0
    for _ in range(200):
        n = rng.randint(3, 4)
        k = random_key(rng, n)
        p = "".join(rng.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ") for _ in range(n * (n + 3)))
        got = known_plaintext_attack(p, hill_encrypt(p, k), n)
        if got is not None:
            assert got == k
            recovered += 1
    assert recovered >= 150
