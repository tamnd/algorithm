# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/simon-algorithm/. The authors are listed in prov/FEHRFQ.jsonl.

import itertools
import random
from fractions import Fraction

from simon_algorithm import Gf2Basis, classical_period, dot2, simon, simon_distribution

TOL = 1e-9


def promise_period(f: list[int], n: int) -> int | None:
    """Brute force: the s of Simon's promise, or None when f breaks the promise."""
    size = 1 << n
    if len(set(f)) == size:
        return 0
    for s in range(1, size):
        if all((f[x] == f[y]) == (y in (x, x ^ s)) for x in range(size) for y in range(size)):
            return s
    return None


def random_simon_function(n: int, s: int, rng: random.Random) -> list[int]:
    """A random f on n bits with period s, with n output bits and random labels."""
    labels = rng.sample(range(1 << n), 1 << n)
    f = [0] * (1 << n)
    done: dict[int, int] = {}
    k = 0
    for x in range(1 << n):
        rep = min(x, x ^ s)
        if rep not in done:
            done[rep] = labels[k]
            k += 1
        f[x] = done[rep]
    return f


def check_distribution(f: list[int], n: int, m: int, s: int) -> None:
    dist = simon_distribution(f, n, m)
    good = [y for y in range(1 << n) if dot2(y, s) == 0]
    p = 1.0 / len(good)
    for y in range(1 << n):
        assert abs(dist[y] - (p if dot2(y, s) == 0 else 0.0)) < TOL


def test_every_function_on_two_bits() -> None:
    # All 4^4 = 256 functions from 2 bits to 2 bits.
    rng = random.Random(1)
    promised = 0
    for f in itertools.product(range(4), repeat=4):
        f = list(f)
        s = promise_period(f, 2)
        if s is None:
            continue
        promised += 1
        check_distribution(f, 2, 2, s)
        assert simon(f, 2, 2, rng)[0] == s == classical_period(f, 2)
    assert promised == 24 + 3 * 12


def test_every_two_to_one_function_from_three_to_two_bits() -> None:
    # For each s != 0, the 4! ways to give the 4 cosets distinct 2-bit labels.
    rng = random.Random(2)
    count = 0
    for s in range(1, 8):
        cosets = sorted({min(x, x ^ s) for x in range(8)})
        for labels in itertools.permutations(range(4)):
            lab = dict(zip(cosets, labels))
            f = [lab[min(x, x ^ s)] for x in range(8)]
            assert promise_period(f, 3) == s
            check_distribution(f, 3, 2, s)
            assert simon(f, 3, 2, rng)[0] == s == classical_period(f, 3)
            count += 1
    assert count == 168


def test_one_to_one_functions_give_uniform_y() -> None:
    rng = random.Random(3)
    for n in (2, 3, 4):
        for _ in range(10):
            f = rng.sample(range(1 << n), 1 << n)
            check_distribution(f, n, n, 0)
            assert simon(f, n, n, rng)[0] == 0


def test_full_algorithm_against_brute_force() -> None:
    rng = random.Random(4)
    for n in range(1, 6):
        for _ in range(6):
            s = rng.randrange(1 << n)
            f = random_simon_function(n, s, rng)
            assert simon(f, n, n, rng)[0] == s == classical_period(f, n)


def span_probability(d: int, k: int) -> Fraction:
    """P(k uniform vectors span GF(2)^d) = prod_{i=0}^{d-1} (1 - 2^(i-k))."""
    p = Fraction(1)
    for i in range(d):
        p *= 1 - Fraction(1, 2 ** (k - i)) if k >= i else 0
    return p


def test_span_probability_by_enumeration() -> None:
    for d in (1, 2, 3):
        for k in range(0, 6):
            hits = 0
            total = 0
            for vs in itertools.product(range(1 << d), repeat=k):
                b = Gf2Basis()
                for v in vs:
                    b.insert(v)
                hits += b.rank() == d
                total += 1
            assert Fraction(hits, total) == span_probability(d, k)
            # The union bound over hyperplanes: failure < 2^(d - k).
            assert 1 - span_probability(d, k) <= Fraction(2 ** d - 1, 2 ** k)


def test_expected_number_of_runs() -> None:
    # For s != 0 the y are uniform on a space of dimension n - 1, so the expected
    # number of runs is sum_{j=1}^{n-1} 1 / (1 - 2^-j) < n - 1 + 1.607.
    rng = random.Random(5)
    n, trials = 3, 400
    want = sum(1 / (1 - 2.0 ** -j) for j in range(1, n))
    total = 0
    for _ in range(trials):
        s = rng.randrange(1, 1 << n)
        f = random_simon_function(n, s, rng)
        got, queries = simon(f, n, n, rng)
        assert got == s
        total += queries - 2
    mean = total / trials
    # The variance of the number of runs is below 3 here, so 5 standard deviations is 0.43.
    assert abs(mean - want) < 0.43
    assert want < n - 1 + 1.607


def test_gf2_null_vector() -> None:
    rng = random.Random(6)
    for n in range(1, 9):
        for _ in range(20):
            s = rng.randrange(1, 1 << n)
            b = Gf2Basis()
            while b.rank() < n - 1:
                y = rng.randrange(1 << n)
                if dot2(y, s) == 0:
                    b.insert(y)
            assert b.null_vector(n) == s
