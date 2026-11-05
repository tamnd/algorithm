# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/pagerank/. The authors are listed in prov/YEWMFK.jsonl.


def pagerank(
    n: int,
    arcs: list[tuple[int, int]],
    alpha: float = 0.85,
    eps: float = 1e-10,
    max_rounds: int = 10_000,
) -> list[float]:
    """Return the PageRank vector of a directed graph by power iteration.

    The vertices are 0 .. n-1 (n >= 1) and arcs is a list of pairs (u, v).
    A repeated arc counts as many times as it appears; a self-loop is an
    ordinary arc. A vertex without out-arcs (dangling) sends its share to all
    vertices. The damping factor alpha is in [0, 1). The loop stops when the
    L1 change of one round is below eps, so the result is within
    alpha * eps / (1 - alpha) of the exact vector in the L1 norm.
    Each round costs O(n + m); the extra space is O(n).
    """
    if n < 1:
        raise ValueError("n must be at least 1")
    if not 0.0 <= alpha < 1.0:
        raise ValueError("alpha must be in [0, 1)")
    out = [0] * n
    for u, v in arcs:
        if not (0 <= u < n and 0 <= v < n):
            raise ValueError("arc endpoint out of range")
        out[u] += 1
    dangling = [u for u in range(n) if out[u] == 0]
    x = [1.0 / n] * n  # @line L1
    for _ in range(max_rounds):  # @line L2
        y = [0.0] * n  # @line L3
        d = sum(x[u] for u in dangling)  # @line L4
        for u, v in arcs:  # @line L5
            y[v] += x[u] / out[u]
        base = (alpha * d + 1.0 - alpha) / n
        for v in range(n):  # @line L6
            y[v] = alpha * y[v] + base
        delta = sum(abs(y[v] - x[v]) for v in range(n))  # @line L7
        x = y  # @line L8
        if delta < eps:  # @line L9
            break
    return x  # @line L10


def ranking(scores: list[float], tol: float = 1e-9) -> list[int]:
    """Return the vertices by decreasing score; scores within tol tie and keep vertex order."""
    order = sorted(range(len(scores)), key=lambda v: -scores[v])
    # stable pass: inside each group of near-equal scores, sort by vertex number
    result: list[int] = []
    i = 0
    while i < len(order):
        j = i + 1
        while j < len(order) and scores[order[i]] - scores[order[j]] <= tol:
            j += 1
        result.extend(sorted(order[i:j]))
        i = j
    return result
