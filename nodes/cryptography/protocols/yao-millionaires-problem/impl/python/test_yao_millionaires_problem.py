# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/yao-millionaires-problem/. The authors are listed in prov/3E3WQE.jsonl.
# There are no official test vectors for Yao's protocol. The tests run every
# pair of inputs on a small range against plain comparison, and check the
# linear cost and the parts of Bob's view that the proof relies on.

import random

from yao_millionaires_problem import (
    millionaires,
    message_bits,
    richer_than,
    rsa_keygen,
    well_spread,
)

N_RANGE = 16


def test_all_pairs_on_a_small_range() -> None:
    rng = random.Random(1982)
    key = rsa_keygen(31, rng)
    for i in range(1, N_RANGE + 1):
        for j in range(1, N_RANGE + 1):
            assert millionaires(i, j, N_RANGE, key, rng).result == (i >= j)


def test_strictly_richer_all_pairs() -> None:
    rng = random.Random(7)
    key = rsa_keygen(31, rng)
    for a in range(10):
        for b in range(10):
            assert richer_than(a, b, 10, key, rng) == (a > b)


def test_cost_is_linear_in_the_range() -> None:
    rng = random.Random(3)
    key = rsa_keygen(31, rng)
    for n in (4, 8, 16, 32):
        run = millionaires(1, 1, n, key, rng)
        assert run.decryptions == n
        assert len(run.alice_values) == n
        assert message_bits(run, key) == key.n.bit_length() + run.p.bit_length() * (n + 1)


def test_alice_values_are_well_spread() -> None:
    rng = random.Random(5)
    key = rsa_keygen(31, rng)
    for _ in range(50):
        i, j = rng.randint(1, N_RANGE), rng.randint(1, N_RANGE)
        run = millionaires(i, j, N_RANGE, key, rng)
        # Undo the +1 Alice added, and check Yao's spacing condition.
        z = [v if u < i else (v - 1) % run.p for u, v in enumerate(run.alice_values)]
        assert well_spread(z, run.p)
        assert run.p.bit_length() == key.n.bit_length() // 2


def test_bob_message_hides_j() -> None:
    # k = E_A(x) is uniform because x is, so k - j + 1 has the same
    # distribution for every j. Check it on a tiny key with a chi-square test.
    from yao_millionaires_problem import RSAKey
    key = RSAKey(3233, 17, 413)
    rng = random.Random(9)
    counts = {}
    for j in (1, 5):
        c = [0] * 8
        for _ in range(8000):
            x = rng.randrange(key.n)
            c[((key.encrypt(x) - j + 1) % key.n) * 8 // key.n] += 1
        counts[j] = c
    stat = sum((a - b) ** 2 / (a + b) for a, b in zip(counts[1], counts[5]))
    assert stat < 24.3  # 7 degrees of freedom, 0.999 quantile
