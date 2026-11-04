# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/meet-in-the-middle-attack/. The authors are listed in prov/ZGTKX7.jsonl.

import random

from meet_in_the_middle_attack import meet_in_the_middle_attack


def rotl(x: int, r: int) -> int:
    return ((x << r) | (x >> (8 - r))) & 255


def rotr(x: int, r: int) -> int:
    return ((x >> r) | (x << (8 - r))) & 255


def toy_encrypt(k: int, x: int) -> int:
    kappa = 17 * k
    return (rotl(x ^ kappa, 3) + kappa) & 255


def toy_decrypt(k: int, y: int) -> int:
    kappa = 17 * k
    return rotr((y - kappa) & 255, 3) ^ kappa


def brute_force(enc, keys: int, pairs) -> list[tuple[int, int]]:
    return sorted(
        ((a, b) for a in range(keys) for b in range(keys) if all(enc(b, enc(a, p)) == c for p, c in pairs)),
        key=lambda kk: (kk[1], kk[0]),
    )


def test_toy_cipher_is_invertible() -> None:
    for k in range(16):
        assert sorted(toy_encrypt(k, x) for x in range(256)) == list(range(256))
        assert all(toy_decrypt(k, toy_encrypt(k, x)) == x for x in range(256))


def test_example() -> None:
    assert toy_encrypt(10, toy_encrypt(3, 42)) == 52
    assert toy_encrypt(10, toy_encrypt(3, 100)) == 228
    assert toy_decrypt(9, 52) == 234 == toy_encrypt(1, 42)
    one = meet_in_the_middle_attack(toy_encrypt, toy_decrypt, 16, [(42, 52)])
    assert one == [(10, 5), (1, 9), (3, 10)]
    two = meet_in_the_middle_attack(toy_encrypt, toy_decrypt, 16, [(42, 52), (100, 228)])
    assert two == [(3, 10)]


def test_edges() -> None:
    assert meet_in_the_middle_attack(toy_encrypt, toy_decrypt, 0, [(1, 2)]) == []
    # One key: the only candidate is (0, 0).
    assert meet_in_the_middle_attack(toy_encrypt, toy_decrypt, 1, [(5, toy_encrypt(0, toy_encrypt(0, 5)))]) == [(0, 0)]
    # Inconsistent pairs: the same plaintext with two ciphertexts.
    assert meet_in_the_middle_attack(toy_encrypt, toy_decrypt, 16, [(42, 52), (42, 53)]) == []
    # All keys equal to the identity: every key pair is consistent.
    ident = lambda k, x: x  # noqa: E731
    assert len(meet_in_the_middle_attack(ident, ident, 4, [(3, 3), (7, 7)])) == 16


def test_against_brute_force() -> None:
    rng = random.Random(1977)
    for _ in range(600):
        blocks = rng.randrange(1, 17)
        keys = rng.randrange(1, 9)
        perms = []
        for _k in range(keys):
            p = list(range(blocks))
            rng.shuffle(p)
            perms.append(p)
        invs = []
        for p in perms:
            inv = [0] * blocks
            for x, y in enumerate(p):
                inv[y] = x
            invs.append(inv)

        def enc(k: int, x: int) -> int:
            return perms[k][x]

        def dec(k: int, y: int) -> int:
            return invs[k][y]

        a, b = rng.randrange(keys), rng.randrange(keys)
        pairs = []
        for _i in range(rng.randrange(1, 4)):
            p = rng.randrange(blocks)
            c = enc(b, enc(a, p)) if rng.random() < 0.9 else rng.randrange(blocks)
            pairs.append((p, c))
        assert meet_in_the_middle_attack(enc, dec, keys, pairs) == brute_force(enc, keys, pairs)
