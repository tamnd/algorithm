# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sum-of-squares-programming/. The authors are listed in prov/501R5E.jsonl.

"""A small sum-of-squares feasibility solver with exact certificates.

A polynomial is a dict that maps an exponent tuple to a coefficient, for
example {(4, 0): 2, (3, 1): 2, (2, 2): -1, (0, 4): 5} is
2 x^4 + 2 x^3 y - x^2 y^2 + 5 y^4.

An SOS program has m free scalars c_1, ..., c_m and a list of constraints.
Constraint j says that p0_j + c_1 p1_j + ... + c_m pm_j equals z_j^T Q_j z_j
for a positive semidefinite Gram matrix Q_j, where z_j is a list of
monomials (the basis). Matching the coefficients of every monomial gives
linear equations A u = b in the unknowns u = (c, entries of the Q_j).

solve() follows the pseudocode of the page (lines L1 to L11). It finds a
point of the affine set {A u = b} whose Gram blocks are positive definite,
by alternating projections between the affine set and the shifted cone
{Q >= eps I} in floating point. Then it rounds to rationals, projects back
onto {A u = b} exactly, and checks every block by an LDL^T factorization in
Fraction. A returned result is therefore an exact certificate. A return
value of None means that the search failed; it is not a proof that no
certificate exists.
"""

import math
from fractions import Fraction


# ---------------------------------------------------------------- polynomials

def monomials(nvars, lo, hi):
    """Exponent tuples of total degree lo..hi, by degree, then lexicographic
    from the largest power of the first variable."""
    out = []

    def rec(prefix, left, k):
        if k == nvars - 1:
            out.append(tuple(prefix + [left]))
            return
        for e in range(left, -1, -1):
            rec(prefix + [e], left - e, k + 1)

    for d in range(lo, hi + 1):
        rec([], d, 0)
    return out


def padd(p, q, s=1):
    r = dict(p)
    for k, v in q.items():
        r[k] = r.get(k, 0) + s * v
        if r[k] == 0:
            del r[k]
    return r


def pscale(p, s):
    return {k: s * v for k, v in p.items() if s * v != 0}


def pmul(p, q):
    r = {}
    for a, u in p.items():
        for b, v in q.items():
            k = tuple(x + y for x, y in zip(a, b))
            r[k] = r.get(k, 0) + u * v
    return {k: v for k, v in r.items() if v != 0}


def pclean(p):
    return {k: v for k, v in p.items() if v != 0}


def peval(p, x):
    s = 0
    for k, v in p.items():
        t = v
        for xi, e in zip(x, k):
            t = t * xi ** e
        s += t
    return s


def pderiv(p, i):
    r = {}
    for k, v in p.items():
        if k[i] > 0:
            kk = list(k)
            kk[i] -= 1
            kk = tuple(kk)
            r[kk] = r.get(kk, 0) + v * k[i]
    return pclean(r)


def gram_form(basis, Q):
    """The polynomial z^T Q z for the monomial list z = basis."""
    r = {}
    n = len(basis)
    for a in range(n):
        for b in range(n):
            if Q[a][b] == 0:
                continue
            k = tuple(x + y for x, y in zip(basis[a], basis[b]))
            r[k] = r.get(k, 0) + Q[a][b]
    return pclean(r)


# ------------------------------------------------------------- linear algebra

def ldl(Q):
    """Exact LDL^T of a symmetric matrix of Fractions.

    Returns (L, D) with Q = L diag(D) L^T if Q is positive semidefinite, and
    None if it is not. A zero pivot is allowed only if the rest of its column
    is zero after elimination."""
    n = len(Q)
    A = [[Fraction(v) for v in row] for row in Q]
    L = [[Fraction(int(i == j)) for j in range(n)] for i in range(n)]
    D = [Fraction(0)] * n
    for k in range(n):
        d = A[k][k] - sum(L[k][j] ** 2 * D[j] for j in range(k))
        col = [A[i][k] - sum(L[i][j] * L[k][j] * D[j] for j in range(k))
               for i in range(k + 1, n)]
        if d < 0:
            return None
        if d == 0:
            if any(v != 0 for v in col):
                return None
            continue
        D[k] = d
        for i, v in zip(range(k + 1, n), col):
            L[i][k] = v / d
    return L, D


def jacobi_eig(S, tol=1e-13, sweeps=60):
    """Eigenvalues and eigenvectors (columns of V) of a symmetric float
    matrix, by the cyclic Jacobi method."""
    n = len(S)
    A = [list(map(float, row)) for row in S]
    V = [[float(i == j) for j in range(n)] for i in range(n)]
    for _ in range(sweeps):
        off = sum(A[i][j] ** 2 for i in range(n) for j in range(n) if i != j)
        if off <= tol * tol * max(1.0, sum(A[i][i] ** 2 for i in range(n))):
            break
        for p in range(n - 1):
            for q in range(p + 1, n):
                if A[p][q] == 0.0:
                    continue
                theta = (A[q][q] - A[p][p]) / (2.0 * A[p][q])
                t = math.copysign(1.0, theta) / (abs(theta) + math.sqrt(theta * theta + 1.0))
                c = 1.0 / math.sqrt(t * t + 1.0)
                s = t * c
                for k in range(n):
                    akp, akq = A[k][p], A[k][q]
                    A[k][p] = c * akp - s * akq
                    A[k][q] = s * akp + c * akq
                for k in range(n):
                    apk, aqk = A[p][k], A[q][k]
                    A[p][k] = c * apk - s * aqk
                    A[q][k] = s * apk + c * aqk
                for k in range(n):
                    vkp, vkq = V[k][p], V[k][q]
                    V[k][p] = c * vkp - s * vkq
                    V[k][q] = s * vkp + c * vkq
    return [A[i][i] for i in range(n)], V


def _orthogonalize(rows, rhs, exact):
    """Gram-Schmidt on the rows of A u = b. Returns (O, g, norms) with
    orthogonal rows O, right-hand sides g, and squared norms; or None if the
    equations are inconsistent."""
    O, g, nn = [], [], []
    tol = 0 if exact else 1e-10
    for r, beta in zip(rows, rhs):
        r = list(r)
        for o, go, no in zip(O, g, nn):
            f = sum(x * y for x, y in zip(r, o)) / no
            if f != 0:
                r = [x - f * y for x, y in zip(r, o)]
                beta = beta - f * go
        n2 = sum(x * x for x in r)
        if n2 <= tol:
            if abs(beta) > (0 if exact else 1e-8):
                return None
            continue
        O.append(r)
        g.append(beta)
        nn.append(n2)
    return O, g, nn


def _project(u, O, g, nn):
    for o, go, no in zip(O, g, nn):
        f = (sum(x * y for x, y in zip(u, o)) - go) / no
        if f != 0:
            u = [x - f * y for x, y in zip(u, o)]
    return u


# ----------------------------------------------------------------- the solver

class SOSProgram:
    """Free scalars c_1..c_m and constraints p0 + sum c_i p_i is SOS."""

    def __init__(self, nfree=0):
        self.m = nfree
        self.cons = []  # (p0, [p_1, ..., p_m], basis)

    def add_sos(self, p0, ps=None, basis=None):
        ps = list(ps or [])
        ps = ps + [{}] * (self.m - len(ps))
        self.cons.append((dict(p0), ps, list(basis)))


def _layout(prog):
    """Index of every unknown: c_i first, then the upper triangle of each Q_j."""
    idx = prog.m
    blocks = []
    for _, _, basis in prog.cons:
        n = len(basis)
        pos = {}
        for a in range(n):
            for b in range(a, n):
                pos[(a, b)] = idx
                idx += 1
        blocks.append(pos)
    return idx, blocks


def _equations(prog, blocks, scale):
    """Rows of A u = b. With scale=True an off-diagonal unknown is sqrt(2)
    times the entry, so that the Euclidean norm of u is the Frobenius norm."""
    N = prog.m + sum(len(p) for p in blocks)
    rows, rhs = [], []
    for (p0, ps, basis), pos in zip(prog.cons, blocks):
        mons = set(p0)
        for p in ps:
            mons |= set(p)
        terms = {}
        for (a, b), k in pos.items():
            al = tuple(x + y for x, y in zip(basis[a], basis[b]))
            mons.add(al)
            if a == b:
                w = 1
            else:
                w = math.sqrt(2.0) if scale else 2
            terms.setdefault(al, []).append((k, w))
        for al in sorted(mons):
            row = [0.0 if scale else Fraction(0)] * N
            for i, p in enumerate(ps):
                if al in p:
                    row[i] = float(p[al]) if scale else Fraction(p[al])
            for k, w in terms.get(al, []):
                row[k] = -w
            b0 = p0.get(al, 0)
            rows.append(row)
            rhs.append(-float(b0) if scale else -Fraction(b0))
    return rows, rhs


def _block(u, pos, n, scale):
    Q = [[0] * n for _ in range(n)]
    for (a, b), k in pos.items():
        v = u[k]
        if a != b and scale:
            v = v / math.sqrt(2.0)
        Q[a][b] = Q[b][a] = v
    return Q


def solve(prog, eps=1e-3, iters=3000, denom=10 ** 6):
    """Search for an exact SOS certificate. Returns a dict with the free
    scalars 'c' (Fractions), the Gram matrices 'Q' and their LDL^T factors
    'ldl', or None if the search fails."""
    N, blocks = _layout(prog)
    rows, rhs = _equations(prog, blocks, True)  # @line L1
    fl = _orthogonalize(rows, rhs, False)  # @line L1
    if fl is None:  # @line L1
        return None  # @line L1
    u = [0.0] * N  # @line L2
    sizes = [len(c[2]) for c in prog.cons]
    found = False
    for _ in range(iters):  # @line L3
        u = _project(u, *fl)  # @line L4
        eig = [jacobi_eig(_block(u, pos, n, True)) for pos, n in zip(blocks, sizes)]
        if all(min(w) >= eps / 2 for w, _ in eig):  # @line L5
            found = True  # @line L5
            break  # @line L5
        for (w, V), pos, n in zip(eig, blocks, sizes):  # @line L6
            Q = [[sum(V[i][k] * max(w[k], eps) * V[j][k] for k in range(n))  # @line L6
                  for j in range(n)] for i in range(n)]  # @line L6
            for (a, b), k in pos.items():  # @line L6
                u[k] = Q[a][b] * (math.sqrt(2.0) if a != b else 1.0)  # @line L6
    if not found:  # @line L7
        return None  # @line L7
    q = list(u)  # @line L8
    for pos in blocks:  # @line L8
        for (a, b), k in pos.items():  # @line L8
            if a != b:  # @line L8
                q[k] = u[k] / math.sqrt(2.0)  # @line L8
    q = [Fraction(v).limit_denominator(denom) for v in q]  # @line L8
    ex = _orthogonalize(*_equations(prog, blocks, False), True)  # @line L9
    if ex is None:  # @line L9
        return None  # @line L9
    q = _project(q, *ex)  # @line L9
    Qs, facs = [], []
    for pos, n in zip(blocks, sizes):  # @line L10
        Q = _block(q, pos, n, False)  # @line L10
        f = ldl(Q)  # @line L10
        if f is None:  # @line L10
            return None  # @line L10
        Qs.append(Q)
        facs.append(f)
    return {"c": q[:prog.m], "Q": Qs, "ldl": facs}  # @line L11


def certificate_holds(prog, res):
    """Exact check: every constraint polynomial equals its Gram form, and
    every Gram matrix is positive semidefinite."""
    c = res["c"]
    for (p0, ps, basis), Q in zip(prog.cons, res["Q"]):
        p = dict(p0)
        for ci, pi in zip(c, ps):
            p = padd(p, pscale(pi, ci))
        if pclean(padd(p, gram_form(basis, Q), -1)):
            return False
        if ldl(Q) is None:
            return False
    return True


def sos_terms(basis, L, D):
    """The decomposition sum_k D[k] * l_k^2 with l_k = (column k of L)^T z."""
    out = []
    n = len(basis)
    for k in range(n):
        if D[k] == 0:
            continue
        lk = {}
        for i in range(n):
            if L[i][k] != 0:
                lk[basis[i]] = L[i][k]
        out.append((D[k], lk))
    return out


def lyapunov_program(f, vbasis, eps, vgram=None, dgram=None):
    """SOS program for a polynomial Lyapunov function V = sum c_i v_i with
    V - eps |x|^2 SOS and -dV/dt - eps |x|^2 SOS, for x' = f(x).

    f is a list of polynomials, vbasis a list of monomials for V, and vgram
    and dgram the Gram bases of the two constraints. By default they are all
    monomials of degree 1 to half the degree of each polynomial, rounded up.
    The solver needs a strictly feasible point, so a basis with monomials
    that no solution can use (outside the half Newton polytope) makes it
    fail; then pass smaller bases."""
    n = len(f)
    sq = {}
    for i in range(n):
        e = [0] * n
        e[i] = 2
        sq[tuple(e)] = Fraction(eps)
    vs = [{m: 1} for m in vbasis]
    vdots = []
    for v in vs:
        d = {}
        for i in range(n):
            d = padd(d, pmul(pderiv(v, i), f[i]))
        vdots.append(d)
    dv = max(sum(m) for m in vbasis)
    df = max(sum(m) for p in f for m in p)
    prog = SOSProgram(len(vbasis))
    if vgram is None:
        vgram = monomials(n, 1, (dv + 1) // 2)
    if dgram is None:
        dgram = monomials(n, 1, (dv + df) // 2)
    prog.add_sos(pscale(sq, -1), vs, vgram)
    prog.add_sos(pscale(sq, -1), [pscale(d, -1) for d in vdots], dgram)
    return prog
