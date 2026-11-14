# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/quadratic-placement/. The authors are listed in prov/01NV03.jsonl.

"""Quadratic placement with the clique net model, solved by conjugate gradients.

Pins 0 .. n-1 are the movable cells, and pins n, n+1, ... are the fixed pads.
Every pin sits at the center of its cell or pad (no pin offsets).
With Fraction input and tol = 0, the conjugate gradient method runs in exact
arithmetic and stops with a zero residual after at most n steps.
"""

from fractions import Fraction
from typing import Optional, Sequence

Number = Fraction | float


def clique_edges(nets: Sequence[Sequence[int]], weights: Optional[Sequence[Number]] = None) -> dict:
    """Two-pin edges of the clique model: each pair of a p-pin net gets w_e / (p - 1)."""
    edges: dict = {}
    for k, e in enumerate(nets):
        pins = sorted(set(e))
        p = len(pins)
        if p < 2:
            continue
        w = (Fraction(1) if weights is None else Fraction(weights[k])) / (p - 1)
        for a in range(p):
            for b in range(a + 1, p):
                key = (pins[a], pins[b])
                edges[key] = edges.get(key, 0) + w  # @line L1
    return edges


def build_system(n: int, nets, pads, weights=None):
    """Return (A, bx, by): A is a list of sparse rows {j: a_ij}, the Laplacian of the
    cell-to-cell edges plus a diagonal for the cell-to-pad edges; b holds w times the pad coordinate."""
    A = [dict() for _ in range(n)]  # @line L2
    bx = [Fraction(0)] * n
    by = [Fraction(0)] * n
    adj = [set() for _ in range(n)]
    anchored = [False] * n
    for (a, b), w in clique_edges(nets, weights).items():
        if b < n:  # a < b, so both are cells
            A[a][a] = A[a].get(a, 0) + w
            A[b][b] = A[b].get(b, 0) + w
            A[a][b] = A[a].get(b, 0) - w
            A[b][a] = A[b].get(a, 0) - w
            adj[a].add(b)
            adj[b].add(a)
        elif a < n:  # a is a cell, b is a pad
            qx, qy = pads[b - n]
            A[a][a] = A[a].get(a, 0) + w
            bx[a] += w * Fraction(qx)
            by[a] += w * Fraction(qy)
            anchored[a] = True
        # an edge between two pads adds a constant and is left out
    seen = [False] * n
    for s in range(n):
        if seen[s]:
            continue
        comp, stack = [], [s]
        seen[s] = True
        while stack:
            u = stack.pop()
            comp.append(u)
            for v in adj[u]:
                if not seen[v]:
                    seen[v] = True
                    stack.append(v)
        if not any(anchored[u] for u in comp):
            raise ValueError("a group of cells has no path to a pad, so the system is singular")  # @line L3
    return A, bx, by


def matvec(A, v):
    return [sum(a * v[j] for j, a in row.items()) for row in A]


def dot(u, v):
    return sum(a * b for a, b in zip(u, v))


def conjugate_gradient(A, b, tol: float = 0, max_iter: Optional[int] = None):
    """Solve A x = b for a symmetric positive definite A, from x = 0.
    Stops when |r|^2 <= tol^2 |b|^2. Returns (x, steps, list of |r|^2 after each step)."""
    n = len(b)
    if max_iter is None:
        max_iter = n if tol == 0 else 10 * n + 10
    zero = b[0] * 0 if n else 0
    x = [zero] * n  # @line L5
    r = list(b)
    p = list(r)
    rr = dot(r, r)
    limit = tol * tol * rr
    history = [rr]
    k = 0
    while rr > limit and k < max_iter:  # @line L6
        Ap = matvec(A, p)
        alpha = rr / dot(p, Ap)  # @line L7
        x = [xi + alpha * pi for xi, pi in zip(x, p)]  # @line L8
        r = [ri - alpha * qi for ri, qi in zip(r, Ap)]
        rr_new = dot(r, r)
        beta = rr_new / rr  # @line L9
        p = [ri + beta * pi for ri, pi in zip(r, p)]
        rr = rr_new
        history.append(rr)
        k += 1
    return x, k, history


def quadratic_placement(n: int, nets, pads, weights=None, exact: bool = True, tol: float = 1e-12):
    """Positions (x_i, y_i) of the n cells that minimize the clique-model quadratic wirelength.
    exact=True keeps Fractions and solves exactly; exact=False uses floats with tolerance tol."""
    A, bx, by = build_system(n, nets, pads, weights)
    if not exact:
        A = [{j: float(a) for j, a in row.items()} for row in A]
        bx = [float(v) for v in bx]
        by = [float(v) for v in by]
        t = tol
    else:
        t = 0
    x, _, _ = conjugate_gradient(A, bx, t)  # @line L4
    y, _, _ = conjugate_gradient(A, by, t)  # @line L10
    return list(zip(x, y))  # @line L11


def quadratic_wirelength(pos, n: int, nets, pads, weights=None):
    """Sum over the clique edges of w_ij ((x_i - x_j)^2 + (y_i - y_j)^2)."""
    pts = list(pos) + [(Fraction(a), Fraction(b)) for a, b in pads]
    total = 0
    for (a, b), w in clique_edges(nets, weights).items():
        total += w * ((pts[a][0] - pts[b][0]) ** 2 + (pts[a][1] - pts[b][1]) ** 2)
    return total


def hpwl(pos, n: int, nets, pads):
    """Total half-perimeter wirelength with every pin at its cell or pad center."""
    pts = list(pos) + [(Fraction(a), Fraction(b)) for a, b in pads]
    total = 0
    for e in nets:
        xs = [pts[p][0] for p in e]
        ys = [pts[p][1] for p in e]
        total += max(xs) - min(xs) + max(ys) - min(ys)
    return total
