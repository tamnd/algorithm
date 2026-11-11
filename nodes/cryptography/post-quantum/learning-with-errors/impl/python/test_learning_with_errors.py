# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/learning-with-errors/. The authors are listed in prov/91A2EW.jsonl.
"""Tests for the LWE sampler and the toy solvers.

LWE is a problem, not a standard algorithm, so there are no official test
vectors. All parameters are toy sizes; real LWE dimensions are in the hundreds.
"""

import math
import random

from learning_with_errors import (
    brute_force_decide,
    centered,
    embedding_basis,
    lll,
    normal_form,
    primal_attack,
    sample_lwe,
    search_from_decision,
    solve_noiseless,
)


def residuals(A, b, s, q):
    return [centered(bi - sum(x * y for x, y in zip(ai, s)), q) for ai, bi in zip(A, b)]


def test_sampler_relation():
    rng = random.Random(1)
    A, b, s, e = sample_lwe(8, 40, 97, 2.5, rng)
    assert len(A) == 40 and all(len(r) == 8 for r in A)
    assert residuals(A, b, s, 97) == e
    assert all(0 <= x < 97 for x in b)


def test_error_width():
    # The discretized Gaussian of width alpha*q has standard deviation about
    # alpha*q / sqrt(2*pi), plus the rounding variance 1/12.
    rng = random.Random(2)
    _, _, _, e = sample_lwe(1, 20000, 10007, 25.0, rng)
    sd = math.sqrt(sum(x * x for x in e) / len(e))
    want = math.sqrt((25.0 / math.sqrt(2 * math.pi)) ** 2 + 1 / 12)
    assert abs(sd - want) < 0.03 * want
    assert abs(sum(e) / len(e)) < 0.3


def test_noiseless_gaussian_elimination():
    rng = random.Random(3)
    for n in (1, 5, 12):
        A, b, s, _ = sample_lwe(n, 2 * n + 3, 101, 0.0, rng, bounded=0)
        assert solve_noiseless(A, b, 101) == s


def test_noiseless_fails_with_noise():
    rng = random.Random(4)
    A, b, s, e = sample_lwe(6, 30, 101, 0.0, rng, bounded=1)
    assert any(e)
    try:
        solve_noiseless(A, b, 101)
    except ValueError:
        return
    raise AssertionError("noisy samples must not look consistent")


def test_lll_small_basis():
    # A classic example: the rows reduce to vectors of norm sqrt(2) or less.
    B = [[1, 1, 1], [-1, 0, 2], [3, 5, 6]]
    R = lll(B)
    norms = sorted(sum(x * x for x in r) for r in R)
    assert norms[0] <= 2
    # Same lattice: the determinant keeps its absolute value.
    def det3(M):
        return (M[0][0] * (M[1][1] * M[2][2] - M[1][2] * M[2][1])
                - M[0][1] * (M[1][0] * M[2][2] - M[1][2] * M[2][0])
                + M[0][2] * (M[1][0] * M[2][1] - M[1][1] * M[2][0]))
    assert abs(det3(R)) == abs(det3(B))


def test_embedding_contains_error_vector():
    rng = random.Random(5)
    q = 97
    A, b, s, e = sample_lwe(5, 12, q, 2.0, rng)
    basis, order = embedding_basis(A, b, q)
    target = [e[i] for i in order] + [1]
    # (e, 1) = (b, 1) - (A s mod q + q k): it is in the lattice.
    # Check with the HNF form: coordinates 0..n-1 fix the combination.
    n = 5
    coeffs = [target[i] - 1 * basis[-1][i] for i in range(n)]
    v = [sum(c * basis[i][j] for i, c in enumerate(coeffs)) + basis[-1][j] for j in range(len(target))]
    diff = [x - y for x, y in zip(target, v)]
    assert all(d % q == 0 for d in diff)


def test_primal_attack_n10():
    rng = random.Random(6)
    q, n, m = 97, 10, 22
    ok = 0
    for _ in range(3):
        A, b, s, e = sample_lwe(n, m, q, 2.5, rng)
        got = primal_attack(A, b, q, bound=4)
        ok += got == s
    assert ok == 3


def test_primal_attack_n16():
    rng = random.Random(7)
    q, n, m = 257, 16, 32
    A, b, s, e = sample_lwe(n, m, q, 2.5, rng)
    assert primal_attack(A, b, q, bound=4) == s


def test_primal_attack_fails_on_uniform():
    rng = random.Random(8)
    q, n, m = 97, 10, 22
    A, _, _, _ = sample_lwe(n, m, q, 2.5, rng)
    b = [rng.randrange(q) for _ in range(m)]
    assert primal_attack(A, b, q, bound=4) is None


def test_normal_form():
    rng = random.Random(9)
    q, n, m = 101, 6, 30
    A, b, s, e = sample_lwe(n, m, q, 3.0, rng)
    A2, b2, rows = normal_form(A, b, q)
    e1 = [e[i] for i in rows]
    rest = [i for i in range(m) if i not in rows]
    assert residuals(A2, b2, e1, q) == [e[i] for i in rest]


def test_search_from_decision():
    rng = random.Random(10)
    q, n, m = 13, 2, 30
    A, b, s, _ = sample_lwe(n, m, q, 0.0, rng, bounded=1)
    samples = list(zip(A, b))
    decide = lambda smp: brute_force_decide(smp, n, q, 1)
    assert decide(samples)
    uniform = [(a, rng.randrange(q)) for a, _ in samples]
    assert not decide(uniform)
    assert search_from_decision(samples, n, q, decide, rng) == s


def test_random_small_noiseless():
    rng = random.Random(11)
    for _ in range(500):
        n = rng.randint(1, 4)
        q = rng.choice([5, 7, 11, 13])
        A, b, s, _ = sample_lwe(n, n + 6, q, 0.0, rng, bounded=0)
        try:
            got = solve_noiseless(A, b, q)
        except ValueError:
            continue  # rank below n: rare, allowed
        assert residuals(A, b, got, q) == [0] * len(A)
        assert got == s
