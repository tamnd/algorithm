# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/distributed-averaging/. The authors are listed in prov/XNYGXK.jsonl.

"""Distributed averaging by a synchronous linear iteration x(t+1) = W x(t).

Graphs are adjacency lists: adj[i] is the list of neighbours of node i, with
no self loops. The weight matrix is a dense list of rows, which is fine for
the small graphs of the tests. Nothing here uses numpy: the second largest
eigenvalue modulus (SLEM) comes from power iteration on W - 11^T/n.
"""

import math
import random


def metropolis_weights(adj: list[list[int]]) -> list[list[float]]:
    """Metropolis weights: W_ij = 1 / (1 + max(d_i, d_j)) on each edge, the
    rest of the row on the diagonal. W is symmetric and doubly stochastic."""
    n = len(adj)
    w = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in adj[i]:
            w[i][j] = 1.0 / (1 + max(len(adj[i]), len(adj[j])))
        w[i][i] = 1.0 - sum(w[i])
    return w


def step(w: list[list[float]], x: list[float]) -> list[float]:
    """One synchronous round: node i sets x_i to sum_j W_ij x_j. Only the
    entries with W_ij != 0 are used, so node i reads only its neighbours."""
    return [sum(wij * xj for wij, xj in zip(row, x) if wij != 0.0) for row in w]


def run(w: list[list[float]], x0: list[float], rounds: int) -> list[list[float]]:
    xs = [list(x0)]
    for _ in range(rounds):
        xs.append(step(w, xs[-1]))
    return xs


def deviation(x: list[float]) -> float:
    """The Euclidean distance from x to the vector (average, ..., average)."""
    a = sum(x) / len(x)
    return math.sqrt(sum((v - a) ** 2 for v in x))


def slem(w: list[list[float]], iters: int = 3000, seed: int = 1) -> float:
    """The spectral radius of W - 11^T/n for a symmetric W, by power
    iteration. For a symmetric matrix A, ||A x|| / ||x|| tends to the largest
    |eigenvalue| when x has a component along that eigenvector, which a
    random start has with probability 1. Removing the mean of x at each step
    applies the projection I - 11^T/n."""
    n = len(w)
    rng = random.Random(seed)
    x = [rng.gauss(0.0, 1.0) for _ in range(n)]
    est = 0.0
    for _ in range(iters):
        a = sum(x) / n
        x = [v - a for v in x]
        norm = math.sqrt(sum(v * v for v in x))
        x = [v / norm for v in x]
        y = step(w, x)
        a = sum(y) / n
        y = [v - a for v in y]
        est = math.sqrt(sum(v * v for v in y))
        x = y
    return est


def converges(w: list[list[float]], tol: float = 1e-9) -> bool:
    """The Xiao-Boyd condition for a symmetric W: rows sum to 1 (so columns
    do too) and the spectral radius of W - 11^T/n is below 1."""
    rows_ok = all(abs(sum(row) - 1.0) < tol for row in w)
    return rows_ok and slem(w) < 1.0 - 1e-6


def cycle(n: int) -> list[list[int]]:
    return [[(i - 1) % n, (i + 1) % n] for i in range(n)]


def grid(r: int, c: int) -> list[list[int]]:
    """An r by c grid without wrap around, nodes numbered row by row."""
    adj: list[list[int]] = [[] for _ in range(r * c)]
    for a in range(r):
        for b in range(c):
            i = a * c + b
            if a + 1 < r:
                adj[i].append(i + c)
                adj[i + c].append(i)
            if b + 1 < c:
                adj[i].append(i + 1)
                adj[i + 1].append(i)
    return adj


def random_connected_graph(n: int, p: float, seed: int) -> list[list[int]]:
    """G(n, p) plus a random spanning path, so the graph is connected."""
    rng = random.Random(seed)
    edges = set()
    order = list(range(n))
    rng.shuffle(order)
    for a, b in zip(order, order[1:]):
        edges.add((min(a, b), max(a, b)))
    for i in range(n):
        for j in range(i + 1, n):
            if rng.random() < p:
                edges.add((i, j))
    adj: list[list[int]] = [[] for _ in range(n)]
    for i, j in sorted(edges):
        adj[i].append(j)
        adj[j].append(i)
    return adj
