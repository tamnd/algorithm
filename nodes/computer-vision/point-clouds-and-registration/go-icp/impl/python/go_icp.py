# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/go-icp/. The authors are listed in prov/AT1CTF.jsonl.
"""Go-ICP of Yang, Li, Campbell and Jia: globally optimal ICP by nested
branch and bound.

The cost is E(R, t) = sum_i e_i^2, with e_i = min_j ||R p_i + t - q_j||.
Rotations are angle-axis vectors r in a cube (by default [-pi, pi]^3, which
holds the pi-ball of all rotations). Translations are in a cube given by
its center and half side.

For a rotation cube of half side sigma_r with center r0, and a translation
cube of half side sigma_t with center t0, every (r, t) in the two cubes has

    e_i(R_r, t) >= max(e_i(R_r0, t0) - gamma_ri - gamma_t, 0),
    gamma_ri = 2 sin(min(sqrt(3) sigma_r / 2, pi / 2)) ||p_i||,
    gamma_t = sqrt(3) sigma_t.

The outer search splits rotation cubes, best first. For each cube it runs
an inner search over translation with the gamma_r of the cube, which
gives a lower bound for the whole cube. The true cost at the center
rotation and the best translation of that search is an upper bound; if it
beats the best cost E*, a local ICP starts there, which often lowers E* at
once. The search stops when E* minus the least lower bound in the queue is
below eps, so E* is within eps of the global minimum over the domain.

Three choices differ from the paper. The paper runs a second inner search
with gamma_r = 0 for the upper bound; here the upper bound is read off the
lower-bound search, which keeps the guarantee and costs much less. The
inner search returns a true lower bound (the least of its best value and
the bounds left in its queue). It stops when that bound is within eps / 2
of its best value, or within eps of E*, so the outer stop rule is always
reached and no work is spent past it. Closest points are found by brute force,
Theta(n m) per evaluation; the paper uses a distance transform.
"""

from __future__ import annotations

import heapq
import itertools
import math
from typing import Dict, List, Optional, Sequence, Tuple

from cvgeom import axis_angle_to_R
from cvla import det, mul, svd, transpose

Matrix = List[List[float]]
Vector = List[float]

SQRT3 = math.sqrt(3.0)
_SIGNS = [(a, b, c) for a in (-1.0, 1.0) for b in (-1.0, 1.0) for c in (-1.0, 1.0)]


def transform(R, t, pts) -> List[Vector]:
    """The points R p + t."""
    return [[sum(R[i][k] * p[k] for k in range(3)) + t[i] for i in range(3)] for p in pts]


def residuals(moved, t, Q) -> List[float]:
    """e_i = distance from moved[i] + t to its closest point of Q (brute force)."""
    out = []
    tx, ty, tz = t
    for x, y, z in moved:
        x, y, z = x + tx, y + ty, z + tz
        best = min((x - a) * (x - a) + (y - b) * (y - b) + (z - c) * (z - c) for a, b, c in Q)
        out.append(math.sqrt(best))
    return out


def cost(R, t, P, Q) -> float:
    """E(R, t) = sum of squared closest-point distances."""
    return sum(e * e for e in residuals(transform(R, [0.0, 0.0, 0.0], P), t, Q))


def rotation_uncertainty(norm_p: float, sigma_r: float) -> float:
    """gamma_r of Theorem 1: a bound on ||R_r p - R_r0 p|| for every r in the
    cube of half side sigma_r around r0."""
    return 2.0 * math.sin(min(SQRT3 * sigma_r / 2.0, math.pi / 2.0)) * norm_p


def _closest_index(pts, Q) -> List[int]:
    idx = []
    for x, y, z in pts:
        best, bj = float("inf"), -1
        for j, (a, b, c) in enumerate(Q):
            d = (x - a) * (x - a) + (y - b) * (y - b) + (z - c) * (z - c)
            if d < best:
                best, bj = d, j
        idx.append(bj)
    return idx


def _kabsch(P, Y) -> Tuple[Matrix, Vector]:
    n = len(P)
    pc = [sum(p[k] for p in P) / n for k in range(3)]
    yc = [sum(y[k] for y in Y) / n for k in range(3)]
    H = [[sum((p[i] - pc[i]) * (y[j] - yc[j]) for p, y in zip(P, Y)) for j in range(3)] for i in range(3)]
    U, _, V = svd(H)
    d = 1.0 if det(mul(V, transpose(U))) >= 0 else -1.0
    R = mul(mul(V, [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, d]]), transpose(U))
    return R, [yc[i] - sum(R[i][k] * pc[k] for k in range(3)) for i in range(3)]


def local_icp(P, Q, R, t, max_iter: int = 50) -> Tuple[Matrix, Vector, float]:
    """Point-to-point ICP from (R, t). Returns (R, t, E) with E the cost at
    the returned pose. The cost never goes up."""
    R, t = [list(r) for r in R], list(t)
    E = cost(R, t, P, Q)
    prev = None
    for _ in range(max_iter):
        idx = _closest_index(transform(R, t, P), Q)
        if idx == prev:
            break
        R2, t2 = _kabsch(P, [Q[j] for j in idx])
        E2 = cost(R2, t2, P, Q)
        if E2 >= E:
            break
        R, t, E, prev = R2, t2, E2, idx
    return R, t, E


def inner_bnb(moved, gammas, Q, t_center, t_half, E_bound, delta, enough=0.0):
    """Branch and bound over the translation cube for one rotation.

    moved holds R_r0 p_i, and gammas the rotation uncertainties gamma_ri
    (zeros to minimize the cost itself). The function to minimize is
    f(t) = sum_i max(e_i(R_r0, t) - gamma_ri, 0)^2. The search stops when
    the least bound in the queue is within delta of the best value found, or
    within enough of E_bound. Returns (E_t, t_best, L):
    E_t = min(E_bound, least f found), t_best its translation (None if no
    value below E_bound was found), and L <= min over the cube of f."""
    Et, tbest = E_bound, None  # @line L9
    e = residuals(moved, t_center, Q)
    up = sum(max(a - g, 0.0) ** 2 for a, g in zip(e, gammas))
    if up < Et:
        Et, tbest = up, list(t_center)
    gt = SQRT3 * t_half
    lb = sum(max(a - g - gt, 0.0) ** 2 for a, g in zip(e, gammas))
    count = itertools.count()
    heap = [(lb, next(count), list(t_center), t_half)] if lb < Et else []  # @line L9
    while heap:  # @line L10
        lb, _, c, s = heap[0]
        if Et - lb < delta or E_bound - lb < enough:  # @line L10
            break
        heapq.heappop(heap)
        h = s / 2.0  # @line L11
        gt = SQRT3 * h  # @line L11
        for sx, sy, sz in _SIGNS:  # @line L11
            c2 = [c[0] + sx * h, c[1] + sy * h, c[2] + sz * h]
            e = residuals(moved, c2, Q)
            up = sum(max(a - g, 0.0) ** 2 for a, g in zip(e, gammas))  # @line L12
            if up < Et:  # @line L12
                Et, tbest = up, c2
            low = sum(max(a - g - gt, 0.0) ** 2 for a, g in zip(e, gammas))  # @line L13
            if low < Et:  # @line L13
                heapq.heappush(heap, (low, next(count), c2, h))
    L = min(Et, heap[0][0]) if heap else Et  # @line L14
    return Et, tbest, L  # @line L14


def go_icp(P: Sequence[Sequence[float]], Q: Sequence[Sequence[float]], eps: float,
           t_center: Sequence[float] = (0.0, 0.0, 0.0), t_half: float = 1.0,
           r_center: Sequence[float] = (0.0, 0.0, 0.0), r_half: float = math.pi,
           R0: Optional[Sequence[Sequence[float]]] = None,
           t0: Optional[Sequence[float]] = None,
           stats: Optional[Dict[str, int]] = None) -> Tuple[Matrix, Vector, float]:
    """Globally optimal registration of P to Q by nested branch and bound.

    The rotation domain is the cube of angle-axis vectors with center
    r_center and half side r_half; the translation domain is the cube with
    center t_center and half side t_half. Sub-cubes that lie wholly outside
    the ball of radius pi are dropped, since that ball already holds every
    rotation. Returns (R, t, E) with E = cost(R, t, P, Q) and E <= m + eps,
    where m is the least cost over the domain poses whose angle-axis vector
    has norm at most pi.
    If stats is a dict, it receives the number of rotation cubes looked at
    and the number of local ICP runs."""
    if eps <= 0:
        raise ValueError("go_icp: eps must be positive")
    eye = [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]
    R, t, E = local_icp(P, Q, R0 if R0 is not None else eye,  # @line L1
                        t0 if t0 is not None else [0.0, 0.0, 0.0])
    norms = [math.sqrt(sum(v * v for v in p)) for p in P]
    count = itertools.count()
    heap = [(0.0, next(count), list(r_center), r_half)]  # @line L1
    cubes = icp_runs = 0
    while heap:  # @line L2
        lb, _, c, s = heap[0]
        if E - lb < eps:  # @line L2
            break
        heapq.heappop(heap)
        h = s / 2.0  # @line L3
        gammas = [rotation_uncertainty(n, h) for n in norms]  # @line L3
        for sx, sy, sz in _SIGNS:  # @line L4
            r0 = [c[0] + sx * h, c[1] + sy * h, c[2] + sz * h]
            if math.sqrt(sum(v * v for v in r0)) - SQRT3 * h > math.pi:  # @line L4
                continue
            cubes += 1
            Rr = axis_angle_to_R(r0)
            moved = transform(Rr, [0.0, 0.0, 0.0], P)
            _, tb, low = inner_bnb(moved, gammas, Q, t_center, t_half, E, eps / 2.0, eps)  # @line L5
            if tb is not None:
                Eu = sum(e * e for e in residuals(moved, tb, Q))  # @line L6
                if Eu < E:  # @line L6
                    R, t, E = Rr, tb, Eu
                    icp_runs += 1
                    R2, t2, E2 = local_icp(P, Q, Rr, tb)  # @line L6
                    if E2 < E:
                        R, t, E = R2, t2, E2
            if low < E:  # @line L7
                heapq.heappush(heap, (low, next(count), r0, h))  # @line L7
    if stats is not None:
        stats["rotation_cubes"] = cubes
        stats["icp_runs"] = icp_runs
    return R, t, E  # @line L8
