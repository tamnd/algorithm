# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dirichlet-hyperbola-method/. The authors are listed in prov/6FBZTF.jsonl.

import random

from dirichlet_hyperbola_method import (
    divisor_summatory,
    hyperbola_sum,
    integer_sqrt,
    sigma_summatory,
)


def brute_divisor_counts(n: int) -> list[int]:
    """d(k) for 0 <= k <= n by trial division of every k (reference only)."""
    d = [0] * (n + 1)
    for k in range(1, n + 1):
        d[k] = sum(1 for a in range(1, k + 1) if k % a == 0)
    return d


def floor_sum(n: int) -> int:
    """D(n) as the sum of floor(n / a) for 1 <= a <= n (reference, O(n))."""
    return sum(n // a for a in range(1, n + 1)) if n > 0 else 0


def fib(n: int) -> int:
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


def test_example() -> None:
    assert divisor_summatory(10) == 27
    assert divisor_summatory(100) == 482
    assert [divisor_summatory(n) for n in range(1, 13)] == [
        1, 3, 5, 8, 10, 14, 16, 20, 23, 27, 29, 35,
    ]


def test_known_powers_of_ten() -> None:
    # OEIS A057494.
    known = [1, 27, 482, 7069, 93668, 1166750, 13970034]
    assert [divisor_summatory(10**k) for k in range(7)] == known


def test_zero_and_negative() -> None:
    assert divisor_summatory(0) == 0
    assert divisor_summatory(-1) == 0
    assert divisor_summatory(-(10**30)) == 0
    assert divisor_summatory(1) == 1
    assert sigma_summatory(0) == 0
    assert sigma_summatory(-5) == 0


def test_against_divisor_counts() -> None:
    n_max = 1500
    d = brute_divisor_counts(n_max)
    running = 0
    sigma = [0] * (n_max + 1)
    for a in range(1, n_max + 1):
        for k in range(a, n_max + 1, a):
            sigma[k] += a
    running_sigma = 0
    for n in range(1, n_max + 1):
        running += d[n]
        running_sigma += sigma[n]
        assert divisor_summatory(n) == running
        assert sigma_summatory(n) == running_sigma


def test_integer_sqrt() -> None:
    rng = random.Random(7)
    values = [0, 1, 2, 3, 4, 15, 16, 17, 2**64, 2**64 - 1, (10**8 + 1) ** 2 - 1]
    values += [rng.randrange(10**rng.randrange(1, 400)) for _ in range(800)]
    values += [x * x + e for x in range(200) for e in (-1, 0, 1) if x * x + e >= 0]
    for v in values:
        s = integer_sqrt(v)
        assert s * s <= v < (s + 1) * (s + 1)


def test_random_against_floor_sum() -> None:
    rng = random.Random(2026)
    for _ in range(600):
        n = rng.randrange(0, 30000)
        assert divisor_summatory(n) == floor_sum(n)


def test_special_inputs() -> None:
    cases = [2**k for k in range(18)] + [fib(k) for k in range(2, 24)]
    cases += [x * x + e for x in (1, 2, 3, 10, 31, 100, 127) for e in (-1, 0, 1)]
    for n in cases:
        assert divisor_summatory(n) == floor_sum(n)


def test_large_inputs_by_block_decomposition() -> None:
    # Independent check: group a by the value q = n // a.
    def by_blocks(n: int) -> int:
        total, a = 0, 1
        while a <= n:
            q = n // a
            last = n // q
            total += q * (last - a + 1)
            a = last + 1
        return total

    rng = random.Random(11)
    for _ in range(40):
        n = rng.randrange(1, 10**11)
        assert divisor_summatory(n) == by_blocks(n)
    # Several hundred digits: the identity D(n) = 2 sum - s^2 against the
    # general hyperbola_sum, with the large n split at the same square root.
    for _ in range(3):
        big = rng.randrange(10**300, 10**301)
        small = big % 10**9 + 1
        assert divisor_summatory(small) == by_blocks(small)
        s = integer_sqrt(big)
        assert s * s <= big < (s + 1) ** 2


def test_general_sum_matches_direct() -> None:
    rng = random.Random(5)
    for _ in range(80):
        n = rng.randrange(0, 400)
        cf = [rng.randrange(-5, 6) for _ in range(n + 1)]
        cg = [rng.randrange(-5, 6) for _ in range(n + 1)]
        pf = [0] * (n + 1)
        pg = [0] * (n + 1)
        for i in range(1, n + 1):
            pf[i] = pf[i - 1] + cf[i]
            pg[i] = pg[i - 1] + cg[i]
        direct = sum(
            cf[a] * cg[b] for a in range(1, n + 1) for b in range(1, n // a + 1)
        )
        got = hyperbola_sum(
            lambda a: cf[a], lambda b: cg[b], lambda x: pf[x], lambda x: pg[x], n
        )
        assert got == direct
