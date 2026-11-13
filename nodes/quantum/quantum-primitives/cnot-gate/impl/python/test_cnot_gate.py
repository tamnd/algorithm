# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cnot-gate/. The authors are listed in prov/TC4WH0.jsonl.

import itertools
import math
import random

from cnot_gate import CNOT, H, X, bell_state, cnot, cnot_permutation, is_product_2q
from qsim import add, apply_1q, basis_state, circuit_matrix, close, dagger, identity, inner, is_unitary, matmul, matvec

I = identity(2)
Y = [[0j, -1j], [1j, 0j]]
Z = [[1 + 0j, 0j], [0j, -1 + 0j]]
P0 = [[1 + 0j, 0j], [0j, 0j]]
P1 = [[0j, 0j], [0j, 1 + 0j]]
R2 = math.sqrt(0.5)


def kron(a, b):
    p = len(b)
    return [[a[r // p][c // p] * b[r % p][c % p] for c in range(len(a) * p)] for r in range(len(a) * p)]


def test_matrix_truth_table_and_inverse() -> None:
    assert is_unitary(CNOT) and close(CNOT, dagger(CNOT))
    assert close(matmul(CNOT, CNOT), identity(4))
    assert close(CNOT, add(kron(P0, I), kron(P1, X)))  # |0><0| (x) I + |1><1| (x) X
    for a, b in itertools.product((0, 1), repeat=2):
        assert close(matvec(CNOT, basis_state(2, 2 * a + b)), basis_state(2, 2 * a + (a ^ b)))
    assert close(circuit_matrix(2, lambda s: cnot(s, 1, 0)), CNOT)


def test_register_permutations() -> None:
    rng = random.Random(23)
    n = 5
    for _ in range(20):
        c, t = rng.sample(range(n), 2)
        perm = cnot_permutation(n, c, t)
        assert sorted(perm) == list(range(1 << n))
        for x in range(1 << n):
            assert perm[x] == x ^ (((x >> c) & 1) << t)
            assert perm[perm[x]] == x
        s = [complex(rng.gauss(0, 1), rng.gauss(0, 1)) for _ in range(1 << n)]
        assert close(cnot(s, c, t), [s[perm[x]] for x in range(1 << n)])  # perm is an involution


def test_bell_states() -> None:
    r = R2
    expected = {
        (0, 0): [r, 0, 0, r],
        (0, 1): [0, r, r, 0],
        (1, 0): [r, 0, 0, -r],
        (1, 1): [0, r, -r, 0],
    }
    states = {k: bell_state(*k) for k in expected}
    for k, v in expected.items():
        assert close(states[k], v)
        assert not is_product_2q(states[k])
    for j, k in itertools.product(expected, repeat=2):
        assert abs(inner(states[j], states[k]) - (1 if j == k else 0)) < 1e-12


def test_swap_and_reversal() -> None:
    swap = circuit_matrix(2, lambda s: cnot(cnot(cnot(s, 1, 0), 0, 1), 1, 0))
    for a, b in itertools.product((0, 1), repeat=2):
        assert close(matvec(swap, basis_state(2, 2 * a + b)), basis_state(2, 2 * b + a))
    hh = kron(H, H)
    reversed_cnot = circuit_matrix(2, lambda s: cnot(s, 0, 1))
    assert close(matmul(hh, matmul(CNOT, hh)), reversed_cnot)
    assert not close(reversed_cnot, CNOT)


def test_pauli_conjugation() -> None:
    # left letter = control (qubit 1), right letter = target (qubit 0)
    table = [
        ((X, I), kron(X, X)),
        ((I, X), kron(I, X)),
        ((Z, I), kron(Z, I)),
        ((I, Z), kron(Z, Z)),
        ((Y, I), kron(Y, X)),
        ((I, Y), kron(Z, Y)),
    ]
    for (a, b), out in table:
        assert close(matmul(CNOT, matmul(kron(a, b), CNOT)), out)


def test_superpositions_and_kickback() -> None:
    plus = [R2, R2]
    minus = [R2, -R2]
    zero = [1, 0]
    # CNOT (|+> (x) |0>) is the Bell state, not |+> (x) |+>
    out = matvec(CNOT, [a * b for a in plus for b in zero])
    assert close(out, [R2, 0, 0, R2])
    assert not close(out, [a * b for a in plus for b in plus])
    # copying works only on basis states
    rng = random.Random(29)
    for _ in range(10):
        t = rng.uniform(0.1, math.pi / 2 - 0.1)
        psi = [math.cos(t), math.sin(t)]
        assert not close(matvec(CNOT, [a * b for a in psi for b in zero]), [a * b for a in psi for b in psi])
    # |+>|+> is unchanged and |+>|-> becomes |->|->: the phase goes back to the control
    pp = [a * b for a in plus for b in plus]
    assert close(matvec(CNOT, pp), pp)
    assert close(matvec(CNOT, [a * b for a in plus for b in minus]), [a * b for a in minus for b in minus])
    # H on the control then CNOT, built with the simulator
    s = cnot(apply_1q(basis_state(2, 0), H, 1), 1, 0)
    assert close(s, [R2, 0, 0, R2])
