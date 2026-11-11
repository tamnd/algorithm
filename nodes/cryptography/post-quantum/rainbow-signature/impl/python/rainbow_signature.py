# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/rainbow-signature/. The authors are listed in prov/DWHJ3K.jsonl.
"""A toy two-layer Rainbow signature over GF(31), and a toy key recovery in
the style of Beullens (2022): the simple attack finds a vector of the second
oil space O2, linear algebra then gives W and all of O2, and an exhaustive
search on the small first layer finishes the key, so that the attacker can
sign. The small systems are searched exhaustively instead of with XL or F4,
and the rectangular MinRank attack is not implemented.

Rainbow is broken: Beullens recovered a key for the NIST security level 1
parameters in about 53 hours on a laptop (Crypto 2022). Do not use it.

For study only. The code is not constant time, uses the random module, and
the toy sizes give no security. It is not the Rainbow of the NIST submission
(no GF(16) or GF(256), no official encoding). For real signatures use a
vetted library, for example a FIPS 140 validated module with ML-DSA.

Quadratic forms are symmetric matrices over GF(q), q odd: p(x) = x^T P x.
"""

import hashlib
import itertools
import random
from typing import List, Optional, Sequence, Tuple

Q = 31
Matrix = List[List[int]]
Vector = List[int]


# ---------------------------------------------------------------- linear algebra mod q

def mat_mul(a: Matrix, b: Matrix) -> Matrix:
    bt = list(zip(*b))
    return [[sum(x * y for x, y in zip(row, col)) % Q for col in bt] for row in a]


def transpose(a: Matrix) -> Matrix:
    return [list(r) for r in zip(*a)]


def mat_vec(a: Matrix, x: Sequence[int]) -> Vector:
    return [sum(r * y for r, y in zip(row, x)) % Q for row in a]


def quad_form(p: Matrix, x: Sequence[int]) -> int:
    return sum(xi * yi for xi, yi in zip(x, mat_vec(p, x))) % Q


def rref(a: Matrix) -> Tuple[Matrix, List[int]]:
    a = [list(r) for r in a]
    rows, cols = len(a), len(a[0]) if a else 0
    piv, r = [], 0
    for c in range(cols):
        p = next((i for i in range(r, rows) if a[i][c]), None)
        if p is None:
            continue
        a[r], a[p] = a[p], a[r]
        inv = pow(a[r][c], Q - 2, Q)
        a[r] = [x * inv % Q for x in a[r]]
        for i in range(rows):
            if i != r and a[i][c]:
                f = a[i][c]
                a[i] = [(x - f * y) % Q for x, y in zip(a[i], a[r])]
        piv.append(c)
        r += 1
        if r == rows:
            break
    return a, piv


def solve_any(a: Matrix, b: Sequence[int], unique: bool = False) -> Optional[Vector]:
    """A solution of a x = b (free variables set to 0), or None if there is
    none. With unique=True, also None when the solution is not unique."""
    cols = len(a[0])
    red, piv = rref([list(row) + [bi] for row, bi in zip(a, b)])
    if cols in piv or (unique and len(piv) < cols):
        return None
    x = [0] * cols
    for i, c in enumerate(piv):
        x[c] = red[i][cols]
    return x


def inverse(a: Matrix) -> Optional[Matrix]:
    n = len(a)
    red, piv = rref([list(row) + [int(i == j) for j in range(n)] for i, row in enumerate(a)])
    if piv != list(range(n)):
        return None
    return [row[n:] for row in red]


def nullspace(a: Matrix) -> List[Vector]:
    cols = len(a[0])
    red, piv = rref(a)
    basis = []
    for f in range(cols):
        if f in piv:
            continue
        x = [0] * cols
        x[f] = 1
        for i, c in enumerate(piv):
            x[c] = -red[i][f] % Q
        basis.append(x)
    return basis


def rank(vectors: Sequence[Sequence[int]]) -> int:
    return len(rref([list(v) for v in vectors])[1]) if vectors else 0


def random_invertible(n: int, rng: random.Random) -> Matrix:
    while True:
        s = [[rng.randrange(Q) for _ in range(n)] for _ in range(n)]
        if inverse(s) is not None:
            return s


def combine(P: Sequence[Matrix], c: Sequence[int]) -> Matrix:
    n = len(P[0])
    return [[sum(ck * Pk[i][j] for ck, Pk in zip(c, P)) % Q for j in range(n)] for i in range(n)]


# ---------------------------------------------------------------- Rainbow

def hash_to_field(message: bytes, salt: bytes, m: int) -> Vector:
    out, k = [], 0
    while len(out) < m:
        stream = hashlib.shake_256(message + salt).digest(4 * m + 16 * k + 16)
        out = [b % Q for b in stream if b < (256 // Q) * Q][:m]
        k += 1
    return out


def central_form(n: int, vin: int, oil: int, rng: random.Random) -> Matrix:
    """A symmetric n x n matrix that uses only the first vin + oil
    coordinates, with a zero oil x oil block (coordinates vin .. vin+oil-1)."""
    f = [[0] * n for _ in range(n)]
    for i in range(vin + oil):
        for j in range(i, vin + oil):
            if i >= vin and j >= vin:
                continue
            f[i][j] = f[j][i] = rng.randrange(Q)
    return f


class SecretKey:
    def __init__(self, F, S, T, v1, o1, o2):
        self.F, self.S, self.T = F, S, T
        self.Sinv, self.Tinv = inverse(S), inverse(T)
        self.v1, self.o1, self.o2 = v1, o1, o2


def keygen(v1: int, o1: int, o2: int, rng: random.Random) -> Tuple[List[Matrix], SecretKey]:
    n, m, v2 = v1 + o1 + o2, o1 + o2, v1 + o1
    F = [central_form(n, v1, o1, rng) for _ in range(o1)]      # @line L1
    F += [central_form(n, v2, o2, rng) for _ in range(o2)]     # @line L2
    S, T = random_invertible(n, rng), random_invertible(m, rng)  # @line L3
    G = [mat_mul(mat_mul(transpose(S), Fj), S) for Fj in F]
    P = [combine(G, T[k]) for k in range(m)]                    # @line L4
    return P, SecretKey(F, S, T, v1, o1, o2)                    # @line L5


def layer_system(F: Sequence[Matrix], z: Sequence[int], oil: int, target: Sequence[int]):
    """With the first p = len(z) coordinates fixed to z, each form
    z^T A z + 2 z^T B x_oil is linear in the next `oil` coordinates."""
    p = len(z)
    lhs = [[2 * sum(z[i] * Fk[i][p + j] for i in range(p)) % Q for j in range(oil)] for Fk in F]
    rhs = [(tk - quad_form([row[:p] for row in Fk[:p]], z)) % Q for Fk, tk in zip(F, target)]
    return lhs, rhs


def sign(sk: SecretKey, message: bytes, rng: random.Random) -> Tuple[Vector, bytes]:
    v1, o1, o2 = sk.v1, sk.o1, sk.o2
    n = v1 + o1 + o2
    salt = bytes(rng.getrandbits(8) for _ in range(16))
    t = mat_vec(sk.Tinv, hash_to_field(message, salt, o1 + o2))  # @line L6
    while True:
        xv = [rng.randrange(Q) for _ in range(v1)]                # @line L7
        x1 = solve_any(*layer_system(sk.F[:o1], xv, o1, t[:o1]), unique=True)  # @line L8
        if x1 is None:
            continue
        x2 = solve_any(*layer_system(sk.F[o1:], xv + x1, o2, t[o1:]), unique=True)  # @line L9
        if x2 is None:
            continue
        x = xv + x1 + x2
        assert len(x) == n
        return mat_vec(sk.Sinv, x), salt                          # @line L10


def verify(P: List[Matrix], message: bytes, sig: Tuple[Vector, bytes]) -> bool:
    s, salt = sig
    t = hash_to_field(message, salt, len(P))
    return all(quad_form(Pk, s) == tk for Pk, tk in zip(P, t))    # @line L11


def secret_subspaces(sk: SecretKey) -> Tuple[List[Vector], List[Vector]]:
    """O2 = S^-1 (last o2 coordinates) and W = T (last o2 outputs)."""
    n, m = sk.v1 + sk.o1 + sk.o2, sk.o1 + sk.o2
    O2 = [mat_vec(sk.Sinv, [int(i == n - sk.o2 + j) for i in range(n)]) for j in range(sk.o2)]
    W = [mat_vec(sk.T, [int(i == m - sk.o2 + j) for i in range(m)]) for j in range(sk.o2)]
    return O2, W


# ---------------------------------------------------------------- toy key recovery

def polar_matrix(P: Sequence[Matrix], x: Sequence[int]) -> Matrix:
    """The m x n matrix of the linear map y -> P'(x, y) = (2 x^T P_k y)_k."""
    return [[2 * v % Q for v in mat_vec(Pk, x)] for Pk in P]


def simple_attack(P: List[Matrix], o2: int, rng: random.Random, tries: int = 2000) -> Optional[Vector]:
    """Beullens' simple attack. D_x maps O2 into the o2-dimensional space W.
    For a random x this restricted map is singular with probability about
    1/q, and then some nonzero o in O2 has D_x(o) = 0. So solve P(o) = 0 for
    o in ker(D_x): m equations in n - m variables. At real sizes this
    overdetermined system goes to XL or F4; at toy size we search it."""
    n = len(P[0])
    for _ in range(tries):
        x = [rng.randrange(Q) for _ in range(n)]
        K = nullspace(polar_matrix(P, x))
        d = len(K)
        for c in itertools.product(range(Q), repeat=d):
            first = next((v for v in c if v), 0)
            if first != 1:                        # one point per line through 0
                continue
            o = [sum(ci * k[i] for ci, k in zip(c, K)) % Q for i in range(n)]
            if all(quad_form(Pk, o) == 0 for Pk in P) and in_O2(P, o, o2):
                return o
    return None


def in_O2(P: Sequence[Matrix], o: Sequence[int], o2: int) -> bool:
    """A vector of O2 has P'(y, o) in W for every y, so the m x n matrix of
    y -> P'(y, o) has rank at most o2 instead of m."""
    return rank([mat_vec(Pk, o) for Pk in P]) <= o2


def recover_W_perp_and_O2(P: List[Matrix], o: Sequence[int]) -> Tuple[List[Vector], List[Vector]]:
    """W is spanned by the P'(y, o). The combinations c orthogonal to W are
    the first layer forms, whose matrices have kernel O2."""
    rows = [mat_vec(Pk, o) for Pk in P]                 # row k is (P_k o)^T
    w_perp = nullspace(transpose(rows))                 # c with sum c_k (P_k o) = 0
    stacked = [row for c in w_perp for row in combine(P, c)]
    return w_perp, nullspace(stacked)


def complement_basis(sub: Sequence[Vector], n: int) -> List[Vector]:
    basis = list(sub)
    out = []
    for i in range(n):
        e = [int(j == i) for j in range(n)]
        if rank(basis + [e]) > len(basis):
            basis.append(e)
            out.append(e)
    return out


def projective_points(d: int):
    """One nonzero vector of GF(q)^d per line through 0."""
    for c in itertools.product(range(Q), repeat=d):
        if next((v for v in c if v), 0) == 1:
            yield c


def isotropic_subspace(L: List[Matrix], dim: int) -> Optional[List[Vector]]:
    """Toy step only: a subspace of dimension dim on which all forms in L
    vanish, by exhaustive search over the points of GF(q)^k (k = len(L[0]))
    and a depth-first search for pairwise orthogonal points."""
    k = len(L[0])
    pts = [list(c) for c in projective_points(k) if all(quad_form(Lc, c) == 0 for Lc in L)]

    def ortho(a, b):
        return all(sum(x * y for x, y in zip(a, mat_vec(Lc, b))) % Q == 0 for Lc in L)

    def extend(chosen, start):
        if len(chosen) == dim:
            return chosen
        for i in range(start, len(pts)):
            u = pts[i]
            if all(ortho(u, w) for w in chosen) and rank(chosen + [u]) > len(chosen):
                got = extend(chosen + [u], i + 1)
                if got:
                    return got
        return None

    return extend([], 0)


class RecoveredKey:
    def __init__(self, w_perp, O1, O2):
        self.w_perp, self.O1, self.O2 = w_perp, O1, O2


def recover_key(P: List[Matrix], o1: int, o2: int, rng: random.Random) -> Optional[RecoveredKey]:
    """Simple attack, then W and O2, then an oil space for the first layer
    forms restricted to a complement of O2. That last step is a smaller UOV
    key recovery; the toy does it by exhaustive search, so keep v1 + o1 <= 4."""
    n = len(P[0])
    o = simple_attack(P, o2, rng)
    if o is None:
        return None
    w_perp, O2 = recover_W_perp_and_O2(P, o)
    if len(w_perp) != o1 or len(O2) != o2:
        return None
    B = complement_basis(O2, n)                         # rows span a complement of O2
    layer1 = [mat_mul(mat_mul(B, combine(P, c)), transpose(B)) for c in w_perp]
    O1c = isotropic_subspace(layer1, o1)
    if O1c is None:
        return None
    O1 = [[sum(ci * b[i] for ci, b in zip(u, B)) % Q for i in range(n)] for u in O1c]
    return RecoveredKey(w_perp, O1, O2)


def forge(P: List[Matrix], key: RecoveredKey, message: bytes, rng: random.Random) -> Tuple[Vector, bytes]:
    """Sign with the recovered subspaces, layer by layer: first choose
    u1 in O1 so that the first layer forms match (linear, since they vanish
    on O1), then u2 in O2 so that all forms match (linear, since P(u2) = 0
    and the first layer forms ignore O2)."""
    n = len(P[0])
    salt = bytes(rng.getrandbits(8) for _ in range(16))
    t = hash_to_field(message, salt, len(P))
    while True:
        y = [rng.randrange(Q) for _ in range(n)]
        L = [combine(P, c) for c in key.w_perp]
        tl = [sum(ck * tk for ck, tk in zip(c, t)) % Q for c in key.w_perp]
        lhs = [[2 * sum(a * b for a, b in zip(y, mat_vec(Lc, u))) % Q for u in key.O1] for Lc in L]
        rhs = [(tc - quad_form(Lc, y)) % Q for Lc, tc in zip(L, tl)]
        a = solve_any(lhs, rhs, unique=True)
        if a is None:
            continue
        z = [(y[i] + sum(ai * u[i] for ai, u in zip(a, key.O1))) % Q for i in range(n)]
        lhs2 = [[2 * sum(a_ * b for a_, b in zip(z, mat_vec(Pk, u))) % Q for u in key.O2] for Pk in P]
        rhs2 = [(tk - quad_form(Pk, z)) % Q for Pk, tk in zip(P, t)]
        b = solve_any(lhs2, rhs2, unique=True)
        if b is None:
            continue
        s = [(z[i] + sum(bi * u[i] for bi, u in zip(b, key.O2))) % Q for i in range(n)]
        return s, salt
