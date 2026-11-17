# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fast-global-registration/. The authors are listed in prov/MFA6WR.jsonl.
"""Fast global registration (Zhou, Park and Koltun, ECCV 2016).

Input: correspondences (p_k, q_k) in R^3, k = 1 .. m, from feature
matching. Most of them can be wrong. Output: a rigid motion T = (R, t) that
minimizes the scaled Geman-McClure cost

    E(T) = sum_k rho(|q_k - T p_k|),   rho(x) = mu x^2 / (mu + x^2).

FGR writes E with a line process: E(T, L) = sum_k l_k |q_k - T p_k|^2 +
sum_k mu (sqrt(l_k) - 1)^2. For a fixed T the best l_k is
(mu / (mu + r_k^2))^2, and minimizing over l_k gives back rho. For a fixed L
the cost is a weighted least squares cost in T, which FGR reduces by one
Gauss-Newton step on the six parameters xi = (omega, v) of a small motion
exp(xi) T. The value mu starts large, so the cost is close to least squares,
and falls every few iterations (graduated non-convexity).

The correspondences come from the features by mutual nearest neighbors
(the reciprocity test) and a tuple test on random triples.
"""

from __future__ import annotations

import math
import random
from typing import Dict, List, Optional, Sequence, Tuple

from cvgeom import axis_angle_to_R
from cvla import matvec, mul, solve

Vector = List[float]
Matrix = List[List[float]]


def _apply(R: Matrix, t: Vector, p: Sequence[float]) -> Vector:
    Rp = matvec(R, p)
    return [Rp[0] + t[0], Rp[1] + t[1], Rp[2] + t[2]]


def _dist2(a: Sequence[float], b: Sequence[float]) -> float:
    return sum((x - y) * (x - y) for x, y in zip(a, b))


def geman_mcclure(r2: float, mu: float) -> float:
    """rho(r) = mu r^2 / (mu + r^2), given r^2."""
    return mu * r2 / (mu + r2)


def line_process_weight(r2: float, mu: float) -> float:
    """The best l for a residual r: (mu / (mu + r^2))^2."""
    return (mu / (mu + r2)) ** 2


def fgr_cost(P, Q, R: Matrix, t: Vector, mu: float) -> float:
    """E(T) = sum_k rho(|q_k - T p_k|)."""
    return sum(geman_mcclure(_dist2(q, _apply(R, t, p)), mu) for p, q in zip(P, Q))


def _nearest(f: Sequence[float], F: Sequence[Sequence[float]]) -> int:
    best, bi = math.inf, -1
    for i, g in enumerate(F):
        d = _dist2(f, g)
        if d < best:
            best, bi = d, i
    return bi


def match_features(P, Q, FP, FQ, tau: float = 0.9, n_tuples: int = 1000,
                   rng: Optional[random.Random] = None) -> List[Tuple[int, int]]:
    """Correspondences from features, by the reciprocity test and the tuple
    test. FP[i] is the feature of P[i] and FQ[j] the feature of Q[j]. Brute
    force nearest neighbors in feature space, O(|P| |Q|) distances."""
    rng = rng or random.Random(0)
    fwd = [_nearest(f, FQ) for f in FP]
    bwd = [_nearest(g, FP) for g in FQ]
    mutual = [(i, j) for i, j in enumerate(fwd) if bwd[j] == i]
    if len(mutual) < 3:
        return mutual
    keep = set()
    for _ in range(n_tuples):
        trio = rng.sample(mutual, 3)
        ok = True
        for a in range(3):
            for b in range(a + 1, 3):
                dp = math.sqrt(_dist2(P[trio[a][0]], P[trio[b][0]]))
                dq = math.sqrt(_dist2(Q[trio[a][1]], Q[trio[b][1]]))
                if dp == 0.0 or dq == 0.0 or not (tau < dp / dq < 1.0 / tau):
                    ok = False
        if ok:
            keep.update(trio)
    return sorted(keep)


def gauss_newton_step(P, Q, R: Matrix, t: Vector, mu: float):
    """One step at the pose T = (R, t). Returns (xi, l, H, g): the weights
    l_k of the line process, the 6 x 6 matrix H = sum_k l_k J_k^T J_k, the
    vector g = sum_k l_k J_k^T r_k, and the step xi = -H^-1 g. Here
    r_k = T p_k - q_k, and J_k = [-[x_k]_x | I] with x_k = T p_k is the
    derivative of exp(xi) T p_k at xi = 0. g is half the gradient of E.
    Raises ValueError if H is singular."""
    Tp = [_apply(R, t, p) for p in P]
    lw = [line_process_weight(_dist2(q, x), mu) for x, q in zip(Tp, Q)]  # @line L3
    H = [[0.0] * 6 for _ in range(6)]
    g = [0.0] * 6
    for x, q, l in zip(Tp, Q, lw):  # @line L4
        r = [x[0] - q[0], x[1] - q[1], x[2] - q[2]]
        J = [[0.0, x[2], -x[1], 1.0, 0.0, 0.0],
             [-x[2], 0.0, x[0], 0.0, 1.0, 0.0],
             [x[1], -x[0], 0.0, 0.0, 0.0, 1.0]]
        for c in range(3):
            Jc = J[c]
            for a in range(6):
                if Jc[a] == 0.0:
                    continue
                g[a] += l * Jc[a] * r[c]
                for b in range(6):
                    H[a][b] += l * Jc[a] * Jc[b]
    xi = solve(H, [-v for v in g])  # @line L5
    return xi, lw, H, g


def compose(xi: Sequence[float], R: Matrix, t: Vector) -> Tuple[Matrix, Vector]:
    """The pose after the small motion xi = (omega, v): x -> dR (R x + t) + v,
    where dR is the rotation by the vector omega."""
    dR = axis_angle_to_R(xi[:3])
    return mul(dR, R), [a + b for a, b in zip(matvec(dR, t), xi[3:])]


def fgr(P: Sequence[Sequence[float]], Q: Sequence[Sequence[float]],
        mu0: Optional[float] = None, delta: float = 0.01, factor: float = 2.0,
        every: int = 4, max_iter: int = 64) -> Dict[str, object]:
    """Align p_k to q_k. mu starts at mu0 (default: D^2, with D the diameter
    of the box around both sets) and is divided by factor every `every`
    iterations, but not below delta^2. Returns R, t, the final mu, the
    weights l and the history of the cost E (at the mu of each step)."""
    m = len(P)
    if m == 0:
        raise ValueError("fgr: no correspondences")
    if mu0 is None:
        pts = list(P) + list(Q)
        D2 = sum((max(p[d] for p in pts) - min(p[d] for p in pts)) ** 2 for d in range(3))
        mu0 = max(D2, delta * delta)
    R: Matrix = [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]  # @line L1
    t: Vector = [0.0, 0.0, 0.0]
    mu = mu0
    history: List[float] = []
    lw: List[float] = [1.0] * m
    for it in range(max_iter):  # @line L2
        try:
            xi, lw, _, _ = gauss_newton_step(P, Q, R, t, mu)
        except ValueError:
            break
        R, t = compose(xi, R, t)  # @line L6
        history.append(fgr_cost(P, Q, R, t, mu))
        if (it + 1) % every == 0 and mu > delta * delta:  # @line L7
            mu = max(mu / factor, delta * delta)
    return {"R": R, "t": t, "mu": mu, "l": lw, "history": history}  # @line L8
