# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/feistel-network/. The authors are listed in prov/NQ29ZT.jsonl.

import random

from feistel_network import feistel, feistel_inverse, toy_round_function

H = 16


def test_round_function_is_not_invertible() -> None:
    images = {toy_round_function(0x0F0F, r) for r in range(1 << H)}
    assert len(images) < 1 << H


def test_round_trip() -> None:
    rng = random.Random(1973)
    for rounds in (1, 2, 3, 4, 8, 16):
        for _ in range(50):
            keys = [rng.getrandbits(H) for _ in range(rounds)]
            x = rng.getrandbits(2 * H)
            assert feistel_inverse(toy_round_function, keys, feistel(toy_round_function, keys, x, H), H) == x


def test_is_a_permutation_on_small_blocks() -> None:
    # With h = 4 the block has 8 bits: check that all 256 outputs differ.
    def f(k: int, r: int) -> int:
        return (r * k) & 0xF  # not a permutation of r when k is even

    rng = random.Random(4)
    for _ in range(20):
        keys = [rng.getrandbits(4) for _ in range(3)]
        outs = {feistel(f, keys, x, 4) for x in range(256)}
        assert len(outs) == 256


def test_one_round_leaks_a_half() -> None:
    # After one round, the output is (L0 XOR F(R0), R0): the right half of the input shows in clear.
    rng = random.Random(5)
    for _ in range(20):
        x = rng.getrandbits(2 * H)
        y = feistel(toy_round_function, [rng.getrandbits(H)], x, H)
        assert y & 0xFFFF == x & 0xFFFF
