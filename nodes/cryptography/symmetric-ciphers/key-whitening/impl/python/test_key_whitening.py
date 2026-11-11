# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/key-whitening/. The authors are listed in prov/89MK42.jsonl.

import random

from key_whitening import em_decrypt, em_encrypt, fx_decrypt, fx_encrypt, public_permutation

N = 16
P, P_INV = public_permutation(N, 1991)
# X holds the 2^(n/2) blocks with high byte 0, U the 2^(n/2) blocks with low byte 0.
# Each n-bit value is x XOR u for exactly one pair (x, u) in X times U.
X = list(range(1 << (N // 2)))
U = [v << (N // 2) for v in range(1 << (N // 2))]


def test_round_trip() -> None:
    rng = random.Random(1)
    for _ in range(200):
        k1, k2, x = rng.getrandbits(N), rng.getrandbits(N), rng.getrandbits(N)
        assert em_decrypt(P_INV, k1, k2, em_encrypt(P, k1, k2, x)) == x

    def e(k: int, x: int) -> int:
        return P[x ^ k]

    def d(k: int, y: int) -> int:
        return P_INV[y] ^ k

    for _ in range(200):
        k, k1, k2, x = (rng.getrandbits(N) for _ in range(4))
        assert fx_decrypt(d, k, k1, k2, fx_encrypt(e, k, k1, k2, x)) == x


def daemen_attack(oracle, delta: int = 1) -> tuple[tuple[int, int] | None, int, int]:
    """Daemen (1991): chosen plaintexts, 2^(n/2) queries and about 2 * 2^(n/2) calls of P.

    E(x) XOR E(x XOR delta) = P(u) XOR P(u XOR delta) when u = x XOR K1.
    """
    queries = {x: oracle(x) for x in X}  # delta is in X, so x XOR delta is in X too
    table: dict[int, list[int]] = {}
    for x in X:
        table.setdefault(queries[x] ^ queries[x ^ delta], []).append(x)
    p_calls = 0
    for u in U:
        diff = P[u] ^ P[u ^ delta]
        p_calls += 2
        for x in table.get(diff, []):
            k1 = x ^ u
            k2 = queries[x] ^ P[u]
            # Check the candidate on two other queried blocks.
            if all(P[z ^ k1] ^ k2 == queries[z] for z in (X[3], X[200])):
                return (k1, k2), len(queries), p_calls
    return None, len(queries), p_calls


def slide_attack(pairs: dict[int, int]) -> tuple[int | None, int]:
    """Dunkelman, Keller and Shamir (2012) on one-key EM: known plaintexts only.

    x XOR E(x) = u XOR P(u) when u = x XOR K, because then E(x) = K XOR P(u).
    """
    table: dict[int, list[int]] = {}
    for x, y in pairs.items():
        table.setdefault(x ^ y, []).append(x)
    p_calls = 0
    for u in U:
        p_calls += 1
        for x in table.get(u ^ P[u], []):
            k = x ^ u
            if all(P[z ^ k] ^ k == pairs[z] for z in (X[5], X[77])):
                return k, p_calls
    return None, p_calls


def test_daemen_attack_breaks_two_key_em() -> None:
    rng = random.Random(91)
    for _ in range(5):
        k1, k2 = rng.getrandbits(N), rng.getrandbits(N)
        got, q, p = daemen_attack(lambda x: em_encrypt(P, k1, k2, x))
        assert got == (k1, k2)
        assert q == 1 << (N // 2) and p <= 2 << (N // 2)


def test_slide_attack_breaks_one_key_em() -> None:
    rng = random.Random(2012)
    for _ in range(5):
        k = rng.getrandbits(N)
        pairs = {x: em_encrypt(P, k, k, x) for x in X}
        got, p = slide_attack(pairs)
        assert got == k
        assert p <= 1 << (N // 2)
