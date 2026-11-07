# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/carry-lookahead-adder/. The authors are listed in prov/ZGRFB8.jsonl.

import random

from carry_lookahead_adder import add, cla_add, from_bits, to_bits


def _levels(n: int, r: int) -> int:
    h, size = 0, n
    while True:
        h += 1
        size = -(-size // r)
        if size == 1:
            return h


def test_example() -> None:
    s, cout, _, depth = cla_add(to_bits(0xA7, 8), to_bits(0x59, 8))
    assert s == [0] * 8 and cout == 1
    assert from_bits(s) + (cout << 8) == 256
    assert depth == 7


def test_exhaustive_small() -> None:
    for r in (2, 3, 4):
        for n in range(1, 6):
            for x in range(1 << n):
                for y in range(1 << n):
                    for c0 in (0, 1):
                        assert add(x, y, n, c0, r) == x + y + c0


def test_edges() -> None:
    for r in (2, 4, 5):
        for n in (1, 2, 4, 15, 16, 17, 64, 100):
            top = (1 << n) - 1
            assert add(0, 0, n, 0, r) == 0
            assert add(top, 0, n, 1, r) == 1 << n
            assert add(top, top, n, 1, r) == 2 * top + 1
            assert add(top, 1, n, 0, r) == 1 << n
            assert add(0x5555555555555555555555555 & top, 0xAAAAAAAAAAAAAAAAAAAAAAAAA & top, n, 1, r) == top + 1


def test_random() -> None:
    rng = random.Random(20261107)
    for _ in range(600):
        n = rng.randint(1, 96)
        r = rng.choice((2, 3, 4, 8))
        x, y = rng.getrandbits(n), rng.getrandbits(n)
        c0 = rng.randint(0, 1)
        assert add(x, y, n, c0, r) == x + y + c0


def test_depth_and_fan_in() -> None:
    for r in (2, 3, 4, 8):
        for n in list(range(1, 40)) + [63, 64, 65, 127, 128, 129, 256, 257]:
            x = (1 << n) - 1
            _, _, k, depth = cla_add(to_bits(x, n), to_bits(0, n), 1, r)
            h = _levels(n, r)
            assert k.levels == h
            assert depth <= 4 * h
            assert k.max_fan_in <= r + 1


def test_exact_depth_at_powers() -> None:
    for r in (2, 4):
        n = r
        while n <= 1024:
            _, _, k, depth = cla_add([1] * n, [0] * n, 1, r)
            expect = 4 * k.levels - (1 if r == 2 and k.levels >= 2 else 0)
            assert depth == expect
            n *= r


def test_linear_size() -> None:
    for n in (2, 4, 8, 16, 64, 256, 1024):
        _, _, k, _ = cla_add([0] * n, [0] * n, 0, 2)
        assert k.and_gates + k.or_gates + k.xor_gates == 8 * n - 5
    for n in (4, 16, 64, 256, 1024):
        _, _, k, _ = cla_add([0] * n, [0] * n, 0, 4)
        assert 3 * (k.and_gates + k.or_gates + k.xor_gates) == 23 * n - 14
    for n in range(1, 130):
        _, _, k, _ = cla_add([0] * n, [0] * n, 0, 4)
        assert k.and_gates + k.or_gates + k.xor_gates <= 8 * n
