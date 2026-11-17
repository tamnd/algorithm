# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/teaser-registration/. The authors are listed in prov/E0TQ57.jsonl.
"""TEASER registration (Yang, Shi and Carlone, IEEE T-RO 2021), in the
TEASER++ form.

Input: m putative correspondences (a_i, b_i) in R^3 with the model
b_i = s R a_i + t + o_i + eps_i, where |eps_i| <= beta for the inliers and
o_i is an arbitrary error for the outliers. The cost is truncated least
squares (TLS): sum_i min(r_i^2 / beta^2, cbar^2).

The steps:
1. Translation invariant measurements (TIMs): abar_ij = a_j - a_i and
   bbar_ij = b_j - b_i, with the noise bound delta_ij = 2 beta.
2. Translation and rotation invariant measurements (TRIMs): the ratios
   s_ij = |bbar_ij| / |abar_ij| with the bounds alpha_ij = delta_ij / |abar_ij|.
3. The scale by adaptive voting: the exact minimizer of the scalar TLS cost.
4. Pruning: keep the edges (i, j) with |s_ij - s| <= cbar alpha_ij, and
   keep only the vertices of a maximum clique of this graph.
5. The rotation from the TIMs of the clique, by graduated non-convexity
   (GNC) on the TLS cost with weighted Wahba steps. TEASER solves this step
   with a semidefinite relaxation and a certificate of optimality; this file
   does not, so it gives no certificate.
6. The translation component by component, by adaptive voting.

The scalar TLS solver and the maximum clique solver are exact. GNC is a
heuristic without a guarantee of global optimality.
"""

from __future__ import annotations

import math
from typing import Dict, List, Optional, Sequence, Set, Tuple

from cvla import det, mul, svd, transpose

Vector = List[float]
Matrix = List[List[float]]


def _sub(a, b):
    return [a[0] - b[0], a[1] - b[1], a[2] - b[2]]


def _norm(a) -> float:
    return math.sqrt(a[0] * a[0] + a[1] * a[1] + a[2] * a[2])


def _rot(R, a):
    return [R[0][0] * a[0] + R[0][1] * a[1] + R[0][2] * a[2],
            R[1][0] * a[0] + R[1][1] * a[1] + R[1][2] * a[2],
            R[2][0] * a[0] + R[2][1] * a[1] + R[2][2] * a[2]]


# ------------------------------------------------------------ scalar TLS

def tls_cost(x: float, values: Sequence[float], bounds: Sequence[float], cbar: float = 1.0) -> float:
    """sum_k min((x - v_k)^2 / b_k^2, cbar^2)."""
    c2 = cbar * cbar
    return sum(min((x - v) ** 2 / (b * b), c2) for v, b in zip(values, bounds))


def adaptive_voting(values: Sequence[float], bounds: Sequence[float],
                    cbar: float = 1.0) -> Tuple[float, List[int]]:
    """The exact minimizer of the scalar TLS cost and its consensus set.

    Each measurement v_k is an inlier of x when |x - v_k| <= cbar b_k. The
    2K interval ends cut the line into at most 2K - 1 bounded pieces; on
    each piece the consensus set is fixed, and the best x for it is the
    weighted mean sum(v / b^2) / sum(1 / b^2). Sweeping the sorted ends with
    running sums takes O(K log K) time. Ties go to the leftmost piece."""
    K = len(values)
    if K == 0:
        raise ValueError("adaptive_voting: no values")
    c2 = cbar * cbar
    events = []
    for k, (v, b) in enumerate(zip(values, bounds)):
        if b <= 0.0:
            raise ValueError("adaptive_voting: bounds must be positive")
        events.append((v - cbar * b, 0, k))  # 0: the interval opens
        events.append((v + cbar * b, 1, k))  # 1: the interval closes
    events.sort()
    sw = swv = swv2 = 0.0
    count = 0
    best_x, best_cost = values[0], math.inf
    for e in range(len(events)):
        pos, kind, k = events[e]
        wk = 1.0 / (bounds[k] * bounds[k])
        sign = 1.0 if kind == 0 else -1.0
        count += 1 if kind == 0 else -1
        sw += sign * wk
        swv += sign * wk * values[k]
        swv2 += sign * wk * values[k] * values[k]
        if count == 0:
            sw = swv = swv2 = 0.0  # clear the rounding drift of the running sums
        if count == 0 or e + 1 == len(events) or events[e + 1][0] == pos:
            continue
        # The open piece (pos, next end) has a fixed consensus set S. The
        # cost of S at its weighted mean is sum_S w (x - v)^2 + (K - |S|) c2.
        x = swv / sw
        cost = max(swv2 - swv * x, 0.0) + (K - count) * c2
        if cost < best_cost:
            best_x, best_cost = x, cost
    best_set = [k for k in range(K) if (best_x - values[k]) ** 2 <= c2 * bounds[k] ** 2]
    return best_x, best_set


# ---------------------------------------------------------- maximum clique

def max_clique(n: int, adj: Sequence[Set[int]]) -> List[int]:
    """A maximum clique of the graph on vertices 0 .. n-1 with the given
    adjacency sets. Bron-Kerbosch with a pivot, cut off when the current
    clique plus all candidates cannot beat the best clique. Exact; the
    worst case is exponential, as the problem is NP-hard."""
    best: List[int] = []

    def expand(r: List[int], p: Set[int], x: Set[int]) -> None:
        nonlocal best
        if not p and not x:
            if len(r) > len(best):
                best = list(r)
            return
        if len(r) + len(p) <= len(best):
            return
        pivot = max(p | x, key=lambda u: len(adj[u] & p))
        for v in sorted(p - adj[pivot]):
            expand(r + [v], p & adj[v], x & adj[v])
            p = p - {v}
            x = x | {v}
            if len(r) + len(p) <= len(best):
                return

    expand([], set(range(n)), set())
    return sorted(best)


# -------------------------------------------------------- rotation by GNC

def weighted_wahba(U: Sequence[Sequence[float]], V: Sequence[Sequence[float]],
                   w: Sequence[float]) -> Matrix:
    """The rotation R that minimizes sum_k w_k |v_k - R u_k|^2 (no
    translation): H = sum w u v^T = U S V^T and R = V diag(1, 1, d) U^T."""
    H = [[sum(wk * u[i] * v[j] for wk, u, v in zip(w, U, V)) for j in range(3)] for i in range(3)]
    Uh, _, Vh = svd(H)
    d = 1.0 if det(mul(Vh, transpose(Uh))) > 0.0 else -1.0
    return mul(mul(Vh, [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, d]]), transpose(Uh))


def gnc_tls_rotation(U: Sequence[Sequence[float]], V: Sequence[Sequence[float]],
                     bounds: Sequence[float], cbar: float = 1.0, factor: float = 1.4,
                     max_iter: int = 100, tol: float = 1e-12) -> Tuple[Matrix, List[float]]:
    """Graduated non-convexity for min_R sum min(|v_k - R u_k|^2 / b_k^2, cbar^2),
    after Yang, Antonante, Tzoumas and Carlone (2020). Returns R and the final
    weights (near 0 or 1)."""
    m = len(U)
    c2 = cbar * cbar
    w = [1.0] * m
    R = weighted_wahba(U, V, w)

    def residuals(R):
        return [sum(x * x for x in _sub(v, _rot(R, u))) / (b * b) for u, v, b in zip(U, V, bounds)]

    r2 = residuals(R)
    rmax = max(r2)
    if rmax <= c2:
        return R, w
    mu = c2 / (2.0 * rmax - c2)
    prev = math.inf
    for _ in range(max_iter):
        lo, hi = mu / (mu + 1.0) * c2, (mu + 1.0) / mu * c2
        w = [1.0 if r <= lo else 0.0 if r >= hi else cbar / math.sqrt(r) * math.sqrt(mu * (mu + 1.0)) - mu
             for r in r2]
        R = weighted_wahba(U, V, w)
        r2 = residuals(R)
        cost = sum(wk * r for wk, r in zip(w, r2))
        if abs(prev - cost) <= tol and all(wk in (0.0, 1.0) for wk in w):
            break
        prev = cost
        mu *= factor
    return R, w


# --------------------------------------------------------------- pipeline

def teaser(A: Sequence[Sequence[float]], B: Sequence[Sequence[float]], beta: float,
           cbar: float = 1.0, scale: Optional[float] = None) -> Dict[str, object]:
    """Estimate (s, R, t) from the correspondences (A[i], B[i]).

    beta is the noise bound of the inliers. If scale is given, the scale is
    known and the pruning uses it. Returns a dict with "s", "R", "t",
    "clique" (the indices kept by the maximum clique) and "inliers" (the
    indices whose final residual is at most cbar beta)."""
    m = len(A)
    pairs = []
    for i in range(m):  # @line L1
        for j in range(i + 1, m):
            ab, bb = _sub(A[j], A[i]), _sub(B[j], B[i])
            na = _norm(ab)
            if na > 0.0:
                pairs.append((i, j, ab, bb, _norm(bb) / na, 2.0 * beta / na))  # @line L2
    if scale is None:
        s_hat, _ = adaptive_voting([p[4] for p in pairs], [p[5] for p in pairs], cbar)  # @line L3
    else:
        s_hat = float(scale)
    adj: List[Set[int]] = [set() for _ in range(m)]
    for i, j, _, _, sij, aij in pairs:  # @line L4
        if abs(sij - s_hat) <= cbar * aij:
            adj[i].add(j)
            adj[j].add(i)
    clique = max_clique(m, adj)  # @line L5
    cs = set(clique)
    U = [[s_hat * x for x in p[2]] for p in pairs if p[0] in cs and p[1] in cs]
    V = [p[3] for p in pairs if p[0] in cs and p[1] in cs]
    if U:
        R, _ = gnc_tls_rotation(U, V, [2.0 * beta] * len(U), cbar)  # @line L6
    else:
        R = [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]
    t = []
    for d in range(3):  # @line L7
        vals = [B[i][d] - s_hat * _rot(R, A[i])[d] for i in clique]
        t.append(adaptive_voting(vals, [beta] * len(vals), cbar)[0])
    inliers = [i for i in range(m)
               if _norm(_sub(B[i], [s_hat * x + y for x, y in zip(_rot(R, A[i]), t)])) <= cbar * beta]
    return {"s": s_hat, "R": R, "t": t, "clique": clique, "inliers": inliers}  # @line L8
