# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/spectral-partitioning/. The authors are listed in prov/VACAVK.jsonl.

import math
import random
from typing import Sequence

Edge = tuple[int, int, float]


def laplacian(n: int, edges: Sequence[Edge]) -> list[list[float]]:
    """Dense Laplacian L = D - A of a weighted undirected graph on 0 .. n-1."""
    lap = [[0.0] * n for _ in range(n)]
    for u, v, w in edges:
        if u == v:
            continue
        lap[u][u] += w
        lap[v][v] += w
        lap[u][v] -= w
        lap[v][u] -= w
    return lap


def cut_weight(edges: Sequence[Edge], side: Sequence[int]) -> float:
    """Total weight of the edges whose ends are on different sides."""
    return sum(w for u, v, w in edges if side[u] != side[v])


def _times_laplacian(adj: list[list[tuple[int, float]]], deg: list[float], x: list[float]) -> list[float]:
    return [deg[u] * x[u] - sum(w * x[v] for v, w in adj[u]) for u in range(len(x))]


def fiedler_vector(
    n: int,
    edges: Sequence[Edge],
    rng: random.Random,
    tol: float = 1e-10,
    max_iter: int = 200000,
) -> tuple[float, list[float], float]:
    """Approximate the second smallest Laplacian eigenvalue and an eigenvector.

    Power iteration on M = c I - L with c = 2 times the largest weighted
    degree, so that the eigenvalues of M are c - lambda_i >= 0. Each step
    removes the component along the all-ones vector, which is the eigenvector
    of lambda_1 = 0. The loop stops when the residual ||L x - rho x|| of the
    unit vector x is at most tol, or after max_iter steps.

    Returns (rho, x, residual), where rho = x^T L x is the Rayleigh quotient.
    Cost: O(n + m) per step for m edges, and O(n + m) space.
    """
    if n < 2:
        raise ValueError("need at least two vertices")
    adj: list[list[tuple[int, float]]] = [[] for _ in range(n)]
    deg = [0.0] * n
    for u, v, w in edges:
        if u != v:
            adj[u].append((v, w))
            adj[v].append((u, w))
            deg[u] += w
            deg[v] += w
    c = 2.0 * max(deg) if max(deg) > 0 else 1.0

    def normalize(y: list[float]) -> list[float]:
        mean = sum(y) / n
        y = [t - mean for t in y]
        norm = math.sqrt(sum(t * t for t in y))
        return [t / norm for t in y]

    x = normalize([rng.uniform(-1.0, 1.0) for _ in range(n)])  # @line L2
    rho, res = 0.0, math.inf
    for _ in range(max_iter):  # @line L3
        lx = _times_laplacian(adj, deg, x)
        rho = sum(a * b for a, b in zip(x, lx))  # @line L4
        res = math.sqrt(sum((a - rho * b) ** 2 for a, b in zip(lx, x)))
        if res <= tol:  # @line L5
            break
        x = normalize([c * a - b for a, b in zip(x, lx)])  # @line L6
    return rho, x, res


def spectral_partitioning(
    n: int,
    edges: Sequence[Edge],
    rng: random.Random,
    mode: str = "bisection",
    tol: float = 1e-10,
) -> list[int]:
    """Split a graph by the order of the entries of its Fiedler vector.

    mode "bisection": the floor(n/2) vertices with the smallest entries go to
    side 0 (a split at the median). mode "ratio": try the n - 1 splits of the
    sorted order and keep the one with the least ratio cut cut/(|A| |B|), as
    in the EIG1 method of Hagen and Kahng. Ties in the entries are broken by
    the vertex number.

    Returns side[v] in {0, 1}. The eigenvector costs O(n + m) per power step;
    the sort costs O(n log n) and the sweep O(n + m).
    """
    lap_edges = [(u, v, w) for u, v, w in edges if u != v]  # @line L1
    _, x, _ = fiedler_vector(n, lap_edges, rng, tol)
    order = sorted(range(n), key=lambda v: (x[v], v))  # @line L7
    side = [1] * n
    if mode == "bisection":
        for v in order[: n // 2]:  # @line L8
            side[v] = 0
        return side
    if mode != "ratio":
        raise ValueError("mode must be 'bisection' or 'ratio'")
    adj: list[list[tuple[int, float]]] = [[] for _ in range(n)]
    for u, v, w in lap_edges:
        adj[u].append((v, w))
        adj[v].append((u, w))
    best_k, best_ratio, cut = 1, math.inf, 0.0
    for k in range(1, n):  # @line L9
        v = order[k - 1]
        side[v] = 0
        for u, w in adj[v]:
            cut += w if side[u] == 1 else -w
        ratio = cut / (k * (n - k))
        if ratio < best_ratio - 1e-12:
            best_k, best_ratio = k, ratio
    side = [1] * n
    for v in order[:best_k]:  # @line L10
        side[v] = 0
    return side
