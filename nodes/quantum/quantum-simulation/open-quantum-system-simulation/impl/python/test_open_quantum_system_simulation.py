# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/open-quantum-system-simulation/. The authors are listed in prov/12TXF0.jsonl.

import cmath
import math
import random

from open_quantum_system_simulation import (
    apply_generator,
    choi,
    evolve,
    lindbladian,
    partial_trace_first,
    purity,
    unvec,
    vec,
)
from qsim import close, dagger, eigvalsh, identity, is_unitary, kron, matmul, matvec, trace, zeros

SM = [[0j, 1 + 0j], [0j, 0j]]  # sigma- = |0><1|, the decay |1> -> |0>
Z = [[1 + 0j, 0j], [0j, -1 + 0j]]


def random_density(d, rng):
    a = [[complex(rng.gauss(0, 1), rng.gauss(0, 1)) for _ in range(d)] for _ in range(d)]
    rho = matmul(a, dagger(a))
    tr = trace(rho)
    return [[x / tr for x in row] for row in rho]


def test_matrix_form_matches_the_formula():
    rng = random.Random(42)
    d = 2
    h = [[0.3 + 0j, 0.1 - 0.2j], [0.1 + 0.2j, -0.4 + 0j]]
    jumps = [[[x * 0.7 for x in row] for row in SM], [[x * 0.2 for x in row] for row in Z]]
    rho = random_density(d, rng)
    got = unvec(matvec(lindbladian(h, jumps), vec(rho)), d)
    assert close(got, apply_generator(h, jumps, rho), 1e-12)


def test_amplitude_damping_closed_form():
    gamma, omega = 0.8, 1.3
    h = [[omega / 2 + 0j, 0j], [0j, -omega / 2 + 0j]]
    jumps = [[[x * math.sqrt(gamma) for x in row] for row in SM]]
    rho0 = [[0.25 + 0j, 0.3 - 0.2j], [0.3 + 0.2j, 0.75 + 0j]]
    for t in (0.0, 0.5, 2.0, 5.0):
        r = evolve(h, jumps, rho0, t)
        p1 = math.exp(-gamma * t) * 0.75
        coh = cmath.exp(-1j * omega * t - gamma * t / 2) * rho0[0][1]
        assert close(r, [[1 - p1, coh], [coh.conjugate(), p1]], 1e-10)


def test_dephasing_closed_form():
    g = 0.6
    jumps = [[[x * math.sqrt(g) for x in row] for row in Z]]
    rho0 = [[0.5 + 0j, 0.5 + 0j], [0.5 + 0j, 0.5 + 0j]]
    for t in (0.3, 1.0, 3.0):
        r = evolve(zeros(2), jumps, rho0, t)
        c = 0.5 * math.exp(-2 * g * t)
        assert close(r, [[0.5, c], [c, 0.5]], 1e-10)


def test_channel_is_completely_positive_and_trace_preserving():
    # two qubits with an XX coupling, damping on qubit 0 and dephasing on qubit 1
    j, gamma, g = 1.0, 0.5, 0.2
    x = [[0j, 1 + 0j], [1 + 0j, 0j]]
    y = [[0j, -1j], [1j, 0j]]
    eye = identity(2)
    h = [[0.5 * j * (a + b) for a, b in zip(ra, rb)] for ra, rb in zip(kron(x, x), kron(y, y))]
    jumps = [
        [[v * math.sqrt(gamma) for v in row] for row in kron(eye, SM)],
        [[v * math.sqrt(g) for v in row] for row in kron(Z, eye)],
    ]
    for t in (0.4, 1.5):
        c = choi(h, jumps, t)
        assert min(eigvalsh(c)) > -1e-10
        # tracing out the output gives the identity on the input: the map preserves the trace
        d = 4
        tr_out = [[sum(c[i * d + a][k * d + a] for a in range(d)) for k in range(d)] for i in range(d)]
        assert close(tr_out, identity(d), 1e-10)


def test_purity_drops_so_no_unitary_on_the_system_does_it():
    gamma = 1.0
    jumps = [[[x * math.sqrt(gamma) for x in row] for row in SM]]
    plus = [[0.5 + 0j, 0.5 + 0j], [0.5 + 0j, 0.5 + 0j]]
    # purity(t) = 1 - e^(-t)/2 + e^(-2t)/2: it falls to 7/8 at t = ln 2 and then rises back to 1
    for t in (0.0, 0.2, 0.7, 1.5, 4.0, 12.0):
        exact = 1 - math.exp(-gamma * t) / 2 + math.exp(-2 * gamma * t) / 2
        assert abs(purity(evolve(zeros(2), jumps, plus, t)) - exact) < 1e-10
    r = evolve(zeros(2), jumps, plus, math.log(2))
    assert abs(purity(r) - 0.875) < 1e-10
    # a unitary keeps the purity fixed, so no unitary on the qubit alone gives this map
    assert purity(r) < 1 - 0.1


def test_one_ancilla_dilates_amplitude_damping():
    gamma, t = 0.9, 0.8
    p = 1 - math.exp(-gamma * t)
    c, s = math.sqrt(1 - p), math.sqrt(p)
    # basis index 2 a + q: the ancilla a is the left factor, the system q the right one
    u = zeros(4)
    u[0][0] = 1
    u[1][1], u[2][1] = c, s
    u[1][2], u[2][2] = -s, c
    u[3][3] = 1
    assert is_unitary(u)
    rho = [[0.4 + 0j, 0.1 + 0.3j], [0.1 - 0.3j, 0.6 + 0j]]
    full = kron([[1 + 0j, 0j], [0j, 0j]], rho)
    out = partial_trace_first(matmul(matmul(u, full), dagger(u)), 2, 2)
    jumps = [[[x * math.sqrt(gamma) for x in row] for row in SM]]
    assert close(out, evolve(zeros(2), jumps, rho, t), 1e-10)
