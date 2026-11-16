# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lie-algebraic-rotation-averaging/. The authors are listed in prov/XFRXH0.jsonl.

"""Lie-algebraic rotation averaging (Govindu; Chatterjee and Govindu).

There are N absolute rotations R_0, ..., R_(N-1) to find and a list of
edges (i, j, R_ij), each a measurement of the relative rotation
R_ij ~ R_j R_i^T. The residual of an edge is the rotation vector
r_ij = log(R_j^T R_ij R_i), which is zero when the edge agrees with the
estimate. Each iteration linearizes r_ij - w_j + w_i for the update
R_k <- R_k exp([w_k]_x), solves the weighted least squares problem in the
w_k (a graph Laplacian system with w_0 = 0) and applies the update.

The weights give the cost: "l2" weights 1 (the squared geodesic cost),
"l1" weights 1 / max(||r||, delta) (the sum of geodesic distances, by
iteratively reweighted least squares) and "gm" weights
sigma^2 / (||r||^2 + sigma^2)^2 (the Geman-McClure cost).
"""

import math
from collections import deque
from typing import Dict, List, Sequence, Tuple

from cvla import mul, solve, transpose

Vector = List[float]
Matrix = List[List[float]]
Edge = Tuple[int, int, Matrix]


def so3_exp(w: Sequence[float]) -> Matrix:
    """exp([w]_x) by the Rodrigues formula."""
    th = math.sqrt(w[0] * w[0] + w[1] * w[1] + w[2] * w[2])
    if th < 1e-8:
        a, b = 1.0 - th * th / 6.0, 0.5 - th * th / 24.0
    else:
        a, b = math.sin(th) / th, (1.0 - math.cos(th)) / (th * th)
    x, y, z = w
    k = [[0.0, -z, y], [z, 0.0, -x], [-y, x, 0.0]]
    k2 = mul(k, k)
    return [[(1.0 if i == j else 0.0) + a * k[i][j] + b * k2[i][j] for j in range(3)] for i in range(3)]


def so3_log(r: Sequence[Sequence[float]]) -> Vector:
    """The rotation vector w with exp([w]_x) = R and ||w|| <= pi."""
    c = max(-1.0, min(1.0, (r[0][0] + r[1][1] + r[2][2] - 1.0) / 2.0))
    v = [r[2][1] - r[1][2], r[0][2] - r[2][0], r[1][0] - r[0][1]]
    th = math.acos(c)
    if th < 1e-6:
        return [x * (0.5 + th * th / 12.0) for x in v]
    if th < math.pi - 1e-4:
        return [x * th / (2.0 * math.sin(th)) for x in v]
    # near pi: (R + R^T)/2 - cos(th) I = (1 - cos(th)) a a^T
    b = [[(r[i][j] + r[j][i]) / 2.0 - (c if i == j else 0.0) for j in range(3)] for i in range(3)]
    k = max(range(3), key=lambda i: b[i][i])
    col = [b[i][k] for i in range(3)]
    nc = math.sqrt(sum(x * x for x in col))
    a = [x / nc for x in col]
    if sum(x * y for x, y in zip(a, v)) < 0:
        a = [-x for x in a]
    return [th * x for x in a]


def angle(r1: Sequence[Sequence[float]], r2: Sequence[Sequence[float]]) -> float:
    """The angle of R1^T R2, in radians."""
    tr = sum(r1[k][i] * r2[k][i] for i in range(3) for k in range(3))
    return math.acos(max(-1.0, min(1.0, (tr - 1.0) / 2.0)))


def residual(rots: Sequence[Matrix], e: Edge) -> Vector:
    """r_ij = log(R_j^T R_ij R_i)."""
    i, j, rij = e
    return so3_log(mul(mul(transpose(rots[j]), rij), rots[i]))


def tree_init(n: int, edges: Sequence[Edge], root: int = 0) -> List[Matrix]:
    """Rotations from a breadth-first spanning tree: R_root = I and
    R_j = R_ij R_i along tree edges. Raises ValueError if the graph is not
    connected."""
    adj: Dict[int, List[Tuple[int, Matrix]]] = {k: [] for k in range(n)}
    for i, j, rij in edges:
        adj[i].append((j, rij))
        adj[j].append((i, transpose(rij)))
    rots: List = [None] * n
    rots[root] = [[1.0 if a == b else 0.0 for b in range(3)] for a in range(3)]
    queue = deque([root])
    while queue:
        i = queue.popleft()
        for j, rij in adj[i]:
            if rots[j] is None:
                rots[j] = mul(rij, rots[i])
                queue.append(j)
    if any(r is None for r in rots):
        raise ValueError("tree_init: the view graph is not connected")
    return rots


def weight(rnorm: float, loss: str, sigma: float, delta: float) -> float:
    """The IRLS weight psi(||r||) / ||r|| of a residual norm."""
    if loss == "l2":
        return 1.0
    if loss == "l1":
        return 1.0 / max(rnorm, delta)
    if loss == "gm":
        return sigma * sigma / (rnorm * rnorm + sigma * sigma) ** 2
    raise ValueError("unknown loss " + loss)


def laplacian_system(n: int, edges: Sequence[Edge], res: Sequence[Vector],
                     wts: Sequence[float]) -> Tuple[Matrix, Matrix]:
    """The grounded weighted Laplacian (node 0 removed) and the right-hand
    sides b_k = sum over edges (i, k) of w r - sum over edges (k, j) of w r."""
    lap = [[0.0] * n for _ in range(n)]
    b = [[0.0] * 3 for _ in range(n)]
    for (i, j, _), r, w in zip(edges, res, wts):
        lap[i][i] += w
        lap[j][j] += w
        lap[i][j] -= w
        lap[j][i] -= w
        for a in range(3):
            b[j][a] += w * r[a]
            b[i][a] -= w * r[a]
    return [row[1:] for row in lap[1:]], b[1:]


def lie_algebraic_rotation_averaging(n: int, edges: Sequence[Edge], loss: str = "l2",
                                     init: Sequence[Matrix] = None, sigma: float = 0.1,
                                     delta: float = 1e-6, max_iter: int = 100,
                                     eps: float = 1e-12) -> Tuple[List[Matrix], int]:
    """Average the relative rotations. Returns (R, iterations); R_0 = I
    unless init says otherwise."""
    rots = [list(map(list, r)) for r in init] if init is not None else tree_init(n, edges)  # @line L1
    it = 0
    for it in range(1, max_iter + 1):  # @line L2
        res = [residual(rots, e) for e in edges]  # @line L3
        wts = [weight(math.sqrt(sum(x * x for x in r)), loss, sigma, delta) for r in res]  # @line L4
        lap, b = laplacian_system(n, edges, res, wts)  # @line L5
        omega = [[0.0, 0.0, 0.0]] + solve(lap, b)
        rots = [mul(r, so3_exp(w)) for r, w in zip(rots, omega)]  # @line L6
        if max(math.sqrt(sum(x * x for x in w)) for w in omega) < eps:  # @line L7
            break
    return rots, it  # @line L8


def robust_rotation_averaging(n: int, edges: Sequence[Edge], sigma: float = 0.1,
                              l1_iter: int = 30, gm_iter: int = 30) -> List[Matrix]:
    """A robust run in the style of Chatterjee and Govindu: a few l1
    iterations from the tree start, then Geman-McClure iterations."""
    rots, _ = lie_algebraic_rotation_averaging(n, edges, loss="l1", max_iter=l1_iter, eps=1e-9)
    rots, _ = lie_algebraic_rotation_averaging(n, edges, loss="gm", init=rots, sigma=sigma,
                                               max_iter=gm_iter, eps=1e-10)
    return rots


def cost(rots: Sequence[Matrix], edges: Sequence[Edge], loss: str = "l2",
         sigma: float = 0.1) -> float:
    """sum ||r||^2 (l2), sum ||r|| (l1) or sum ||r||^2 / (||r||^2 + sigma^2) (gm)."""
    total = 0.0
    for e in edges:
        r = residual(rots, e)
        s = sum(x * x for x in r)
        if loss == "l2":
            total += s
        elif loss == "l1":
            total += math.sqrt(s)
        else:
            total += s / (s + sigma * sigma)
    return total
