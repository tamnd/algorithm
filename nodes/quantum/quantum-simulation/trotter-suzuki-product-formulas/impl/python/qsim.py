# SPDX-License-Identifier: MIT
# Shared helper of the qsim1 quantum pages of https://algorithm.tamnd.com/. The authors are listed in prov/.
"""A small pure-Python state-vector and matrix toolkit.

Conventions:
- A state on n qubits is a list of 2^n complex amplitudes.
- Qubit 0 is the least significant bit of the basis index.
- A Pauli string is text such as "XIZ" of length n. Its first character acts
  on qubit n - 1 and its last character on qubit 0, so the string is read as
  the tensor product P_(n-1) (x) ... (x) P_0, the order of kron().
- A Pauli sum is a list of (coefficient, string) pairs with real coefficients.
- A matrix is a list of rows, each a list of complex numbers.
"""

import cmath
import math
import random

PAULI = {
    "I": [[1, 0], [0, 1]],
    "X": [[0, 1], [1, 0]],
    "Y": [[0, -1j], [1j, 0]],
    "Z": [[1, 0], [0, -1]],
}


# ---------------------------------------------------------------- matrices


def identity(d):
    return [[1.0 + 0j if i == j else 0j for j in range(d)] for i in range(d)]


def mat_mul(a, b):
    bt = list(zip(*b))
    return [[sum(x * y for x, y in zip(row, col)) for col in bt] for row in a]


def mat_add(a, b, s=1.0):
    """Return a + s b."""
    return [[x + s * y for x, y in zip(ra, rb)] for ra, rb in zip(a, b)]


def mat_scale(a, s):
    return [[s * x for x in row] for row in a]


def dagger(a):
    return [[complex(x).conjugate() for x in col] for col in zip(*a)]


def kron(a, b):
    return [[x * y for x in ra for y in rb] for ra in a for rb in b]


def mat_vec(a, v):
    return [sum(x * y for x, y in zip(row, v)) for row in a]


def trace(a):
    return sum(a[i][i] for i in range(len(a)))


def commutator(a, b):
    return mat_add(mat_mul(a, b), mat_mul(b, a), -1.0)


def max_abs_diff(a, b):
    return max(abs(x - y) for ra, rb in zip(a, b) for x, y in zip(ra, rb))


def is_unitary(u, tol=1e-9):
    return max_abs_diff(mat_mul(u, dagger(u)), identity(len(u))) <= tol


# ---------------------------------------------------------------- Hermitian eigenproblem


def eigh(h, tol=1e-15, max_sweeps=60):
    """Eigenvalues and eigenvectors of a Hermitian matrix by complex Jacobi rotations.

    Returns (values, vectors) where vectors[:, k] (column k) has eigenvalue values[k].
    """
    n = len(h)
    a = [[complex(x) for x in row] for row in h]
    v = identity(n)
    scale = max(1e-300, math.sqrt(sum(abs(x) ** 2 for row in a for x in row)))
    for _ in range(max_sweeps):
        off = math.sqrt(sum(abs(a[i][j]) ** 2 for i in range(n) for j in range(n) if i != j))
        if off <= tol * scale:
            break
        for p in range(n - 1):
            for q in range(p + 1, n):
                apq = a[p][q]
                m = abs(apq)
                if m <= 1e-300:
                    continue
                e = apq / m  # e^(i phi)
                theta = 0.5 * math.atan2(2 * m, a[p][p].real - a[q][q].real)
                c, s = math.cos(theta), math.sin(theta)
                ec = e.conjugate()
                for k in range(n):  # columns: A <- A J, with J e_p = c e_p + s ec e_q
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


def expm_hermitian(h, t):
    """e^(-i h t) for Hermitian h, by eigen-decomposition."""
    vals, v = eigh(h)
    n = len(h)
    ph = [cmath.exp(-1j * lam * t) for lam in vals]
    return [[sum(v[i][k] * ph[k] * v[j][k].conjugate() for k in range(n)) for j in range(n)] for i in range(n)]


def expm_taylor(m, tol=1e-18):
    """e^m for a square matrix m, by a Taylor series with scaling and squaring.

    m is divided by 2^s so that its max row sum is at most 1/2. The series is cut
    when a term has max row sum below tol, then the result is squared s times.
    """
    norm = max(sum(abs(x) for x in row) for row in m)
    s = 0
    while norm > 0.5:
        norm /= 2
        s += 1
    ms = mat_scale(m, 2.0 ** -s)
    d = len(m)
    result = identity(d)
    term = identity(d)
    for k in range(1, 60):
        term = mat_scale(mat_mul(term, ms), 1.0 / k)
        result = mat_add(result, term)
        if max(sum(abs(x) for x in row) for row in term) < tol:
            break
    for _ in range(s):
        result = mat_mul(result, result)
    return result


def op_norm(a):
    """Spectral norm (largest singular value)."""
    vals, _ = eigh(mat_mul(dagger(a), a))
    return math.sqrt(max(0.0, max(vals)))


def trace_norm_hermitian(a):
    vals, _ = eigh(a)
    return sum(abs(x) for x in vals)


# ---------------------------------------------------------------- states


def basis_state(n, x=0):
    psi = [0j] * (1 << n)
    psi[x] = 1.0 + 0j
    return psi


def random_state(n, rng):
    psi = [complex(rng.gauss(0, 1), rng.gauss(0, 1)) for _ in range(1 << n)]
    norm = math.sqrt(sum(abs(z) ** 2 for z in psi))
    return [z / norm for z in psi]


def apply_1q(psi, q, u):
    out = list(psi)
    bit = 1 << q
    for x in range(len(psi)):
        if not x & bit:
            a0, a1 = psi[x], psi[x | bit]
            out[x] = u[0][0] * a0 + u[0][1] * a1
            out[x | bit] = u[1][0] * a0 + u[1][1] * a1
    return out


def apply_controlled(psi, c, q, u):
    out = list(psi)
    cb, bit = 1 << c, 1 << q
    for x in range(len(psi)):
        if x & cb and not x & bit:
            a0, a1 = psi[x], psi[x | bit]
            out[x] = u[0][0] * a0 + u[0][1] * a1
            out[x | bit] = u[1][0] * a0 + u[1][1] * a1
    return out


def apply_permutation(psi, perm):
    """|x> -> |perm[x]>."""
    out = [0j] * len(psi)
    for x, y in enumerate(perm):
        out[y] = psi[x]
    return out


def apply_diagonal(psi, phases):
    return [p * a for p, a in zip(phases, psi)]


def probabilities(psi):
    return [abs(a) ** 2 for a in psi]


def measure(psi, rng: random.Random):
    u = rng.random()
    acc = 0.0
    probs = probabilities(psi)
    for x, p in enumerate(probs):
        acc += p
        if u < acc:
            return x
    return len(probs) - 1


def inner(a, b):
    return sum(x.conjugate() * y for x, y in zip(a, b))


def vec_dist(a, b):
    return math.sqrt(sum(abs(x - y) ** 2 for x, y in zip(a, b)))


# ---------------------------------------------------------------- Pauli strings


def pauli_masks(s):
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


def apply_pauli(psi, s):
    """P |psi>, in O(2^n) operations: P|x> = i^ny (-1)^popcount(x & zmask) |x xor xmask>."""
    xm, zm, ny = pauli_masks(s)
    ph = 1j ** ny
    out = [0j] * len(psi)
    for x, a in enumerate(psi):
        if a:
            sign = -1 if bin(x & zm).count("1") & 1 else 1
            out[x ^ xm] = ph * sign * a
    return out


def pauli_rotation(psi, s, theta):
    """e^(-i theta P) |psi> = cos(theta) |psi> - i sin(theta) P |psi>."""
    p = apply_pauli(psi, s)
    c, sn = math.cos(theta), math.sin(theta)
    return [c * a - 1j * sn * b for a, b in zip(psi, p)]


def pauli_matrix(s):
    m = [[1.0 + 0j]]
    for ch in s:
        m = kron(m, PAULI[ch])
    return m


def pauli_sum_matrix(terms):
    n = len(terms[0][1])
    d = 1 << n
    h = [[0j] * d for _ in range(d)]
    for c, s in terms:
        xm, zm, ny = pauli_masks(s)
        ph = 1j ** ny
        for x in range(d):
            sign = -1 if bin(x & zm).count("1") & 1 else 1
            h[x ^ xm][x] += c * ph * sign
    return h


def pauli_sum_apply(terms, psi):
    out = [0j] * len(psi)
    for c, s in terms:
        for i, b in enumerate(apply_pauli(psi, s)):
            out[i] += c * b
    return out


def anticommute(s, t):
    """Two Pauli strings anticommute when an odd number of positions hold different non-identity letters."""
    k = sum(1 for a, b in zip(s, t) if a != "I" and b != "I" and a != b)
    return k % 2 == 1


def all_pauli_strings(n):
    out = [""]
    for _ in range(n):
        out = [w + ch for w in out for ch in "IXYZ"]
    return out


def pauli_decompose(m, tol=0.0):
    """Coefficients c_P = Tr(P m) / 2^n of a 2^n x 2^n matrix, in O(n 4^n) operations.

    For each X-part mask a, the vector y -> m[y xor a][y] is Walsh-Hadamard
    transformed over y; entry b of the result is Tr(X^a Z^b m). Then
    P = i^(popcount(a & b)) X^a Z^b gives Tr(P m). Returns {string: coefficient}
    for the coefficients with absolute value above tol.
    """
    d = len(m)
    n = d.bit_length() - 1
    if 1 << n != d:
        raise ValueError("the size must be a power of two")
    out = {}
    for a in range(d):
        f = [m[y ^ a][y] for y in range(d)]
        h = 1
        while h < d:  # Walsh-Hadamard transform: f[b] = sum_y (-1)^(b.y) f[y]
            for i in range(0, d, 2 * h):
                for j in range(i, i + h):
                    u, w = f[j], f[j + h]
                    f[j], f[j + h] = u + w, u - w
            h *= 2
        for b in range(d):
            # Tr(X^a Z^b m) = sum_y (-1)^(b.(y xor a)) m[y xor a][y] = (-1)^(b.a) f[b]
            sign = -1 if bin(a & b).count("1") & 1 else 1
            val = (1j ** bin(a & b).count("1")) * sign * f[b] / d
            if abs(val) > tol:
                chars = []
                for q in range(n - 1, -1, -1):
                    xa, zb = (a >> q) & 1, (b >> q) & 1
                    chars.append("IZXY"[2 * xa + zb])
                out["".join(chars)] = val
    return out
