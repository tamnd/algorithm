# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/unbalanced-oil-and-vinegar/. The authors are listed in prov/PHGT6X.jsonl.
"""Unbalanced oil and vinegar (UOV) signatures over GF(31) at toy size, and
the Kipnis-Shamir attack on balanced oil and vinegar (v = o).

For study only. The code is not constant time, uses the random module, and
the toy sizes give no security. It is not the UOV of the NIST submission (no
GF(256) or GF(16), no key compression, no official encoding). For real
signatures use a vetted library, for example a FIPS 140 validated module with
ML-DSA, or libsodium with Ed25519 where quantum attacks are not a concern.

Quadratic forms are symmetric matrices over GF(q), q odd: p(x) = x^T P x.
Coordinates 0 .. v-1 are vinegar and v .. n-1 are oil.
"""

import hashlib
import random
from typing import List, Optional, Sequence, Tuple

Q = 31
Matrix = List[List[int]]
Vector = List[int]


# ---------------------------------------------------------------- linear algebra mod q

def mat_mul(a: Matrix, b: Matrix, q: int = Q) -> Matrix:
    bt = list(zip(*b))
    return [[sum(x * y for x, y in zip(row, col)) % q for col in bt] for row in a]


def transpose(a: Matrix) -> Matrix:
    return [list(r) for r in zip(*a)]


def mat_vec(a: Matrix, x: Sequence[int], q: int = Q) -> Vector:
    return [sum(r * y for r, y in zip(row, x)) % q for row in a]


def quad_form(p: Matrix, x: Sequence[int], q: int = Q) -> int:
    return sum(xi * yi for xi, yi in zip(x, mat_vec(p, x, q))) % q


def rref(a: Matrix, q: int = Q) -> Tuple[Matrix, List[int]]:
    """Reduced row echelon form mod q and the pivot columns."""
    a = [list(r) for r in a]
    rows, cols = len(a), len(a[0]) if a else 0
    piv, r = [], 0
    for c in range(cols):
        p = next((i for i in range(r, rows) if a[i][c] % q), None)
        if p is None:
            continue
        a[r], a[p] = a[p], a[r]
        inv = pow(a[r][c], q - 2, q)
        a[r] = [x * inv % q for x in a[r]]
        for i in range(rows):
            if i != r and a[i][c]:
                f = a[i][c]
                a[i] = [(x - f * y) % q for x, y in zip(a[i], a[r])]
        piv.append(c)
        r += 1
        if r == rows:
            break
    return a, piv


def solve(a: Matrix, b: Sequence[int], q: int = Q) -> Optional[Vector]:
    """The unique x with a x = b for a square a, or None if a is singular."""
    n = len(a)
    red, piv = rref([list(row) + [bi] for row, bi in zip(a, b)], q)
    if piv != list(range(n)):
        return None
    return [red[i][n] for i in range(n)]


def inverse(a: Matrix, q: int = Q) -> Optional[Matrix]:
    n = len(a)
    red, piv = rref([list(row) + [int(i == j) for j in range(n)] for i, row in enumerate(a)], q)
    if piv != list(range(n)):
        return None
    return [row[n:] for row in red]


def nullspace(a: Matrix, q: int = Q) -> List[Vector]:
    """A basis of {x : a x = 0}."""
    cols = len(a[0])
    red, piv = rref(a, q)
    basis = []
    for f in range(cols):
        if f in piv:
            continue
        x = [0] * cols
        x[f] = 1
        for i, c in enumerate(piv):
            x[c] = -red[i][f] % q
        basis.append(x)
    return basis


def rank(vectors: Sequence[Sequence[int]], q: int = Q) -> int:
    return len(rref([list(v) for v in vectors], q)[1]) if vectors else 0


def random_invertible(n: int, rng: random.Random, q: int = Q) -> Matrix:
    while True:
        s = [[rng.randrange(q) for _ in range(n)] for _ in range(n)]
        if inverse(s, q) is not None:
            return s


# ---------------------------------------------------------------- UOV

def hash_to_field(message: bytes, salt: bytes, m: int, q: int = Q) -> Vector:
    """m elements of GF(q) from SHAKE256(message || salt), by rejection."""
    out, k = [], 0
    while len(out) < m:
        stream = hashlib.shake_256(message + salt).digest(4 * m + 16 * k + 16)
        out = [b % q for b in stream if b < (256 // q) * q][:m]
        k += 1
    return out


def random_central(v: int, o: int, rng: random.Random, q: int = Q) -> Matrix:
    """A symmetric n x n matrix with a zero oil x oil block."""
    n = v + o
    f = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i, n):
            if i >= v and j >= v:
                continue
            f[i][j] = f[j][i] = rng.randrange(q)
    return f


class SecretKey:
    def __init__(self, F: List[Matrix], S: Matrix, v: int, o: int):
        self.F, self.S, self.Sinv, self.v, self.o = F, S, inverse(S), v, o


def keygen(v: int, o: int, rng: random.Random) -> Tuple[List[Matrix], SecretKey]:
    n = v + o
    F = [random_central(v, o, rng) for _ in range(o)]          # @line L1
    S = random_invertible(n, rng)                               # @line L2
    St = transpose(S)
    P = [mat_mul(mat_mul(St, Fk), S) for Fk in F]               # @line L3
    return P, SecretKey(F, S, v, o)                             # @line L4


def sign(sk: SecretKey, message: bytes, rng: random.Random) -> Tuple[Vector, bytes]:
    v, o = sk.v, sk.o
    salt = bytes(rng.getrandbits(8) for _ in range(16))
    t = hash_to_field(message, salt, o)                         # @line L5
    while True:
        xv = [rng.randrange(Q) for _ in range(v)]               # @line L6
        # f_k(xv, xo) = xv^T A_k xv + 2 xv^T B_k xo, linear in xo
        lhs = [[2 * sum(xv[i] * Fk[i][v + j] for i in range(v)) % Q for j in range(o)]
               for Fk in sk.F]                                  # @line L7
        rhs = [(t[k] - quad_form([row[:v] for row in Fk[:v]], xv)) % Q for k, Fk in enumerate(sk.F)]
        xo = solve(lhs, rhs)
        if xo is None:                                          # @line L8
            continue
        x = xv + xo                                             # @line L9
        return mat_vec(sk.Sinv, x), salt                        # @line L10


def verify(P: List[Matrix], message: bytes, sig: Tuple[Vector, bytes]) -> bool:
    s, salt = sig
    t = hash_to_field(message, salt, len(P))
    return all(quad_form(Pk, s) == tk for Pk, tk in zip(P, t))  # @line L11


def oil_space(sk: SecretKey) -> List[Vector]:
    """The secret oil space O = S^-1 {x : x_vinegar = 0}, a basis."""
    n = sk.v + sk.o
    return [mat_vec(sk.Sinv, [int(i == sk.v + j) for i in range(n)]) for j in range(sk.o)]


def sign_with_oil_space(P: List[Matrix], O: List[Vector], message: bytes,
                        rng: random.Random) -> Tuple[Vector, bytes]:
    """Sign with any basis of a subspace O of dimension m on which P
    vanishes: P(y + o) = P(y) + 2 y^T P_k o, linear in o. This is how the
    modern UOV specification signs, and how an attacker forges once O is known."""
    m, n = len(P), len(P[0])
    salt = bytes(rng.getrandbits(8) for _ in range(16))
    t = hash_to_field(message, salt, m)
    while True:
        y = [rng.randrange(Q) for _ in range(n)]
        lhs = [[2 * sum(a * b for a, b in zip(y, mat_vec(Pk, oj))) % Q for oj in O] for Pk in P]
        rhs = [(tk - quad_form(Pk, y)) % Q for Pk, tk in zip(P, t)]
        c = solve(lhs, rhs)
        if c is None:
            continue
        s = [(y[i] + sum(cj * oj[i] for cj, oj in zip(c, O))) % Q for i in range(n)]
        return s, salt


# ---------------------------------------------------------------- Kipnis-Shamir attack

def vanishes(P: List[Matrix], vectors: Sequence[Vector]) -> bool:
    """P(a + b) = 0 on the span iff x^T P_k y = 0 for all basis pairs."""
    return all(sum(a * b for a, b in zip(x, mat_vec(Pk, y))) % Q == 0
               for Pk in P for x in vectors for y in vectors)


def kipnis_shamir(P: List[Matrix], rng: random.Random, tries: int = 200) -> Optional[List[Vector]]:
    """Recover the oil space of balanced oil and vinegar (n = 2m).
    For invertible combinations W1, W2 of the public matrices,
    M = W1^-1 W2 = S^-1 F1^-1 F2 S keeps O invariant, and its characteristic
    polynomial is g^2 where g is that of M on O. So an eigenvector with a
    one-dimensional eigenspace lies in O. Collect such vectors until they
    span m dimensions, then check that P vanishes on the span."""
    m, n = len(P), len(P[0])
    found: List[Vector] = []
    for _ in range(tries):
        c1 = [rng.randrange(Q) for _ in range(m)]
        c2 = [rng.randrange(Q) for _ in range(m)]
        w1 = [[sum(c * Pk[i][j] for c, Pk in zip(c1, P)) % Q for j in range(n)] for i in range(n)]
        w2 = [[sum(c * Pk[i][j] for c, Pk in zip(c2, P)) % Q for j in range(n)] for i in range(n)]
        w1inv = inverse(w1)
        if w1inv is None:
            continue
        M = mat_mul(w1inv, w2)
        for lam in range(Q):
            ker = nullspace([[(M[i][j] - (lam if i == j else 0)) % Q for j in range(n)] for i in range(n)])
            if len(ker) == 1 and quad_form(P[0], ker[0]) == 0 and rank(found + ker) > rank(found):
                if vanishes(P, found + ker):
                    found.append(ker[0])
        if len(found) == m:
            return found
    return None
