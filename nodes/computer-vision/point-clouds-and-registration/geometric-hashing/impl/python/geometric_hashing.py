# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/geometric-hashing/. The authors are listed in prov/56HCXG.jsonl.
"""Geometric hashing for 2D point sets under affine maps, after Lamdan and
Wolfson (ICCV 1988).

A basis is an ordered triple (o, a, b) of points that are not on one line.
Any point p has unique affine coordinates (alpha, beta) with
p = o + alpha (a - o) + beta (b - o). These coordinates do not change when
one affine map is applied to p and to the basis.

Preprocessing stores, for every model and every basis of its points, the
quantized coordinates of the other model points in a hash table. Recognition
picks a basis of scene points, computes the coordinates of the other scene
points, and lets each one vote for the (model, basis) entries in its bin.
A (model, basis) pair with many votes is a hypothesis; it is verified by
mapping the whole model into the scene.
"""

from __future__ import annotations

import math
import random
from typing import Dict, List, Optional, Sequence, Tuple

Point = Sequence[float]
Basis = Tuple[int, int, int]
Key = Tuple[int, int]
Entry = Tuple[str, Basis]


def affine_coords(o: Point, a: Point, b: Point, p: Point,
                  eps: float = 1e-9) -> Optional[Tuple[float, float]]:
    """(alpha, beta) with p = o + alpha (a - o) + beta (b - o), or None if
    the basis is (nearly) on one line. eps is relative to the basis size."""
    ux, uy = a[0] - o[0], a[1] - o[1]
    vx, vy = b[0] - o[0], b[1] - o[1]
    det = ux * vy - uy * vx
    if abs(det) <= eps * (ux * ux + uy * uy + vx * vx + vy * vy):
        return None
    wx, wy = p[0] - o[0], p[1] - o[1]
    return ((wx * vy - wy * vx) / det, (ux * wy - uy * wx) / det)


def quantize(c: Tuple[float, float], q: float) -> Key:
    return (math.floor(c[0] / q), math.floor(c[1] / q))


def build_table(models: Dict[str, Sequence[Point]], q: float) -> Dict[Key, List[Entry]]:
    """The hash table: bin -> list of (model name, basis)."""
    table: Dict[Key, List[Entry]] = {}
    for name, pts in models.items():
        m = len(pts)
        for i in range(m):  # @line L1
            for j in range(m):
                for k in range(m):
                    if len({i, j, k}) < 3:
                        continue
                    if affine_coords(pts[i], pts[j], pts[k], pts[i]) is None:
                        continue  # a basis on one line
                    for l in range(m):  # @line L2
                        if l in (i, j, k):
                            continue
                        c = affine_coords(pts[i], pts[j], pts[k], pts[l])
                        table.setdefault(quantize(c, q), []).append((name, (i, j, k)))  # @line L3
    return table


def vote(table: Dict[Key, List[Entry]], scene: Sequence[Point], basis: Basis,
         q: float) -> Dict[Entry, int]:
    """Votes for each (model, basis) from the other scene points. Each point
    looks in its bin and the 8 bins around it, to allow for noise, and gives
    at most one vote to each entry."""
    i, j, k = basis
    votes: Dict[Entry, int] = {}
    for l, p in enumerate(scene):
        if l in basis:
            continue
        c = affine_coords(scene[i], scene[j], scene[k], p)  # @line L5
        if c is None:
            return {}
        bx, by = quantize(c, q)
        seen = set()
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                for entry in table.get((bx + dx, by + dy), ()):
                    seen.add(entry)
        for entry in seen:  # @line L6
            votes[entry] = votes.get(entry, 0) + 1
    return votes


def fit_affine(src: Sequence[Point], dst: Sequence[Point]):
    """The affine map x -> A x + t that sends the three points src to dst."""
    (o, a, b), (o2, a2, b2) = src, dst
    ux, uy, vx, vy = a[0] - o[0], a[1] - o[1], b[0] - o[0], b[1] - o[1]
    det = ux * vy - uy * vx
    # Inverse of [[ux, vx], [uy, vy]].
    i00, i01, i10, i11 = vy / det, -vx / det, -uy / det, ux / det
    px, py, rx, ry = a2[0] - o2[0], a2[1] - o2[1], b2[0] - o2[0], b2[1] - o2[1]
    A = [[px * i00 + rx * i10, px * i01 + rx * i11],
         [py * i00 + ry * i10, py * i01 + ry * i11]]
    t = [o2[0] - A[0][0] * o[0] - A[0][1] * o[1], o2[1] - A[1][0] * o[0] - A[1][1] * o[1]]
    return A, t


def apply_affine(A, t, p: Point) -> List[float]:
    return [A[0][0] * p[0] + A[0][1] * p[1] + t[0], A[1][0] * p[0] + A[1][1] * p[1] + t[1]]


def verify(model: Sequence[Point], scene: Sequence[Point], A, t, tol: float) -> int:
    """The number of model points that land within tol of a scene point."""
    count = 0
    for p in model:
        x = apply_affine(A, t, p)
        if any(math.dist(x, s) <= tol for s in scene):
            count += 1
    return count


def recognize(models: Dict[str, Sequence[Point]], table: Dict[Key, List[Entry]],
              scene: Sequence[Point], q: float, min_votes: int, tol: float,
              rng: random.Random, max_trials: int = 500,
              min_fit: Optional[int] = None) -> Optional[Dict[str, object]]:
    """Pick random scene bases until a hypothesis with at least min_votes
    votes maps at least min_fit model points (default: all of them) within
    tol of scene points. Returns the model, the bases and the affine map,
    or None after max_trials bases."""
    n = len(scene)
    if n < 4:
        return None
    for trial in range(max_trials):  # @line L4
        basis = tuple(rng.sample(range(n), 3))
        votes = vote(table, scene, basis, q)
        if not votes:
            continue
        ranked = sorted(votes.items(), key=lambda kv: -kv[1])
        for (name, mb), v in ranked:
            if v < min_votes:  # @line L7
                break
            model = models[name]
            A, t = fit_affine([model[i] for i in mb], [scene[i] for i in basis])
            need = len(model) if min_fit is None else min_fit
            fit = verify(model, scene, A, t, tol)
            if fit >= need:
                return {"model": name, "model_basis": mb, "scene_basis": basis,
                        "A": A, "t": t, "votes": v, "fit": fit, "trials": trial + 1}  # @line L8
    return None
