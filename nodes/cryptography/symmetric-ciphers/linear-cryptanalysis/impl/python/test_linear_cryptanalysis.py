# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/linear-cryptanalysis/. The authors are listed in prov/X8G9S4.jsonl.

import random
from itertools import product

from heys_spn import SBOX, decrypt, encrypt, lat, nibble, parity
from linear_cryptanalysis import (
    P_MASK,
    TRAIL,
    U4_MASK,
    algorithm_1,
    algorithm_2,
    key_parity,
    known_plaintexts_needed,
    piling_up,
    three_round_cipher,
    trail_bias,
)


def test_spn_round_trip() -> None:
    keys = [0x1111, 0x2222, 0x3333, 0x4444, 0x5555]
    for p in range(0, 1 << 16, 257):
        assert decrypt(encrypt(p, keys), keys) == p


def test_lat_entries_of_the_trail() -> None:
    t = lat()
    assert t[0][0] == 8
    assert [t[a][b] for _, _, a, b in TRAIL] == [4, -4, -4, -4]
    assert trail_bias() == -1 / 32


def test_piling_up_exact_for_independent_inputs() -> None:
    # Four S-box approximations on four independent uniform inputs: count all
    # 16^4 input tuples and compare with 2^3 * product of the biases.
    t = lat()
    approx = [(0xB, 0x4), (0x4, 0x5), (0x1, 0x1), (0x8, 0xF)]
    zeros = 0
    for xs in product(range(16), repeat=4):
        bit = 0
        for (a, b), x in zip(approx, xs):
            bit ^= parity(a & x) ^ parity(b & SBOX[x])
        zeros += bit == 0
    exact = zeros / 16 ** 4 - 0.5
    assert exact == piling_up([t[a][b] / 16 for a, b in approx])


def test_piling_up_matches_three_round_cipher() -> None:
    # Exact enumeration of all 2^16 plaintexts: the bias of the full relation
    # (key bits included) is exactly -1/32 for these keys.
    rng = random.Random(3)
    for _ in range(3):
        keys = [rng.getrandbits(16) for _ in range(4)]
        k = key_parity(keys)
        zeros = sum(1 for p in range(1 << 16)
                    if parity(p & P_MASK) ^ parity(three_round_cipher(p, keys) & U4_MASK) ^ k == 0)
        assert zeros / (1 << 16) - 0.5 == trail_bias()


def test_algorithm_1_with_one_over_eps_squared() -> None:
    # N = 1 / eps^2 = 1024 known plaintexts; the normal approximation predicts
    # success probability Phi(2) = 0.977.
    n = known_plaintexts_needed(1)
    assert n == 1024
    rng = random.Random(11)
    ok = 0
    for _ in range(40):
        keys = [rng.getrandbits(16) for _ in range(4)]
        pairs = [(p, three_round_cipher(p, keys)) for p in (rng.getrandbits(16) for _ in range(n))]
        ok += algorithm_1(pairs, trail_bias()) == key_parity(keys)
    assert ok >= 36


def test_algorithm_2_with_eight_over_eps_squared() -> None:
    # N = 8 / eps^2 = 8192 known plaintexts on the full 4-round cipher.
    n = known_plaintexts_needed(8)
    assert n == 8192
    rng = random.Random(12)
    first = 0
    for _ in range(20):
        keys = [rng.getrandbits(16) for _ in range(5)]
        pairs = [(p, encrypt(p, keys)) for p in (rng.getrandbits(16) for _ in range(n))]
        best, biases = algorithm_2(pairs)
        target = (nibble(keys[4], 2) << 4) | nibble(keys[4], 4)
        ranking = sorted(range(256), key=lambda g: -abs(biases[g]))
        first += best == target
        assert ranking.index(target) < 16  # the key is always near the top
        assert abs(abs(biases[target]) - 1 / 32) < 0.02
    assert first >= 15
