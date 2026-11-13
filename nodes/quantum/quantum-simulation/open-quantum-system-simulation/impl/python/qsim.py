# SPDX-License-Identifier: MIT
# Shared helper of the qsim3 quantum pages of https://algorithm.tamnd.com/. The authors are listed in prov/.
"""A small pure-Python state-vector simulator, with the linear algebra, the Pauli
algebra and the Fock-space matrices that the qsim3 pages share.

Qubit order convention (the same on every qp1 page):
a state on n qubits is a list of 2**n complex amplitudes, indexed by x = sum_j b_j * 2**j,
where b_j is the value of qubit j. Qubit 0 is the least significant bit. The ket
|b_{n-1} ... b_1 b_0> is the binary numeral of x, and it is |b_{n-1}> (x) ... (x) |b_0>,
so qubit n-1 is the leftmost tensor factor and qubit 0 is the rightmost one.

A Pauli string is text such as "XIZ": the first character acts on qubit n-1 and the
last character acts on qubit 0. A qubit operator is a dict {Pauli string: coefficient}.

Fock space convention (qsim3): n fermionic modes, the occupation number state
|n_{n-1} ... n_1 n_0> has the index x = sum_k n_k * 2**k, so mode k is bit k.
"""

import cmath
import math
import random

TOL = 1e-9

Vector = list[complex]
Matrix = list[list[complex]]


def num_qubits(state: Vector) -> int:
    n = len(state).bit_length() - 1
    if n < 0 or 1 << n != len(state):
        raise ValueError("the length of a state must be a power of two")
    return n


def basis_state(n: int, x: int) -> Vector:
    if not 0 <= x < 1 << n:
        raise ValueError("basis index out of range")
    v = [0j] * (1 << n)
    v[x] = 1 + 0j
    return v


def bit(x: int, j: int) -> int:
    return (x >> j) & 1


def apply_1q(state: Vector, u: Matrix, q: int) -> Vector:
    """Apply the 2 x 2 matrix u to qubit q. Returns a new list."""
    n = num_qubits(state)
    if not 0 <= q < n:
        raise ValueError("qubit out of range")
    out = list(state)
    m = 1 << q
    for x in range(1 << n):
        if x & m == 0:
            a0, a1 = state[x], state[x | m]
            out[x] = u[0][0] * a0 + u[0][1] * a1
            out[x | m] = u[1][0] * a0 + u[1][1] * a1
    return out


def apply_controlled(state: Vector, u: Matrix, controls: list[int], target: int) -> Vector:
    """Apply u to the target qubit on the basis states where every control qubit is 1."""
    n = num_qubits(state)
    if target in controls or not all(0 <= c < n for c in controls) or not 0 <= target < n:
        raise ValueError("bad control or target qubit")
    cmask = sum(1 << c for c in controls)
    out = list(state)
    m = 1 << target
    for x in range(1 << n):
        if x & m == 0 and x & cmask == cmask:
            a0, a1 = state[x], state[x | m]
            out[x] = u[0][0] * a0 + u[0][1] * a1
            out[x | m] = u[1][0] * a0 + u[1][1] * a1
    return out


def apply_permutation(state: Vector, perm: list[int]) -> Vector:
    """Map the basis state |x> to |perm[x]>. perm must be a bijection of range(2**n)."""
    if sorted(perm) != list(range(len(state))):
        raise ValueError("not a permutation of the basis states")
    out = [0j] * len(state)
    for x, a in enumerate(state):
        out[perm[x]] = a
    return out


def apply_diagonal(state: Vector, phases: list[complex]) -> Vector:
    """Multiply the amplitude of |x> by phases[x]."""
    if len(phases) != len(state):
        raise ValueError("length mismatch")
    return [p * a for p, a in zip(phases, state)]


def inner(phi: Vector, psi: Vector) -> complex:
    """<phi|psi>, conjugate-linear in the first argument."""
    return sum(a.conjugate() * b for a, b in zip(phi, psi))


def norm(state: Vector) -> float:
    return math.sqrt(sum(abs(a) ** 2 for a in state))


def probabilities(state: Vector) -> list[float]:
    """Exact outcome probabilities of a measurement in the computational basis."""
    return [a.real * a.real + a.imag * a.imag for a in state]


def measure(state: Vector, rng: random.Random) -> tuple[int, Vector]:
    """Measure all qubits in the computational basis. Returns (x, |x>)."""
    n = num_qubits(state)
    r = rng.random()
    acc = 0.0
    p = probabilities(state)
    x = len(p) - 1
    for i, pi in enumerate(p):
        acc += pi
        if r < acc:
            x = i
            break
    while p[x] == 0:  # guard against round-off at the end of the list
        x -= 1
    return x, basis_state(n, x)


def measure_qubit(state: Vector, q: int, rng: random.Random) -> tuple[int, Vector]:
    """Measure qubit q in the computational basis. Returns (b, the normalized post-measurement state)."""
    m = 1 << q
    p1 = sum(a.real * a.real + a.imag * a.imag for x, a in enumerate(state) if x & m)
    b = 1 if rng.random() < p1 else 0
    pb = p1 if b else 1 - p1
    s = 1 / math.sqrt(pb)
    return b, [a * s if bool(x & m) == bool(b) else 0j for x, a in enumerate(state)]


def identity(d: int) -> Matrix:
    return [[1 + 0j if i == j else 0j for j in range(d)] for i in range(d)]


def matmul(a: Matrix, b: Matrix) -> Matrix:
    return [[sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]


def matvec(a: Matrix, v: Vector) -> Vector:
    return [sum(a[i][k] * v[k] for k in range(len(v))) for i in range(len(a))]


def dagger(a: Matrix) -> Matrix:
    return [[a[j][i].conjugate() for j in range(len(a))] for i in range(len(a[0]))]


def scale(c: complex, a: Matrix) -> Matrix:
    return [[c * x for x in row] for row in a]


def add(a: Matrix, b: Matrix) -> Matrix:
    return [[x + y for x, y in zip(ra, rb)] for ra, rb in zip(a, b)]


def close(a, b, tol: float = TOL) -> bool:
    """Entrywise comparison of two vectors or two matrices."""
    if len(a) != len(b):
        return False
    for x, y in zip(a, b):
        if isinstance(x, list):
            if not close(x, y, tol):
                return False
        elif abs(x - y) > tol:
            return False
    return True


def is_unitary(u: Matrix, tol: float = TOL) -> bool:
    d = len(u)
    if any(len(row) != d for row in u):
        return False
    return close(matmul(dagger(u), u), identity(d), tol) and close(matmul(u, dagger(u)), identity(d), tol)


def circuit_matrix(n: int, run) -> Matrix:
    """The matrix of a linear map given as a function on states: column x is run(|x>)."""
    cols = [run(basis_state(n, x)) for x in range(1 << n)]
    return [[cols[x][y] for x in range(1 << n)] for y in range(1 << n)]


# ---------------------------------------------------------------- more linear algebra (qsim3)


def zeros(r: int, c: int | None = None) -> Matrix:
    return [[0j] * (r if c is None else c) for _ in range(r)]


def kron(a: Matrix, b: Matrix) -> Matrix:
    """The Kronecker product; a is the left (more significant) factor."""
    return [[x * y for x in ra for y in rb] for ra in a for rb in b]


def trace(a: Matrix) -> complex:
    return sum(a[i][i] for i in range(len(a)))


def sub(a: Matrix, b: Matrix) -> Matrix:
    return [[x - y for x, y in zip(ra, rb)] for ra, rb in zip(a, b)]


def commutator(a: Matrix, b: Matrix) -> Matrix:
    return sub(matmul(a, b), matmul(b, a))


def anticommutator(a: Matrix, b: Matrix) -> Matrix:
    return add(matmul(a, b), matmul(b, a))


def max_abs(a: Matrix) -> float:
    return max((abs(x) for row in a for x in row), default=0.0)


def eigh(h: Matrix, tol: float = 1e-15, max_sweeps: int = 60) -> tuple[list[float], Matrix]:
    """Eigenvalues and eigenvectors of a Hermitian matrix by complex Jacobi rotations.

    Returns (values, vectors) where column k of vectors has the eigenvalue values[k].
    """
    n = len(h)
    a = [[complex(x) for x in row] for row in h]
    v = identity(n)
    size = max(1e-300, math.sqrt(sum(abs(x) ** 2 for row in a for x in row)))
    for _ in range(max_sweeps):
        off = math.sqrt(sum(abs(a[i][j]) ** 2 for i in range(n) for j in range(n) if i != j))
        if off <= tol * size:
            break
        for p in range(n - 1):
            for q in range(p + 1, n):
                apq = a[p][q]
                m = abs(apq)
                if m <= 1e-300:
                    continue
                e = apq / m
                theta = 0.5 * math.atan2(2 * m, a[p][p].real - a[q][q].real)
                c, s = math.cos(theta), math.sin(theta)
                ec = e.conjugate()
                for k in range(n):
                    akp, akq = a[k][p], a[k][q]
                    a[k][p] = c * akp + s * ec * akq
                    a[k][q] = -s * akp + c * ec * akq
                    vkp, vkq = v[k][p], v[k][q]
                    v[k][p] = c * vkp + s * ec * vkq
                    v[k][q] = -s * vkp + c * ec * vkq
                for k in range(n):
                    apk, aqk = a[p][k], a[q][k]
                    a[p][k] = c * apk + s * e * aqk
                    a[q][k] = -s * apk + c * e * aqk
                a[p][q] = a[q][p] = 0j
    return [a[i][i].real for i in range(n)], v


def eigvalsh(h: Matrix) -> list[float]:
    """The eigenvalues of a Hermitian matrix in increasing order."""
    return sorted(eigh(h)[0])


def expm_hermitian(h: Matrix, t: float) -> Matrix:
    """e^(-i h t) for a Hermitian h, by the eigendecomposition."""
    vals, v = eigh(h)
    n = len(h)
    ph = [cmath.exp(-1j * lam * t) for lam in vals]
    return [[sum(v[i][k] * ph[k] * v[j][k].conjugate() for k in range(n)) for j in range(n)] for i in range(n)]


def expm_taylor(m: Matrix, tol: float = 1e-18) -> Matrix:
    """e^m for any square matrix m, by a Taylor series with scaling and squaring."""
    size = max(sum(abs(x) for x in row) for row in m)
    s = 0
    while size > 0.5:
        size /= 2
        s += 1
    ms = scale(2.0 ** -s, m)
    result = identity(len(m))
    term = identity(len(m))
    for k in range(1, 60):
        term = scale(1.0 / k, matmul(term, ms))
        result = add(result, term)
        if max(sum(abs(x) for x in row) for row in term) < tol:
            break
    for _ in range(s):
        result = matmul(result, result)
    return result


def op_norm(a: Matrix) -> float:
    """The spectral norm (the largest singular value)."""
    vals, _ = eigh(matmul(dagger(a), a))
    return math.sqrt(max(0.0, max(vals)))


# ---------------------------------------------------------------- Pauli strings and qubit operators (qsim3)

PAULI = {
    "I": [[1 + 0j, 0j], [0j, 1 + 0j]],
    "X": [[0j, 1 + 0j], [1 + 0j, 0j]],
    "Y": [[0j, -1j], [1j, 0j]],
    "Z": [[1 + 0j, 0j], [0j, -1 + 0j]],
}

# The product of two single-qubit Pauli letters: (a, b) -> (phase, c) with a b = phase c.
_TIMES = {}
for _a in "IXYZ":
    _TIMES[("I", _a)] = (1 + 0j, _a)
    _TIMES[(_a, "I")] = (1 + 0j, _a)
    _TIMES[(_a, _a)] = (1 + 0j, "I")
for _a, _b, _c in (("X", "Y", "Z"), ("Y", "Z", "X"), ("Z", "X", "Y")):
    _TIMES[(_a, _b)] = (1j, _c)
    _TIMES[(_b, _a)] = (-1j, _c)


def pauli_on(n: int, ops: dict[int, str]) -> str:
    """The Pauli string on n qubits with the letter ops[q] on qubit q and I elsewhere."""
    return "".join(ops.get(q, "I") for q in range(n - 1, -1, -1))


def weight(s: str) -> int:
    """The number of non-identity letters of a Pauli string."""
    return sum(1 for ch in s if ch != "I")


def pauli_string_mul(s: str, t: str) -> tuple[complex, str]:
    """s t = phase * u for two Pauli strings of the same length."""
    phase = 1 + 0j
    out = []
    for a, b in zip(s, t):
        p, c = _TIMES[(a, b)]
        phase *= p
        out.append(c)
    return phase, "".join(out)


def qop_clean(a: dict, tol: float = 1e-12) -> dict:
    return {s: c for s, c in a.items() if abs(c) > tol}


def qop_add(a: dict, b: dict, coef: complex = 1) -> dict:
    """a + coef * b."""
    out = dict(a)
    for s, c in b.items():
        out[s] = out.get(s, 0j) + coef * c
    return qop_clean(out)


def qop_scale(a: dict, coef: complex) -> dict:
    return qop_clean({s: coef * c for s, c in a.items()})


def qop_mul(a: dict, b: dict) -> dict:
    out: dict = {}
    for s, c in a.items():
        for t, d in b.items():
            p, u = pauli_string_mul(s, t)
            out[u] = out.get(u, 0j) + p * c * d
    return qop_clean(out)


def qop_dagger(a: dict) -> dict:
    return {s: c.conjugate() for s, c in a.items()}


def qop_matrix(a: dict, n: int) -> Matrix:
    """The 2^n x 2^n matrix of a qubit operator. P|x> = i^ny (-1)^popcount(x & zmask) |x xor xmask>."""
    d = 1 << n
    h = zeros(d)
    for s, c in a.items():
        xm = zm = ny = 0
        for pos, ch in enumerate(s):
            b = 1 << (n - 1 - pos)
            if ch in "XY":
                xm |= b
            if ch in "YZ":
                zm |= b
            if ch == "Y":
                ny += 1
        ph = c * 1j**ny
        for x in range(d):
            sign = -1 if bin(x & zm).count("1") & 1 else 1
            h[x ^ xm][x] += ph * sign
    return h


# ---------------------------------------------------------------- Fock space (qsim3)


def annihilation_matrix(n: int, j: int) -> Matrix:
    """The matrix of a_j on n modes, straight from the definition in the occupation basis.

    a_j |x> = (-1)^(n_0 + ... + n_{j-1}) |x - 2^j> when n_j = 1, and a_j |x> = 0 when n_j = 0.
    """
    d = 1 << n
    m = zeros(d)
    for x in range(d):
        if x >> j & 1:
            sign = -1 if bin(x & ((1 << j) - 1)).count("1") & 1 else 1
            m[x ^ (1 << j)][x] = sign + 0j
    return m


def number_matrix(n: int, j: int) -> Matrix:
    """n_j = a_j^dagger a_j, the diagonal matrix of bit j."""
    d = 1 << n
    m = zeros(d)
    for x in range(d):
        m[x][x] = complex(x >> j & 1)
    return m


def fermion_matrix(n: int, terms: list) -> Matrix:
    """The Fock-space matrix of a fermionic operator given as a list of (coefficient, word) pairs.

    A word is a tuple of (mode, dagger) pairs read from left to right, so
    (1.5, ((0, True), (2, False))) is 1.5 a_0^dagger a_2.
    """
    d = 1 << n
    a = [annihilation_matrix(n, j) for j in range(n)]
    ad = [dagger(m) for m in a]
    out = zeros(d)
    for coef, word in terms:
        m = identity(d)
        for j, is_dagger in word:
            m = matmul(m, ad[j] if is_dagger else a[j])
        out = add(out, scale(coef, m))
    return out
