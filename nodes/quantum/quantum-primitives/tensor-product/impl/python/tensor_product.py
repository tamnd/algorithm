# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tensor-product/. The authors are listed in prov/XDTSZS.jsonl.
"""Tensor products of qubit states and gates as Kronecker products, in the qubit order of the encyclopedia.

The left factor of kron holds the high-order qubits: |b1> (x) |b0> is the basis state with index 2*b1 + b0.
"""

import math

from qsim import TOL, identity, norm

Vector = list[complex]
Matrix = list[list[complex]]


def kron(a: Matrix, b: Matrix) -> Matrix:
    """The Kronecker product: (a (x) b)[i*p + k][j*q + l] = a[i][j] * b[k][l], where b is p x q."""
    p, q = len(b), len(b[0])
    return [[a[r // p][c // q] * b[r % p][c % q] for c in range(len(a[0]) * q)] for r in range(len(a) * p)]


def kron_vec(u: Vector, v: Vector) -> Vector:
    """|u> (x) |v>: entry i*len(v) + k is u[i] * v[k]."""
    return [x * y for x in u for y in v]


def kron_all(factors: list) -> list:
    """factors[0] (x) factors[1] (x) ... , for vectors or for matrices. factors[0] is the leftmost factor."""
    out = factors[0]
    for f in factors[1:]:
        out = kron(out, f) if isinstance(f[0], list) else kron_vec(out, f)
    return out


def on_qubit(n: int, u: Matrix, j: int) -> Matrix:
    """The 2^n x 2^n matrix I^(x)(n-1-j) (x) u (x) I^(x)j of the gate u on qubit j."""
    if not 0 <= j < n:
        raise ValueError("qubit out of range")
    return kron(kron(identity(1 << (n - 1 - j)), u), identity(1 << j))


def swap_matrix() -> Matrix:
    """SWAP on two qubits: |a b> -> |b a>."""
    s = [[0j] * 4 for _ in range(4)]
    for a in range(2):
        for b in range(2):
            s[2 * b + a][2 * a + b] = 1 + 0j
    return s


def product_defect(state: Vector) -> float:
    """|a00 a11 - a01 a10| for a two-qubit state. It is 0 exactly when the state is a product state."""
    if len(state) != 4:
        raise ValueError("a two-qubit state has 4 amplitudes")
    return abs(state[0] * state[3] - state[1] * state[2])


def is_product_2q(state: Vector, tol: float = TOL) -> bool:
    return product_defect(state) <= tol


def factor_2q(state: Vector, tol: float = TOL) -> tuple[Vector, Vector]:
    """Unit vectors (u, v) on qubit 1 and qubit 0 with u (x) v = state. Raises ValueError if the state is entangled."""
    if not is_product_2q(state, tol):
        raise ValueError("the state is not a product state")
    # The 2 x 2 matrix M[b1][b0] = state[2*b1 + b0] has rank one, M = u v^T. Take a nonzero row as v.
    rows = [state[0:2], state[2:4]]
    r = max(range(2), key=lambda i: norm(rows[i]))
    nv = norm(rows[r])
    v = [a / nv for a in rows[r]]
    # u[i] = <v*|row i>, so that row i = u[i] v.
    u = [sum(row[k] * v[k].conjugate() for k in range(2)) for row in rows]
    return u, v


def product_state_parameters(n: int) -> int:
    """Real parameters of a product of n one-qubit pure states (2 each, up to one global phase)."""
    return 2 * n


def general_state_parameters(n: int) -> int:
    return 2 * (1 << n) - 2


def plus() -> Vector:
    return [complex(math.sqrt(0.5)), complex(math.sqrt(0.5))]
