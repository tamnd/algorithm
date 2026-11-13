# SPDX-License-Identifier: MIT
# Shared helper of the qp4 quantum pages of https://algorithm.tamnd.com/. The authors are listed in prov/.
"""Small exact linear algebra for quantum states, in pure Python.

Conventions:
- A state vector is a list of complex numbers. A matrix is a list of rows,
  each row a list of complex numbers.
- On n qubits, qubit 0 is the least significant bit of the basis index.
  So the n-qubit space is qubit (n-1) tensor ... tensor qubit 0, and
  kron(A, B) acts with A on the high-order part and B on the low-order part.
- For a space H_A tensor H_B of dimensions da and db, the basis index of
  |a>|b> is a * db + b.
"""

import cmath
import math
import random
from typing import Callable, List, Sequence, Tuple

Vector = List[complex]
Matrix = List[List[complex]]

SQRT_HALF = 1 / math.sqrt(2)
I2: Matrix = [[1, 0], [0, 1]]
X: Matrix = [[0, 1], [1, 0]]
Y: Matrix = [[0, -1j], [1j, 0]]
Z: Matrix = [[1, 0], [0, -1]]
H: Matrix = [[SQRT_HALF, SQRT_HALF], [SQRT_HALF, -SQRT_HALF]]
S_DAG: Matrix = [[1, 0], [0, -1j]]


# ---------------------------------------------------------------- matrices


def zeros(n: int, m: int = -1) -> Matrix:
    return [[0j] * (n if m < 0 else m) for _ in range(n)]


def identity(n: int) -> Matrix:
    return [[1 + 0j if i == j else 0j for j in range(n)] for i in range(n)]


def matmul(a: Matrix, b: Matrix) -> Matrix:
    bt = list(zip(*b))
    return [[sum(x * y for x, y in zip(row, col)) for col in bt] for row in a]


def matvec(a: Matrix, v: Sequence[complex]) -> Vector:
    return [sum(x * y for x, y in zip(row, v)) for row in a]


def dagger(a: Matrix) -> Matrix:
    return [[complex(a[j][i]).conjugate() for j in range(len(a))] for i in range(len(a[0]))]


def add(a: Matrix, b: Matrix) -> Matrix:
    return [[x + y for x, y in zip(ra, rb)] for ra, rb in zip(a, b)]


def sub(a: Matrix, b: Matrix) -> Matrix:
    return [[x - y for x, y in zip(ra, rb)] for ra, rb in zip(a, b)]


def scale(c: complex, a: Matrix) -> Matrix:
    return [[c * x for x in row] for row in a]


def trace(a: Matrix) -> complex:
    return sum(a[i][i] for i in range(len(a)))


def kron(a: Matrix, b: Matrix) -> Matrix:
    return [[x * y for x in ra for y in rb] for ra in a for rb in b]


def kron_vec(u: Sequence[complex], v: Sequence[complex]) -> Vector:
    return [x * y for x in u for y in v]


def inner(u: Sequence[complex], v: Sequence[complex]) -> complex:
    """<u|v>, linear in the second argument."""
    return sum(complex(x).conjugate() * y for x, y in zip(u, v))


def outer(u: Sequence[complex], v: Sequence[complex]) -> Matrix:
    """|u><v|."""
    return [[x * complex(y).conjugate() for y in v] for x in u]


def pure_density(psi: Sequence[complex]) -> Matrix:
    return outer(psi, psi)


def max_abs_diff(a: Matrix, b: Matrix) -> float:
    return max(abs(x - y) for ra, rb in zip(a, b) for x, y in zip(ra, rb))


def is_hermitian(a: Matrix, tol: float = 1e-9) -> bool:
    n = len(a)
    return all(abs(a[i][j] - complex(a[j][i]).conjugate()) <= tol for i in range(n) for j in range(n))


# ---------------------------------------------------------------- eigenvalues


def eigh(a: Matrix, tol: float = 1e-14, max_sweeps: int = 60) -> Tuple[List[float], Matrix]:
    """Eigenvalues (ascending) and eigenvectors (the columns of V) of a Hermitian matrix.

    Cyclic complex Jacobi method: each step zeroes one off-diagonal pair with
    a unitary J = D R, where D = diag(1, e^(-i phi)) makes the pair real and
    R is a real plane rotation. Cost O(n^3) per sweep; a few sweeps suffice
    for n <= 32.
    """
    n = len(a)
    a = [[complex(x) for x in row] for row in a]
    v = identity(n)
    scale_ = max(1.0, max(abs(x) for row in a for x in row))
    for _ in range(max_sweeps):
        off = sum(abs(a[p][q]) ** 2 for p in range(n) for q in range(p + 1, n))
        if off <= (tol * scale_) ** 2:
            break
        for p in range(n):
            for q in range(p + 1, n):
                apq = a[p][q]
                r = abs(apq)
                if r <= 1e-300:
                    continue
                ph = apq / r
                theta = 0.5 * math.atan2(2 * r, a[q][q].real - a[p][p].real)
                c, s = math.cos(theta), math.sin(theta)
                e = ph.conjugate()
                # J = [[c, s], [-s e, c e]] in the (p, q) plane.
                j00, j01, j10, j11 = c, s, -s * e, c * e
                for k in range(n):  # A <- A J
                    akp, akq = a[k][p], a[k][q]
                    a[k][p] = akp * j00 + akq * j10
                    a[k][q] = akp * j01 + akq * j11
                for k in range(n):  # A <- J^dagger A
                    apk, aqk = a[p][k], a[q][k]
                    a[p][k] = j00 * apk + j10.conjugate() * aqk
                    a[q][k] = j01 * apk + j11.conjugate() * aqk
                a[p][q] = a[q][p] = 0j
                for k in range(n):  # V <- V J
                    vkp, vkq = v[k][p], v[k][q]
                    v[k][p] = vkp * j00 + vkq * j10
                    v[k][q] = vkp * j01 + vkq * j11
    order = sorted(range(n), key=lambda i: a[i][i].real)
    vals = [a[i][i].real for i in order]
    vecs = [[v[k][i] for i in order] for k in range(n)]
    return vals, vecs


def eigvalsh(a: Matrix) -> List[float]:
    return eigh(a)[0]


def matrix_function(a: Matrix, f: Callable[[float], float]) -> Matrix:
    """f(A) = V diag(f(lambda)) V^dagger for a Hermitian matrix A."""
    vals, v = eigh(a)
    n = len(a)
    fv = [f(x) for x in vals]
    return [[sum(v[i][k] * fv[k] * v[j][k].conjugate() for k in range(n)) for j in range(n)] for i in range(n)]


def sqrtm_psd(a: Matrix) -> Matrix:
    """Square root of a positive semidefinite matrix; tiny negative eigenvalues are set to 0."""
    return matrix_function(a, lambda x: math.sqrt(max(x, 0.0)))


# ---------------------------------------------------------------- partial trace of two parts


def trace_out_second(rho: Matrix, da: int, db: int) -> Matrix:
    """Tr_B of an operator on H_A tensor H_B (index a * db + b)."""
    return [[sum(rho[i * db + k][j * db + k] for k in range(db)) for j in range(da)] for i in range(da)]


def trace_out_first(rho: Matrix, da: int, db: int) -> Matrix:
    """Tr_A of an operator on H_A tensor H_B (index a * db + b)."""
    return [[sum(rho[k * db + i][k * db + j] for k in range(da)) for j in range(db)] for i in range(db)]


# ---------------------------------------------------------------- state vectors on qubits


def apply_1q(state: Vector, u: Matrix, q: int) -> Vector:
    """Apply a 2 x 2 matrix to qubit q (qubit 0 is the least significant bit)."""
    out = list(state)
    bit = 1 << q
    for i in range(len(state)):
        if not i & bit:
            a0, a1 = state[i], state[i | bit]
            out[i] = u[0][0] * a0 + u[0][1] * a1
            out[i | bit] = u[1][0] * a0 + u[1][1] * a1
    return out


def apply_permutation(state: Vector, perm: Callable[[int], int]) -> Vector:
    """Apply the unitary |i> -> |perm(i)> for a bijection perm of the basis indices."""
    out = [0j] * len(state)
    for i, amp in enumerate(state):
        out[perm(i)] = amp
    return out


def apply_diagonal(state: Vector, phases: Sequence[complex]) -> Vector:
    return [p * x for p, x in zip(phases, state)]


def probabilities(state: Sequence[complex]) -> List[float]:
    return [abs(x) ** 2 for x in state]


def prob_qubit_zero(state: Sequence[complex], q: int) -> float:
    bit = 1 << q
    return sum(abs(x) ** 2 for i, x in enumerate(state) if not i & bit)


def measure_qubit(state: Vector, q: int, rng: random.Random) -> Tuple[int, Vector]:
    """Measure qubit q in the computational basis. Returns the outcome and the post-measurement state."""
    p0 = prob_qubit_zero(state, q)
    outcome = 0 if rng.random() < p0 else 1
    bit = 1 << q
    norm = math.sqrt(p0 if outcome == 0 else 1 - p0)
    post = [x / norm if bool(i & bit) == bool(outcome) else 0j for i, x in enumerate(state)]
    return outcome, post


def apply_to_density(rho: Matrix, op: Callable[[Vector], Vector]) -> Matrix:
    """U rho U^dagger, where op(v) = U v is a linear map on state vectors."""
    n = len(rho)
    cols = [op([rho[i][j] for i in range(n)]) for j in range(n)]  # columns of U rho
    m = [[cols[j][i] for j in range(n)] for i in range(n)]  # U rho
    cols2 = [op([m[i][j].conjugate() for j in range(n)]) for i in range(n)]  # U (U rho)^dagger, column i
    return [[cols2[j][i] for j in range(n)] for i in range(n)]


# ---------------------------------------------------------------- random inputs


def random_state(rng: random.Random, d: int) -> Vector:
    """A random unit vector of C^d (normalized complex Gaussian, which is unitarily invariant)."""
    v = [complex(rng.gauss(0, 1), rng.gauss(0, 1)) for _ in range(d)]
    nrm = math.sqrt(sum(abs(x) ** 2 for x in v))
    return [x / nrm for x in v]


def random_density(rng: random.Random, d: int, rank: int = 0) -> Matrix:
    """G G^dagger / Tr(G G^dagger) for a d x rank complex Gaussian G (rank 0 means full rank)."""
    k = rank or d
    g = [[complex(rng.gauss(0, 1), rng.gauss(0, 1)) for _ in range(k)] for _ in range(d)]
    m = matmul(g, dagger(g))
    t = trace(m).real
    return scale(1 / t, m)


def random_unitary(rng: random.Random, d: int) -> Matrix:
    """Gram-Schmidt on the columns of a complex Gaussian matrix."""
    cols: List[Vector] = []
    while len(cols) < d:
        v = [complex(rng.gauss(0, 1), rng.gauss(0, 1)) for _ in range(d)]
        for c in cols:
            ip = inner(c, v)
            v = [x - ip * y for x, y in zip(v, c)]
        nrm = math.sqrt(sum(abs(x) ** 2 for x in v))
        if nrm > 1e-8:
            cols.append([x / nrm for x in v])
    return [[cols[j][i] for j in range(d)] for i in range(d)]


def phase(theta: float) -> complex:
    return cmath.exp(1j * theta)
