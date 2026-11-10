# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/expander-walk-sampler/. The authors are listed in prov/RB6W2D.jsonl.

"""Random walks on a regular graph as a randomness-efficient sampler.

A graph is a list `nbrs` of N neighbour lists, each of the same length d.
Entry nbrs[v][j] is the j-th neighbour of v. The graph must be undirected as
a multigraph: for each pair u, v, the number of j with nbrs[u][j] == v is the
number of j with nbrs[v][j] == u. Then the walk matrix M = A / d is symmetric.
"""

import math
import random
from collections.abc import Callable
from fractions import Fraction


def check_regular_undirected(nbrs: list[list[int]]) -> int:
    """Return the degree d, or raise ValueError if the graph is not d-regular and undirected."""
    n = len(nbrs)
    if n == 0:
        raise ValueError("the graph is empty")
    d = len(nbrs[0])
    count: dict[tuple[int, int], int] = {}
    for u, row in enumerate(nbrs):
        if len(row) != d:
            raise ValueError("the graph is not regular")
        for v in row:
            if not 0 <= v < n:
                raise ValueError("a neighbour is out of range")
            count[(u, v)] = count.get((u, v), 0) + 1
    for (u, v), c in count.items():
        if count.get((v, u), 0) != c:
            raise ValueError("the graph is not undirected")
    return d


def walk_from_choices(nbrs: list[list[int]], start: int, choices: list[int]) -> list[int]:
    """The walk that starts at `start` and takes edge choices[i] at step i."""
    path = [start]
    v = start
    for j in choices:
        v = nbrs[v][j]
        path.append(v)
    return path


def expander_walk_sample(nbrs: list[list[int]], t: int, rng: random.Random) -> list[int]:
    """Return t vertices: a uniform start vertex and t - 1 uniform walk steps."""
    if t < 1:
        raise ValueError("t must be at least 1")
    d = len(nbrs[0])
    start = rng.randrange(len(nbrs))
    return walk_from_choices(nbrs, start, [rng.randrange(d) for _ in range(t - 1)])


def random_bits_used(num_vertices: int, d: int, t: int) -> float:
    """log2 N + (t - 1) log2 d, the entropy of the walk; an integer when N and d are powers of 2."""
    return math.log2(num_vertices) + (t - 1) * math.log2(d)


def amplify_one_sided(test: Callable[[int], bool], nbrs: list[list[int]], t: int, rng: random.Random) -> bool:
    """Accept if the test accepts some vertex of one walk of t vertices.

    For an RP test whose accepting set has density at least 1 - mu, the
    probability of a wrong reject is at most mu * (mu + lam * (1 - mu))^(t - 1).
    The random choices are drawn in the same order as in expander_walk_sample.
    """
    if t < 1:
        raise ValueError("t must be at least 1")
    d = len(nbrs[0])
    v = rng.randrange(len(nbrs))  # @line L1
    path = [v]
    for _ in range(t - 1):  # @line L2
        j = rng.randrange(d)  # @line L3
        v = nbrs[v][j]  # @line L4
        path.append(v)
    for u in path:  # @line L5
        if test(u):  # @line L6
            return True
    return False  # @line L7


def stay_probability(nbrs: list[list[int]], bad: set[int], t: int) -> Fraction:
    """Exact probability that all t vertices of the walk lie in `bad`."""
    n, d = len(nbrs), len(nbrs[0])
    p = {v: Fraction(1, n) for v in bad}
    for _ in range(t - 1):
        q: dict[int, Fraction] = {}
        for v, pv in p.items():
            share = pv / d
            for w in nbrs[v]:
                if w in bad:
                    q[w] = q.get(w, Fraction(0)) + share
        p = q
    return sum(p.values(), Fraction(0))


def spectral_expansion(nbrs: list[list[int]], sweeps: int = 100) -> float:
    """lambda = max(|lambda_2|, |lambda_N|) of M = A / d, by the cyclic Jacobi method.

    Meant for small graphs (N up to about 100).
    """
    d = check_regular_undirected(nbrs)
    n = len(nbrs)
    a = [[0.0] * n for _ in range(n)]
    for u, row in enumerate(nbrs):
        for v in row:
            a[u][v] += 1.0 / d
    for _ in range(sweeps):
        off = sum(a[i][j] ** 2 for i in range(n) for j in range(n) if i != j)
        if off < 1e-24:
            break
        for p in range(n - 1):
            for q in range(p + 1, n):
                if abs(a[p][q]) < 1e-300:
                    continue
                theta = (a[q][q] - a[p][p]) / (2 * a[p][q])
                tan = math.copysign(1.0, theta) / (abs(theta) + math.sqrt(theta * theta + 1))
                c = 1 / math.sqrt(tan * tan + 1)
                s = tan * c
                for k in range(n):
                    akp, akq = a[k][p], a[k][q]
                    a[k][p], a[k][q] = c * akp - s * akq, s * akp + c * akq
                for k in range(n):
                    apk, aqk = a[p][k], a[q][k]
                    a[p][k], a[q][k] = c * apk - s * aqk, s * apk + c * aqk
    eig = sorted((a[i][i] for i in range(n)), reverse=True)
    return max(abs(x) for x in eig[1:]) if n > 1 else 0.0


def margulis_gabber_galil(m: int) -> list[list[int]]:
    """An 8-regular multigraph on Z_m x Z_m built from affine maps of the
    Margulis-Gabber-Galil kind; vertex (x, y) has index x * m + y."""
    nbrs = []
    for x in range(m):
        for y in range(m):
            pts = [
                (x + y, y), (x - y, y), (x + y + 1, y), (x - y - 1, y),
                (x, y + x), (x, y - x), (x, y + x + 1), (x, y - x - 1),
            ]
            nbrs.append([(px % m) * m + (py % m) for px, py in pts])
    return nbrs


def petersen() -> list[list[int]]:
    """The Petersen graph: outer cycle 0..4, spokes i -- i + 5, inner pentagram."""
    nbrs: list[list[int]] = [[] for _ in range(10)]
    edges = [(i, (i + 1) % 5) for i in range(5)] + [(i, i + 5) for i in range(5)]
    edges += [(5 + i, 5 + (i + 2) % 5) for i in range(5)]
    for u, v in edges:
        nbrs[u].append(v)
        nbrs[v].append(u)
    return nbrs
