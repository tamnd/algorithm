# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/generalized-geography/. The authors are listed in prov/261S19.jsonl.

"""Generalized geography and its variants, solved by exhaustive search, with
the reduction from quantified Boolean formulas.

Vertex geography: a token starts on vertex s, which counts as used. The
players alternate, each moving the token along an edge to an unused vertex,
which then becomes used. The player who cannot move loses. Edge geography
is the same with used edges in place of used vertices."""

from functools import lru_cache
from itertools import combinations, product
from typing import Dict, List, Sequence, Tuple

Edge = Tuple[int, int]


def _succ(n: int, edges: Sequence[Edge], undirected: bool = False) -> List[List[int]]:
    succ: List[List[int]] = [[] for _ in range(n)]
    for u, v in edges:
        succ[u].append(v)
        if undirected:
            succ[v].append(u)
    return succ


def vertex_geography_first_wins(n: int, edges: Sequence[Edge], start: int, undirected: bool = False) -> bool:
    """True when the first player wins, by search over (vertex, used set)
    with a memo. The state space has at most n * 2^n states."""
    succ = _succ(n, edges, undirected)

    @lru_cache(maxsize=None)
    def win(v: int, used: int) -> bool:
        return any(not win(w, used | (1 << w)) for w in succ[v] if not used >> w & 1)

    return win(start, 1 << start)


def vertex_geography_plain(n: int, edges: Sequence[Edge], start: int) -> bool:
    """The same game by plain minimax without a memo: an independent check."""
    succ = _succ(n, edges)

    def win(v: int, used: frozenset) -> bool:
        for w in succ[v]:
            if w not in used and not win(w, used | {w}):
                return True
        return False

    return win(start, frozenset([start]))


def edge_geography_first_wins(n: int, edges: Sequence[Edge], start: int, undirected: bool = False) -> bool:
    """Edge geography: each edge may be used once; vertices may repeat."""
    m = len(edges)
    out: List[List[Tuple[int, int]]] = [[] for _ in range(n)]
    for i, (u, v) in enumerate(edges):
        out[u].append((i, v))
        if undirected:
            out[v].append((i, u))

    @lru_cache(maxsize=None)
    def win(v: int, used: int) -> bool:
        return any(not win(w, used | (1 << i)) for i, w in out[v] if not used >> i & 1)

    return win(start, 0)


def maximum_matching_size(n: int, edges: Sequence[Edge], removed: int = -1) -> int:
    """Size of a maximum matching by brute force (small graphs only)."""
    es = [(u, v) for u, v in edges if u != removed and v != removed and u != v]

    @lru_cache(maxsize=None)
    def best(i: int, used: int) -> int:
        if i == len(es):
            return 0
        u, v = es[i]
        skip = best(i + 1, used)
        if not used >> u & 1 and not used >> v & 1:
            return max(skip, 1 + best(i + 1, used | 1 << u | 1 << v))
        return skip

    return best(0, 0)


def undirected_vertex_geography_by_matching(n: int, edges: Sequence[Edge], start: int) -> bool:
    """Fraenkel, Scheinerman and Ullman: the first player wins undirected
    vertex geography from start exactly when every maximum matching covers
    start, that is, when removing start lowers the matching number."""
    return maximum_matching_size(n, edges, removed=start) < maximum_matching_size(n, edges)


# The reduction from QBF. The formula is
#   exists x1 forall x2 exists x3 ... phi
# with phi in CNF; clauses are lists of nonzero integers (k for x_k, -k for
# not x_k). The number of variables is made odd with a dummy variable, so
# that player I sets the odd variables and player II picks the clause.

def qbf_to_geography(num_vars: int, clauses: Sequence[Sequence[int]]):
    """Return (n, edges, start). Diamond k has top t_k, nodes P_k and N_k,
    and bottom b_k. Choosing N_k sets x_k true and leaves P_k unused, so a
    clause can then move to P_k for the literal x_k."""
    nv = num_vars if num_vars % 2 == 1 else num_vars + 1
    ids: Dict[Tuple[str, int], int] = {}

    def node(kind: str, k: int) -> int:
        if (kind, k) not in ids:
            ids[(kind, k)] = len(ids)
        return ids[(kind, k)]

    edges: List[Edge] = []
    for k in range(1, nv + 1):
        t, p, q, b = node("t", k), node("P", k), node("N", k), node("b", k)
        edges += [(t, p), (t, q), (p, b), (q, b)]
        edges.append((b, node("t", k + 1) if k < nv else node("c", 0)))
    c = node("c", 0)
    for j, clause in enumerate(clauses):
        cj = node("C", j)
        edges.append((c, cj))
        for lit in clause:
            edges.append((cj, node("P", lit) if lit > 0 else node("N", -lit)))
    return len(ids), edges, node("t", 1)


def qbf_true(num_vars: int, clauses: Sequence[Sequence[int]]) -> bool:
    """Evaluate exists x1 forall x2 ... phi by brute force."""

    def sat(assign: Tuple[bool, ...]) -> bool:
        return all(any(assign[abs(l) - 1] == (l > 0) for l in cl) for cl in clauses)

    def ev(prefix: Tuple[bool, ...]) -> bool:
        k = len(prefix)
        if k == num_vars:
            return sat(prefix)
        branches = (ev(prefix + (True,)), ev(prefix + (False,)))
        return any(branches) if k % 2 == 0 else all(branches)

    return ev(())


def random_graph(rng, n: int, p: float, undirected: bool = False) -> List[Edge]:
    if undirected:
        return [(u, v) for u, v in combinations(range(n), 2) if rng.random() < p]
    return [(u, v) for u, v in product(range(n), repeat=2) if u != v and rng.random() < p]
