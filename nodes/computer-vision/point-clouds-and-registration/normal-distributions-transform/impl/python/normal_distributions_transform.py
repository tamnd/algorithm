# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/normal-distributions-transform/. The authors are listed in prov/2WB2RV.jsonl.
"""The normal distributions transform (NDT) for 2D scan registration, after
Biber and Strasser (IROS 2003).

The reference scan is cut into square cells of side `cell`. Each cell with
at least 3 points gets the mean q and the covariance S of its points: a
normal distribution. Four grids are used, shifted by half a cell in x, in y
and in both, so that every point falls into four cells.

A pose p = (tx, ty, phi) maps a point x of the current scan to
x' = R(phi) x + t. The cost is the negative NDT score

    f(p) = - sum_x sum_grids exp(-(x' - q)^T S^-1 (x' - q) / 2),

where q and S belong to the cell that contains x' in each grid (cells
without a distribution add nothing). f is minimized by Newton steps with
the analytic gradient and Hessian. If the Hessian is not positive definite,
the code adds a multiple of the identity, and it halves the step until f
decreases. These two safeguards are choices of this code.
"""

from __future__ import annotations

import math
from typing import Dict, List, Optional, Sequence, Tuple

Vector = List[float]
Matrix = List[List[float]]
Cell = Tuple[float, float, float, float, float]  # qx, qy, and S^-1 as a, b, c: [[a, b], [b, c]]

OFFSETS = ((0.0, 0.0), (0.5, 0.0), (0.0, 0.5), (0.5, 0.5))


def _key(x: float, y: float, cell: float, off: Tuple[float, float]) -> Tuple[int, int]:
    return (math.floor(x / cell - off[0]), math.floor(y / cell - off[1]))


def build_ndt(ref: Sequence[Sequence[float]], cell: float, min_points: int = 3,
              eig_floor: float = 0.001) -> List[Dict[Tuple[int, int], Cell]]:
    """The four grids of normal distributions. The covariance of a cell is
    sum (x - q)(x - q)^T / count. Its smaller eigenvalue is raised to at
    least eig_floor times the larger one (a choice of this code), so that
    points on a straight wall do not give a singular matrix."""
    grids = []
    for off in OFFSETS:
        groups: Dict[Tuple[int, int], List[Sequence[float]]] = {}
        for p in ref:
            groups.setdefault(_key(p[0], p[1], cell, off), []).append(p)
        cells: Dict[Tuple[int, int], Cell] = {}
        for k, pts in groups.items():
            n = len(pts)
            if n < min_points:
                continue
            qx = sum(p[0] for p in pts) / n
            qy = sum(p[1] for p in pts) / n
            sxx = sum((p[0] - qx) ** 2 for p in pts) / n
            sxy = sum((p[0] - qx) * (p[1] - qy) for p in pts) / n
            syy = sum((p[1] - qy) ** 2 for p in pts) / n
            # Eigen decomposition of the 2 x 2 covariance.
            tr, dif = sxx + syy, math.hypot(sxx - syy, 2.0 * sxy)
            l1, l2 = (tr + dif) / 2.0, (tr - dif) / 2.0
            if l1 <= 0.0:
                continue
            l2 = max(l2, eig_floor * l1)
            ang = 0.5 * math.atan2(2.0 * sxy, sxx - syy)
            c, s = math.cos(ang), math.sin(ang)
            # S^-1 = U diag(1/l1, 1/l2) U^T with U = [[c, -s], [s, c]].
            a = c * c / l1 + s * s / l2
            b = c * s / l1 - c * s / l2
            d = s * s / l1 + c * c / l2
            cells[k] = (qx, qy, a, b, d)
        grids.append(cells)
    return grids


def transform(p: Sequence[float], x: Sequence[float]) -> Vector:
    c, s = math.cos(p[2]), math.sin(p[2])
    return [c * x[0] - s * x[1] + p[0], s * x[0] + c * x[1] + p[1]]


def score(grids, cell: float, scan: Sequence[Sequence[float]], p: Sequence[float],
          derivatives: bool = False):
    """f(p), and if derivatives is True also the gradient g and Hessian H
    of f for the current assignment of points to cells."""
    c, s = math.cos(p[2]), math.sin(p[2])
    f = 0.0
    g = [0.0, 0.0, 0.0]
    H = [[0.0] * 3 for _ in range(3)]
    for x in scan:
        xp = [c * x[0] - s * x[1] + p[0], s * x[0] + c * x[1] + p[1]]
        # d x' / d phi and d^2 x' / d phi^2; d x' / d tx = (1, 0), d x' / d ty = (0, 1).
        j3 = [-s * x[0] - c * x[1], c * x[0] - s * x[1]]
        h33 = [-c * x[0] + s * x[1], -s * x[0] - c * x[1]]
        J = ([1.0, 0.0], [0.0, 1.0], j3)
        for off, cells in zip(OFFSETS, grids):
            cd = cells.get(_key(xp[0], xp[1], cell, off))
            if cd is None:
                continue
            qx, qy, a, b, d = cd
            u = [xp[0] - qx, xp[1] - qy]
            Au = [a * u[0] + b * u[1], b * u[0] + d * u[1]]
            e = math.exp(-0.5 * (u[0] * Au[0] + u[1] * Au[1]))
            f -= e
            if not derivatives:
                continue
            gi = [Au[0] * Ji[0] + Au[1] * Ji[1] for Ji in J]  # u^T A J_i
            for i in range(3):
                g[i] += e * gi[i]
                for k in range(i, 3):
                    Ji, Jk = J[i], J[k]
                    JAJ = (Ji[0] * (a * Jk[0] + b * Jk[1]) + Ji[1] * (b * Jk[0] + d * Jk[1]))
                    second = Au[0] * h33[0] + Au[1] * h33[1] if i == 2 and k == 2 else 0.0
                    H[i][k] += e * (-gi[i] * gi[k] + JAJ + second)
    if not derivatives:
        return f
    for i in range(3):
        for k in range(i):
            H[i][k] = H[k][i]
    return f, g, H


def _solve3(H: Matrix, r: Sequence[float]) -> Optional[Vector]:
    """Solve H x = r for a symmetric 3 x 3 H by Cholesky; None if H is not
    positive definite."""
    L = [[0.0] * 3 for _ in range(3)]
    for i in range(3):
        for j in range(i + 1):
            v = H[i][j] - sum(L[i][k] * L[j][k] for k in range(j))
            if i == j:
                if v <= 0.0:
                    return None
                L[i][i] = math.sqrt(v)
            else:
                L[i][j] = v / L[j][j]
    y = [0.0] * 3
    for i in range(3):
        y[i] = (r[i] - sum(L[i][k] * y[k] for k in range(i))) / L[i][i]
    out = [0.0] * 3
    for i in reversed(range(3)):
        out[i] = (y[i] - sum(L[k][i] * out[k] for k in range(i + 1, 3))) / L[i][i]
    return out


def ndt_register(ref: Sequence[Sequence[float]], scan: Sequence[Sequence[float]], cell: float,
                 p0: Sequence[float] = (0.0, 0.0, 0.0), max_iter: int = 50, tol: float = 1e-9,
                 max_halvings: int = 20) -> Dict[str, object]:
    """Align scan to ref. Returns the pose p = (tx, ty, phi), the cost f(p)
    and the history of f, one value per accepted step."""
    grids = build_ndt(ref, cell)  # @line L1
    p = list(p0)
    f = score(grids, cell, scan, p)
    history = [f]
    for _ in range(max_iter):  # @line L2
        f, g, H = score(grids, cell, scan, p, derivatives=True)  # @line L3
        lam = 0.0
        while True:  # @line L4
            Hl = [[H[i][k] + (lam if i == k else 0.0) for k in range(3)] for i in range(3)]
            dp = _solve3(Hl, [-v for v in g])
            if dp is not None:
                break
            lam = max(2.0 * lam, 1e-6 * (1.0 + max(abs(H[i][i]) for i in range(3))))
        step = 1.0
        accepted = False
        for _ in range(max_halvings):  # @line L5
            q = [p[i] + step * dp[i] for i in range(3)]
            fq = score(grids, cell, scan, q)
            if fq < f:
                accepted = True
                break
            step *= 0.5
        if not accepted:
            break
        p = q  # @line L6
        history.append(fq)
        if f - fq <= tol * max(1.0, abs(fq)):  # @line L7
            break
    return {"p": p, "f": history[-1], "history": history}  # @line L8
