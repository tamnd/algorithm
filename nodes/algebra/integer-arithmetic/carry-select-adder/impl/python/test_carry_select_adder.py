# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/carry-select-adder/. The authors are listed in prov/0D2Z2R.jsonl.

import random

from carry_select_adder import (
    Stats,
    add,
    carry_select_add,
    from_bits,
    growing_sizes,
    to_bits,
    uniform_sizes,
)


def _depth(n: int, sizes: list[int]) -> int:
    _, d = carry_select_add([1] * n, [0] * n, 1, sizes)
    return d


def test_example() -> None:
    bits, depth = carry_select_add(to_bits(0xB6D3, 16), to_bits(0x69E5, 16), 0, [4, 4, 4, 4])
    assert from_bits(bits) == 0x120B8
    assert depth == 15


def test_exhaustive_small() -> None:
    for n in range(1, 6):
        schedules = [[n], uniform_sizes(n, 1), uniform_sizes(n, 2), growing_sizes(n)]
        for sizes in schedules:
            for x in range(1 << n):
                for y in range(1 << n):
                    for c in (0, 1):
                        assert add(x, y, n, c, sizes) == x + y + c


def test_edges() -> None:
    for n in (1, 2, 5, 16, 17, 64, 100):
        top = (1 << n) - 1
        for sizes in (uniform_sizes(n, 3), growing_sizes(n), [n]):
            assert add(0, 0, n, 0, sizes) == 0
            assert add(top, 0, n, 1, sizes) == 1 << n
            assert add(top, 1, n, 0, sizes) == 1 << n
            assert add(top, top, n, 1, sizes) == 2 * top + 1


def test_random() -> None:
    rng = random.Random(1962)
    for _ in range(800):
        n = rng.randint(1, 120)
        sizes, left = [], n
        while left:
            k = rng.randint(1, left)
            sizes.append(k)
            left -= k
        x, y, c = rng.getrandbits(n), rng.getrandbits(n), rng.randint(0, 1)
        assert add(x, y, n, c, sizes) == x + y + c


def test_depth_formulas() -> None:
    for n in range(2, 70):
        assert _depth(n, [n]) == 2 * n + 1
        for k in range(1, n):
            sizes = uniform_sizes(n, k)
            assert _depth(n, sizes) == 2 * k + 2 * len(sizes) - 1
        for k0 in (1, 2, 3):
            sizes = growing_sizes(n, k0)
            if len(sizes) >= 2:
                assert _depth(n, sizes) == 2 * k0 + 2 * (len(sizes) - 1) + 1


def test_square_root_depth() -> None:
    for m in range(2, 24):
        n = m * m
        assert _depth(n, uniform_sizes(n, m)) == 4 * m - 1
        assert _depth(n, growing_sizes(n)) < 2 * (2 * n) ** 0.5 + 5


def test_linear_size() -> None:
    for n in (16, 64, 256, 1024):
        st = Stats()
        carry_select_add([0] * n, [0] * n, 0, uniform_sizes(n, 4), st)
        assert st.gates <= 11 * n
