# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/optimal-hamiltonian-simulation/. The authors are listed in prov/WBXH9G.jsonl.

import cmath
import math
import random

from optimal_hamiltonian_simulation import (
    KAPPA,
    amplified_block,
    chebyshev_sum,
    degree_for,
    error_bound,
    jacobi_anger,
    lcu_block_encoding,
    qet_real,
    select_two,
    simulate,
    truncation_error,
)
from qsim import (
    expm_hermitian,
    scale,
    hermitian_function,
    is_unitary,
    max_abs_diff,
    op_norm,
    pauli_sum_matrix,
    sub,
    top_left_block,
)

EXAMPLE = [(0.6, "X"), (0.3, "Z"), (0.1, "Y")]


def random_terms(rng, n, big_l):
    seen, terms = set(), []
    while len(terms) < big_l:
        s = "".join(rng.choice("IXYZ") for _ in range(n))
        if s not in seen and set(s) != {"I"}:
            seen.add(s)
            terms.append((rng.uniform(-1, 1), s))
    return terms


def test_jacobi_anger_truncation_is_within_its_bound():
    grid = [math.cos(math.pi * j / 400) for j in range(401)]
    for tau in [0.5, 2.0, 5.0]:
        for big_r in [1, 3, 6]:
            cos_c, sin_c = jacobi_anger(tau, big_r)
            pc, ps = chebyshev_sum(cos_c), chebyshev_sum(sin_c)
            ec = max(abs(pc(x) - math.cos(tau * x)) for x in grid)
            es = max(abs(ps(x) - math.sin(tau * x)) for x in grid)
            assert max(ec, es) <= truncation_error(tau, big_r) + 1e-12
            assert len(cos_c) == 2 * big_r + 1 and len(sin_c) == 2 * big_r + 2


def test_the_lcu_block_is_a_multiple_of_the_truncated_exponential():
    u, alpha, a = lcu_block_encoding(EXAMPLE)
    hn = scale(1 / alpha, pauli_sum_matrix(EXAMPLE))
    tau, big_r = 3.0, 4
    cos_c, sin_c = jacobi_anger(tau, big_r)
    pc = chebyshev_sum([KAPPA * c for c in cos_c])
    ps = chebyshev_sum([KAPPA * c for c in sin_c])
    v = select_two(qet_real(u, 2, pc, 2 * big_r), scale(-1j, qet_real(u, 2, ps, 2 * big_r + 1)))
    assert len(v) == 32 and is_unitary(v, 1e-9)
    want = hermitian_function(hn, lambda x: (pc(x) - 1j * ps(x)) / 2)
    assert max_abs_diff(top_left_block(v, 2), want) < 1e-9
    ideal = hermitian_function(hn, lambda x: math.sin(math.pi / 10) * cmath.exp(-1j * tau * x))
    assert max_abs_diff(top_left_block(v, 2), ideal) < KAPPA * truncation_error(tau, big_r)


def test_two_rounds_apply_the_fifth_order_polynomial_to_the_block():
    u, alpha, a = lcu_block_encoding(EXAMPLE)
    for big_r in [2, 4]:
        g = simulate(u, alpha, 1, 3.0, big_r)
        tau = alpha * 3.0
        cos_c, sin_c = jacobi_anger(tau, big_r)
        pc = chebyshev_sum([KAPPA * c for c in cos_c])
        ps = chebyshev_sum([KAPPA * c for c in sin_c])
        v = select_two(qet_real(u, 2, pc, 2 * big_r), scale(-1j, qet_real(u, 2, ps, 2 * big_r + 1)))
        assert max_abs_diff(top_left_block(g, 2), amplified_block(top_left_block(v, 2))) < 1e-9


def test_the_error_is_below_its_bound():
    h = pauli_sum_matrix(EXAMPLE)
    u, alpha, a = lcu_block_encoding(EXAMPLE)
    want = {2: 0.0059537, 3: 0.00087866, 4: 1.01547e-5, 5: 3.7013e-7, 6: 2.955e-9}
    for big_r, err0 in want.items():
        g = simulate(u, alpha, 1, 3.0, big_r)
        assert is_unitary(g, 1e-9)
        err = op_norm(sub(top_left_block(g, 2), expm_hermitian(h, 3.0)))
        assert err <= error_bound(3.0, big_r)
        assert abs(err / err0 - 1) < 1e-3


def test_random_two_qubit_hamiltonians():
    rng = random.Random(81)
    for _ in range(2):
        terms = random_terms(rng, 2, 4)
        h = pauli_sum_matrix(terms)
        u, alpha, a = lcu_block_encoding(terms)
        t = rng.uniform(0.5, 2.0)
        big_r = degree_for(alpha * t, 1e-9)
        g = simulate(u, alpha, 2, t, big_r)
        assert len(g) == 1 << (2 + a + 2)
        err = op_norm(sub(top_left_block(g, 4), expm_hermitian(h, t)))
        assert err <= error_bound(alpha * t, big_r) and err < 1e-8


def test_the_degree_grows_as_tau_plus_log_of_one_over_epsilon():
    table = {1: [5, 9, 11], 2: [7, 11, 13], 4: [11, 15, 17], 8: [15, 21, 25]}
    for tau, degs in table.items():
        assert [2 * degree_for(tau, e) + 1 for e in [1e-3, 1e-6, 1e-9]] == degs
