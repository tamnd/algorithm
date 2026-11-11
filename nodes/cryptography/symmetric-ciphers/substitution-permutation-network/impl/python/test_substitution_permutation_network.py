# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/substitution-permutation-network/. The authors are listed in prov/H2EQ3A.jsonl.

import random

from substitution_permutation_network import PERM, decrypt, encrypt, permute


def test_permutation_of_the_tutorial() -> None:
    # Heys (2002), the permutation of the toy cipher: 1->1, 2->5, 3->9, 4->13, 5->2, ..., 16->16.
    assert [PERM[i] for i in range(1, 17)] == [1, 5, 9, 13, 2, 6, 10, 14, 3, 7, 11, 15, 4, 8, 12, 16]
    for x in range(1 << 16):
        assert permute(permute(x)) == x


def test_round_trip() -> None:
    rng = random.Random(2002)
    for r in (1, 2, 3, 4, 6):
        for _ in range(100):
            keys = [rng.getrandbits(16) for _ in range(r + 1)]
            x = rng.getrandbits(16)
            assert decrypt(keys, encrypt(keys, x)) == x


def test_is_a_permutation() -> None:
    rng = random.Random(7)
    keys = [rng.getrandbits(16) for _ in range(5)]
    assert len({encrypt(keys, x) for x in range(1 << 16)}) == 1 << 16


def test_avalanche_grows_with_rounds() -> None:
    rng = random.Random(16)
    means = []
    for r in (1, 2, 3, 4):
        total = 0
        trials = 400
        for _ in range(trials):
            keys = [rng.getrandbits(16) for _ in range(r + 1)]
            x = rng.getrandbits(16)
            bit = 1 << rng.randrange(16)
            total += bin(encrypt(keys, x) ^ encrypt(keys, x ^ bit)).count("1")
        means.append(total / trials)
    # One round changes only the bits of one S-box; four rounds come near 16 / 2 = 8.
    assert means[0] <= 4
    assert means[0] < means[1] < means[2]
    assert 7 <= means[3] <= 9
