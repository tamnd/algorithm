# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bloch-sphere/. The authors are listed in prov/R8N0ZK.jsonl.

import cmath
import math
import random

import pytest

from bloch_sphere import (
    X, Y, Z, angles, apply_rotation, bloch_vector, density, density_from_vector, length, rotation, so3,
    state_from_angles, vector_of_density,
)
from qsim import close, inner, is_unitary, matvec

R = math.sqrt(0.5)
H = [[complex(R), complex(R)], [complex(R), complex(-R)]]


def near(u, v, tol: float = 1e-9) -> bool:
    return all(abs(a - b) <= tol for a, b in zip(u, v))


def rand_state(rng: random.Random) -> list[complex]:
    v = [complex(rng.gauss(0, 1), rng.gauss(0, 1)) for _ in range(2)]
    s = math.sqrt(sum(abs(a) ** 2 for a in v))
    return [a / s for a in v]


def test_cardinal_states() -> None:
    cases = {
        (1, 0, 0): [complex(R), complex(R)],
        (-1, 0, 0): [complex(R), complex(-R)],
        (0, 1, 0): [complex(R), 1j * R],
        (0, -1, 0): [complex(R), -1j * R],
        (0, 0, 1): [1 + 0j, 0j],
        (0, 0, -1): [0j, 1 + 0j],
    }
    for r, s in cases.items():
        assert near(bloch_vector(s), r)


def test_angles_match_the_amplitudes() -> None:
    rng = random.Random(41)
    for _ in range(200):
        theta, phi = rng.uniform(0.01, math.pi - 0.01), rng.uniform(0, 2 * math.pi)
        s = state_from_angles(theta, phi)
        t2, p2 = angles(s)
        assert abs(t2 - theta) < 1e-9 and abs(cmath.exp(1j * p2) - cmath.exp(1j * phi)) < 1e-9
        x, y, z = bloch_vector(s)
        assert near((x, y, z), (math.sin(theta) * math.cos(phi), math.sin(theta) * math.sin(phi), math.cos(theta)))
        # the probability of outcome 0 is cos^2(theta/2) = (1 + z) / 2
        assert abs(abs(s[0]) ** 2 - (1 + z) / 2) < 1e-12


def test_global_phase_does_not_move_the_point() -> None:
    rng = random.Random(42)
    for _ in range(100):
        s = rand_state(rng)
        g = cmath.exp(1j * rng.uniform(0, 2 * math.pi))
        assert near(bloch_vector(s), bloch_vector([g * a for a in s]))
        assert abs(length(bloch_vector(s)) - 1) < 1e-12


def test_orthogonal_states_are_antipodal_and_overlap_formula() -> None:
    rng = random.Random(43)
    for _ in range(100):
        s, t = rand_state(rng), rand_state(rng)
        perp = [-s[1].conjugate(), s[0].conjugate()]
        assert abs(inner(s, perp)) < 1e-12
        assert near(bloch_vector(perp), tuple(-c for c in bloch_vector(s)))
        r, q = bloch_vector(s), bloch_vector(t)
        assert abs(abs(inner(s, t)) ** 2 - (1 + sum(a * b for a, b in zip(r, q))) / 2) < 1e-12


def test_mixed_states_are_inside_the_ball() -> None:
    zero, one = density([1 + 0j, 0j]), density([0j, 1 + 0j])
    mix = [[(zero[i][j] + one[i][j]) / 2 for j in range(2)] for i in range(2)]
    assert near(vector_of_density(mix), (0, 0, 0))
    rng = random.Random(44)
    for _ in range(50):
        p = rng.random()
        s, t = rand_state(rng), rand_state(rng)
        rs, rt = density(s), density(t)
        rho = [[p * rs[i][j] + (1 - p) * rt[i][j] for j in range(2)] for i in range(2)]
        r = vector_of_density(rho)
        assert length(r) <= 1 + 1e-12
        assert near(r, tuple(p * a + (1 - p) * b for a, b in zip(bloch_vector(s), bloch_vector(t))))
        assert close(density_from_vector(r), rho)
    # |r| > 1 gives a matrix with a negative eigenvalue: (1 - |r|) / 2 < 0
    m = density_from_vector((0, 0, 1.5))
    assert m[1][1].real < 0


def test_gates_are_rotations() -> None:
    # H maps (x, y, z) to (z, -y, x): the half turn about (x + z) / sqrt(2).
    rng = random.Random(45)
    for _ in range(50):
        s = rand_state(rng)
        x, y, z = bloch_vector(s)
        assert near(bloch_vector(matvec(H, s)), (z, -y, x))
    assert near(bloch_vector(matvec(X, [1 + 0j, 0j])), (0, 0, -1))
    # Rz(alpha) adds alpha to phi
    for _ in range(50):
        theta, phi, alpha = rng.uniform(0.1, 3.0), rng.uniform(0, 6.28), rng.uniform(0, 6.28)
        s = matvec(rotation((0, 0, 1), alpha), state_from_angles(theta, phi))
        assert near(bloch_vector(s), bloch_vector(state_from_angles(theta, phi + alpha)))
    # a general rotation acts on Bloch vectors through its SO(3) matrix
    for _ in range(30):
        n = [rng.gauss(0, 1) for _ in range(3)]
        ln = length(n)
        axis = tuple(c / ln for c in n)
        u = rotation(axis, rng.uniform(0, 2 * math.pi))
        assert is_unitary(u)
        r3 = so3(u)
        s = rand_state(rng)
        assert near(bloch_vector(matvec(u, s)), apply_rotation(r3, bloch_vector(s)))
        assert near(apply_rotation(r3, axis), axis)
    for p, ax in ((X, (1, 0, 0)), (Y, (0, 1, 0)), (Z, (0, 0, 1))):
        assert close(rotation(ax, math.pi), [[-1j * e for e in row] for row in p])
    with pytest.raises(ValueError):
        rotation((1, 1, 0), 1.0)
