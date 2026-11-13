# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/quantum-eigenvalue-transformation/. The authors are listed in prov/6TMH0A.jsonl.

import math
import random

from quantum_eigenvalue_transformation import (
    lcu_block_encoding,
    phased_sequence,
    qet_any_parity,
    qet_real,
    reflection_phases,
)
from qsim import (
    chebyshev_t,
    eigh,
    hermitian_function,
    is_unitary,
    max_abs_diff,
    pauli_sum_matrix,
    qsp_real_phases,
    scale,
    solve_linear,
    top_left_block,
)

TOL = 1e-9


def random_terms(rng, n, big_l):
    seen, terms = set(), []
    while len(terms) < big_l:
        s = "".join(rng.choice("IXYZ") for _ in range(n))
        if s not in seen and set(s) != {"I"}:
            seen.add(s)
            terms.append((rng.uniform(-1, 1), s))
    return terms


def random_parity_polynomial(rng, d, bound):
    coeffs = [rng.uniform(-1, 1) if k % 2 == d % 2 else 0.0 for k in range(d + 1)]
    fine = [math.cos(math.pi * j / 1000) for j in range(1001)]
    peak = max(abs(sum(c * chebyshev_t(k, x) for k, c in enumerate(coeffs))) for x in fine)
    coeffs = [c * bound / peak for c in coeffs]
    return lambda x: sum(c * chebyshev_t(k, x) for k, c in enumerate(coeffs))


def test_zero_phases_give_chebyshev_polynomials_of_the_matrix():
    rng = random.Random(51)
    terms = random_terms(rng, 2, 3)
    u, alpha, a = lcu_block_encoding(terms)
    hn = scale(1 / alpha, pauli_sum_matrix(terms))
    for d in range(1, 6):
        m = phased_sequence(u, 4, reflection_phases([0.0] * (d + 1)))
        target = scale((-1j) ** d, hermitian_function(hn, lambda x: chebyshev_t(d, x)))
        assert max_abs_diff(top_left_block(m, 4), target) < TOL


def test_real_polynomials_of_definite_parity():
    rng = random.Random(52)
    terms = random_terms(rng, 2, 3)
    u, alpha, a = lcu_block_encoding(terms)
    hn = scale(1 / alpha, pauli_sum_matrix(terms))
    for d in [2, 3, 4, 5]:
        f = random_parity_polynomial(rng, d, 0.9)
        q = qet_real(u, a, 2, f, d)
        assert len(q) == 1 << (1 + a + 2) and is_unitary(q, 1e-9)
        assert max_abs_diff(top_left_block(q, 4), hermitian_function(hn, f)) < TOL


def test_one_branch_alone_gives_a_complex_polynomial():
    # Without the average over Phi and -Phi, the block is P(H/alpha) with Re P = f, and Im P is not small.
    rng = random.Random(53)
    terms = random_terms(rng, 1, 2)
    u, alpha, a = lcu_block_encoding(terms)
    hn = scale(1 / alpha, pauli_sum_matrix(terms))
    f = lambda x: 0.5 * x ** 3 - 0.2 * x
    ph = qsp_real_phases(f, 3)
    m = scale(1j ** 3, phased_sequence(u, 2, reflection_phases(ph)))
    blk = top_left_block(m, 2)
    herm_part = [[(blk[i][j] + blk[j][i].conjugate()) / 2 for j in range(2)] for i in range(2)]
    assert max_abs_diff(herm_part, hermitian_function(hn, f)) < TOL
    assert max_abs_diff(blk, hermitian_function(hn, f)) > 0.1


def test_arbitrary_parity_by_mixing_even_and_odd_parts():
    rng = random.Random(54)
    terms = random_terms(rng, 1, 2)
    u, alpha, a = lcu_block_encoding(terms)
    hn = scale(1 / alpha, pauli_sum_matrix(terms))
    f = lambda x: 0.25 + 0.2 * x - 0.15 * x ** 2 + 0.1 * x ** 3  # |f| <= 1/2 on [-1, 1]
    q = qet_any_parity(u, a, 1, f, 3)
    assert len(q) == 1 << (2 + a + 1) and is_unitary(q, 1e-9)
    assert max_abs_diff(top_left_block(q, 2), hermitian_function(hn, f)) < TOL


def test_the_linear_system_example():
    # H = 0.6 X + 0.2 Z + 0.1 I, alpha = 0.9, and an odd degree-5 fit p of 1/(2x) on [1/2, 1].
    c = [3.02619, -5.376791, 2.891417]
    p = lambda x: c[0] * x + c[1] * x ** 3 + c[2] * x ** 5
    terms = [(0.6, "X"), (0.2, "Z"), (0.1, "I")]
    h = pauli_sum_matrix(terms)
    u, alpha, a = lcu_block_encoding(terms)
    assert abs(alpha - 0.9) < 1e-12 and a == 2
    vals, _ = eigh(h)
    assert abs(max(vals) - (0.1 + math.sqrt(0.4))) < 1e-12 and abs(min(vals) - (0.1 - math.sqrt(0.4))) < 1e-12
    q = qet_real(u, a, 1, p, 5)
    assert len(q) == 16
    out = [top_left_block(q, 2)[0][0], top_left_block(q, 2)[1][0]]  # the block applied to b = |0>
    prob = sum(abs(z) ** 2 for z in out)
    assert abs(prob - 0.5031408542771751) < 1e-9
    x = solve_linear(h, [1.0, 0.0])  # the exact solution of H x = b
    assert abs(x[0] - 10 / 39) < 1e-12 and abs(x[1] - 60 / 39) < 1e-12
    nx = math.sqrt(sum(abs(z) ** 2 for z in x))
    overlap = abs(sum(z.conjugate() * w for z, w in zip(out, x))) / (math.sqrt(prob) * nx)
    assert abs(overlap ** 2 - 0.9985309043876582) < 1e-9
