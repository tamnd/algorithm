# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/block-encoding/. The authors are listed in prov/5SF402.jsonl.

import math
import random

from block_encoding import apply_block, lcu_block_encoding, product_block_encoding, sparse_block_encoding
from qsim import (
    dagger,
    identity,
    is_unitary,
    matmul,
    matvec,
    max_abs_diff,
    norm,
    op_norm,
    pauli_sum_matrix,
    random_state,
    scale,
    top_left_block,
)

EXACT = 1e-12


def random_terms(rng, n, big_l):
    letters = "IXYZ"
    seen, terms = set(), []
    while len(terms) < big_l:
        s = "".join(rng.choice(letters) for _ in range(n))
        if s not in seen and set(s) != {"I"}:
            seen.add(s)
            terms.append((rng.uniform(-1, 1), s))
    return terms


def test_hand_example_x_plus_z():
    # H = X + Z: PREP is the Hadamard gate, alpha = 2, and every block of U is (X + Z)/2 or (X - Z)/2.
    u, alpha, a = lcu_block_encoding([(1.0, "X"), (1.0, "Z")])
    assert alpha == 2.0 and a == 1
    r = 0.5
    expected = [[r, r, -r, r], [r, -r, r, r], [-r, r, r, r], [r, r, r, -r]]
    assert max_abs_diff(u, expected) < EXACT


def test_pauli_lcu_top_left_block_is_h_over_lambda():
    rng = random.Random(11)
    for n, big_l in [(1, 3), (2, 4), (2, 5), (3, 6)]:
        terms = random_terms(rng, n, big_l)
        u, alpha, a = lcu_block_encoding(terms)
        h = pauli_sum_matrix(terms)
        assert abs(alpha - sum(abs(c) for c, _ in terms)) < EXACT
        assert is_unitary(u, 1e-10)
        assert max_abs_diff(top_left_block(u, 1 << n), scale(1 / alpha, h)) < EXACT
        # SELECT is Hermitian and PREP is a Householder reflection, so U is Hermitian and U^2 = I.
        assert max_abs_diff(u, dagger(u)) < EXACT
        assert max_abs_diff(matmul(u, u), identity(len(u))) < 1e-10


def test_sparse_top_left_block_is_h_over_s_max_entry():
    rng = random.Random(12)
    d = 4
    for _ in range(4):
        h = [[0j] * d for _ in range(d)]
        for j in range(d):
            h[j][j] = complex(rng.uniform(-1, 1))  # negative diagonal entries are allowed
        for j, k in [(0, 1), (2, 3), (0, 3)]:
            z = complex(rng.uniform(-1, 1), rng.uniform(-1, 1))
            h[j][k], h[k][j] = z, z.conjugate()
        u, alpha, a = sparse_block_encoding(h)
        s = max(sum(1 for x in row if x != 0) for row in h)
        big_x = max(abs(x) for row in h for x in row)
        assert a == 3 and abs(alpha - s * big_x) < EXACT
        assert is_unitary(u, 1e-10)
        assert max_abs_diff(top_left_block(u, d), scale(1 / alpha, h)) < EXACT


def test_sparse_encoding_of_a_non_hermitian_matrix():
    # The construction never uses Hermiticity: a random 2-sparse complex matrix works too.
    rng = random.Random(13)
    d = 4
    h = [[0j] * d for _ in range(d)]
    for j in range(d):
        for k in rng.sample(range(d), 2):
            h[j][k] = complex(rng.uniform(-1, 1), rng.uniform(-1, 1))
    u, alpha, _ = sparse_block_encoding(h)
    assert max_abs_diff(top_left_block(u, d), scale(1 / alpha, h)) < EXACT


def test_alpha_is_at_least_the_norm():
    rng = random.Random(14)
    for _ in range(5):
        terms = random_terms(rng, 2, 4)
        _, alpha, _ = lcu_block_encoding(terms)
        assert op_norm(pauli_sum_matrix(terms)) <= alpha + 1e-12


def test_product_of_block_encodings():
    rng = random.Random(15)
    ta = random_terms(rng, 1, 2)
    tb = random_terms(rng, 1, 3)
    ua, alpha, aa = lcu_block_encoding(ta)
    ub, beta, ab = lcu_block_encoding(tb)
    u, ab_norm, a = product_block_encoding(ua, alpha, aa, ub, beta, ab, 1)
    assert a == aa + ab and is_unitary(u, 1e-10)
    target = scale(1 / ab_norm, matmul(pauli_sum_matrix(ta), pauli_sum_matrix(tb)))
    assert max_abs_diff(top_left_block(u, 2), target) < EXACT


def test_post_selection_applies_h_with_probability_norm_squared_over_alpha_squared():
    rng = random.Random(16)
    terms = random_terms(rng, 2, 4)
    u, alpha, a = lcu_block_encoding(terms)
    h = pauli_sum_matrix(terms)
    for _ in range(3):
        psi = random_state(2, rng)
        p, out = apply_block(u, a, psi)
        hpsi = matvec(h, psi)
        assert abs(p - (norm(hpsi) / alpha) ** 2) < EXACT
        assert max(abs(x - y / norm(hpsi)) for x, y in zip(out, hpsi)) < 1e-10
    assert math.isclose(sum(abs(c) for c, _ in terms), alpha)
