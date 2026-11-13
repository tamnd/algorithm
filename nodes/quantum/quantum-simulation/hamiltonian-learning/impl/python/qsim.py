# SPDX-License-Identifier: MIT
# Shared helper of the qsim4 quantum pages of https://algorithm.tamnd.com/. The authors are listed in prov/.
"""A small pure-Python state-vector and density-matrix simulator.

This file is a copy of the qp1 helper, extended for the qsim4 pages with
density matrices, a Hermitian eigensolver, functions of Hermitian matrices
and Pauli strings. It holds no algorithm of any page.

Qubit order convention (the same as on the qp1 pages):
a state on n qubits is a list of 2**n complex amplitudes, indexed by x = sum_j b_j * 2**j,
where b_j is the value of qubit j. Qubit 0 is the least significant bit. The ket
|b_{n-1} ... b_1 b_0> is the binary numeral of x, and it is |b_{n-1}> (x) ... (x) |b_0>,
so qubit n-1 is the leftmost tensor factor and qubit 0 is the rightmost one.
A Pauli string such as "XIZ" is read the same way: its first letter acts on
qubit n-1 and its last letter on qubit 0. A Pauli sum is a list of
(real coefficient, string) pairs. A matrix is a list of rows of complex numbers.
"""

import cmath
import math
import random

TOL = 1e-9

Vector = list[complex]
Matrix = list[list[complex]]

PAULI = {
    "I": [[1 + 0j, 0j], [0j, 1 + 0j]],
    "X": [[0j, 1 + 0j], [1 + 0j, 0j]],
    "Y": [[0j, -1j], [1j, 0j]],
    "Z": [[1 + 0j, 0j], [0j, -1 + 0j]],
}


# ---------------------------------------------------------------- states (qp1)


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


def normalize(state: Vector) -> Vector:
    s = norm(state)
    if s == 0:
        raise ValueError("the zero vector has no direction")
    return [a / s for a in state]


def probabilities(state: Vector) -> list[float]:
    """Exact outcome probabilities of a measurement in the computational basis."""
    return [a.real * a.real + a.imag * a.imag for a in state]


def sample_index(p: list[float], rng: random.Random) -> int:
    """Draw an index i with probability p[i]."""
    r = rng.random()
    acc = 0.0
    x = len(p) - 1
    for i, pi in enumerate(p):
        acc += pi
        if r < acc:
            x = i
            break
    while p[x] == 0:  # guard against round-off at the end of the list
        x -= 1
    return x


def measure(state: Vector, rng: random.Random) -> tuple[int, Vector]:
    """Measure all qubits in the computational basis. Returns (x, |x>)."""
    x = sample_index(probabilities(state), rng)
    return x, basis_state(num_qubits(state), x)


def measure_qubit(state: Vector, q: int, rng: random.Random) -> tuple[int, Vector]:
    """Measure qubit q in the computational basis. Returns (b, the normalized post-measurement state)."""
    m = 1 << q
    p1 = sum(a.real * a.real + a.imag * a.imag for x, a in enumerate(state) if x & m)
    b = 1 if rng.random() < p1 else 0
    pb = p1 if b else 1 - p1
    s = 1 / math.sqrt(pb)
    return b, [a * s if bool(x & m) == bool(b) else 0j for x, a in enumerate(state)]


# ---------------------------------------------------------------- matrices (qp1)


def identity(d: int) -> Matrix:
    return [[1 + 0j if i == j else 0j for j in range(d)] for i in range(d)]


def zeros(d: int) -> Matrix:
    return [[0j] * d for _ in range(d)]


def matmul(a: Matrix, b: Matrix) -> Matrix:
    bt = list(zip(*b))
    return [[sum(x * y for x, y in zip(row, col)) for col in bt] for row in a]


def matvec(a: Matrix, v: Vector) -> Vector:
    return [sum(x * y for x, y in zip(row, v)) for row in a]


def dagger(a: Matrix) -> Matrix:
    return [[a[j][i].conjugate() for j in range(len(a))] for i in range(len(a[0]))]


def scale(c: complex, a: Matrix) -> Matrix:
    return [[c * x for x in row] for row in a]


def add(a: Matrix, b: Matrix) -> Matrix:
    return [[x + y for x, y in zip(ra, rb)] for ra, rb in zip(a, b)]


def sub(a: Matrix, b: Matrix) -> Matrix:
    return [[x - y for x, y in zip(ra, rb)] for ra, rb in zip(a, b)]


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


# ---------------------------------------------------------------- matrices (qsim4 additions)


def kron(a: Matrix, b: Matrix) -> Matrix:
    """The Kronecker product; a acts on the high (left) qubits."""
    return [[x * y for x in ra for y in rb] for ra in a for rb in b]


def trace(a: Matrix) -> complex:
    return sum(a[i][i] for i in range(len(a)))


def commutator(a: Matrix, b: Matrix) -> Matrix:
    return sub(matmul(a, b), matmul(b, a))


def max_abs_diff(a: Matrix, b: Matrix) -> float:
    return max(abs(x - y) for ra, rb in zip(a, b) for x, y in zip(ra, rb))


def outer(psi: Vector, phi: Vector) -> Matrix:
    """|psi><phi|."""
    return [[a * b.conjugate() for b in phi] for a in psi]


def expectation(a: Matrix, psi: Vector) -> float:
    """<psi|a|psi> for a Hermitian a and a normalized psi (the real part)."""
    return inner(psi, matvec(a, psi)).real


def partial_trace(rho: Matrix, keep: list[int]) -> Matrix:
    """Trace out every qubit not in keep. The result is ordered by the kept qubits,
    with keep[0] as the least significant qubit of the reduced state."""
    n = len(rho).bit_length() - 1
    out_d = 1 << len(keep)
    traced = [q for q in range(n) if q not in keep]
    out = zeros(out_d)

    def index(r: int, e: int) -> int:
        x = 0
        for k, q in enumerate(keep):
            x |= ((r >> k) & 1) << q
        for k, q in enumerate(traced):
            x |= ((e >> k) & 1) << q
        return x

    for r in range(out_d):
        for c in range(out_d):
            out[r][c] = sum(rho[index(r, e)][index(c, e)] for e in range(1 << len(traced)))
    return out


def eigh(h: Matrix, tol: float = 1e-15, max_sweeps: int = 80) -> tuple[list[float], Matrix]:
    """Eigenvalues and eigenvectors of a Hermitian matrix by complex Jacobi rotations.

    Returns (values, vectors), sorted by increasing value; column k of vectors
    is a unit eigenvector for values[k].
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
    order = sorted(range(n), key=lambda k: a[k][k].real)
    vals = [a[k][k].real for k in order]
    vecs = [[v[i][k] for k in order] for i in range(n)]
    return vals, vecs


def column(m: Matrix, k: int) -> Vector:
    return [row[k] for row in m]


def matrix_function(h: Matrix, f) -> Matrix:
    """f(h) for a Hermitian h, by eigendecomposition; f maps a real number to a complex one."""
    vals, v = eigh(h)
    n = len(h)
    fv = [f(lam) for lam in vals]
    return [[sum(v[i][k] * fv[k] * v[j][k].conjugate() for k in range(n)) for j in range(n)] for i in range(n)]


def expm_taylor(m: Matrix, tol: float = 1e-18) -> Matrix:
    """e^m for any square matrix m, by a Taylor series with scaling and squaring.

    m is divided by 2^s so that its largest row sum is at most 1/2. The series stops
    when a term has largest row sum below tol; the result is then squared s times.
    It uses no eigendecomposition, so it is an independent reference for matrix_function.
    """
    size = max(sum(abs(x) for x in row) for row in m)
    s = 0
    while size > 0.5:
        size /= 2
        s += 1
    ms = scale(2.0 ** -s, m)
    d = len(m)
    result = identity(d)
    term = identity(d)
    for k in range(1, 80):
        term = scale(1.0 / k, matmul(term, ms))
        result = add(result, term)
        if max(sum(abs(x) for x in row) for row in term) < tol:
            break
    for _ in range(s):
        result = matmul(result, result)
    return result


def trace_norm_hermitian(a: Matrix) -> float:
    vals, _ = eigh(a)
    return sum(abs(x) for x in vals)


def trace_distance(rho: Matrix, sigma: Matrix) -> float:
    """(1/2) ||rho - sigma||_1 for Hermitian rho and sigma."""
    return 0.5 * trace_norm_hermitian(sub(rho, sigma))


def solve_symmetric(a: list[list[float]], b: list[float], cutoff: float = 1e-10) -> list[float]:
    """The minimum-norm least-squares solution of a x = b for a real symmetric a,
    by the pseudo-inverse: eigenvalues below cutoff times the largest one are dropped."""
    vals, v = eigh([[complex(x) for x in row] for row in a])
    top = max([abs(x) for x in vals] + [1e-300])
    n = len(b)
    x = [0.0] * n
    for k, lam in enumerate(vals):
        if abs(lam) > cutoff * top:
            coef = sum(v[i][k].conjugate() * b[i] for i in range(n)) / lam
            for i in range(n):
                x[i] += (coef * v[i][k]).real
    return x


# ---------------------------------------------------------------- Pauli strings


def pauli_masks(s: str) -> tuple[int, int, int]:
    """Return (xmask, zmask, ny) with P = i^ny X^xmask Z^zmask as an operator."""
    n = len(s)
    xm = zm = ny = 0
    for pos, ch in enumerate(s):
        b = 1 << (n - 1 - pos)
        if ch == "X":
            xm |= b
        elif ch == "Z":
            zm |= b
        elif ch == "Y":
            xm |= b
            zm |= b
            ny += 1
        elif ch != "I":
            raise ValueError("not a Pauli string: " + s)
    return xm, zm, ny


def apply_pauli(psi: Vector, s: str) -> Vector:
    """P |psi>: P|x> = i^ny (-1)^popcount(x & zmask) |x xor xmask>."""
    xm, zm, ny = pauli_masks(s)
    ph = 1j ** ny
    out = [0j] * len(psi)
    for x, a in enumerate(psi):
        if a:
            sign = -1 if bin(x & zm).count("1") & 1 else 1
            out[x ^ xm] = ph * sign * a
    return out


def pauli_rotation(psi: Vector, s: str, theta: float) -> Vector:
    """e^(-i theta P / 2) |psi> = cos(theta/2) |psi> - i sin(theta/2) P |psi>."""
    p = apply_pauli(psi, s)
    c, sn = math.cos(theta / 2), math.sin(theta / 2)
    return [c * a - 1j * sn * b for a, b in zip(psi, p)]


def pauli_matrix(s: str) -> Matrix:
    m = [[1 + 0j]]
    for ch in s:
        m = kron(m, PAULI[ch])
    return m


def pauli_sum_matrix(terms: list[tuple[float, str]]) -> Matrix:
    n = len(terms[0][1])
    d = 1 << n
    h = zeros(d)
    for c, s in terms:
        xm, zm, ny = pauli_masks(s)
        ph = 1j ** ny
        for x in range(d):
            sign = -1 if bin(x & zm).count("1") & 1 else 1
            h[x ^ xm][x] += c * ph * sign
    return h


def pauli_sum_apply(terms: list[tuple[float, str]], psi: Vector) -> Vector:
    out = [0j] * len(psi)
    for c, s in terms:
        for i, b in enumerate(apply_pauli(psi, s)):
            out[i] += c * b
    return out


def pauli_expectation(psi: Vector, s: str) -> float:
    return inner(psi, apply_pauli(psi, s)).real


def all_pauli_strings(n: int) -> list[str]:
    out = [""]
    for _ in range(n):
        out = [w + ch for w in out for ch in "IXYZ"]
    return out
