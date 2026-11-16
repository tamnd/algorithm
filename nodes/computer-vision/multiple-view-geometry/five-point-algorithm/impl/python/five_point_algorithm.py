# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/five-point-algorithm/. The authors are listed in prov/SJPGET.jsonl.
"""Nister's five-point algorithm for the essential matrix.

Given 5 point pairs x1[i] <-> x2[i] in normalized image coordinates
(x = K^-1 (u, v, 1), given here by their first 2 entries), find every
essential matrix E with x2[i]^T E x1[i] = 0. The 5 linear equations leave a
4-dimensional space E = x X + y Y + z Z + W. The 10 cubic constraints
det E = 0 and 2 E E^T E - tr(E E^T) E = 0 are reduced by Gauss-Jordan
elimination to a 3 x 3 matrix B(z) of polynomials in z, with
B(z) (x, y, 1)^T = 0, and det B(z) is a polynomial of degree 10. Each real
root z gives one solution. A few Gauss-Newton steps on the 10 cubic
equations then polish (x, y, z); this step is an addition of this code, and
it restores the digits that a root of det B(z) loses when another root is near.

The code also accepts n > 5 points: the four right singular vectors of the
smallest singular values then span the space of least algebraic error.

The scale w = 1 of W is a choice: a solution with w = 0 is missed. This is
a set of measure zero. Every output has Frobenius norm 1, and its entry of
largest absolute value is positive. Cost: O(1) for 5 points (a 10 x 20
elimination and the roots of a polynomial of degree 10), O(n) for n points.
"""

from __future__ import annotations

from typing import Dict, List, Sequence, Tuple

from cvla import cross, norm, polyroots_real, scale, solve, svd

Matrix = List[List[float]]
Poly = Dict[Tuple[int, int, int], float]

# The 20 monomials x^a y^b z^c of degree <= 3, in the order of Nister (2004).
MONOMIALS = [(3, 0, 0), (0, 3, 0), (2, 1, 0), (1, 2, 0), (2, 0, 1), (2, 0, 0),
             (0, 2, 1), (0, 2, 0), (1, 1, 1), (1, 1, 0),
             (1, 0, 2), (1, 0, 1), (1, 0, 0), (0, 1, 2), (0, 1, 1), (0, 1, 0),
             (0, 0, 3), (0, 0, 2), (0, 0, 1), (0, 0, 0)]


def canonical(E: Sequence[Sequence[float]]) -> Matrix:
    """E scaled to Frobenius norm 1, with its entry of largest absolute
    value positive (the first such entry, in row order, on a tie)."""
    f = norm(E)
    if f == 0.0:
        raise ValueError("zero matrix")
    big = max((x for row in E for x in row), key=abs)
    return scale(E, (1.0 if big > 0 else -1.0) / f)


# ------------------------------------------ polynomials in x, y and z

def _padd(p: Poly, q: Poly, c: float = 1.0) -> Poly:
    out = dict(p)
    for k, v in q.items():
        out[k] = out.get(k, 0.0) + c * v
    return out


def _pmul(p: Poly, q: Poly) -> Poly:
    out: Poly = {}
    for (a, b, c), u in p.items():
        for (d, e, f), v in q.items():
            k = (a + d, b + e, c + f)
            out[k] = out.get(k, 0.0) + u * v
    return out


def _pmatmul(A, B):
    return [[_padd(_padd(_pmul(A[i][0], B[0][j]), _pmul(A[i][1], B[1][j])), _pmul(A[i][2], B[2][j]))
             for j in range(3)] for i in range(3)]


def constraint_matrix(X: Matrix, Y: Matrix, Z: Matrix, W: Matrix) -> Matrix:
    """The 10 x 20 matrix of the cubic constraints on E = x X + y Y + z Z + W,
    in the monomial order MONOMIALS: row 0 is det E, rows 1 to 9 are the
    entries of 2 E E^T E - tr(E E^T) E."""
    E = [[{(1, 0, 0): X[i][j], (0, 1, 0): Y[i][j], (0, 0, 1): Z[i][j], (0, 0, 0): W[i][j]}
          for j in range(3)] for i in range(3)]
    Et = [[E[j][i] for j in range(3)] for i in range(3)]
    EEt = _pmatmul(E, Et)
    tr = _padd(_padd(EEt[0][0], EEt[1][1]), EEt[2][2])
    EEtE = _pmatmul(EEt, E)
    rows: List[Poly] = []
    d = _padd(_padd(_pmul(E[0][0], _padd(_pmul(E[1][1], E[2][2]), _pmul(E[1][2], E[2][1]), -1.0)),
                    _pmul(E[0][1], _padd(_pmul(E[1][2], E[2][0]), _pmul(E[1][0], E[2][2]), -1.0))),
              _pmul(E[0][2], _padd(_pmul(E[1][0], E[2][1]), _pmul(E[1][1], E[2][0]), -1.0)))
    rows.append(d)
    for i in range(3):
        for j in range(3):
            rows.append(_padd({k: 2.0 * v for k, v in EEtE[i][j].items()}, _pmul(tr, E[i][j]), -1.0))
    return [[r.get(m, 0.0) for m in MONOMIALS] for r in rows]


# ------------------------------------------- polynomials in z only

def _zadd(p: List[float], q: List[float], c: float = 1.0) -> List[float]:
    """p + c q, coefficients from the constant term up."""
    n = max(len(p), len(q))
    return [(p[i] if i < len(p) else 0.0) + c * (q[i] if i < len(q) else 0.0) for i in range(n)]


def _zmul(p: List[float], q: List[float]) -> List[float]:
    out = [0.0] * (len(p) + len(q) - 1)
    for i, a in enumerate(p):
        for j, b in enumerate(q):
            out[i + j] += a * b
    return out


def _zeval(p: List[float], z: float) -> float:
    s = 0.0
    for c in reversed(p):
        s = s * z + c
    return s


def _row_polys(c: List[float]) -> List[List[float]]:
    """The x, y and 1 parts of a reduced row, as polynomials in z (constant
    term first). c holds the 10 coefficients of xz^2, xz, x, yz^2, yz, y,
    z^3, z^2, z, 1."""
    return [[c[2], c[1], c[0]], [c[5], c[4], c[3]], [c[9], c[8], c[7], c[6]]]


def hidden_variable_matrix(C: Matrix) -> List[List[List[float]]]:
    """B(z) from the reduced rows: row r of B is row (4 + 2r) minus z times
    row (5 + 2r) of [I | C] (0-based), which removes x^2 z, y^2 z and x y z."""
    B = []
    for r in range(3):
        top, bottom = _row_polys(C[4 + 2 * r]), _row_polys(C[5 + 2 * r])
        B.append([_zadd(top[k], [0.0] + bottom[k], -1.0) for k in range(3)])
    return B


def _det3(B):
    def minor(a, b, c, d):
        return _zadd(_zmul(a, d), _zmul(b, c), -1.0)
    t0 = _zmul(B[0][0], minor(B[1][1], B[1][2], B[2][1], B[2][2]))
    t1 = _zmul(B[0][1], minor(B[1][0], B[1][2], B[2][0], B[2][2]))
    t2 = _zmul(B[0][2], minor(B[1][0], B[1][1], B[2][0], B[2][1]))
    return _zadd(_zadd(t0, t1, -1.0), t2)


def _monomials(x: float, y: float, z: float) -> List[float]:
    return [x ** a * y ** b * z ** c for a, b, c in MONOMIALS]


def _residual(M: Matrix, x: float, y: float, z: float) -> List[float]:
    m = _monomials(x, y, z)
    return [sum(p * q for p, q in zip(row, m)) for row in M]


def polish(M: Matrix, x: float, y: float, z: float, steps: int = 4) -> Tuple[float, float, float]:
    """Gauss-Newton steps on the 10 cubic equations M m(x, y, z) = 0. A step
    is kept only if it lowers the norm of the residual. A root of det B(z)
    that is close to another root has few correct digits; this restores
    them, because the solutions are far apart in (x, y, z)."""
    r = _residual(M, x, y, z)
    for _ in range(steps):
        cols = []
        for k in range(3):
            d = []
            for e in MONOMIALS:
                if e[k] == 0:
                    d.append(0.0)
                    continue
                f = list(e)
                f[k] -= 1
                d.append(e[k] * x ** f[0] * y ** f[1] * z ** f[2])
            cols.append([sum(p * q for p, q in zip(row, d)) for row in M])
        jtj = [[sum(a * b for a, b in zip(cols[i], cols[j])) for j in range(3)] for i in range(3)]
        jtr = [-sum(a * b for a, b in zip(cols[i], r)) for i in range(3)]
        try:
            step = solve(jtj, jtr)
        except ValueError:
            break
        nx, ny, nz = x + step[0], y + step[1], z + step[2]
        nr = _residual(M, nx, ny, nz)
        if norm(nr) >= norm(r):
            break
        x, y, z, r = nx, ny, nz, nr
    return x, y, z


# ------------------------------------------------------- the solver

def null_space_basis(x1: Sequence[Sequence[float]], x2: Sequence[Sequence[float]]) -> List[Matrix]:
    """X, Y, Z, W: the right singular vectors of the 4 smallest singular
    values of the n x 9 matrix of the epipolar constraints."""
    a = []
    for p, q in zip(x1, x2):  # @line L1
        y1, y2 = [float(p[0]), float(p[1]), 1.0], [float(q[0]), float(q[1]), 1.0]
        a.append([u * w for u in y2 for w in y1])  # @line L1
    a += [[0.0] * 9 for _ in range(9 - len(a))]
    _, _, v = svd(a)
    basis = []
    for col in range(5, 9):  # @line L2
        f = [v[i][col] for i in range(9)]
        basis.append([f[0:3], f[3:6], f[6:9]])
    return basis


def five_point(x1: Sequence[Sequence[float]], x2: Sequence[Sequence[float]]) -> List[Matrix]:
    """All essential matrices for n >= 5 pairs of normalized points, in
    canonical form. There are at most 10 solutions; often 2 to 4 are real."""
    if len(x1) != len(x2) or len(x1) < 5:
        raise ValueError("need at least 5 point pairs")
    X, Y, Z, W = null_space_basis(x1, x2)  # @line L2
    M = constraint_matrix(X, Y, Z, W)  # @line L3
    left = [row[:10] for row in M]  # @line L4
    right = [row[10:] for row in M]  # @line L4
    C = solve(left, right)  # @line L5
    B = hidden_variable_matrix(C)  # @line L6
    coeffs = _det3(B)  # @line L7
    out = []
    for z in polyroots_real(list(reversed(coeffs))):  # @line L7
        Bz = [[_zeval(p, z) for p in row] for row in B]
        cands = [cross(Bz[0], Bz[1]), cross(Bz[0], Bz[2]), cross(Bz[1], Bz[2])]
        v = max(cands, key=norm)  # @line L8
        if abs(v[2]) <= 1e-12 * norm(v):
            continue
        x, y = v[0] / v[2], v[1] / v[2]  # @line L8
        x, y, z = polish(M, x, y, z)  # @line L9
        E = [[x * X[i][j] + y * Y[i][j] + z * Z[i][j] + W[i][j] for j in range(3)] for i in range(3)]
        out.append(canonical(E))  # @line L10
    return out  # @line L11
