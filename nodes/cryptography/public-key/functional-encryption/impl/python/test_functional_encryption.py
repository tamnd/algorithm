# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/functional-encryption/. The authors are listed in prov/YYQV99.jsonl.
#
# There are no official test vectors for inner-product FE. The tests check the worked example of
# the page modulo 23, that a key for y gives exactly <x, y> for random small vectors, that the
# keys reveal x only through inner products, and the baby-step giant-step search, with fixed
# seeds. The groups are NOT secure.

import random

import functional_encryption as fe


def test_worked_example_mod_23() -> None:
    G = fe.TINY
    assert G.q == 11 and [G.exp(4, k) for k in range(1, 12)][-1] == 1
    s = [3, 5]
    mpk = [G.exp(G.g, si) for si in s]
    assert mpk == [18, 12]
    ct = fe.encrypt(G, mpk, [2, 1], None, r=6)
    assert ct == (2, [13, 13])
    y = [1, 3]
    sk = fe.keygen(G, s, y)
    assert sk == 7
    assert fe.decrypt_to_group(G, sk, y, ct) == 12 == G.exp(4, 5)
    assert fe.decrypt(G, sk, y, ct, 5) == 5


def test_baby_step_giant_step() -> None:
    G = fe.TOY
    for t in (-1000, -1, 0, 1, 999, 1000):
        assert fe.baby_step_giant_step(G, G.exp(G.g, t), -1000, 1000) == t
    assert fe.baby_step_giant_step(G, G.exp(G.g, 5000), -1000, 1000) is None


def test_inner_products_random() -> None:
    G = fe.TOY
    rng = random.Random(2015)
    n = 6
    mpk, msk = fe.setup(G, n, rng)
    for _ in range(4):
        x = [rng.randrange(-20, 21) for _ in range(n)]
        y = [rng.randrange(-20, 21) for _ in range(n)]
        ct = fe.encrypt(G, mpk, x, rng)
        sk = fe.keygen(G, msk, y)
        assert fe.decrypt(G, sk, y, ct, 3000) == sum(a * b for a, b in zip(x, y))


def test_wrong_vector_with_a_key_fails() -> None:
    G = fe.TOY
    rng = random.Random(7)
    mpk, msk = fe.setup(G, 3, rng)
    x = [4, -2, 7]
    ct = fe.encrypt(G, mpk, x, rng)
    sk = fe.keygen(G, msk, [1, 1, 1])
    assert fe.decrypt(G, sk, [1, 1, 1], ct, 100) == 9
    # Using the key for (1, 1, 1) with another vector does not give that vector's inner product.
    assert fe.decrypt(G, sk, [1, 0, 0], ct, 100) is None


def test_independent_keys_reveal_x() -> None:
    # The functionality itself: n linearly independent keys determine x (here, the unit vectors).
    G = fe.TOY
    rng = random.Random(11)
    mpk, msk = fe.setup(G, 3, rng)
    x = [-5, 12, 0]
    ct = fe.encrypt(G, mpk, x, rng)
    units = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    assert [fe.decrypt(G, fe.keygen(G, msk, u), u, ct, 50) for u in units] == x
