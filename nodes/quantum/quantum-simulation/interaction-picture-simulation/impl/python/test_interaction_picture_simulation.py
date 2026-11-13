# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/interaction-picture-simulation/. The authors are listed in prov/514Y6M.jsonl.

import math
import random

from interaction_picture_simulation import (
    discretization_bound,
    dyson_lcu,
    error_bound,
    ip_simulate,
    midpoint_product,
    midpoints,
    segments,
    tail,
)
from qsim import (
    add,
    commutator,
    dagger,
    expm_hermitian,
    identity,
    matmul,
    matvec,
    max_abs_diff,
    norm,
    op_norm,
    pauli_sum_matrix,
    scale,
    sub,
)

A_TERMS = [(2.0, "ZI"), (1.0, "IZ")]
B_TERMS = [(0.3, "XX"), (0.2, "IX")]
PSI = [0.5 + 0j, 0.5j, -0.5 + 0j, 0.5 + 0j]


def lcu_sum(betas, unitaries):
    d = len(unitaries[0])
    out = [[0j] * d for _ in range(d)]
    for beta, u in zip(betas, unitaries):
        for i in range(d):
            for j in range(d):
                out[i][j] += beta * u[i][j]
    return out


def truncated_product(a, b, tau, big_m, big_k):
    """The terms of degree <= K in h of the product of e^(-i h H_I(s_q)), by polynomial arithmetic."""
    d = len(a)
    h = tau / big_m
    poly = [identity(d)] + [[[0j] * d for _ in range(d)] for _ in range(big_k)]
    for s in midpoints(tau, big_m):
        h_i = matmul(expm_hermitian(a, -s), matmul(b, expm_hermitian(a, s)))
        factor, power = [], identity(d)
        for j in range(big_k + 1):
            factor.append(scale((-1j * h) ** j / math.factorial(j), power))
            power = matmul(h_i, power)
        new = [[[0j] * d for _ in range(d)] for _ in range(big_k + 1)]
        for i, f in enumerate(factor):
            for j, p in enumerate(poly):
                if i + j <= big_k:
                    new[i + j] = add(new[i + j], matmul(f, p))
        poly = new
    out = poly[0]
    for p in poly[1:]:
        out = add(out, p)
    return out


def constants(a, b):
    return op_norm(commutator(a, b)), op_norm(commutator(a, commutator(a, b)))


def test_the_lcu_sum_is_the_truncated_midpoint_product():
    a, b = pauli_sum_matrix(A_TERMS), pauli_sum_matrix(B_TERMS)
    for big_m, big_k in [(2, 3), (4, 2), (3, 1)]:
        betas, unitaries = dyson_lcu(a, B_TERMS, 1.0, big_m, big_k)
        assert len(betas) == sum((2 * big_m) ** k for k in range(big_k + 1))
        assert abs(sum(betas) - sum(0.5 ** k / math.factorial(k) for k in range(big_k + 1))) < 1e-12
        assert max_abs_diff(lcu_sum(betas, unitaries), truncated_product(a, b, 1.0, big_m, big_k)) < 1e-12


def test_the_series_tends_to_the_product_of_exponentials():
    a, b = pauli_sum_matrix(A_TERMS), pauli_sum_matrix(B_TERMS)
    full = midpoint_product(a, b, 1.0, 4)
    for big_k in [1, 3, 6]:
        err = op_norm(sub(truncated_product(a, b, 1.0, 4, big_k), full))
        assert err <= tail(0.5, big_k) + 1e-12


def test_the_midpoint_rule_has_order_two():
    a, b = pauli_sum_matrix(A_TERMS), pauli_sum_matrix(B_TERMS)
    c1, c2 = constants(a, b)
    exact = matmul(expm_hermitian(a, -1.0), expm_hermitian(add(a, b), 1.0))
    errs = {}
    for big_m in [4, 8, 16, 32, 64]:
        errs[big_m] = op_norm(sub(midpoint_product(a, b, 1.0, big_m), exact))
        assert errs[big_m] <= discretization_bound(0.5, c1, c2, 1.0, big_m)
    for big_m in [8, 16, 32, 64]:
        assert 3.9 < errs[big_m // 2] / errs[big_m] < 4.4
    assert abs(errs[8] / 0.0012149 - 1) < 1e-3 and abs(errs[64] / 1.88872e-5 - 1) < 1e-3


def test_the_circuit_on_the_example():
    a, b = pauli_sum_matrix(A_TERMS), pauli_sum_matrix(B_TERMS)
    h = add(a, b)
    c1, c2 = constants(a, b)
    exact = matvec(expm_hermitian(h, 2.0), PSI)
    want = {(2, 3): 0.029254, (4, 1): 0.045346, (4, 2): 0.013064, (4, 3): 0.0061062, (8, 2): 0.0088357}
    for (big_m, big_k), err0 in want.items():
        out, prob, r = ip_simulate(a, B_TERMS, 2.0, big_m, big_k, PSI)
        assert r == 2
        err = norm([x - y for x, y in zip(out, exact)])
        assert abs(err / err0 - 1) < 1e-3
        assert err <= error_bound(0.5, c1, c2, 2.0, big_m, big_k)
        assert abs(prob - norm(out) ** 2) < 1e-12 and prob > 0.99
        d = lcu_sum(*dyson_lcu(a, B_TERMS, 1.0, big_m, big_k))
        seg = sub(scale(1.5, d), scale(0.5, matmul(d, matmul(dagger(d), d))))
        state = list(PSI)
        for _ in range(r):
            state = matvec(expm_hermitian(a, 1.0), matvec(seg, state))
        assert norm([x - y for x, y in zip(out, state)]) < 1e-12


def test_the_segments_depend_only_on_b():
    for factor in [1, 10, 100]:
        lam = sum(abs(c) for c, _ in B_TERMS)
        assert segments(lam, 2.0) == (2, 1.0)
        assert len(dyson_lcu(scale(factor, pauli_sum_matrix(A_TERMS)), B_TERMS, 1.0, 2, 2)[0]) == 21
    lam_all = sum(abs(c) for c, _ in A_TERMS + B_TERMS)
    assert segments(lam_all, 2.0)[0] == 11


def test_random_two_qubit_hamiltonians():
    rng = random.Random(514)
    for _ in range(3):
        a_terms = [(rng.uniform(-2, 2), s) for s in ["ZI", "IZ", "ZZ"]]
        b_terms = [(rng.uniform(-0.3, 0.3), s) for s in rng.sample(["XI", "IX", "XX", "YY", "XZ", "ZY"], 2)]
        a, b = pauli_sum_matrix(a_terms), pauli_sum_matrix(b_terms)
        c1, c2 = constants(a, b)
        lam = sum(abs(c) for c, _ in b_terms)
        t = rng.uniform(0.5, 2.0)
        out, prob, r = ip_simulate(a, b_terms, t, 8, 2, PSI)
        err = norm([x - y for x, y in zip(out, matvec(expm_hermitian(add(a, b), t), PSI))])
        assert err <= error_bound(lam, c1, c2, t, 8, 2)
        assert prob > 0.99
