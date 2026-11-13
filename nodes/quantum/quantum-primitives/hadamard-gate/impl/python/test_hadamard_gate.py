# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hadamard-gate/. The authors are listed in prov/0GVHJA.jsonl.

import cmath
import math
import random

from hadamard_gate import H, R, fwht, hadamard_all, hadamard_entry, hadamard_matrix, hadamard_transform
from qsim import add, basis_state, close, dagger, identity, is_unitary, matmul, matvec, scale

X = [[0j, 1 + 0j], [1 + 0j, 0j]]
Y = [[0j, -1j], [1j, 0j]]
Z = [[1 + 0j, 0j], [0j, -1 + 0j]]


def kron(a, b):
    p = len(b)
    return [[a[r // p][c // p] * b[r % p][c % p] for c in range(len(a) * p)] for r in range(len(a) * p)]


def test_definition_and_basic_identities() -> None:
    assert close(H, scale(R, add(X, Z)))
    assert is_unitary(H) and close(H, dagger(H))
    assert close(matmul(H, H), identity(2))
    assert close(matmul(matmul(H, X), H), Z)
    assert close(matmul(matmul(H, Z), H), X)
    assert close(matmul(matmul(H, Y), H), scale(-1, Y))
    assert close(matvec(H, basis_state(1, 0)), [R, R]) and close(matvec(H, basis_state(1, 1)), [R, -R])


def test_hadamard_is_a_half_turn() -> None:
    # H = i exp(-i (pi/2) n . sigma) with n = (x + z)/sqrt 2, and exp(-i (pi/2) n . sigma) = -i (n . sigma)
    ns = scale(R, add(X, Z))
    rot = add(scale(math.cos(math.pi / 2), identity(2)), scale(-1j * math.sin(math.pi / 2), ns))
    assert close(scale(1j, rot), H)
    assert abs(cmath.phase(H[0][0] * H[1][1] - H[0][1] * H[1][0]) - math.pi) < 1e-12  # det H = -1


def test_tensor_power_entries() -> None:
    m = [[1 + 0j]]
    for n in range(1, 6):
        m = kron(m, H)
        assert close(m, hadamard_matrix(n))
    # Sylvester recursion: H_n = H (x) H_(n-1); the first row and column are all 2^(-n/2)
    assert all(abs(hadamard_entry(5, 0, y) - 2 ** -2.5) < 1e-15 for y in range(32))
    assert hadamard_entry(3, 0b101, 0b111) == hadamard_entry(3, 0b111, 0b101) > 0  # parity of 101 & 111 is even
    assert hadamard_entry(3, 0b100, 0b110) < 0


def test_uniform_superposition() -> None:
    for n in range(1, 9):
        s = hadamard_all(basis_state(n, 0))
        assert all(abs(a - 2 ** (-n / 2)) < 1e-12 for a in s)
    # on |x> the signs are (-1)^(x . y)
    s = hadamard_all(basis_state(3, 5))
    assert close(s, [hadamard_entry(3, y, 5) for y in range(8)])


def bloch(s):
    a, b = s
    c = a.conjugate() * b
    return (2 * c.real, 2 * c.imag, abs(a) ** 2 - abs(b) ** 2)


def test_bloch_sphere_map() -> None:
    # H maps the Bloch vector (x, y, z) to (z, -y, x)
    rng = random.Random(7)
    for _ in range(100):
        s = [complex(rng.gauss(0, 1), rng.gauss(0, 1)) for _ in range(2)]
        r = math.sqrt(sum(abs(a) ** 2 for a in s))
        s = [a / r for a in s]
        x, y, z = bloch(s)
        assert all(abs(u - v) < 1e-12 for u, v in zip(bloch(matvec(H, s)), (z, -y, x)))


def test_fast_transform_matches_the_gates() -> None:
    rng = random.Random(101)
    n = 10
    v = [complex(rng.gauss(0, 1), rng.gauss(0, 1)) for _ in range(1 << n)]
    assert close(hadamard_transform(v), hadamard_all(v), 1e-9)
    # small case against the matrix
    w = [complex(rng.gauss(0, 1), rng.gauss(0, 1)) for _ in range(16)]
    assert close(hadamard_transform(w), matvec(hadamard_matrix(4), w))
    # integer transform, applied twice, multiplies by 2^n
    u = [rng.randint(-5, 5) for _ in range(64)]
    assert fwht(fwht(u)) == [64 * a for a in u]
