# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/brent-kung-adder/. The authors are listed in prov/XD1FWT.jsonl.

import random

from brent_kung_adder import Stats, add, brent_kung_add, from_bits, to_bits


def _expected_levels(n: int) -> int:
    up = n.bit_length() - 1
    down = (n // 3).bit_length() if n >= 3 else 0
    return up + down


def test_example() -> None:
    st = Stats()
    bits, depth = brent_kung_add(to_bits(182, 8), to_bits(91, 8), 0, st)
    assert from_bits(bits) == 273
    assert st.cells == 11 and st.levels == 5 and depth == 12


def test_exhaustive_small() -> None:
    for n in range(1, 7):
        for x in range(1 << n):
            for y in range(1 << n):
                for c in (0, 1):
                    assert add(x, y, n, c) == x + y + c


def test_edges() -> None:
    for n in (1, 2, 3, 7, 8, 9, 31, 32, 33, 64, 100):
        top = (1 << n) - 1
        assert add(0, 0, n) == 0
        assert add(top, 0, n, 1) == 1 << n
        assert add(top, 1, n) == 1 << n
        assert add(top, top, n, 1) == 2 * top + 1
        alt = int("10" * n, 2) & top
        assert add(alt, top ^ alt, n, 1) == 1 << n


def test_random() -> None:
    rng = random.Random(1982)
    for _ in range(800):
        n = rng.randint(1, 120)
        x, y, c = rng.getrandbits(n), rng.getrandbits(n), rng.randint(0, 1)
        assert add(x, y, n, c) == x + y + c


def test_cells_levels_depth() -> None:
    for n in range(1, 300):
        st = Stats()
        _, depth = brent_kung_add([1] * n, [0] * n, 1, st)
        floor_log = n.bit_length() - 1
        assert st.cells == 2 * n - 1 - bin(n).count("1") - floor_log
        assert st.levels == _expected_levels(n)
        assert depth <= 2 * st.levels + 4


def test_powers_of_two() -> None:
    for L in range(2, 11):
        n = 1 << L
        st = Stats()
        _, depth = brent_kung_add([1] * n, [0] * n, 1, st)
        assert st.cells == 2 * n - 2 - L
        assert st.levels == 2 * L - 1
        assert depth == 4 * L
