# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/deutsch-jozsa-algorithm/. The authors are listed in prov/W9842S.jsonl.

import itertools
import random

from deutsch_jozsa_algorithm import classical_deutsch_jozsa, deutsch_jozsa, deutsch_jozsa_distribution

TOL = 1e-9


def brute_force(f: list[int]) -> str | None:
    """Evaluate f on every input: constant, balanced, or None (no promise)."""
    w = sum(f)
    if w in (0, len(f)):
        return "constant"
    if 2 * w == len(f):
        return "balanced"
    return None


def all_functions(n: int):
    for bits in itertools.product((0, 1), repeat=1 << n):
        yield list(bits)


def test_every_function_up_to_three_bits() -> None:
    # Each of the 2^(2^n) functions, also the ones outside the promise.
    rng = random.Random(1)
    for n in (1, 2, 3):
        size = 1 << n
        for f in all_functions(n):
            dist = deutsch_jozsa_distribution(f, n)
            assert abs(sum(dist) - 1.0) < TOL
            # Closed form: P(y = 0) = ((2^n - 2|f|) / 2^n)^2.
            want0 = ((size - 2 * sum(f)) / size) ** 2
            assert abs(dist[0] - want0) < TOL
            kind = brute_force(f)
            if kind is not None:
                assert deutsch_jozsa(f, n, rng) == kind
                assert classical_deutsch_jozsa(f, n)[0] == kind


def test_every_balanced_function_on_four_bits() -> None:
    n, size = 4, 16
    count = 0
    for ones in itertools.combinations(range(size), size // 2):
        f = [0] * size
        for x in ones:
            f[x] = 1
        assert deutsch_jozsa_distribution(f, n)[0] < TOL
        count += 1
    assert count == 12870
    for c in (0, 1):
        assert abs(deutsch_jozsa_distribution([c] * size, n)[0] - 1.0) < TOL


def test_balanced_output_amplitudes_are_the_walsh_hadamard_coefficients() -> None:
    # P(y) = (2^-n sum_x (-1)^(f(x) + x.y))^2 for every y.
    rng = random.Random(2)
    for n in (2, 3, 4, 5):
        size = 1 << n
        for _ in range(20):
            f = [rng.randrange(2) for _ in range(size)]
            dist = deutsch_jozsa_distribution(f, n)
            for y in range(size):
                c = sum((-1) ** (f[x] ^ (bin(x & y).count("1") & 1)) for x in range(size)) / size
                assert abs(dist[y] - c * c) < TOL


def test_classical_worst_case_needs_half_plus_one() -> None:
    for n in (1, 2, 3, 4):
        half = 1 << (n - 1)
        assert classical_deutsch_jozsa([0] * (1 << n), n) == ("constant", half + 1)
        # A balanced function that agrees with the constant 0 on the first 2^(n-1) inputs:
        # after only 2^(n-1) queries the two cases cannot be told apart.
        f = [0] * half + [1] * half
        assert classical_deutsch_jozsa(f, n) == ("balanced", half + 1)


def test_deutsch_problem_n_equals_one() -> None:
    rng = random.Random(3)
    for f0, f1 in itertools.product((0, 1), repeat=2):
        want = "constant" if f0 == f1 else "balanced"
        assert deutsch_jozsa([f0, f1], 1, rng) == want
