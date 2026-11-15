# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/invariant-subspace-algorithm/. The authors are listed in prov/55N3T2.jsonl.

"""The invariant subspace algorithm (ISA) of geometric control.

For x' = A x + B u and a subspace K of R^n (for example ker C), the
sequence

    V_0 = K,    V_(k+1) = K intersected with A^(-1)(V_k + im B)

is nonincreasing and stops after at most dim K + 1 steps at V*, the largest
(A, B)-invariant subspace contained in K. A subspace V is (A, B)-invariant
when A V is contained in V + im B; then some K_f gives (A - B K_f) V in V.

All subspace operations are exact in Fraction: a subspace is a list of basis
vectors (flat lists), kept in reduced row echelon form, so two equal
subspaces have the same representation.

The disturbance decoupling problem (DDP) for x' = A x + B u + E d, y = C x,
with state feedback u = -K x, is solvable if and only if im E is contained
in V*, the largest (A, B)-invariant subspace in ker C.
"""

from fractions import Fraction

__all__ = [
    "rref", "span", "kernel", "image", "subspace_sum", "intersection",
    "preimage", "contains", "is_ab_invariant", "isa", "friend",
    "ddp", "markov_zero",
]


def _frac_matrix(a):
    return [[Fraction(v) for v in row] for row in a]


def rref(rows):
    """Return the nonzero rows of the reduced row echelon form of rows."""
    m = [[Fraction(v) for v in r] for r in rows]
    if not m:
        return []
    ncol = len(m[0])
    out_row = 0
    for c in range(ncol):
        piv = None
        for r in range(out_row, len(m)):
            if m[r][c] != 0:
                piv = r
                break
        if piv is None:
            continue
        m[out_row], m[piv] = m[piv], m[out_row]
        p = m[out_row][c]
        m[out_row] = [v / p for v in m[out_row]]
        for r in range(len(m)):
            if r != out_row and m[r][c] != 0:
                f = m[r][c]
                m[r] = [x - f * y for x, y in zip(m[r], m[out_row])]
        out_row += 1
        if out_row == len(m):
            break
    return [r for r in m[:out_row] if any(v != 0 for v in r)]


def span(vectors):
    """Return the canonical basis (reduced row echelon form) of the span."""
    return rref(vectors)


def kernel(a, n=None):
    """Return a basis of {x : a x = 0}; n is the number of columns if a is empty."""
    a = _frac_matrix(a)
    if n is None:
        n = len(a[0]) if a else 0
    r = rref(a) if a else []
    pivots = []
    for row in r:
        for j, v in enumerate(row):
            if v != 0:
                pivots.append(j)
                break
    free = [j for j in range(n) if j not in pivots]
    basis = []
    for f in free:
        x = [Fraction(0)] * n
        x[f] = Fraction(1)
        for row, pj in zip(r, pivots):
            x[pj] = -row[f]
        basis.append(x)
    return span(basis)


def image(a):
    """Return a basis of the column space of a."""
    if not a or not a[0]:
        return []
    cols = [[Fraction(a[i][j]) for i in range(len(a))] for j in range(len(a[0]))]
    return span(cols)


def subspace_sum(u, v):
    """Return a basis of U + V."""
    return span(list(u) + list(v))


def intersection(u, v, n):
    """Return a basis of U intersected with V, both subspaces of R^n."""
    if not u or not v:
        return []
    # x = U a = V b: solve [U, -V] (a, b) = 0 and map back with U.
    k = len(u)
    mat = [[u[j][i] for j in range(k)] + [-v[j][i] for j in range(len(v))] for i in range(n)]
    sols = kernel(mat, k + len(v))
    vecs = [[sum(s[j] * u[j][i] for j in range(k)) for i in range(n)] for s in sols]
    return span(vecs)


def preimage(a, v):
    """Return a basis of A^(-1) V = {x : A x in V}."""
    n = len(a[0])
    # A x - V b = 0: solve [A, -V] (x, b) = 0 and keep the x part.
    mat = [[Fraction(a[i][j]) for j in range(n)] + [-w[i] for w in v] for i in range(len(a))]
    sols = kernel(mat, n + len(v))
    return span([s[:n] for s in sols])


def contains(u, v):
    """Return True if the subspace V is contained in U."""
    return len(subspace_sum(u, v)) == len(span(u))


def _matvec(a, x):
    return [sum(Fraction(ai) * xi for ai, xi in zip(row, x)) for row in a]


def is_ab_invariant(a, b, v):
    """Return True if A V is contained in V + im B."""
    target = subspace_sum(v, image(b))
    return all(contains(target, [_matvec(a, x)]) for x in v)


def isa(a, b, k_space):
    """Return (V*, dims): the largest (A, B)-invariant subspace in K.

    k_space is a basis of K. dims lists dim V_0, dim V_1, ... up to the
    first repeated value, so the last two entries are equal.
    """
    n = len(a)
    im_b = image(b)
    v = span(k_space)  # @line L1
    dims = [len(v)]
    while True:  # @line L2
        w = intersection(span(k_space), preimage(a, subspace_sum(v, im_b)), n)  # @line L3
        dims.append(len(w))
        if len(w) == len(v):  # @line L4
            return w, dims  # @line L5
        v = w  # @line L6


def _solve_square(m, rhs):
    """Solve m x = rhs exactly; m is square and invertible, rhs is a matrix."""
    n = len(m)
    aug = [list(map(Fraction, m[i])) + list(map(Fraction, rhs[i])) for i in range(n)]
    r = rref(aug)
    if len(r) < n or any(r[i][i] != 1 for i in range(n)):
        raise ValueError("matrix is singular")
    return [row[n:] for row in r]


def friend(a, b, v):
    """Return K (m by n, Fraction) with (A - B K) V contained in V.

    K is chosen on a basis of V and set to 0 on a complement of V. Raises
    ValueError if V is not (A, B)-invariant.
    """
    n = len(a)
    m = len(b[0]) if b and b[0] else 0
    basis = span(v)
    cols = []
    for x in basis:
        ax = _matvec(a, x)
        # A x = V w + B u: solve [V, B] (w, u) = A x.
        mat = [[w[i] for w in basis] + [Fraction(b[i][j]) for j in range(m)] for i in range(n)]
        sol = _particular(mat, ax)
        if sol is None:
            raise ValueError("V is not (A, B)-invariant")
        cols.append(sol[len(basis):])
    # Complete the basis of V to a basis T of R^n with unit vectors.
    t = list(basis)
    for i in range(n):
        e = [Fraction(int(i == j)) for j in range(n)]
        if len(span(t + [e])) > len(t):
            t.append(e)
    # K T = [u_1 ... u_k, 0 ... 0], so K = U T^(-1).
    u = [[cols[j][i] if j < len(cols) else Fraction(0) for j in range(n)] for i in range(m)]
    tmat = [[t[j][i] for j in range(n)] for i in range(n)]
    # Solve T^T K^T = U^T for K^T.
    tt = [[tmat[j][i] for j in range(n)] for i in range(n)]
    ut = [[u[i][j] for i in range(m)] for j in range(n)]
    kt = _solve_square(tt, ut)
    return [[kt[j][i] for j in range(n)] for i in range(m)]


def _particular(mat, rhs):
    """Return one solution x of mat x = rhs, or None if there is none."""
    ncol = len(mat[0])
    aug = [list(map(Fraction, mat[i])) + [Fraction(rhs[i])] for i in range(len(mat))]
    r = rref(aug)
    x = [Fraction(0)] * ncol
    for row in r:
        lead = next(j for j, v in enumerate(row) if v != 0)
        if lead == ncol:
            return None
        x[lead] = row[ncol]
    return x


def ddp(a, b, c, e):
    """Solve the disturbance decoupling problem by state feedback.

    Returns (K, V*) with C (A - B K)^j E = 0 for all j, or (None, V*) when
    im E is not contained in V*.
    """
    n = len(a)
    vstar, _ = isa(a, b, kernel(c, n))
    if not contains(vstar, image(e)):
        return None, vstar
    return friend(a, b, vstar), vstar


def markov_zero(a, b, c, e, k):
    """Return True if C (A - B K)^j E = 0 for j = 0, ..., n - 1."""
    n = len(a)
    m = len(b[0])
    acl = [[Fraction(a[i][j]) - sum(Fraction(b[i][t]) * k[t][j] for t in range(m)) for j in range(n)] for i in range(n)]
    cols = [[Fraction(e[i][j]) for i in range(n)] for j in range(len(e[0]))]
    for _ in range(n):
        for x in cols:
            if any(v != 0 for v in _matvec(c, x)):
                return False
        cols = [_matvec(acl, x) for x in cols]
    return True
