# SPDX-License-Identifier: MIT
# Shared helper of the qp2 quantum pages of https://algorithm.tamnd.com/. The authors are listed in prov/.
"""A small pure-Python state-vector simulator for the qp2 pages.

Qubit order convention (the same as on the qp1 pages quantum-state and tensor-product):
a state on n qubits is a list of 2**n complex amplitudes, indexed by x = sum_j b_j * 2**j,
where b_j is the value of qubit j. Qubit 0 is the least significant bit. The ket
|b_{n-1} ... b_1 b_0> is the binary numeral of x, and it equals |b_{n-1}> (x) ... (x) |b_0>.

A gate list is a list of tuples, applied from left to right:
  ("x", q), ("h", q), ("z", q), ("s", q), ("sdg", q), ("t", q), ("tdg", q)
  ("cx", c, t)            a CNOT with control c and target t
  ("mcx", (c1, ..., ck), t)  an X on t when all of c1, ..., ck are 1 (k = 0 is a plain X)
The helper holds no algorithm of any page. It only applies matrices, permutations and phases.
"""

import cmath
import math
import random

TOL = 1e-9

Vector = list
Matrix = list

S2 = 1 / math.sqrt(2)
I2 = [[1, 0], [0, 1]]
X = [[0, 1], [1, 0]]
Y = [[0, -1j], [1j, 0]]
Z = [[1, 0], [0, -1]]
H = [[S2, S2], [S2, -S2]]
S = [[1, 0], [0, 1j]]
SDG = [[1, 0], [0, -1j]]
T = [[1, 0], [0, cmath.exp(1j * math.pi / 4)]]
TDG = [[1, 0], [0, cmath.exp(-1j * math.pi / 4)]]

ONE_QUBIT = {"x": X, "y": Y, "z": Z, "h": H, "s": S, "sdg": SDG, "t": T, "tdg": TDG}


def num_qubits(state: Vector) -> int:
    n = len(state).bit_length() - 1
    if n < 0 or 1 << n != len(state):
        raise ValueError("the length of a state must be a power of two")
    return n


def bit(x: int, j: int) -> int:
    return (x >> j) & 1


def basis_state(n: int, x: int) -> Vector:
    if not 0 <= x < 1 << n:
        raise ValueError("basis index out of range")
    v = [0j] * (1 << n)
    v[x] = 1 + 0j
    return v


def uniform_state(n: int) -> Vector:
    a = 1 / math.sqrt(1 << n)
    return [complex(a)] * (1 << n)


def apply_1q(state: Vector, u: Matrix, q: int) -> Vector:
    """Apply the 2 x 2 matrix u to qubit q."""
    return apply_controlled_1q(state, u, (), q)


def apply_controlled_1q(state: Vector, u: Matrix, controls, q: int) -> Vector:
    """Apply u to qubit q on the basis states where every qubit in controls is 1."""
    n = num_qubits(state)
    if not 0 <= q < n or q in controls:
        raise ValueError("bad target qubit")
    cmask = 0
    for c in controls:
        if not 0 <= c < n:
            raise ValueError("bad control qubit")
        cmask |= 1 << c
    out = list(state)
    m = 1 << q
    for x in range(1 << n):
        if x & m or (x & cmask) != cmask:
            continue
        a0, a1 = state[x], state[x | m]
        out[x] = u[0][0] * a0 + u[0][1] * a1
        out[x | m] = u[1][0] * a0 + u[1][1] * a1
    return out


def apply_matrix(state: Vector, u: Matrix, targets, controls=()) -> Vector:
    """Apply the 2**k x 2**k matrix u to the qubits targets (targets[i] is bit i of the row index of u),
    on the basis states where every qubit in controls is 1."""
    n = num_qubits(state)
    targets, controls = list(targets), list(controls)
    if len(set(targets + controls)) != len(targets) + len(controls):
        raise ValueError("targets and controls must be different qubits")
    if any(not 0 <= q < n for q in targets + controls) or len(u) != 1 << len(targets):
        raise ValueError("bad qubits or matrix size")
    cmask = sum(1 << c for c in controls)
    tmask = sum(1 << t for t in targets)
    out = list(state)
    for base in range(1 << n):
        if base & tmask or (base & cmask) != cmask:
            continue
        idx = [base | sum(((r >> i) & 1) << t for i, t in enumerate(targets)) for r in range(len(u))]
        amps = [state[i] for i in idx]
        for r, i in enumerate(idx):
            out[i] = sum(u[r][c] * amps[c] for c in range(len(u)))
    return out


def apply_permutation(state: Vector, perm) -> Vector:
    """Map the basis state |x> to |perm(x)>. perm is a function or a list; it must be a bijection."""
    n = num_qubits(state)
    size = 1 << n
    out = [0j] * size
    seen = [False] * size
    for x in range(size):
        y = perm(x) if callable(perm) else perm[x]
        if not 0 <= y < size or seen[y]:
            raise ValueError("the map is not a bijection on basis states")
        seen[y] = True
        out[y] = state[x]
    return out


def apply_diagonal(state: Vector, phase) -> Vector:
    """Multiply the amplitude of |x> by phase(x) (a function or a list)."""
    return [a * (phase(x) if callable(phase) else phase[x]) for x, a in enumerate(state)]


def apply_gate(state: Vector, g) -> Vector:
    name = g[0]
    if name in ONE_QUBIT:
        return apply_1q(state, ONE_QUBIT[name], g[1])
    if name == "cx":
        return apply_controlled_1q(state, X, (g[1],), g[2])
    if name == "mcx":
        return apply_controlled_1q(state, X, tuple(g[1]), g[2])
    raise ValueError(f"unknown gate {name!r}")


def run(state: Vector, gates) -> Vector:
    for g in gates:
        state = apply_gate(state, g)
    return state


def inverse_gates(gates):
    """The inverse of a gate list: the gates in reverse order, each one inverted."""
    inv = {"s": "sdg", "sdg": "s", "t": "tdg", "tdg": "t"}
    out = []
    for g in reversed(gates):
        out.append((inv.get(g[0], g[0]),) + tuple(g[1:]))
    return out


def run_classical(x: int, gates) -> int:
    """Run a gate list of x, cx and mcx gates on one classical bit string x."""
    for g in gates:
        name = g[0]
        if name == "x":
            x ^= 1 << g[1]
        elif name == "cx":
            if bit(x, g[1]):
                x ^= 1 << g[2]
        elif name == "mcx":
            if all(bit(x, c) for c in g[1]):
                x ^= 1 << g[2]
        else:
            raise ValueError(f"gate {name!r} is not a classical reversible gate")
    return x


def unitary_of(n: int, apply) -> Matrix:
    """The 2**n x 2**n matrix whose column x is apply(|x>)."""
    cols = [apply(basis_state(n, x)) for x in range(1 << n)]
    return [[cols[c][r] for c in range(1 << n)] for r in range(1 << n)]


def dagger(m: Matrix) -> Matrix:
    return [[complex(m[c][r]).conjugate() for c in range(len(m))] for r in range(len(m[0]))]


def matmul(a: Matrix, b: Matrix) -> Matrix:
    return [[sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]


def max_abs_diff(a: Matrix, b: Matrix) -> float:
    return max(abs(a[i][j] - b[i][j]) for i in range(len(a)) for j in range(len(a[0])))


def is_unitary(m: Matrix, tol: float = TOL) -> bool:
    eye = [[1 if i == j else 0 for j in range(len(m))] for i in range(len(m))]
    return max_abs_diff(matmul(dagger(m), m), eye) <= tol


def inner(a: Vector, b: Vector) -> complex:
    """<a|b>, linear in b."""
    return sum(complex(u).conjugate() * v for u, v in zip(a, b))


def norm(a: Vector) -> float:
    return math.sqrt(sum(abs(u) ** 2 for u in a))


def probabilities(state: Vector) -> list:
    return [abs(a) ** 2 for a in state]


def prob_qubit(state: Vector, q: int, value: int) -> float:
    return sum(abs(a) ** 2 for x, a in enumerate(state) if bit(x, q) == value)


def measure_qubit(state: Vector, q: int, rng: random.Random):
    """Measure qubit q in the computational basis. Returns (outcome, post-measurement state)."""
    p1 = prob_qubit(state, q, 1)
    b = 1 if rng.random() < p1 else 0
    p = p1 if b else 1 - p1
    s = 1 / math.sqrt(p)
    return b, [a * s if bit(x, q) == b else 0j for x, a in enumerate(state)]


def reduced_density_matrix(state: Vector, keep) -> Matrix:
    """The partial trace over every qubit not in keep. Row index r has bit i equal to qubit keep[i]."""
    n = num_qubits(state)
    keep = list(keep)
    rest = [q for q in range(n) if q not in keep]
    k = len(keep)

    def split(x):
        r = sum(bit(x, q) << i for i, q in enumerate(keep))
        e = sum(bit(x, q) << i for i, q in enumerate(rest))
        return r, e

    rho = [[0j] * (1 << k) for _ in range(1 << k)]
    groups = {}
    for x, a in enumerate(state):
        if a != 0:
            r, e = split(x)
            groups.setdefault(e, []).append((r, a))
    for items in groups.values():
        for r1, a1 in items:
            for r2, a2 in items:
                rho[r1][r2] += a1 * complex(a2).conjugate()
    return rho


def purity(rho: Matrix) -> float:
    """Tr(rho^2); it is 1 exactly for a pure state."""
    return sum((rho[i][j] * rho[j][i]).real for i in range(len(rho)) for j in range(len(rho)))


def random_state(n: int, rng: random.Random) -> Vector:
    v = [complex(rng.gauss(0, 1), rng.gauss(0, 1)) for _ in range(1 << n)]
    s = norm(v)
    return [a / s for a in v]


def random_unitary_2x2(rng: random.Random) -> Matrix:
    """A random 2 x 2 unitary e^(i d) [[a, -conj(b)], [b, conj(a)]] with |a|^2 + |b|^2 = 1."""
    a = complex(rng.gauss(0, 1), rng.gauss(0, 1))
    b = complex(rng.gauss(0, 1), rng.gauss(0, 1))
    s = math.sqrt(abs(a) ** 2 + abs(b) ** 2)
    a, b = a / s, b / s
    ph = cmath.exp(1j * rng.uniform(0, 2 * math.pi))
    return [[ph * a, -ph * b.conjugate()], [ph * b, ph * a.conjugate()]]
