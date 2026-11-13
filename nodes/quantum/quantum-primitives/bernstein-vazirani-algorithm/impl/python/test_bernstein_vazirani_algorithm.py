# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bernstein-vazirani-algorithm/. The authors are listed in prov/93HVEH.jsonl.

import itertools
import random

from bernstein_vazirani_algorithm import (
    bernstein_vazirani,
    bernstein_vazirani_distribution,
    classical_bernstein_vazirani,
    dot2,
    truth_table,
)

TOL = 1e-9


def brute_force_hidden_string(f: list[int], n: int) -> int | None:
    """Evaluate f everywhere and search all (s, c) with f(x) = s.x xor c."""
    for s in range(1 << n):
        for c in (0, 1):
            if all(f[x] == dot2(s, x) ^ c for x in range(1 << n)):
                return s
    return None


def test_every_hidden_string_up_to_six_bits() -> None:
    rng = random.Random(1)
    for n in range(1, 7):
        for s in range(1 << n):
            for c in (0, 1):
                f = truth_table(s, n, c)
                dist = bernstein_vazirani_distribution(f, n)
                assert abs(dist[s] - 1.0) < TOL
                assert bernstein_vazirani(f, n, rng) == s
                assert classical_bernstein_vazirani(f, n) == (s, n + 1)


def test_every_function_up_to_three_bits() -> None:
    # For a function that is not affine, the output y has probability equal to the
    # square of the normalized Walsh-Hadamard coefficient of (-1)^f at y.
    for n in (1, 2, 3):
        size = 1 << n
        for bits in itertools.product((0, 1), repeat=size):
            f = list(bits)
            dist = bernstein_vazirani_distribution(f, n)
            for y in range(size):
                c = sum((-1) ** (f[x] ^ dot2(x, y)) for x in range(size)) / size
                assert abs(dist[y] - c * c) < TOL
            s = brute_force_hidden_string(f, n)
            if s is not None:
                assert abs(dist[s] - 1.0) < TOL
            else:
                assert max(dist) < 1.0 - 1e-6


def test_fewer_than_n_classical_queries_leave_two_candidates() -> None:
    # For each set of n - 1 query points, two different strings give the same answers.
    for n in (2, 3, 4):
        for pts in itertools.combinations(range(1 << n), n - 1):
            seen = {}
            clash = False
            for s in range(1 << n):
                key = tuple(dot2(s, x) for x in pts)
                if key in seen:
                    clash = True
                    break
                seen[key] = s
            assert clash
