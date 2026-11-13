# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/quantum-measurement/. The authors are listed in prov/GQ7MFN.jsonl.
"""Projective measurements, POVMs and the Naimark dilation of a rank-one POVM.

States are lists of complex amplitudes. On qubits, qubit 0 is the least significant bit of the index.
"""

import math
import random

from qsim import TOL, add, close, dagger, identity, inner, matmul, matvec, norm

Vector = list[complex]
Matrix = list[list[complex]]


def outer(u: Vector, v: Vector) -> Matrix:
    """|u><v|."""
    return [[a * b.conjugate() for b in v] for a in u]


def basis_projectors(basis: list[Vector]) -> list[Matrix]:
    return [outer(e, e) for e in basis]


def is_projective(projectors: list[Matrix], tol: float = TOL) -> bool:
    """Hermitian, P_m P_m' = delta P_m, and sum P_m = I."""
    d = len(projectors[0])
    total = [[0j] * d for _ in range(d)]
    for i, p in enumerate(projectors):
        if not close(p, dagger(p), tol):
            return False
        for j, q in enumerate(projectors):
            target = p if i == j else [[0j] * d for _ in range(d)]
            if not close(matmul(p, q), target, tol):
                return False
        total = add(total, p)
    return close(total, identity(d), tol)


def probabilities(state: Vector, ops: list[Matrix]) -> list[float]:
    """<psi|E_m|psi> for each element E_m of a projective measurement or a POVM."""
    return [inner(state, matvec(e, state)).real for e in ops]


def post_state(state: Vector, p: Matrix) -> Vector:
    """P|psi> / sqrt(<psi|P|psi>), the state after the outcome with projector P."""
    v = matvec(p, state)
    r = norm(v)
    if r <= TOL:
        raise ValueError("this outcome has probability 0")
    return [a / r for a in v]


def measure(state: Vector, projectors: list[Matrix], rng: random.Random) -> tuple[int, Vector]:
    """Sample an outcome m with the Born rule and return (m, the post-measurement state)."""
    p = probabilities(state, projectors)
    r = rng.random()
    acc = 0.0
    m = max(k for k in range(len(p)) if p[k] > TOL)
    for k, pk in enumerate(p):
        acc += pk
        if r < acc and pk > TOL:
            m = k
            break
    return m, post_state(state, projectors[m])


def averaged_state(state: Vector, projectors: list[Matrix]) -> Matrix:
    """sum_m P_m |psi><psi| P_m, the density matrix after the measurement when the outcome is not recorded."""
    rho = outer(state, state)
    d = len(state)
    out = [[0j] * d for _ in range(d)]
    for p in projectors:
        out = add(out, matmul(p, matmul(rho, p)))
    return out


def purity(rho: Matrix) -> float:
    """tr(rho^2): 1 for a pure state and less than 1 for a mixed state."""
    m = matmul(rho, rho)
    return sum(m[i][i] for i in range(len(m))).real


def trine_vectors() -> list[Vector]:
    """sqrt(2/3) |psi_k>, |psi_k> = cos(2 pi k / 3)|0> + sin(2 pi k / 3)|1>, k = 0, 1, 2."""
    c = math.sqrt(2 / 3)
    return [[complex(c * math.cos(2 * math.pi * k / 3)), complex(c * math.sin(2 * math.pi * k / 3))] for k in range(3)]


def povm_from_vectors(vectors: list[Vector]) -> list[Matrix]:
    """The rank-one POVM E_k = |e_k><e_k|."""
    return [outer(e, e) for e in vectors]


def is_povm_of_vectors(vectors: list[Vector], tol: float = TOL) -> bool:
    """E_k = |e_k><e_k| are positive by construction, so the only condition is sum_k E_k = I."""
    d = len(vectors[0])
    total = [[0j] * d for _ in range(d)]
    for e in povm_from_vectors(vectors):
        total = add(total, e)
    return close(total, identity(d), tol)


def naimark_isometry(vectors: list[Vector]) -> Matrix:
    """V with V|psi> = sum_k <e_k|psi> |k>: row k of V is the conjugate of e_k. V^dagger V = sum_k E_k = I."""
    return [[a.conjugate() for a in e] for e in vectors]


def complete_to_unitary(v: Matrix, tol: float = 1e-9) -> Matrix:
    """A D x D unitary whose first d columns are the orthonormal columns of the D x d matrix v (Gram-Schmidt)."""
    big = len(v)
    cols = [[v[i][j] for i in range(big)] for j in range(len(v[0]))]
    for x in range(big):
        w = [0j] * big
        w[x] = 1 + 0j
        for c in cols:
            ip = inner(c, w)
            w = [a - ip * b for a, b in zip(w, c)]
        r = norm(w)
        if r > tol:
            cols.append([a / r for a in w])
        if len(cols) == big:
            break
    return [[cols[j][i] for j in range(big)] for i in range(big)]


def naimark_unitary(vectors: list[Vector], big: int) -> Matrix:
    """A unitary on C^big. On the input |psi> padded with zeros, a measurement in the standard basis gives k with probability <psi|E_k|psi>."""
    rows = naimark_isometry(vectors)
    while len(rows) < big:
        rows.append([0j] * len(vectors[0]))
    return complete_to_unitary(rows)


def embed(state: Vector, big: int) -> Vector:
    """|psi> padded with zeros: on qubits, the ancilla qubits above the system are |0>."""
    return list(state) + [0j] * (big - len(state))
