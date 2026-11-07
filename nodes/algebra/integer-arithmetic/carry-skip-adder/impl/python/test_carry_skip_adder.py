# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/carry-skip-adder/. The authors are listed in prov/FWJCMW.jsonl.

import itertools
import random

from carry_skip_adder import (
    Stats,
    add,
    carry_skip_add,
    delay_bound,
    depth_formula,
    from_bits,
    to_bits,
    uniform_sizes,
    worst_input,
)


def _max_delay(n: int, sizes: list[int]) -> int:
    """The largest settle time over all inputs. Only the kind of each position
    (kill, propagate, generate) and the carry-in matter for the timing."""
    worst = 0
    for kinds in itertools.product((0, 1, 2), repeat=n):
        a = [1 if t >= 1 else 0 for t in kinds]
        b = [1 if t == 2 else 0 for t in kinds]
        for c in (0, 1):
            worst = max(worst, carry_skip_add(a, b, c, sizes)[1])
    return worst


def test_example() -> None:
    bits, delay, depth = carry_skip_add(to_bits(0x9A3C, 16), to_bits(0x65C4, 16), 0, [4, 4, 4, 4])
    assert from_bits(bits) == 0x9A3C + 0x65C4
    assert delay == 15 and depth == 39


def test_exhaustive_small() -> None:
    for n in range(1, 6):
        for sizes in ([n], uniform_sizes(n, 1), uniform_sizes(n, 2), uniform_sizes(n, 3)):
            for x in range(1 << n):
                for y in range(1 << n):
                    for c in (0, 1):
                        assert add(x, y, n, c, sizes) == x + y + c


def test_edges() -> None:
    for n in (1, 2, 7, 16, 33, 100):
        top = (1 << n) - 1
        for sizes in (uniform_sizes(n, 4), [n]):
            assert add(0, 0, n, 0, sizes) == 0
            assert add(top, 0, n, 1, sizes) == 1 << n
            assert add(top, top, n, 1, sizes) == 2 * top + 1
            assert add(top - 1, 0, n, 1, sizes) == top


def test_random() -> None:
    rng = random.Random(1961)
    for _ in range(800):
        n = rng.randint(1, 120)
        sizes, left = [], n
        while left:
            k = rng.randint(1, left)
            sizes.append(k)
            left -= k
        x, y, c = rng.getrandbits(n), rng.getrandbits(n), rng.randint(0, 1)
        assert add(x, y, n, c, sizes) == x + y + c


def test_delay_bound_is_exact_for_small_n() -> None:
    rng = random.Random(7)
    for n in range(1, 7):
        schedules = [uniform_sizes(n, k) for k in range(1, n + 1)]
        for _ in range(2):
            sizes, left = [], n
            while left:
                k = rng.randint(1, left)
                sizes.append(k)
                left -= k
            schedules.append(sizes)
        for sizes in schedules:
            assert _max_delay(n, sizes) == delay_bound(sizes)


def test_worst_input_and_depth() -> None:
    for n in (8, 16, 64, 256):
        a, b, c = worst_input(n)
        for k in range(1, 20):
            sizes = uniform_sizes(n, k)
            _, delay, depth = carry_skip_add(to_bits(a, n), to_bits(b, n), c, sizes)
            assert delay == delay_bound(sizes)
            assert depth == depth_formula(n, len(sizes))


def test_square_root_delay() -> None:
    for n in (64, 256, 1024):
        best = min(delay_bound(uniform_sizes(n, k)) for k in range(1, n + 1))
        assert best <= 4 * (2 * n) ** 0.5
        st = Stats()
        carry_skip_add([0] * n, [0] * n, 0, uniform_sizes(n, 8), st)
        assert st.gates <= 7 * n
