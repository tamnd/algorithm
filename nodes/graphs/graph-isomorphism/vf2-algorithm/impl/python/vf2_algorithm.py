# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/vf2-algorithm/. The authors are listed in prov/M8JFJA.jsonl.
"""VF2 state-space search for graph isomorphism, induced subgraph isomorphism and monomorphism.

Graphs are undirected and simple, given as (n, edges) with vertices 0..n-1, and may carry
integer vertex labels that a mapping must keep. G1 is the pattern and G2 the host.
The search is iterative, with an explicit stack, so its depth is not limited by recursion.
"""

from collections.abc import Iterator

Graph = tuple[int, list[tuple[int, int]]]
MODES = ("iso", "induced", "mono")


def _adj(n: int, edges: list[tuple[int, int]]) -> list[set[int]]:
    a: list[set[int]] = [set() for _ in range(n)]
    for u, v in edges:
        a[u].add(v)
        a[v].add(u)
    return a


def vf2_matches(g1: Graph, g2: Graph, mode: str = "iso",
                labels1: list[int] | None = None, labels2: list[int] | None = None) -> Iterator[list[int]]:
    """Yield every mapping m (m[u] is the host vertex of pattern vertex u) of the given kind.

    mode "iso": bijection keeping edges and non-edges; "induced": injection keeping edges and
    non-edges; "mono": injection keeping edges. Cost: exponential in the worst case; each search
    state costs O(n1 + n2 + d1 * d2) time for degree bounds d1, d2; space O(n1 + n2 + m1 + m2).
    """
    if mode not in MODES:
        raise ValueError("mode must be one of " + ", ".join(MODES))
    n1, e1 = g1
    n2, e2 = g2
    if mode == "iso" and (n1 != n2 or len(e1) != len(e2)):
        return
    if n1 > n2:
        return
    a1, a2 = _adj(n1, e1), _adj(n2, e2)
    lab1 = labels1 if labels1 is not None else [0] * n1
    lab2 = labels2 if labels2 is not None else [0] * n2
    core1 = [-1] * n1
    core2 = [-1] * n2
    t1 = [0] * n1  # number of mapped neighbors; an unmapped vertex with t > 0 is in T
    t2 = [0] * n2

    def candidates() -> list[tuple[int, int]]:
        # @line L3
        term1 = [u for u in range(n1) if core1[u] < 0 and t1[u] > 0]
        term2 = [v for v in range(n2) if core2[v] < 0 and t2[v] > 0]
        if term1:
            if not term2:
                return []
            u = term1[0]
            return [(u, v) for v in term2]
        if mode == "iso" and term2:
            return []
        u = next(x for x in range(n1) if core1[x] < 0)
        pool = [v for v in range(n2) if core2[v] < 0] if mode != "iso" else [v for v in range(n2) if core2[v] < 0 and t2[v] == 0]
        return [(u, v) for v in pool]

    def feasible(u: int, v: int) -> bool:
        # @line L9
        if lab1[u] != lab2[v]:
            return False
        if mode == "iso" and len(a1[u]) != len(a2[v]):
            return False
        if mode != "iso" and len(a1[u]) > len(a2[v]):
            return False
        # @line L10
        for w in a1[u]:
            if core1[w] >= 0 and core1[w] not in a2[v]:
                return False
        if mode != "mono":
            for x in a2[v]:
                if core2[x] >= 0 and core2[x] not in a1[u]:
                    return False
        # @line L11
        term_u = sum(1 for w in a1[u] if core1[w] < 0 and t1[w] > 0)
        term_v = sum(1 for x in a2[v] if core2[x] < 0 and t2[x] > 0)
        new_u = sum(1 for w in a1[u] if core1[w] < 0 and t1[w] == 0)
        new_v = sum(1 for x in a2[v] if core2[x] < 0 and t2[x] == 0)
        if mode == "iso":
            return term_u == term_v and new_u == new_v
        # @line L12
        if mode == "induced":
            return term_u <= term_v and new_u <= new_v
        return term_u <= term_v and term_u + new_u <= term_v + new_v

    def push(u: int, v: int) -> None:
        core1[u], core2[v] = v, u
        for w in a1[u]:
            t1[w] += 1
        for x in a2[v]:
            t2[x] += 1

    def pop(u: int, v: int) -> None:
        core1[u], core2[v] = -1, -1
        for w in a1[u]:
            t1[w] -= 1
        for x in a2[v]:
            t2[x] -= 1

    # @line L1
    if n1 == 0:
        yield []
        return
    depth = 0
    # a frame is [candidate pairs, index of the next pair to try, pair applied from this frame or None]
    stack: list[list] = [[candidates(), 0, None]]
    while stack:
        frame = stack[-1]
        if frame[2] is not None:
            # @line L8
            pop(*frame[2])
            frame[2] = None
            depth -= 1
        pairs, i = frame[0], frame[1]
        # @line L4
        while i < len(pairs) and not feasible(*pairs[i]):
            i += 1
        if i == len(pairs):
            stack.pop()
            continue
        # @line L5
        u, v = pairs[i]
        frame[1] = i + 1
        # @line L6
        push(u, v)
        frame[2] = (u, v)
        depth += 1
        # @line L2
        if depth == n1:
            yield list(core1)
            continue
        # @line L7
        stack.append([candidates(), 0, None])


def vf2_isomorphic(g1: Graph, g2: Graph, labels1: list[int] | None = None, labels2: list[int] | None = None) -> bool:
    """True when g1 and g2 are isomorphic (labels kept). Cost: as vf2_matches, stopping at the first match."""
    return next(vf2_matches(g1, g2, "iso", labels1, labels2), None) is not None


def vf2_count(g1: Graph, g2: Graph, mode: str = "iso") -> int:
    """Number of mappings of the given mode. Cost: as vf2_matches, over the whole search."""
    return sum(1 for _ in vf2_matches(g1, g2, mode))
