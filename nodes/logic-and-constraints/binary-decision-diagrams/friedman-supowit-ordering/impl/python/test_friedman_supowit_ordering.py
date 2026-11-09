# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/friedman-supowit-ordering/. The authors are listed in prov/T03ZRT.jsonl.

import random
from itertools import permutations

from friedman_supowit_ordering import brute_force, friedman_supowit, obdd_size


def hwb_table(n: int) -> list[int]:
    out = []
    for a in range(1 << n):
        s = bin(a).count("1")
        out.append(0 if s == 0 else (a >> (s - 1)) & 1)
    return out


def mul_table(n: int) -> list[int]:
    """The middle bit (bit n - 1) of x * y for n-bit x and y; x is variables 0..n-1."""
    mask = (1 << n) - 1
    return [((a & mask) * (a >> n)) >> (n - 1) & 1 for a in range(1 << (2 * n))]


def pairs_table(k: int) -> list[int]:
    n = 2 * k
    return [int(any(a >> (2 * i) & 1 and a >> (2 * i + 1) & 1 for i in range(k))) for a in range(1 << n)]


def test_small_cases() -> None:
    assert friedman_supowit([0, 1], 1) == (3, [0])
    assert friedman_supowit([1, 1, 1, 1], 2)[0] == 1
    assert friedman_supowit([0, 0, 0, 1], 2)[0] == 4
    assert friedman_supowit([0, 1, 1, 0, 1, 0, 0, 1], 3)[0] == 2 * 3 + 1


def test_random_against_all_orders() -> None:
    rng = random.Random(20260)
    checked = 0
    for n in range(1, 7):
        for _ in range(110 if n < 6 else 40):
            density = rng.random()
            table = [int(rng.random() < density) for _ in range(1 << n)]
            lo, order = friedman_supowit(table, n)
            hi, worst = friedman_supowit(table, n, maximize=True)
            assert (lo, hi) == brute_force(table, n)
            assert obdd_size(table, n, order) == lo
            assert obdd_size(table, n, worst) == hi
            checked += 1
    assert checked >= 500


def test_n7_against_all_orders() -> None:
    rng = random.Random(7)
    for _ in range(2):
        table = [rng.randrange(2) for _ in range(1 << 7)]
        lo, order = friedman_supowit(table, 7)
        sizes = [obdd_size(table, 7, list(p)) for p in permutations(range(7))]
        assert lo == min(sizes) and obdd_size(table, 7, order) == lo


def test_multi_terminal() -> None:
    rng = random.Random(11)
    for n in range(1, 6):
        for _ in range(20):
            table = [rng.randrange(4) for _ in range(1 << n)]
            assert friedman_supowit(table, n)[0] == brute_force(table, n)[0]


def test_measured_tables() -> None:
    assert [friedman_supowit(pairs_table(k), 2 * k)[0] for k in range(1, 5)] == [4, 6, 8, 10]
    assert [friedman_supowit(pairs_table(k), 2 * k, True)[0] for k in range(1, 5)] == [4, 8, 16, 32]
    assert [friedman_supowit(mul_table(n), 2 * n)[0] for n in range(1, 6)] == [4, 8, 14, 31, 63]
    assert [friedman_supowit(mul_table(n), 2 * n, True)[0] for n in range(1, 6)] == [4, 9, 24, 71, 207]
    assert [friedman_supowit(hwb_table(n), n)[0] for n in range(3, 11)] == [5, 9, 16, 23, 33, 46, 63, 82]
