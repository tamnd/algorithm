# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/partial-trace/. The authors are listed in prov/Z8AWR0.jsonl.

import math
import random

from partial_trace import partial_trace, trace_out_qubits, trace_out_second_by_sandwich
from qsim import (
    H,
    apply_1q,
    eigvalsh,
    identity,
    is_hermitian,
    kron,
    kron_vec,
    matmul,
    max_abs_diff,
    outer,
    random_density,
    random_state,
    random_unitary,
    scale,
    trace,
    trace_out_first,
    trace_out_second,
)

TOL = 1e-9


def random_matrix(rng, d):
    return [[complex(rng.gauss(0, 1), rng.gauss(0, 1)) for _ in range(d)] for _ in range(d)]


def is_state(rho):
    return is_hermitian(rho) and abs(trace(rho) - 1) < TOL and eigvalsh(rho)[0] > -TOL


def test_product_operators():
    rng = random.Random(11)
    for _ in range(40):
        da, db = rng.randint(1, 4), rng.randint(1, 4)
        a, b = random_matrix(rng, da), random_matrix(rng, db)
        ab = kron(a, b)
        assert max_abs_diff(partial_trace(ab, [da, db], [0]), scale(trace(b), a)) < TOL
        assert max_abs_diff(partial_trace(ab, [da, db], [1]), scale(trace(a), b)) < TOL


def test_bell_state_gives_maximally_mixed_parts():
    s = 1 / math.sqrt(2)
    bell = outer([s, 0, 0, s], [s, 0, 0, s])
    half = scale(0.5, identity(2))
    assert max_abs_diff(partial_trace(bell, [2, 2], [0]), half) < TOL
    assert max_abs_diff(partial_trace(bell, [2, 2], [1]), half) < TOL
    assert abs(trace(matmul(bell, bell)) - 1) < TOL  # the whole state is pure


def test_defining_property_on_random_states():
    rng = random.Random(12)
    for _ in range(40):
        da, db = rng.randint(2, 4), rng.randint(2, 4)
        rho = random_density(rng, da * db)
        xa, xb = random_matrix(rng, da), random_matrix(rng, db)
        rho_a = partial_trace(rho, [da, db], [0])
        rho_b = partial_trace(rho, [da, db], [1])
        lhs_a = trace(matmul(rho_a, xa))
        rhs_a = trace(matmul(rho, kron(xa, identity(db))))
        assert abs(lhs_a - rhs_a) < TOL
        lhs_b = trace(matmul(rho_b, xb))
        rhs_b = trace(matmul(rho, kron(identity(da), xb)))
        assert abs(lhs_b - rhs_b) < TOL
        assert is_state(rho_a) and is_state(rho_b)


def test_three_methods_agree():
    rng = random.Random(13)
    for _ in range(30):
        da, db = rng.randint(1, 4), rng.randint(1, 4)
        rho = random_density(rng, da * db)
        general = partial_trace(rho, [da, db], [0])
        assert max_abs_diff(general, trace_out_second(rho, da, db)) < TOL
        assert max_abs_diff(general, trace_out_second_by_sandwich(rho, da, db)) < TOL
        assert max_abs_diff(partial_trace(rho, [da, db], [1]), trace_out_first(rho, da, db)) < TOL


def test_three_qubit_states():
    ghz = [0j] * 8
    ghz[0] = ghz[7] = 1 / math.sqrt(2)
    rho = outer(ghz, ghz)
    two = trace_out_qubits(rho, 3, [2])
    expected = [[0.5 if (i == j and i in (0, 3)) else 0 for j in range(4)] for i in range(4)]
    assert max_abs_diff(two, expected) < TOL
    w = [0j] * 8
    w[1] = w[2] = w[4] = 1 / math.sqrt(3)
    one = trace_out_qubits(outer(w, w), 3, [1, 2])
    assert max_abs_diff(one, [[2 / 3, 0], [0, 1 / 3]]) < TOL


def test_qubit_order_convention():
    # |q2 q1 q0> = |1>|0>|+>: qubit 0 is the least significant bit.
    plus = apply_1q([1, 0], H, 0)
    psi = kron_vec([0, 1], kron_vec([1, 0], plus))
    rho = outer(psi, psi)
    assert max_abs_diff(trace_out_qubits(rho, 3, [1, 2]), outer(plus, plus)) < TOL
    assert max_abs_diff(trace_out_qubits(rho, 3, [0, 1]), [[0, 0], [0, 1]]) < TOL


def test_trace_out_in_steps():
    rng = random.Random(14)
    for _ in range(20):
        dims = [rng.randint(2, 3) for _ in range(3)]
        rho = random_density(rng, dims[0] * dims[1] * dims[2])
        at_once = partial_trace(rho, dims, [0])
        steps = partial_trace(partial_trace(rho, dims, [0, 1]), dims[:2], [0])
        assert max_abs_diff(at_once, steps) < TOL
        middle = partial_trace(rho, dims, [1])
        other = partial_trace(partial_trace(rho, dims, [1, 2]), dims[1:], [0])
        assert max_abs_diff(middle, other) < TOL


def test_local_unitary_on_traced_part_does_nothing():
    rng = random.Random(15)
    for _ in range(30):
        da, db = rng.randint(2, 3), rng.randint(2, 3)
        psi = random_state(rng, da * db)
        rho = outer(psi, psi)
        u = kron(identity(da), random_unitary(rng, db))
        moved = matmul(matmul(u, rho), [[x.conjugate() for x in row] for row in zip(*u)])
        assert max_abs_diff(partial_trace(rho, [da, db], [0]), partial_trace(moved, [da, db], [0])) < 1e-8


def test_pure_state_parts_share_nonzero_spectrum():
    rng = random.Random(16)
    for _ in range(30):
        da, db = rng.randint(2, 4), rng.randint(2, 4)
        psi = random_state(rng, da * db)
        rho = outer(psi, psi)
        ea = [x for x in eigvalsh(partial_trace(rho, [da, db], [0])) if x > 1e-9]
        eb = [x for x in eigvalsh(partial_trace(rho, [da, db], [1])) if x > 1e-9]
        assert len(ea) == len(eb) == min(da, db)
        assert max(abs(x - y) for x, y in zip(ea, eb)) < 1e-8
