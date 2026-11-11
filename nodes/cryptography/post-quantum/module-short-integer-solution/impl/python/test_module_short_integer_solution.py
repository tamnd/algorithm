# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/module-short-integer-solution/. The authors are listed in prov/2Y9DFJ.jsonl.
"""Tests for the Module-SIS generator, checker and toy solver.

Module-SIS is a problem, not a standard algorithm, so there are no official
test vectors. The ML-DSA shapes are checked against FIPS 204, Table 1.
"""

import random

from module_short_integer_solution import (
    as_sis_matrix,
    birthday_solver,
    generate_instance,
    inf_norm,
    is_solution,
    mat_vec,
    ml_dsa_shape,
    poly_mul,
)


def test_poly_mul_wraps_with_minus_sign():
    assert poly_mul([0, 0, 0, 1], [0, 1, 0, 0], 17) == [16, 0, 0, 0]


def test_matrix_form_matches_ring_form():
    rng = random.Random(1)
    n, k, l, q = 4, 2, 3, 97
    A = generate_instance(n, k, l, q, rng)
    M = as_sis_matrix(A, q)
    assert len(M) == k * n and len(M[0]) == l * n
    for _ in range(500):
        z = [[rng.randint(-2, 2) % q for _ in range(n)] for _ in range(l)]
        flat = [c for p in z for c in p]
        want = [sum(x * y for x, y in zip(row, flat)) % q for row in M]
        assert [c for p in mat_vec(A, z, q) for c in p] == want


def test_solver_rank_two_module():
    # n = 2, k = 2, l = 8, q = 17: 2^16 binary inputs, 17^4 outputs.
    rng = random.Random(2)
    for _ in range(5):
        A = generate_instance(2, 2, 8, 17, rng)
        z = birthday_solver(A, 17, rng)
        assert is_solution(A, z, 17, beta=1)
        assert inf_norm(z) == 1


def test_solver_ring_case():
    # k = 1 is Ring-SIS: n = 4, l = 4, q = 17.
    rng = random.Random(3)
    A = generate_instance(4, 1, 4, 17, rng)
    z = birthday_solver(A, 17, rng)
    assert is_solution(A, z, 17, beta=1)


def test_checker_rejects():
    rng = random.Random(4)
    n, k, l, q = 2, 2, 8, 17
    A = generate_instance(n, k, l, q, rng)
    z = birthday_solver(A, q, rng)
    assert not is_solution(A, [[0] * n for _ in range(l)], q, 1)  # zero
    big = [[c * q for c in p] for p in z]
    assert not is_solution(A, big, q, 1)  # A big = 0 but too long
    assert is_solution(A, big, q, q)
    bad = [list(p) for p in z]
    i = next(i for i, p in enumerate(bad) if any(p))
    bad[i] = [0] * n
    bad[i][0] = 1
    flat_bad = [c for p in bad for c in p]
    if any(c for p in mat_vec(A, [[c % q for c in p] for p in bad], q) for c in p):
        assert not is_solution(A, bad, q, 1)
    assert len(flat_bad) == l * n
    assert not is_solution(A, z[:-1], q, 1)  # wrong length


def test_trivial_solution_from_identity_block():
    # For [A | I], z = (e_1, -A e_1 mod q) solves A' z = 0 but is long.
    rng = random.Random(5)
    n, k, l, q = 4, 2, 2, 101
    A = generate_instance(n, k, l, q, rng)
    ident = [[[1 if (i == j and t == 0) else 0 for t in range(n)] for j in range(k)] for i in range(k)]
    Ap = [A[i] + ident[i] for i in range(k)]
    e1 = [[1] + [0] * (n - 1)] + [[0] * n for _ in range(l - 1)]
    neg = [[(-c) % q for c in p] for p in mat_vec(A, e1, q)]
    z = e1 + [[c if c <= q // 2 else c - q for c in p] for p in neg]
    assert is_solution(Ap, z, q, beta=q // 2)
    assert not is_solution(Ap, z, q, beta=1)


def test_ml_dsa_shapes():
    assert ml_dsa_shape("ML-DSA-44") == (256, 4, 4, 8380417)
    assert ml_dsa_shape("ML-DSA-65") == (256, 6, 5, 8380417)
    assert ml_dsa_shape("ML-DSA-87") == (256, 8, 7, 8380417)
    assert 8380417 == 2**23 - 2**13 + 1
