# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/linial-coloring-lower-bound/. The authors are listed in prov/781NR6.jsonl.

"""Objects of Linial's lower bound for colouring a directed cycle, for brute-force checks on tiny cases.

neighbourhood_graph(t, n) is Linial's graph B(t, n): its vertices are the
views of a node after t rounds on a directed cycle with identifiers from
{0, ..., n-1}, and two views are adjacent when they can belong to two
consecutive nodes. A t-round c-colouring algorithm exists exactly when this
graph has a proper c-colouring. shift_graph(n, k) keeps only increasing
tuples, as in the proof on the page, and reduce_colouring is the step of that
proof that turns a k-ary colouring into a (k - 1)-ary one.

Precondition: small n and k; the graphs have n^(2t+1) vertices or fewer.
Cost: chromatic_number is exponential (backtracking), for tiny graphs only.
"""

import itertools


def neighbourhood_graph(t: int, n: int) -> tuple[list[tuple[int, ...]], list[set[int]]]:
    """Vertices are (2t+1)-tuples of distinct ids; edges join x[0:k] and x[1:k+1] for distinct x of length k+1."""
    k = 2 * t + 1
    verts = list(itertools.permutations(range(n), k))
    index = {v: i for i, v in enumerate(verts)}
    adj: list[set[int]] = [set() for _ in verts]
    for x in itertools.permutations(range(n), k + 1):
        a, b = index[x[:k]], index[x[1:]]
        adj[a].add(b)
        adj[b].add(a)
    return verts, adj


def shift_graph(n: int, k: int) -> tuple[list[tuple[int, ...]], list[set[int]]]:
    """Vertices are increasing k-tuples of {0, ..., n-1}; edges join x[0:k] and x[1:k+1] for increasing x."""
    verts = list(itertools.combinations(range(n), k))
    index = {v: i for i, v in enumerate(verts)}
    adj: list[set[int]] = [set() for _ in verts]
    for x in itertools.combinations(range(n), k + 1):
        a, b = index[x[:k]], index[x[1:]]
        adj[a].add(b)
        adj[b].add(a)
    return verts, adj


def colourable(adj: list[set[int]], c: int) -> list[int] | None:
    """Return a proper colouring with colours in range(c), or None. Backtracking with the most constrained vertex first."""
    n = len(adj)
    col = [-1] * n

    def go(done: int, used: int) -> bool:
        if done == n:
            return True
        best, best_free = -1, None
        for v in range(n):
            if col[v] < 0:
                free = set(range(min(c, used + 1))) - {col[u] for u in adj[v]}
                if best_free is None or len(free) < len(best_free):
                    best, best_free = v, free
                    if not free:
                        return False
        assert best_free is not None
        for x in sorted(best_free):
            col[best] = x
            if go(done + 1, max(used, x + 1)):
                return True
        col[best] = -1
        return False

    return col if go(0, 0) else None


def chromatic_number(adj: list[set[int]]) -> int:
    """The least c such that the graph has a proper c-colouring."""
    c = 0 if not adj else 1
    while adj and colourable(adj, c) is None:
        c += 1
    return c


def reduce_colouring(f: dict[tuple[int, ...], int], n: int, k: int) -> dict[tuple[int, ...], frozenset[int]]:
    """g(x_1..x_{k-1}) = the set of f(x_1..x_{k-1}, y) over y > x_{k-1}: a (k-1)-ary colouring with 2^c colours."""
    g: dict[tuple[int, ...], frozenset[int]] = {}
    for x in itertools.combinations(range(n), k - 1):
        g[x] = frozenset(f[x + (y,)] for y in range(x[-1] + 1, n))
    return g


def is_proper_kary(f: dict, n: int, k: int) -> bool:
    """f is proper when f(x_1..x_k) != f(x_2..x_{k+1}) for every increasing (k+1)-tuple."""
    return all(f[x[:k]] != f[x[1:]] for x in itertools.combinations(range(n), k + 1))


def tower_bound(k: int, c: int = 3) -> int:
    """c_1 = c and c_{j+1} = 2^(c_j); a proper k-ary c-colouring of {0..n-1} forces n <= c_k."""
    v = c
    for _ in range(k - 1):
        v = 2**v
    return v
