# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/deadbeat-control/. The authors are listed in prov/HZQ8MT.jsonl.

"""Deadbeat state feedback for x_(k+1) = A x_k + B u_k, with u_k = -K x_k.

The gain makes A - B K nilpotent, (A - B K)^N = 0, with the least possible N,
so every initial state reaches 0 in at most N steps. It works with any
number of inputs.

Method: the subspaces S_0 = {0} and S_j = {x : A x in S_(j-1) + range B}
are the states that some input sequence brings to 0 in j steps. They grow
until S_N = R^n. Choose a basis of R^n that runs through S_1, S_2, ...,
and for each basis vector v of S_j solve A v = s + B c with s in S_(j-1).
Setting K v = c gives (A - B K) v = s, so A - B K maps S_j into S_(j-1).

All arithmetic is exact (Fraction) for int and Fraction data. With float
data the rank decisions use a tolerance and the result is approximate.
"""

from fractions import Fraction

from ctlmat import mul, solve, transpose

__all__ = ["rref", "nullspace", "deadbeat_gain", "steps_to_zero"]


def _exact(M):
    return all(isinstance(v, (int, Fraction)) for row in M for v in row)


def rref(M, tol=1e-10):
    """Return (R, pivots): the reduced row echelon form of M and its pivot columns."""
    exact = _exact(M)
    R = [[Fraction(v) for v in row] for row in M] if exact else [[float(v) for v in row] for row in M]
    rows = len(R)
    cols = len(R[0]) if R else 0
    scale = 1.0 if exact else max([abs(v) for row in R for v in row] + [1.0])
    pivots = []
    r = 0
    for c in range(cols):
        if r == rows:
            break
        p = max(range(r, rows), key=lambda i: abs(R[i][c]))
        if (R[p][c] == 0) if exact else (abs(R[p][c]) <= tol * scale):
            continue
        R[r], R[p] = R[p], R[r]
        piv = R[r][c]
        R[r] = [v / piv for v in R[r]]
        for i in range(rows):
            if i != r and R[i][c] != 0:
                f = R[i][c]
                R[i] = [a - f * b for a, b in zip(R[i], R[r])]
        pivots.append(c)
        r += 1
    return R, pivots


def nullspace(M, tol=1e-10):
    """Return a basis (list of flat vectors) of the null space of M."""
    cols = len(M[0])
    R, pivots = rref(M, tol)
    free = [c for c in range(cols) if c not in pivots]
    basis = []
    one = Fraction(1) if _exact(M) else 1.0
    for f in free:
        v = [0 * one] * cols
        v[f] = one
        for i, p in enumerate(pivots):
            v[p] = -R[i][f]
        basis.append(v)
    return basis


def _rank(vectors, tol=1e-10):
    """Return the rank of a list of flat vectors."""
    if not vectors:
        return 0
    return len(rref(vectors, tol)[1])


def deadbeat_gain(A, B, tol=1e-10):
    """Return (K, N): a gain with (A - B K)^N = 0 and the least such N.

    A is n by n, B is n by m (lists of rows). Raises ValueError if no
    feedback makes A - B K nilpotent, that is, if some state cannot be
    brought to 0 in finite time (an uncontrollable eigenvalue is not 0).
    """
    n = len(A)
    m = len(B[0])
    V = []  # basis of S_(j-1), flat vectors
    C = []  # C[i] = c with A V[i] - B c in the previous subspace
    N = 0
    while len(V) < n:  # @line L1
        N += 1
        # Rows of [A, -V, -B]; a null vector (x, a, c) gives A x = V a + B c.
        big = [list(A[i]) + [-v[i] for v in V] + [-B[i][j] for j in range(m)] for i in range(n)]
        found = False
        offset = n + len(V)
        for z in nullspace(big, tol):  # @line L2
            x = z[:n]
            c = z[offset:]
            if _rank(V + [x], tol) > len(V):  # @line L3
                V.append(x)
                C.append(c)
                found = True
        if not found:  # @line L4
            raise ValueError("A - B K cannot be made nilpotent: an uncontrollable eigenvalue is not 0")
    # K V = C, so K = C V^(-1); solve V^T K^T = C^T.
    Vm = transpose(V)
    Cm = transpose(C)
    K = transpose(solve(transpose(Vm), transpose(Cm)))  # @line L5
    return K, N


def steps_to_zero(A, B):
    """Return the least j with range A^j inside range [B, A B, ..., A^(j-1) B].

    This is the least number of steps in which every state can be brought
    to 0 by some input sequence. Brute force, exact for exact data. Raises
    ValueError if there is no such j at most n.
    """
    n = len(A)
    R = []  # the columns of [B, A B, ..., A^(j-1) B]
    P = [[1 if i == j else 0 for j in range(n)] for i in range(n)]  # A^j
    for j in range(0, n + 1):
        if _rank(R + transpose(P)) == _rank(R):
            return j
        R = R + transpose(mul(P, B))
        P = mul(A, P)
    raise ValueError("some state cannot be brought to 0 in n steps")
