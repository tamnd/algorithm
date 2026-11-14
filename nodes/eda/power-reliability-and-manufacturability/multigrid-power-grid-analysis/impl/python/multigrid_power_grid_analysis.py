# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/multigrid-power-grid-analysis/. The authors are listed in prov/C6B46K.jsonl.
"""Multigrid-like power grid analysis after Kozhaya, Nassif and Najm (2002).

The fine grid is a mesh of nx by ny nodes with the matrix A = G of the drop
equations A x = b. One reduction keeps every other row and every other column
(and the last ones). A dropped node takes its value from its kept neighbors,
with weights that are the conductances to them. This gives the interpolation
matrix P. The coarse system is A_c = P^T A P, b_c = P^T b. The reduction is
applied again to the coarse system, a dense direct solve ends the recursion,
and x = P x_c maps the answer back. There is no smoothing in this one-pass
method.

two_grid_iterate is NOT the method of the paper. It is a variant of this page
that adds Gauss-Seidel sweeps and repeats the coarse correction, so that the
answer converges to the exact solution.
"""

from __future__ import annotations

from typing import Dict, List, Optional, Sequence, Tuple

from pgrid import matmul, matvec, solve, transpose


def kept_lines(n: int) -> List[int]:
    """Indices of the lines that stay: every other one, and the last one."""
    return sorted(set(range(0, n, 2)) | {n - 1})


def prolongation(a: Sequence[Sequence[object]], shape: Tuple[int, int]):
    """Interpolation matrix P (fine by coarse) and the coarse shape.

    Classes of fine nodes: K is on a kept row and a kept column; H is on a
    kept row between two K nodes; V is on a kept column between two K nodes;
    C is on two dropped lines and takes its value from its four H and V
    neighbors. The weight of neighbor j of node m is the conductance -a[m][j].
    """
    nx, ny = shape
    kc, kr = kept_lines(nx), kept_lines(ny)
    col_of = {c: i for i, c in enumerate(kc)}
    row_of = {r: i for i, r in enumerate(kr)}
    ncx = len(kc)
    zero = a[0][0] * 0
    one = zero + 1
    rows: Dict[int, Dict[int, object]] = {}

    def at(r: int, c: int) -> int:
        return r * nx + c

    def blend(m: int, nbrs: List[int]) -> Dict[int, object]:
        ws = [max(-a[m][j], zero) for j in nbrs]
        tot = sum(ws, zero)
        if tot == 0:
            ws, tot = [one] * len(nbrs), one * len(nbrs)
        out: Dict[int, object] = {}
        for j, w in zip(nbrs, ws):
            for q, p in rows[j].items():
                out[q] = out.get(q, zero) + w * p / tot
        return out

    for r in kr:  # @line L2: kept nodes map to themselves
        for c in kc:
            rows[at(r, c)] = {row_of[r] * ncx + col_of[c]: one}
    for r in kr:  # H nodes: v_m = (g_mA v_A + g_mB v_B) / (g_mA + g_mB)
        for c in range(nx):
            if c not in col_of:
                rows[at(r, c)] = blend(at(r, c), [at(r, c - 1), at(r, c + 1)])
    for r in range(ny):  # V nodes, the same rule along the column
        if r not in row_of:
            for c in kc:
                rows[at(r, c)] = blend(at(r, c), [at(r - 1, c), at(r + 1, c)])
    for r in range(ny):  # C nodes, from their four H and V neighbors
        if r not in row_of:
            for c in range(nx):
                if c not in col_of:
                    nb = [at(r, c - 1), at(r, c + 1), at(r - 1, c), at(r + 1, c)]
                    rows[at(r, c)] = blend(at(r, c), nb)
    nc = ncx * len(kr)
    p = [[zero] * nc for _ in range(nx * ny)]
    for m, row in rows.items():
        for q, w in row.items():
            p[m][q] = w
    return p, (ncx, len(kr))


def knn_solve_with_basis(a, b, shape: Tuple[int, int], levels: int, min_size: int = 4):
    """One-pass multigrid-like solve. Returns x and the composite P of all levels."""
    n = len(b)
    nx, ny = shape
    if levels == 0 or n <= min_size or (len(kept_lines(nx)) == nx and len(kept_lines(ny)) == ny):
        zero = a[0][0] * 0
        ident = [[zero + (1 if i == j else 0) for j in range(n)] for i in range(n)]
        return solve(a, b), ident  # @line L1: a direct solve ends the recursion
    p, cshape = prolongation(a, shape)  # @line L2
    pt = transpose(p)
    ac = matmul(matmul(pt, a), p)  # @line L3: A_c = P^T A P
    bc = matvec(pt, b)  # @line L3: b_c = P^T b
    xc, pc = knn_solve_with_basis(ac, bc, cshape, levels - 1, min_size)  # @line L4
    return matvec(p, xc), matmul(p, pc)  # @line L5: x = P x_c, no smoothing


def knn_solve(a, b, shape: Tuple[int, int], levels: int, min_size: int = 4):
    """The one-pass answer x = P x_c."""
    return knn_solve_with_basis(a, b, shape, levels, min_size)[0]


def energy_error(a, x_exact, x) -> object:
    """||x_exact - x||_A squared, that is e^T A e."""
    e = [u - v for u, v in zip(x_exact, x)]
    ae = matvec(a, e)
    return sum((u * v for u, v in zip(e, ae)), e[0] * 0)


def gauss_seidel(a, b, x, sweeps: int):
    """Forward Gauss-Seidel sweeps, in place."""
    n = len(b)
    for _ in range(sweeps):
        for k in range(n):
            s = b[k]
            for j in range(n):
                if j != k and a[k][j] != 0:
                    s = s - a[k][j] * x[j]
            x[k] = s / a[k][k]
    return x


def two_grid_iterate(a, b, shape, cycles: int, sweeps: int = 1, x0: Optional[list] = None):
    """VARIANT, not in the paper: smoothing plus repeated coarse correction.

    Returns x and the list of residual norms max |b - A x| after each cycle.
    """
    p, _ = prolongation(a, shape)
    pt = transpose(p)
    ac = matmul(matmul(pt, a), p)
    x = list(x0) if x0 is not None else knn_solve(a, b, shape, 1)  # @line L6
    hist = []
    for _ in range(cycles):  # @line L7
        gauss_seidel(a, b, x, sweeps)  # @line L8
        r = [bi - ai for bi, ai in zip(b, matvec(a, x))]  # @line L9
        ec = solve(ac, matvec(pt, r))  # @line L10
        x = [xi + di for xi, di in zip(x, matvec(p, ec))]  # @line L10
        gauss_seidel(a, b, x, sweeps)  # @line L11
        hist.append(max(abs(bi - ai) for bi, ai in zip(b, matvec(a, x))))
    return x, hist
