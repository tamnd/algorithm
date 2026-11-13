# SPDX-License-Identifier: MIT
# Shared helper of the qp5 quantum pages of https://algorithm.tamnd.com/. The authors are listed in prov/.

"""A small state-vector and density-matrix simulator in pure Python.

Conventions:
- An n-qubit state is a list of 2**n amplitudes.
- Qubit 0 is the least significant bit of the index. The ket |q_(n-1) ... q_1 q_0>
  is the binary form of the index, so the leftmost symbol is the highest qubit.
- kron_vec(u, v) and kron_mat(A, B) put u (or A) on the high qubits.
- A matrix is a list of rows.
- The functions only add and multiply, so they also work with the exact
  numbers of the class R2 below.
"""

import math
from fractions import Fraction


class R2:
    """An exact real number a + b * sqrt(2), with rational a and b."""

    __slots__ = ("a", "b")

    def __init__(self, a=0, b=0):
        self.a = Fraction(a)
        self.b = Fraction(b)

    @staticmethod
    def _of(x):
        return x if isinstance(x, R2) else R2(x)

    def __add__(self, o):
        o = R2._of(o)
        return R2(self.a + o.a, self.b + o.b)

    __radd__ = __add__

    def __neg__(self):
        return R2(-self.a, -self.b)

    def __sub__(self, o):
        return self + (-R2._of(o))

    def __rsub__(self, o):
        return R2._of(o) - self

    def __mul__(self, o):
        o = R2._of(o)
        return R2(self.a * o.a + 2 * self.b * o.b, self.a * o.b + self.b * o.a)

    __rmul__ = __mul__

    def __truediv__(self, o):
        o = R2._of(o)
        n = o.a * o.a - 2 * o.b * o.b  # (a + b r)(a - b r) with r = sqrt(2); zero only for o = 0
        return self * R2(o.a / n, -o.b / n)

    def __rtruediv__(self, o):
        return R2._of(o) / self

    def __eq__(self, o):
        if isinstance(o, (int, Fraction, R2)):
            o = R2._of(o)
            return self.a == o.a and self.b == o.b
        return NotImplemented

    def __hash__(self):
        return hash((self.a, self.b))

    def conjugate(self):
        return self

    def __float__(self):
        return float(self.a) + float(self.b) * math.sqrt(2)

    def __repr__(self):
        return f"R2({self.a}, {self.b})"


S = 1 / math.sqrt(2)
I2 = [[1, 0], [0, 1]]
X = [[0, 1], [1, 0]]
Y = [[0, -1j], [1j, 0]]
Z = [[1, 0], [0, -1]]
H = [[S, S], [S, -S]]
H_EXACT = [[R2(0, Fraction(1, 2)), R2(0, Fraction(1, 2))], [R2(0, Fraction(1, 2)), R2(0, Fraction(-1, 2))]]


def basis_state(n, index):
    v = [0] * (1 << n)
    v[index] = 1
    return v


def kron_vec(u, v):
    return [a * b for a in u for b in v]


def kron_mat(A, B):
    return [[a * b for a in ra for b in rb] for ra in A for rb in B]


def apply_1q(state, U, q):
    """Apply the 2 x 2 matrix U to qubit q. Returns a new list."""
    out = list(state)
    m = 1 << q
    for i in range(len(state)):
        if not i & m:
            a0, a1 = state[i], state[i | m]
            out[i] = U[0][0] * a0 + U[0][1] * a1
            out[i | m] = U[1][0] * a0 + U[1][1] * a1
    return out


def apply_controlled(state, U, control, target):
    """Apply U to qubit target on the basis states where qubit control is 1."""
    out = list(state)
    c, m = 1 << control, 1 << target
    for i in range(len(state)):
        if i & c and not i & m:
            a0, a1 = state[i], state[i | m]
            out[i] = U[0][0] * a0 + U[0][1] * a1
            out[i | m] = U[1][0] * a0 + U[1][1] * a1
    return out


def apply_cnot(state, control, target):
    return apply_controlled(state, X, control, target)


def apply_permutation(state, perm):
    """Move the amplitude of basis state i to basis state perm[i]."""
    out = [0] * len(state)
    for i, a in enumerate(state):
        out[perm[i]] = a
    return out


def apply_diagonal(state, phases):
    return [p * a for p, a in zip(phases, state)]


def inner(u, v):
    """<u|v>, conjugate-linear in u."""
    return sum(a.conjugate() * b for a, b in zip(u, v))


def probabilities(state):
    return [abs(a) ** 2 for a in state]


def project_qubit(state, q, bit):
    """Project qubit q on |bit>. Returns (probability, normalized state or None)."""
    m = 1 << q
    kept = [a if bool(i & m) == bool(bit) else 0 for i, a in enumerate(state)]
    p = sum(abs(a) ** 2 for a in kept)
    if p == 0:
        return 0.0, None
    r = math.sqrt(p)
    return p, [a / r for a in kept]


def measure_qubit(state, q, rng):
    """Measure qubit q in the computational basis with the random.Random object rng."""
    p1, post1 = project_qubit(state, q, 1)
    if rng.random() < p1:
        return 1, post1
    return 0, project_qubit(state, q, 0)[1]


def random_state(n, rng):
    v = [complex(rng.gauss(0, 1), rng.gauss(0, 1)) for _ in range(1 << n)]
    r = math.sqrt(sum(abs(a) ** 2 for a in v))
    return [a / r for a in v]


def random_unitary_1q(rng):
    a, b = random_state(1, rng)
    t = rng.uniform(0, 2 * math.pi)
    ph = complex(math.cos(t), math.sin(t))
    return [[a * ph, -b.conjugate() * ph], [b * ph, a.conjugate() * ph]]


def matrix_of(n, f):
    """The 2^n x 2^n matrix of a linear function f on n-qubit states."""
    cols = [f(basis_state(n, j)) for j in range(1 << n)]
    return [[cols[j][i] for j in range(1 << n)] for i in range(1 << n)]


def dagger(A):
    return [[A[j][i].conjugate() for j in range(len(A))] for i in range(len(A[0]))]


def matmul(A, B):
    Bt = list(zip(*B))
    return [[sum(a * b for a, b in zip(row, col)) for col in Bt] for row in A]


def matvec(A, v):
    return [sum(a * b for a, b in zip(row, v)) for row in A]


def outer(u, v):
    """|u><v|."""
    return [[a * b.conjugate() for b in v] for a in u]


def trace(A):
    return sum(A[i][i] for i in range(len(A)))


def mat_add(A, B, ca=1, cb=1):
    return [[ca * a + cb * b for a, b in zip(ra, rb)] for ra, rb in zip(A, B)]


def identity(d):
    return [[1 if i == j else 0 for j in range(d)] for i in range(d)]


def max_abs_diff(A, B):
    """The largest entry of |A - B|, for two vectors or two matrices."""
    if A and isinstance(A[0], list):
        return max(abs(a - b) for ra, rb in zip(A, B) for a, b in zip(ra, rb))
    return max(abs(a - b) for a, b in zip(A, B))


def _compress(i, qubits):
    return sum(((i >> q) & 1) << k for k, q in enumerate(qubits))


def partial_trace(rho, n, keep):
    """Trace out every qubit not in keep. The kept qubits keep their relative order."""
    keep = sorted(keep)
    gone = [q for q in range(n) if q not in keep]
    d = 1 << len(keep)
    out = [[0] * d for _ in range(d)]
    for i in range(1 << n):
        gi, ki = _compress(i, gone), _compress(i, keep)
        for j in range(1 << n):
            if _compress(j, gone) == gi:
                out[ki][_compress(j, keep)] += rho[i][j]
    return out


def reduced_density(state, n, keep):
    """rho_keep = Tr_rest |state><state|, computed from the state vector."""
    keep = sorted(keep)
    gone = [q for q in range(n) if q not in keep]
    d = 1 << len(keep)
    blocks = {}
    for i, a in enumerate(state):
        blocks.setdefault(_compress(i, gone), [0] * d)[_compress(i, keep)] = a
    out = [[0] * d for _ in range(d)]
    for col in blocks.values():
        for r in range(d):
            if col[r] != 0:
                for c in range(d):
                    out[r][c] += col[r] * col[c].conjugate()
    return out


def _jacobi_real(Sym, sweeps=100, tol=1e-15):
    """Eigenvalues and eigenvector columns of a real symmetric matrix (cyclic Jacobi)."""
    n = len(Sym)
    A = [list(map(float, r)) for r in Sym]
    V = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    for _ in range(sweeps):
        off = sum(A[i][j] ** 2 for i in range(n) for j in range(n) if i != j)
        if off < tol * tol:
            break
        for p in range(n - 1):
            for q in range(p + 1, n):
                if abs(A[p][q]) < 1e-300:
                    continue
                theta = (A[q][q] - A[p][p]) / (2 * A[p][q])
                t = math.copysign(1.0, theta) / (abs(theta) + math.sqrt(theta * theta + 1))
                c = 1 / math.sqrt(t * t + 1)
                s = t * c
                for k in range(n):
                    akp, akq = A[k][p], A[k][q]
                    A[k][p], A[k][q] = c * akp - s * akq, s * akp + c * akq
                for k in range(n):
                    apk, aqk = A[p][k], A[q][k]
                    A[p][k], A[q][k] = c * apk - s * aqk, s * apk + c * aqk
                for k in range(n):
                    vkp, vkq = V[k][p], V[k][q]
                    V[k][p], V[k][q] = c * vkp - s * vkq, s * vkp + c * vkq
    return [A[i][i] for i in range(n)], V


def _real_form(A):
    """The real 2d x 2d form [[B, -C], [C, B]] of the Hermitian matrix A = B + iC."""
    d = len(A)
    B = [[complex(A[i][j]).real for j in range(d)] for i in range(d)]
    C = [[complex(A[i][j]).imag for j in range(d)] for i in range(d)]
    return [B[i] + [-c for c in C[i]] for i in range(d)] + [C[i] + B[i] for i in range(d)]


def eigvalsh(A):
    """The eigenvalues of a Hermitian matrix, in increasing order."""
    vals, _ = _jacobi_real(_real_form(A))
    return sorted(vals)[::2]


def positive_part_projector(A):
    """The projector on the span of the eigenvectors of the Hermitian A with eigenvalue > 0."""
    d = len(A)
    vals, V = _jacobi_real(_real_form(A))
    cols = [k for k in range(2 * d) if vals[k] > 1e-12]
    R = [[sum(V[i][k] * V[j][k] for k in cols) for j in range(2 * d)] for i in range(2 * d)]
    return [[complex(R[i][j], R[i + d][j]) for j in range(d)] for i in range(d)]


def entropy_of(eigenvalues):
    """-sum p log2 p over the eigenvalues, with 0 log 0 = 0."""
    return -sum(p * math.log2(p) for p in eigenvalues if p > 1e-15)
