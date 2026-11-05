# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/node2vec/. The authors are listed in prov/3SC38Y.jsonl.

import math
import random


def build_graph(
    n: int, edges: list[tuple[int, int] | tuple[int, int, float]]
) -> list[dict[int, float]]:
    """Return the adjacency maps of an undirected weighted graph on 0 .. n-1.

    Each edge is (u, v) with weight 1 or (u, v, w) with w > 0. A repeated edge
    adds its weight to the earlier one. Self-loops are not allowed.
    """
    if n < 0:
        raise ValueError("n must be non-negative")
    adj: list[dict[int, float]] = [{} for _ in range(n)]
    for e in edges:
        u, v = e[0], e[1]
        w = float(e[2]) if len(e) == 3 else 1.0
        if not (0 <= u < n and 0 <= v < n):
            raise ValueError("edge endpoint out of range")
        if u == v:
            raise ValueError("self-loops are not allowed")
        if not w > 0.0:
            raise ValueError("edge weights must be positive")
        adj[u][v] = adj[u].get(v, 0.0) + w
        adj[v][u] = adj[v].get(u, 0.0) + w
    return adj


def transition_weights(
    adj: list[dict[int, float]], t: int, v: int, p: float, q: float
) -> list[tuple[int, float]]:
    """Return the unnormalized weights of the next step after the step t -> v.

    The weight of a neighbour x of v is w(v, x) / p if x = t, w(v, x) if x is
    a neighbour of t, and w(v, x) / q otherwise.
    """
    out = []
    for x, w in adj[v].items():  # @line L1
        if x == t:
            out.append((x, w / p))
        elif x in adj[t]:
            out.append((x, w))
        else:
            out.append((x, w / q))
    return out


def _choose(items: list[tuple[int, float]], rng: random.Random) -> int:
    total = sum(w for _, w in items)
    r = rng.random() * total
    acc = 0.0
    for x, w in items:
        acc += w
        if r < acc:
            return x
    return items[-1][0]


def node2vec_walk(
    adj: list[dict[int, float]],
    start: int,
    length: int,
    p: float,
    q: float,
    rng: random.Random,
) -> list[int]:
    """Return one biased walk with `length` vertices that starts at `start`.

    The first step goes to a neighbour chosen with probability proportional
    to the edge weight; later steps use transition_weights. A walk from an
    isolated vertex is just [start].
    """
    walk = [start]  # @line L5
    if length > 1 and adj[start]:
        walk.append(_choose(list(adj[start].items()), rng))
    while 1 < len(walk) < length:  # @line L6
        t, v = walk[-2], walk[-1]
        walk.append(_choose(transition_weights(adj, t, v, p, q), rng))  # @line L7
    return walk


def _sigmoid(x: float) -> float:
    if x >= 0:
        return 1.0 / (1.0 + math.exp(-x))
    e = math.exp(x)
    return e / (1.0 + e)


def skipgram(
    n: int,
    walks: list[list[int]],
    dim: int,
    window: int,
    negatives: int,
    epochs: int,
    rate: float,
    rng: random.Random,
) -> list[list[float]]:
    """Train skip-gram with negative sampling on the walks by plain SGD.

    For each pair (u, c) with c within `window` positions of u in a walk, the
    loss is -log s(z_u . y_c) - sum over `negatives` sampled vertices m of
    -log s(-z_u . y_m), where s is the logistic function and negatives are
    drawn with probability proportional to count ** 0.75.
    """
    z = [[(rng.random() - 0.5) / dim for _ in range(dim)] for _ in range(n)]
    y = [[0.0] * dim for _ in range(n)]
    count = [0] * n
    for walk in walks:
        for u in walk:
            count[u] += 1
    pool = [u for u in range(n) if count[u] > 0]
    if not pool:
        return z
    cum = []
    acc = 0.0
    for u in pool:
        acc += count[u] ** 0.75
        cum.append(acc)

    def draw() -> int:
        r = rng.random() * acc
        lo, hi = 0, len(cum) - 1
        while lo < hi:
            mid = (lo + hi) // 2
            if cum[mid] > r:
                hi = mid
            else:
                lo = mid + 1
        return pool[lo]

    pairs_total = max(1, epochs * sum(len(w) for w in walks))
    done = 0
    for _ in range(epochs):
        for walk in walks:
            for i, u in enumerate(walk):
                lr = max(rate * 1e-4, rate * (1.0 - done / pairs_total))
                done += 1
                lo, hi = max(0, i - window), min(len(walk), i + window + 1)
                for j in range(lo, hi):
                    if j == i:
                        continue
                    zu = z[u]
                    grad = [0.0] * dim
                    targets = [(walk[j], 1.0)] + [(draw(), 0.0) for _ in range(negatives)]
                    for c, label in targets:
                        yc = y[c]
                        g = lr * (label - _sigmoid(sum(a * b for a, b in zip(zu, yc))))
                        for k in range(dim):
                            grad[k] += g * yc[k]
                            yc[k] += g * zu[k]
                    for k in range(dim):
                        zu[k] += grad[k]
    return z


def node2vec(
    n: int,
    edges: list[tuple[int, int] | tuple[int, int, float]],
    dim: int = 16,
    walks_per_vertex: int = 10,
    length: int = 20,
    window: int = 5,
    p: float = 1.0,
    q: float = 1.0,
    negatives: int = 5,
    epochs: int = 1,
    rate: float = 0.025,
    seed: int = 0,
) -> list[list[float]]:
    """Return a dim-dimensional vector for each vertex of an undirected graph.

    The graph has vertices 0 .. n-1 and edges (u, v) or (u, v, w) with w > 0.
    The return parameter p and the in-out parameter q must be positive. The
    result depends only on the inputs and the seed.
    """
    if dim < 1 or walks_per_vertex < 0 or length < 1 or window < 1 or negatives < 0:
        raise ValueError("invalid size parameter")
    if not (p > 0.0 and q > 0.0):
        raise ValueError("p and q must be positive")
    adj = build_graph(n, edges)
    rng = random.Random(seed)
    walks: list[list[int]] = []  # @line L2
    for _ in range(walks_per_vertex):  # @line L3
        order = list(range(n))
        rng.shuffle(order)
        for u in order:  # @line L4
            walk = node2vec_walk(adj, u, length, p, q, rng)
            walks.append(walk)  # @line L8
    z = skipgram(n, walks, dim, window, negatives, epochs, rate, rng)  # @line L9
    return z  # @line L10
