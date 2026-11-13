# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/von-neumann-entropy/. The authors are listed in prov/AFM9DC.jsonl.

import math
import random

from qsim import (
    add,
    dagger,
    eigvalsh,
    identity,
    kron,
    matmul,
    matrix_function,
    outer,
    random_density,
    random_state,
    random_unitary,
    scale,
    trace,
    trace_out_first,
    trace_out_second,
    zeros,
)
from von_neumann_entropy import (
    binary_entropy,
    conditional_entropy,
    mutual_information,
    qubit_entropy,
    relative_entropy,
    shannon_entropy,
    von_neumann_entropy,
)

TOL = 1e-8


def diag(p):
    return [[p[i] if i == j else 0 for j in range(len(p))] for i in range(len(p))]


def test_eigenvalues_and_matrix_logarithm():
    rng = random.Random(51)
    for _ in range(40):
        d = rng.randint(2, 6)
        rho = random_density(rng, d)
        lam = eigvalsh(rho)
        power = identity(d)
        for k in range(1, d + 1):  # the power sums fix the eigenvalues
            power = matmul(power, rho)
            assert abs(sum(x**k for x in lam) - trace(power).real) < 1e-10
        log_rho = matrix_function(rho, lambda x: math.log2(x))
        assert abs(von_neumann_entropy(rho) + trace(matmul(rho, log_rho)).real) < TOL


def test_diagonal_states_and_bases():
    rng = random.Random(52)
    for _ in range(30):
        d = rng.randint(2, 6)
        p = [rng.random() for _ in range(d)]
        p = [x / sum(p) for x in p]
        u = random_unitary(rng, d)
        rho = matmul(matmul(u, diag(p)), dagger(u))
        assert abs(von_neumann_entropy(rho) - shannon_entropy(p)) < TOL
        nats = von_neumann_entropy(rho, base=math.e)
        assert abs(nats - von_neumann_entropy(rho) * math.log(2)) < TOL


def test_qubit_closed_form():
    rng = random.Random(53)
    for _ in range(100):
        rho = random_density(rng, 2)
        assert abs(von_neumann_entropy(rho) - qubit_entropy(rho)) < 1e-7
    rho = [[0.75, 0.25], [0.25, 0.25]]  # the example of the density matrix page, |r| = 1/sqrt(2)
    expected = binary_entropy((2 + math.sqrt(2)) / 4)
    assert abs(von_neumann_entropy(rho) - expected) < TOL
    assert abs(expected - 0.6009) < 1e-4


def test_bounds():
    rng = random.Random(54)
    for d in range(1, 9):
        assert abs(von_neumann_entropy(scale(1 / d, identity(d))) - math.log2(d)) < TOL
        psi = random_state(rng, d)
        assert abs(von_neumann_entropy(outer(psi, psi))) < 1e-7
        rho = random_density(rng, d)
        assert -TOL <= von_neumann_entropy(rho) <= math.log2(d) + TOL


def test_pure_bipartite_states_have_equal_parts():
    rng = random.Random(55)
    for _ in range(30):
        da, db = rng.randint(2, 4), rng.randint(2, 4)
        psi = random_state(rng, da * db)
        rho = outer(psi, psi)
        s_a = von_neumann_entropy(trace_out_second(rho, da, db))
        s_b = von_neumann_entropy(trace_out_first(rho, da, db))
        assert abs(s_a - s_b) < 1e-7
    s = 1 / math.sqrt(2)
    bell = outer([s, 0, 0, s], [s, 0, 0, s])
    assert abs(von_neumann_entropy(bell)) < 1e-7
    assert abs(von_neumann_entropy(trace_out_second(bell, 2, 2)) - 1) < TOL
    assert abs(conditional_entropy(bell, 2, 2) + 1) < 1e-7
    assert abs(mutual_information(bell, 2, 2) - 2) < 1e-7


def test_subadditivity_and_araki_lieb():
    rng = random.Random(56)
    for _ in range(60):
        da, db = rng.randint(2, 3), rng.randint(2, 3)
        rho = random_density(rng, da * db, rank=rng.randint(1, da * db))
        s_ab = von_neumann_entropy(rho)
        s_a = von_neumann_entropy(trace_out_second(rho, da, db))
        s_b = von_neumann_entropy(trace_out_first(rho, da, db))
        assert s_ab <= s_a + s_b + 1e-7
        assert abs(s_a - s_b) <= s_ab + 1e-7
        assert mutual_information(rho, da, db) >= -1e-7
    a, b = random_density(rng, 2), random_density(rng, 3)
    assert abs(mutual_information(kron(a, b), 2, 3)) < 1e-7  # equality for products


def test_strong_subadditivity_on_three_qubits():
    rng = random.Random(57)
    for _ in range(60):
        rho = random_density(rng, 8, rank=rng.randint(1, 8))
        ab = trace_out_second(rho, 4, 2)
        bc = trace_out_first(rho, 2, 4)
        b = trace_out_first(ab, 2, 2)
        lhs = von_neumann_entropy(rho) + von_neumann_entropy(b)
        rhs = von_neumann_entropy(ab) + von_neumann_entropy(bc)
        assert lhs <= rhs + 1e-7


def test_concavity_and_mixing_bound():
    rng = random.Random(58)
    for _ in range(40):
        d, m = rng.randint(2, 4), rng.randint(2, 4)
        p = [rng.random() for _ in range(m)]
        p = [x / sum(p) for x in p]
        states = [random_density(rng, d, rank=rng.randint(1, d)) for _ in range(m)]
        mix = zeros(d)
        for w, s in zip(p, states):
            mix = add(mix, scale(w, s))
        avg = sum(w * von_neumann_entropy(s) for w, s in zip(p, states))
        assert avg - 1e-7 <= von_neumann_entropy(mix) <= avg + shannon_entropy(p) + 1e-7


def test_klein_inequality():
    rng = random.Random(59)
    for _ in range(40):
        d = rng.randint(2, 4)
        rho, sigma = random_density(rng, d, rank=rng.randint(1, d)), random_density(rng, d)
        assert relative_entropy(rho, sigma) >= -1e-7
        # S(rho || I/d) = log d - S(rho)
        gap = relative_entropy(rho, scale(1 / d, identity(d))) - (math.log2(d) - von_neumann_entropy(rho))
        assert abs(gap) < 1e-7
