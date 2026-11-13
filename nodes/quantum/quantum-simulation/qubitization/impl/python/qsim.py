# SPDX-License-Identifier: MIT
# Shared helper of the qsim2 quantum pages of https://algorithm.tamnd.com/. The authors are listed in prov/.
"""A small pure-Python state-vector simulator.

Qubit order convention (the same on every qp1 page):
a state on n qubits is a list of 2**n complex amplitudes, indexed by x = sum_j b_j * 2**j,
where b_j is the value of qubit j. Qubit 0 is the least significant bit. The ket
|b_{n-1} ... b_1 b_0> is the binary numeral of x, and it is |b_{n-1}> (x) ... (x) |b_0>,
so qubit n-1 is the leftmost tensor factor and qubit 0 is the rightmost one.

The qsim2 extensions at the end of the file add Pauli strings, a Hermitian
eigensolver, matrix functions, block extraction, Householder preparation maps,
Chebyshev polynomials, Bessel functions and a solver for the phases of quantum
signal processing. A block encoding on a ancilla qubits and n system qubits
puts the ancillas on the high qubits, so the top-left 2**n x 2**n block of
the matrix is <0^a| U |0^a>.
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


# ---------------------------------------------------------------- qsim2 extensions: matrices

PAULI = {
    "I": [[1 + 0j, 0j], [0j, 1 + 0j]],
    "X": [[0j, 1 + 0j], [1 + 0j, 0j]],
    "Y": [[0j, -1j], [1j, 0j]],
    "Z": [[1 + 0j, 0j], [0j, -1 + 0j]],
}


def kron(a: Matrix, b: Matrix) -> Matrix:
    return [[x * y for x in ra for y in rb] for ra in a for rb in b]


def pauli_matrix(s: str) -> Matrix:
    """The matrix of a Pauli string. Its first letter acts on the highest qubit, its last on qubit 0."""
    m = [[1 + 0j]]
    for ch in s:
        m = kron(m, PAULI[ch])
    return m


def pauli_sum_matrix(terms) -> Matrix:
    """sum_j c_j P_j for a list of (c_j, string) pairs."""
    d = 1 << len(terms[0][1])
    h = [[0j] * d for _ in range(d)]
    for c, s in terms:
        p = pauli_matrix(s)
        for i in range(d):
            for j in range(d):
                if p[i][j] != 0:
                    h[i][j] += c * p[i][j]
    return h


def sub(a: Matrix, b: Matrix) -> Matrix:
    return [[x - y for x, y in zip(ra, rb)] for ra, rb in zip(a, b)]


def trace(a: Matrix) -> complex:
    return sum(a[i][i] for i in range(len(a)))


def commutator(a: Matrix, b: Matrix) -> Matrix:
    return sub(matmul(a, b), matmul(b, a))


def max_abs_diff(a: Matrix, b: Matrix) -> float:
    return max(abs(x - y) for ra, rb in zip(a, b) for x, y in zip(ra, rb))


def eigh(h: Matrix, tol: float = 1e-15, max_sweeps: int = 80):
    """Eigenvalues and eigenvectors of a Hermitian matrix by complex Jacobi rotations.

    Returns (values, v) where column k of v is a unit eigenvector for values[k].
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
                for k in range(n):  # columns: A <- A J with J e_p = c e_p + s ec e_q
                    akp, akq = a[k][p], a[k][q]
                    a[k][p] = c * akp + s * ec * akq
                    a[k][q] = -s * akp + c * ec * akq
                    vkp, vkq = v[k][p], v[k][q]
                    v[k][p] = c * vkp + s * ec * vkq
                    v[k][q] = -s * vkp + c * ec * vkq
                for k in range(n):  # rows: A <- J^dagger A
                    apk, aqk = a[p][k], a[q][k]
                    a[p][k] = c * apk + s * e * aqk
                    a[q][k] = -s * apk + c * e * aqk
                a[p][q] = a[q][p] = 0j
    return [a[i][i].real for i in range(n)], v


def hermitian_function(h: Matrix, f) -> Matrix:
    """f(h) for Hermitian h: V diag(f(lambda)) V^dagger, with f a scalar function that may return complex values."""
    vals, v = eigh(h)
    n = len(h)
    fv = [complex(f(lam)) for lam in vals]
    return [[sum(v[i][k] * fv[k] * v[j][k].conjugate() for k in range(n)) for j in range(n)] for i in range(n)]


def expm_hermitian(h: Matrix, t: float) -> Matrix:
    """The exact e^(-i h t) for Hermitian h, by eigendecomposition."""
    return hermitian_function(h, lambda lam: cmath.exp(-1j * lam * t))


def op_norm(a: Matrix) -> float:
    """The spectral norm: the square root of the largest eigenvalue of a^dagger a."""
    vals, _ = eigh(matmul(dagger(a), a))
    return math.sqrt(max(0.0, max(vals)))


def submatrix(a: Matrix, r0: int, c0: int, rows: int, cols: int) -> Matrix:
    return [row[c0:c0 + cols] for row in a[r0:r0 + rows]]


def top_left_block(u: Matrix, d: int) -> Matrix:
    """The block <0^a| u |0^a> of a matrix whose ancillas are the high qubits; d = 2**n."""
    return submatrix(u, 0, 0, d, d)


def random_state(n: int, rng: random.Random) -> Vector:
    psi = [complex(rng.gauss(0, 1), rng.gauss(0, 1)) for _ in range(1 << n)]
    s = norm(psi)
    return [z / s for z in psi]


def random_hermitian(d: int, rng: random.Random) -> Matrix:
    h = [[0j] * d for _ in range(d)]
    for i in range(d):
        h[i][i] = complex(rng.gauss(0, 1))
        for j in range(i + 1, d):
            z = complex(rng.gauss(0, 1), rng.gauss(0, 1)) / math.sqrt(2)
            h[i][j] = z
            h[j][i] = z.conjugate()
    return h


def random_unitary(d: int, rng: random.Random) -> Matrix:
    return expm_hermitian(random_hermitian(d, rng), 1.0)


def householder(v: Vector) -> Matrix:
    """A Hermitian unitary B with B|0> = v, for a unit vector v whose entry 0 is real.

    B = I - 2 w w^dagger / (w^dagger w) with w = |0> - v. Since B = B^dagger = B^-1,
    the same matrix is the preparation map and its inverse.
    """
    d = len(v)
    if isinstance(v[0], complex) and abs(v[0].imag) > 1e-12:
        raise ValueError("entry 0 of v must be real")
    w = [(1.0 if i == 0 else 0.0) - complex(v[i]) for i in range(d)]
    ww = sum(abs(x) ** 2 for x in w)
    if ww < 1e-30:
        return identity(d)
    return [[(1.0 if i == j else 0.0) - 2 * w[i] * w[j].conjugate() / ww for j in range(d)] for i in range(d)]


def complete_unitary(cols: list[Vector], d: int) -> Matrix:
    """A d x d unitary whose first columns are the given orthonormal vectors (Gram-Schmidt on the standard basis)."""
    basis = [list(map(complex, c)) for c in cols]
    for e in range(d):
        if len(basis) == d:
            break
        v = [1 + 0j if i == e else 0j for i in range(d)]
        for b in basis:
            p = inner(b, v)
            v = [x - p * y for x, y in zip(v, b)]
        for b in basis:  # a second pass for round-off
            p = inner(b, v)
            v = [x - p * y for x, y in zip(v, b)]
        s = norm(v)
        if s > 1e-8:
            basis.append([x / s for x in v])
    if len(basis) != d:
        raise ValueError("the columns are not orthonormal")
    return [[basis[j][i] for j in range(d)] for i in range(d)]


def split_registers(state: Vector, n: int) -> list[Vector]:
    """Cut a state on (ancilla, system) into the system vectors <a|state>, one for each ancilla basis state a."""
    d = 1 << n
    return [state[k:k + d] for k in range(0, len(state), d)]


def join_registers(parts: list[Vector]) -> Vector:
    out = []
    for p in parts:
        out.extend(p)
    return out


def solve_linear(a, b):
    """Solve a x = b for a small square real or complex system by Gaussian elimination with pivoting."""
    n = len(a)
    m = [list(row) + [b[i]] for i, row in enumerate(a)]
    for c in range(n):
        p = max(range(c, n), key=lambda r: abs(m[r][c]))
        if abs(m[p][c]) < 1e-300:
            raise ValueError("singular system")
        m[c], m[p] = m[p], m[c]
        for r in range(n):
            if r != c:
                f = m[r][c] / m[c][c]
                if f != 0:
                    for k in range(c, n + 1):
                        m[r][k] -= f * m[c][k]
    return [m[i][n] / m[i][i] for i in range(n)]


# ---------------------------------------------------------------- qsim2 extensions: special functions


def chebyshev_t(k: int, x: float) -> float:
    """T_k(x) by the three-term recurrence T_(j+1) = 2x T_j - T_(j-1)."""
    if k == 0:
        return 1.0
    a, b = 1.0, x
    for _ in range(k - 1):
        a, b = b, 2 * x * b - a
    return b


def bessel_j(k: int, x: float) -> float:
    """The Bessel function J_k(x) of integer order k >= 0, by its power series (accurate for |x| <= 20)."""
    term = (x / 2) ** k / math.factorial(k)
    total = term
    m = 0
    while True:
        m += 1
        term *= -(x / 2) ** 2 / (m * (m + k))
        total += term
        if abs(term) < 1e-17 * max(1.0, abs(total)) and m > x:
            return total


# ---------------------------------------------------------------- qsim2 extensions: quantum signal processing


def qsp_matrix(phases: list[float], x: float) -> Matrix:
    """U_Phi(x) = e^(i phi_0 Z) prod_j W(x) e^(i phi_j Z) with W(x) = [[x, i s], [i s, x]], s = sqrt(1 - x^2)."""
    s = math.sqrt(max(0.0, 1.0 - x * x))
    u = [[cmath.exp(1j * phases[0]), 0j], [0j, cmath.exp(-1j * phases[0])]]
    for ph in phases[1:]:
        a, b = cmath.exp(1j * ph), cmath.exp(-1j * ph)
        u = [
            [(u[0][0] * x + u[0][1] * 1j * s) * a, (u[0][0] * 1j * s + u[0][1] * x) * b],
            [(u[1][0] * x + u[1][1] * 1j * s) * a, (u[1][0] * 1j * s + u[1][1] * x) * b],
        ]
    return u


def qsp_full_phases(reduced: list[float], d: int) -> list[float]:
    """Symmetric phases phi_j = phi_(d-j) = reduced[min(j, d-j)], plus pi/4 on phi_0 and on phi_d."""
    full = [reduced[min(j, d - j)] for j in range(d + 1)]
    full[0] += math.pi / 4
    full[d] += math.pi / 4
    return full


def _qsp_value_and_grad(full: list[float], x: float):
    """Re <0|U_Phi(x)|0> and its gradient with respect to the d + 1 phases."""
    d = len(full) - 1
    s = math.sqrt(max(0.0, 1.0 - x * x))
    w = [[x + 0j, 1j * s], [1j * s, x + 0j]]

    def rz(ph):
        return [[cmath.exp(1j * ph), 0j], [0j, cmath.exp(-1j * ph)]]

    def mul(a, b):
        return [[a[0][0] * b[0][0] + a[0][1] * b[1][0], a[0][0] * b[0][1] + a[0][1] * b[1][1]],
                [a[1][0] * b[0][0] + a[1][1] * b[1][0], a[1][0] * b[0][1] + a[1][1] * b[1][1]]]

    left = [None] * (d + 1)  # left[j] = A_0 W A_1 ... W A_j
    left[0] = rz(full[0])
    for j in range(1, d + 1):
        left[j] = mul(mul(left[j - 1], w), rz(full[j]))
    right = [None] * (d + 1)  # right[j] = W A_(j+1) ... W A_d
    right[d] = [[1 + 0j, 0j], [0j, 1 + 0j]]
    for j in range(d - 1, -1, -1):
        right[j] = mul(mul(w, rz(full[j + 1])), right[j + 1])
    value = left[d][0][0].real
    grad = []
    for j in range(d + 1):
        lj, rj = left[j], right[j]
        g = 1j * (lj[0][0] * rj[0][0] - lj[0][1] * rj[1][0])
        grad.append(g.real)
    return value, grad


def qsp_real_phases(f, d: int, tol: float = 1e-13, max_iter: int = 100) -> list[float]:
    """Phases Phi (d + 1 of them) with Re <0|U_Phi(x)|0> = f(x) on [-1, 1].

    f must be a real polynomial of degree at most d with parity d mod 2 and
    max |f| < 1 on [-1, 1]. Newton's method on the symmetric reduced phases,
    matched at the m = floor(d/2) + 1 positive Chebyshev nodes, from the start
    point reduced = 0 where Re P = 0.
    """
    m = d // 2 + 1
    nodes = [math.cos((2 * k - 1) * math.pi / (4 * m)) for k in range(1, m + 1)]
    target = [f(x) for x in nodes]
    red = [0.0] * m

    def residual(r):
        full = qsp_full_phases(r, d)
        return [_qsp_value_and_grad(full, x)[0] - y for x, y in zip(nodes, target)]

    res = residual(red)
    for _ in range(max_iter):
        err = max(abs(v) for v in res)
        if err <= tol:
            return qsp_full_phases(red, d)
        full = qsp_full_phases(red, d)
        jac = []
        for x in nodes:
            _, g = _qsp_value_and_grad(full, x)
            row = [0.0] * m
            for j in range(d + 1):
                row[min(j, d - j)] += g[j]
            jac.append(row)
        step = solve_linear(jac, res)
        t = 1.0
        while True:  # backtracking keeps Newton from overshooting far from the solution
            trial = [a - t * b for a, b in zip(red, step)]
            tres = residual(trial)
            if max(abs(v) for v in tres) < err or t < 1e-4:
                red, res = trial, tres
                break
            t /= 2
    raise RuntimeError("QSP phase solver did not converge")
