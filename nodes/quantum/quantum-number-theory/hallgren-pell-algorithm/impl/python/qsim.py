# SPDX-License-Identifier: MIT
# Shared helper of the qn2 quantum pages of https://algorithm.tamnd.com/. The authors are listed in prov/.
"""A small pure-Python state-vector simulator.

Qubit order convention (the same on every qn2 page):
a state on n qubits is a list of 2**n complex amplitudes, indexed by x = sum_j b_j * 2**j,
where b_j is the value of qubit j. Qubit 0 is the least significant bit. The ket
|b_{n-1} ... b_1 b_0> is the binary numeral of x, and it is |b_{n-1}> (x) ... (x) |b_0>,
so qubit n-1 is the leftmost tensor factor and qubit 0 is the rightmost one.

A register is a list of qubit indices, least significant bit first. The first part of the
file is the qp1 simulator. The second part adds register helpers for the qn2 pages: reading
and writing register values, a dense unitary on one register, the Fourier matrix of Z_N
padded to a register, oracles of the form |x>|y> -> |x>|y xor f(x)>, and marginals.
This file holds no algorithm of any page.
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


# ---------------------------------------------------------------- registers (qn2 additions)


def get_reg(x: int, reg: list[int]) -> int:
    """The integer held by the register reg in the basis state x."""
    v = 0
    for k, q in enumerate(reg):
        v |= ((x >> q) & 1) << k
    return v


def set_reg(x: int, reg: list[int], value: int) -> int:
    """The basis state x with the register reg set to value."""
    if value >> len(reg):
        raise ValueError("the value does not fit in the register")
    for k, q in enumerate(reg):
        if (value >> k) & 1:
            x |= 1 << q
        else:
            x &= ~(1 << q)
    return x


def registers(*sizes: int) -> list[list[int]]:
    """Consecutive registers of the given sizes, starting at qubit 0."""
    out, q = [], 0
    for s in sizes:
        out.append(list(range(q, q + s)))
        q += s
    return out


def apply_register_unitary(state: Vector, u: Matrix, reg: list[int]) -> Vector:
    """Apply the 2**k x 2**k matrix u to the register reg of k qubits. Returns a new list."""
    d = 1 << len(reg)
    if len(u) != d or any(len(row) != d for row in u):
        raise ValueError("the matrix does not match the register")
    mask = sum(1 << q for q in reg)
    offsets = [set_reg(0, reg, v) for v in range(d)]
    out = [0j] * len(state)
    for base in range(len(state)):
        if base & mask:
            continue
        col = [state[base | o] for o in offsets]
        if not any(col):
            continue
        for i in range(d):
            row = u[i]
            out[base | offsets[i]] = sum(row[j] * col[j] for j in range(d) if col[j])
    return out


def fourier_matrix(N: int, inverse: bool = False) -> Matrix:
    """The unitary of the Fourier transform of Z_N: |j> -> N^(-1/2) sum_k e^(2 pi i jk/N) |k>."""
    s = -1 if inverse else 1
    c = 1 / math.sqrt(N)
    return [[c * cmath.exp(s * 2j * math.pi * ((j * k) % N) / N) for j in range(N)] for k in range(N)]


def padded(u: Matrix, d: int) -> Matrix:
    """u acting on the first len(u) basis states of a d-dimensional space, the identity on the rest."""
    m = len(u)
    if m > d:
        raise ValueError("the matrix is larger than the space")
    out = identity(d)
    for i in range(m):
        for j in range(m):
            out[i][j] = u[i][j]
    return out


def apply_oracle(state: Vector, in_regs: list[list[int]], out_reg: list[int], f) -> Vector:
    """|x_1>...|x_k>|y> -> |x_1>...|x_k>|y xor f(x_1, ..., x_k)>, a permutation of the basis states."""
    perm = []
    for x in range(len(state)):
        v = f(*[get_reg(x, r) for r in in_regs])
        perm.append(set_reg(x, out_reg, get_reg(x, out_reg) ^ v))
    return apply_permutation(state, perm)


def marginal(probs: list[float], regs: list[list[int]]) -> dict:
    """The joint distribution of the values of the registers regs, as {tuple of values: probability}."""
    out: dict = {}
    for x, p in enumerate(probs):
        if p > 1e-15:
            key = tuple(get_reg(x, r) for r in regs)
            out[key] = out.get(key, 0.0) + p
    return out


def sample(dist: dict, rng: random.Random):
    """Draw one key from a distribution given as {key: probability}."""
    keys = sorted(dist)
    u = rng.random() * sum(dist.values())
    acc = 0.0
    for k in keys:
        acc += dist[k]
        if u < acc:
            return k
    return keys[-1]
