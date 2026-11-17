# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/four-points-congruent-sets/. The authors are listed in prov/2MMXJS.jsonl.
"""4-points congruent sets (Aiger, Mitra and Cohen-Or, SIGGRAPH 2008).

Input: two point clouds P and Q in R^3 that overlap, an error bound delta
and a number of trials. Output: a rigid motion T = (R, t) with T P close to
Q on as many points as possible: the largest common pointset (LCP) score,
the number of points p of P with a point of Q within delta of T p.

Each trial picks a wide, nearly coplanar base (a, b, c, d) from P, whose
segments ab and cd meet at a point e. The two ratios
r1 = |a - e| / |a - b| and r2 = |c - e| / |c - d| do not change under an
affine map, so they also hold for the image of the base in Q. The trial
finds all pairs of Q at the distances |a - b| and |c - d|, computes the
points that the ratios give on each pair, and matches these points. Each
match is a 4-point set of Q that is congruent to the base up to delta. The
best rigid motion from the base to each set is then scored by the LCP.

The extraction uses brute force over pairs, O(n^2) per trial, and a grid
for the matching of points, as the reference stand-in for the range search
of the paper.
"""

from __future__ import annotations

import math
import random
from typing import Dict, List, Optional, Sequence, Tuple

from cvla import det, mul, svd, transpose

Vector = List[float]
Matrix = List[List[float]]


def _sub(a, b):
    return [a[0] - b[0], a[1] - b[1], a[2] - b[2]]


def _dot(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def _dist(a, b) -> float:
    return math.sqrt(_dot(_sub(a, b), _sub(a, b)))


def _cross(a, b):
    return [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]]


def apply(R: Matrix, t: Sequence[float], p: Sequence[float]) -> Vector:
    return [R[i][0] * p[0] + R[i][1] * p[1] + R[i][2] * p[2] + t[i] for i in range(3)]


def kabsch(A: Sequence[Sequence[float]], B: Sequence[Sequence[float]]) -> Tuple[Matrix, Vector]:
    """The rigid motion (R, t) that minimizes sum |R a + t - b|^2, by the SVD
    of the cross-covariance with the sign fix, so that det R = +1."""
    n = len(A)
    ca = [sum(a[i] for a in A) / n for i in range(3)]
    cb = [sum(b[i] for b in B) / n for i in range(3)]
    H = [[sum((a[i] - ca[i]) * (b[j] - cb[j]) for a, b in zip(A, B)) for j in range(3)] for i in range(3)]
    U, _, V = svd(H)
    d = 1.0 if det(mul(V, transpose(U))) > 0.0 else -1.0
    R = mul(mul(V, [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, d]]), transpose(U))
    Rc = [sum(R[i][k] * ca[k] for k in range(3)) for i in range(3)]
    return R, [cb[i] - Rc[i] for i in range(3)]


def base_invariants(a, b, c, d) -> Optional[Tuple[float, float, float, float, float]]:
    """For the segments ab and cd, the parameters r1, r2 of the closest
    points e1 = a + r1 (b - a) and e2 = c + r2 (d - c) of the two lines, the
    lengths d1 = |a - b| and d2 = |c - d|, and the gap |e1 - e2|. Returns
    None if the lines are parallel or the closest points are not inside
    both segments."""
    u, v, w = _sub(b, a), _sub(d, c), _sub(a, c)
    A, B, C = _dot(u, u), _dot(u, v), _dot(v, v)
    D, E = _dot(u, w), _dot(v, w)
    den = A * C - B * B
    if den <= 1e-12 * A * C:
        return None
    r1 = (B * E - C * D) / den
    r2 = (A * E - B * D) / den
    if not (0.0 < r1 < 1.0 and 0.0 < r2 < 1.0):
        return None
    e1 = [a[i] + r1 * u[i] for i in range(3)]
    e2 = [c[i] + r2 * v[i] for i in range(3)]
    return r1, r2, math.sqrt(A), math.sqrt(C), _dist(e1, e2)


def select_base(P: Sequence[Sequence[float]], rng: random.Random, delta: float,
                tries: int = 30, max_width: float = math.inf
                ) -> Optional[Tuple[Tuple[int, int, int, int], Tuple[float, float, float, float]]]:
    """A wide base: the widest of `tries` random triangles (a, b, c) with
    sides at most max_width, then the point d nearest to their plane, within
    max_width of a, for which one of the three pairings of the four points
    into two segments gives segments that meet within delta. Returns
    ((ia, ib, ic, id), (r1, r2, d1, d2)) or None."""
    n = len(P)
    best, best_area = None, 0.0
    for _ in range(tries):
        i, j, k = rng.sample(range(n), 3)
        if max(_dist(P[i], P[j]), _dist(P[i], P[k]), _dist(P[j], P[k])) > max_width:
            continue
        nrm = _cross(_sub(P[j], P[i]), _sub(P[k], P[i]))
        area = math.sqrt(_dot(nrm, nrm))
        if area > best_area:
            best, best_area = (i, j, k), area
    if best is None or best_area == 0.0:
        return None
    i, j, k = best
    normal = _cross(_sub(P[j], P[i]), _sub(P[k], P[i]))
    nn = math.sqrt(_dot(normal, normal))
    order = sorted((abs(_dot(_sub(P[l], P[i]), normal)) / nn, l) for l in range(n)
                   if l not in best and _dist(P[l], P[i]) <= max_width)
    for h, l in order:
        if h > delta:
            break
        for ia, ib, ic, id_ in ((i, j, k, l), (i, k, j, l), (i, l, j, k)):
            inv = base_invariants(P[ia], P[ib], P[ic], P[id_])
            if inv is not None and inv[4] <= delta:
                return (ia, ib, ic, id_), inv[:4]
    return None


class Grid:
    """Points hashed into cubes of side `cell`, for radius queries with a
    radius of at most `cell`."""

    def __init__(self, points: Sequence[Sequence[float]], cell: float):
        self.cell = cell
        self.points = points
        self.cells: Dict[Tuple[int, int, int], List[int]] = {}
        for idx, p in enumerate(points):
            self.cells.setdefault(self._key(p), []).append(idx)

    def _key(self, p):
        return (math.floor(p[0] / self.cell), math.floor(p[1] / self.cell), math.floor(p[2] / self.cell))

    def near(self, x: Sequence[float], radius: float) -> List[int]:
        kx, ky, kz = self._key(x)
        r2 = radius * radius
        out = []
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                for dz in (-1, 0, 1):
                    for idx in self.cells.get((kx + dx, ky + dy, kz + dz), ()):
                        p = self.points[idx]
                        if (p[0] - x[0]) ** 2 + (p[1] - x[1]) ** 2 + (p[2] - x[2]) ** 2 <= r2:
                            out.append(idx)
        return out


def pairs_at_distance(Q: Sequence[Sequence[float]], dist: float, eps: float) -> List[Tuple[int, int]]:
    """All ordered pairs (i, j), i != j, with | |q_i - q_j| - dist | <= eps."""
    out = []
    for i in range(len(Q)):
        for j in range(i + 1, len(Q)):
            if abs(_dist(Q[i], Q[j]) - dist) <= eps:
                out.append((i, j))
                out.append((j, i))
    return out


def congruent_sets(Q: Sequence[Sequence[float]], r1: float, r2: float, d1: float, d2: float,
                   eps: float) -> List[Tuple[int, int, int, int]]:
    """All (i, j, k, l) with |q_i q_j| = d1 and |q_k q_l| = d2 up to eps and
    |(q_i + r1 (q_j - q_i)) - (q_k + r2 (q_l - q_k))| <= eps."""
    R1 = pairs_at_distance(Q, d1, eps)  # @line L4
    R2 = pairs_at_distance(Q, d2, eps)
    E1 = [[Q[i][c] + r1 * (Q[j][c] - Q[i][c]) for c in range(3)] for i, j in R1]
    grid = Grid(E1, max(eps, 1e-12))
    out = []
    for k, l in R2:  # @line L5
        e2 = [Q[k][c] + r2 * (Q[l][c] - Q[k][c]) for c in range(3)]
        for s in grid.near(e2, eps):
            i, j = R1[s]
            if len({i, j, k, l}) == 4:
                out.append((i, j, k, l))
    return out


def lcp_score(P: Sequence[Sequence[float]], grid_q: Grid, R: Matrix, t: Sequence[float], delta: float) -> int:
    """The number of points p with a point of Q within delta of R p + t."""
    return sum(1 for p in P if grid_q.near(apply(R, t, p), delta))


def four_pcs(P: Sequence[Sequence[float]], Q: Sequence[Sequence[float]], delta: float,
             n_trials: int = 20, rng: Optional[random.Random] = None,
             sample: Optional[int] = None, tries: int = 30,
             max_width: float = math.inf) -> Dict[str, object]:
    """Align P to Q. `sample` limits the points of P used for the LCP score;
    `tries` and `max_width` control the base, see select_base. Returns R,
    t, the LCP score, and the number of candidate sets tried."""
    rng = rng or random.Random(0)
    grid_q = Grid(Q, delta)
    Ps = list(P) if sample is None or sample >= len(P) else rng.sample(list(P), sample)
    best = {"R": [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]], "t": [0.0, 0.0, 0.0],
            "score": -1, "candidates": 0}
    for _ in range(n_trials):  # @line L1
        found = select_base(P, rng, delta, tries, max_width)  # @line L2
        if found is None:
            continue
        base, (r1, r2, d1, d2) = found  # @line L3
        for i, j, k, l in congruent_sets(Q, r1, r2, d1, d2, delta):
            best["candidates"] += 1
            R, t = kabsch([P[x] for x in base], [Q[i], Q[j], Q[k], Q[l]])  # @line L6
            if max(_dist(apply(R, t, P[x]), Q[y]) for x, y in zip(base, (i, j, k, l))) > 2.0 * delta:
                continue
            score = lcp_score(Ps, grid_q, R, t, delta)  # @line L7
            if score > best["score"]:
                best.update(R=R, t=t, score=score)
    return best  # @line L8
