# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/phase-and-t-gates/. The authors are listed in prov/XQY3VF.jsonl.

import cmath
import math
import random

from phase_and_t_gates import H, S, T, apply_phase, canonical, generate_group, phase, rotation_angle, rz
from qsim import add, apply_1q, basis_state, close, dagger, identity, is_unitary, matmul, probabilities, scale

X = [[0j, 1 + 0j], [1 + 0j, 0j]]
Y = [[0j, -1j], [1j, 0j]]
Z = [[1 + 0j, 0j], [0j, -1 + 0j]]
I = identity(2)
R2 = math.sqrt(0.5)


def power(u, k):
    m = identity(2)
    for _ in range(k):
        m = matmul(m, u)
    return m


def conj(u, p):
    return matmul(matmul(u, p), dagger(u))


def test_powers() -> None:
    for g in (S, T):
        assert is_unitary(g)
    assert close(matmul(T, T), S)
    assert close(matmul(S, S), Z)
    assert close(power(T, 4), Z)
    assert close(power(T, 8), I)
    assert close(power(S, 4), I)
    assert close(dagger(S), power(S, 3)) and close(dagger(T), power(T, 7))
    assert close(phase(math.pi / 2), S) and close(phase(math.pi / 4), T) and close(phase(math.pi), Z)


def test_pi_over_8_name_and_rz() -> None:
    # T = e^(i pi/8) diag(e^(-i pi/8), e^(i pi/8)) = e^(i pi/8) R_z(pi/4)
    w = cmath.exp(1j * math.pi / 8)
    assert close(T, scale(w, [[cmath.exp(-1j * math.pi / 8), 0j], [0j, cmath.exp(1j * math.pi / 8)]]))
    rng = random.Random(5)
    for _ in range(20):
        phi = rng.uniform(-math.pi, math.pi)
        assert close(phase(phi), scale(cmath.exp(0.5j * phi), rz(phi)))


def test_conjugation_of_paulis() -> None:
    assert close(conj(S, X), Y)
    assert close(conj(S, Y), scale(-1, X))
    assert close(conj(S, Z), Z)
    # T X T^dagger = (X + Y)/sqrt 2, which is not a Pauli matrix up to phase
    txt = conj(T, X)
    assert close(txt, scale(R2, add(X, Y)))
    paulis = [scale(ph, p) for ph in (1, -1, 1j, -1j) for p in (I, X, Y, Z)]
    assert not any(close(txt, p) for p in paulis)
    assert close(conj(T, Y), scale(R2, add(Y, scale(-1, X))))
    assert close(conj(T, Z), Z)


def test_clifford_group_has_24_elements() -> None:
    group = generate_group([H, S])
    assert len(group) == 24
    for u in group.values():  # each element maps Paulis to Paulis up to sign
        for p in (X, Y, Z):
            q = conj(u, p)
            assert any(close(q, scale(s, r)) for s in (1, -1) for r in (X, Y, Z))
    assert canonical(T) not in group
    sqrt_x = matmul(H, matmul(S, H))
    assert close(matmul(sqrt_x, sqrt_x), X) and canonical(sqrt_x) in group
    # (HS)^3 is a global phase: HS has order 3 up to phase
    hs = matmul(H, S)
    assert canonical(power(hs, 3)) == canonical(I)


def test_t_and_htht_angle() -> None:
    # T H T H: a rotation by theta with cos(theta/2) = cos^2(pi/8)
    u = matmul(T, matmul(H, matmul(T, H)))
    theta = rotation_angle(u)
    assert abs(math.cos(theta / 2) - math.cos(math.pi / 8) ** 2) < 1e-12
    assert abs(abs(u[0][0] + u[1][1]) / 2 - math.cos(math.pi / 8) ** 2) < 1e-12
    # adding T to the Clifford generators gives more than any finite limit we try
    try:
        generate_group([H, T], limit=2000)
        raise AssertionError("expected an infinite group")
    except ValueError:
        pass


def test_phase_gates_do_not_change_computational_probabilities() -> None:
    rng = random.Random(17)
    n = 4
    s = [complex(rng.gauss(0, 1), rng.gauss(0, 1)) for _ in range(1 << n)]
    r = math.sqrt(sum(abs(a) ** 2 for a in s))
    s = [a / r for a in s]
    t = apply_phase(apply_phase(s, math.pi / 4, 2), math.pi / 2, 0)
    assert all(abs(a - b) < 1e-15 for a, b in zip(probabilities(s), probabilities(t)))
    assert close(apply_phase(s, math.pi / 4, 1), apply_1q(s, T, 1))
    # but in the X basis they do: H T H |0> has P(1) = sin^2(pi/8)
    v = apply_1q(apply_1q(apply_1q(basis_state(1, 0), H, 0), T, 0), H, 0)
    assert abs(probabilities(v)[1] - math.sin(math.pi / 8) ** 2) < 1e-12
