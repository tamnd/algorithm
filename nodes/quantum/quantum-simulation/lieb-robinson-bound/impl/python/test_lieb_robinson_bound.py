# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lieb-robinson-bound/. The authors are listed in prov/TYMAXR.jsonl.

import math

from lieb_robinson_bound import (
    bound_exponential,
    bound_series,
    chain_hamiltonian,
    commutator_norm,
    first_time_above,
    free_commutator_norms,
    heisenberg_bond,
    semi_infinite_norm,
    xx_bond,
)
from qsim import op_norm, pauli_on, qop_matrix

J = 1.0


def test_bond_norms():
    n = 2
    assert abs(op_norm(qop_matrix(xx_bond(J)(n, 0), n)) - J) < 1e-9
    assert abs(op_norm(qop_matrix(heisenberg_bond(J)(n, 0), n)) - 0.75 * J) < 1e-9


def test_series_is_below_the_exponential_form():
    for d in range(1, 30):
        for t in (0.01, 0.1, 0.3, 1.0, 2.0):
            assert bound_series(d, J, t) <= bound_exponential(d, J, t) * (1 + 1e-12)


def test_free_fermion_formula_matches_the_spin_chain():
    # ||[tau_t(sigma-_0), Z_d]|| computed on 2^5 amplitudes equals 2 |U_0d(t)| of the 5 x 5 hopping matrix
    n = 5
    h = chain_hamiltonian(n, xx_bond(J))
    a = {pauli_on(n, {0: "X"}): 0.5, pauli_on(n, {0: "Y"}): 0.5j}
    free = free_commutator_norms(n, J, 0.7)
    for d in range(1, n):
        (m,) = commutator_norm(n, h, a, {pauli_on(n, {d: "Z"}): 1.0}, [0.7])
        assert abs(m - free[d]) < 1e-9


def test_long_free_chain_matches_the_bessel_closed_form():
    n = 40
    for t in (1.0, 3.0):
        free = free_commutator_norms(n, J, t)
        for d in range(1, 20):
            assert abs(free[d] - semi_infinite_norm(d, J, t)) < 1e-12


def test_measured_values_are_below_the_bound():
    n = 40
    for t in (0.25, 0.5, 1.0, 2.0):
        free = free_commutator_norms(n, J, t)
        for d in range(1, 20):
            assert free[d] <= bound_series(d, J, t)
    n = 5
    h = chain_hamiltonian(n, heisenberg_bond(J))
    a = {pauli_on(n, {0: "Z"}): 1.0}
    times = [0.1, 0.25, 0.5]
    for d in range(1, n):
        got = commutator_norm(n, h, a, {pauli_on(n, {d: "Z"}): 1.0}, times)
        for t, m in zip(times, got):
            assert m <= bound_series(d, 0.75 * J, t)
    # far outside the cone both are tiny, the bound much less so
    assert semi_infinite_norm(16, J, 0.5) < 1e-17 < 1e-6 < bound_series(16, J, 0.5) < 1e-5


def test_light_cone_table():
    eps = 1e-3
    rows = {}
    for d in (4, 8, 16, 24, 32):
        t_meas = first_time_above(lambda t: semi_infinite_norm(d, J, t), eps, 0.005)
        t_bound = first_time_above(lambda t: bound_series(d, J, t), eps, 0.0005)
        rows[d] = (t_meas, t_bound)
        assert t_bound < t_meas
    assert abs(rows[16][0] - 4.556) < 1e-3 and abs(rows[32][0] - 11.474) < 1e-3
    v_meas = 8 / (rows[32][0] - rows[24][0])
    v_bound = 8 / (rows[32][1] - rows[24][1])
    assert 2.0 < v_meas < 2.4  # the true front moves at 2J
    assert 15.5 < v_bound < 6 * math.e * J + 0.5  # the series bound moves at about 6eJ
