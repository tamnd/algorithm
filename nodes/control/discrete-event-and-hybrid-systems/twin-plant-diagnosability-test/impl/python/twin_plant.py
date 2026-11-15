# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/twin-plant-diagnosability-test/. The authors are listed in prov/4TC48W.jsonl.

"""The twin plant (verifier) test of diagnosability.

The plant G is a dict with the keys "init" and "delta" (a dict that maps
(state, event) to the next state). `observable` is the set of observable
events and `faults` is the set of fault events of the fault type under test.
Fault events are unobservable. G must have no cycle of unobservable events.

The verifier runs two copies of G. Copy 1 is the full plant and records in
a flag whether a fault has happened. Copy 2 is the plant without the fault
transitions. The copies move alone on unobservable events and together on
observable events, so both always have the same observation. G is
diagnosable for `faults` if and only if the verifier has no cycle of states
whose flag is set (Yoo and Lafortune 2002; Jiang et al. 2001 use a similar
product of the observable reduction of G).

Cost: at most 2 |X|^2 verifier states, each with at most 2 |Sigma| outgoing
edges, for |X| states and an alphabet of size |Sigma|. So there are at most
4 |X|^2 |Sigma| edges, and the test takes O(|X|^2 |Sigma|) dict operations.
"""

from collections import deque
from typing import Iterable, Optional


def out_edges(delta: dict) -> dict:
    out: dict = {}
    for (q, e), r in delta.items():
        out.setdefault(q, {})[e] = r
    return out


def build_verifier(g: dict, observable: Iterable, faults: Iterable):
    """Return (v0, states, edges); edges[v] is a list of (w, (event of copy 1, event of copy 2))."""
    obs, flt = set(observable), set(faults)
    out = out_edges(g["delta"])
    normal = {y: {e: z for e, z in d.items() if e not in flt} for y, d in out.items()}  # @line L1
    v0 = (g["init"], False, g["init"])  # @line L2
    states = {v0}
    edges: dict = {}
    queue = deque([v0])
    while queue:  # @line L3
        v = queue.popleft()  # @line L4
        x, flag, y = v
        succ = []
        for e, x2 in out.get(x, {}).items():
            if e not in obs:
                succ.append(((x2, flag or e in flt, y), (e, None)))  # @line L5
        for e, y2 in normal.get(y, {}).items():
            if e not in obs:
                succ.append(((x, flag, y2), (None, e)))  # @line L6
        for e, x2 in out.get(x, {}).items():
            if e in obs and e in normal.get(y, {}):
                succ.append(((x2, flag, normal[y][e]), (e, e)))  # @line L7
        edges[v] = succ
        for w, _ in succ:  # @line L8
            if w not in states:
                states.add(w)
                queue.append(w)
    return v0, states, edges


def _kahn_remaining(nodes: set, edges: dict) -> set:
    """The nodes that Kahn's algorithm cannot remove; empty if and only if the graph on nodes has no cycle."""
    indeg = {v: 0 for v in nodes}
    for v in nodes:
        for w, _ in edges.get(v, ()):
            if w in nodes:
                indeg[w] += 1
    queue = deque(v for v in nodes if indeg[v] == 0)
    left = set(nodes)
    while queue:
        v = queue.popleft()
        left.discard(v)
        for w, _ in edges.get(v, ()):
            if w in nodes:
                indeg[w] -= 1
                if indeg[w] == 0:
                    queue.append(w)
    return left


def diagnosable(g: dict, observable: Iterable, faults: Iterable) -> bool:
    """True if G is diagnosable for the given fault events."""
    v0, states, edges = build_verifier(g, observable, faults)
    w = {v for v in states if v[1]}  # @line L9
    return not _kahn_remaining(w, edges)  # @line L10


def witness(g: dict, observable: Iterable, faults: Iterable) -> Optional[tuple]:
    """If G is not diagnosable, return (p1, c1, p2, c2): copy 1 runs p1 c1 c1 ..., copy 2 runs p2 c2 c2 ...

    p1 c1^k is in L(G) and holds a fault, p2 c2^k is in L(G) and holds none, and both have the same
    projection for every k. Return None if G is diagnosable.
    """
    v0, states, edges = build_verifier(g, observable, faults)
    w = {v for v in states if v[1]}
    left = _kahn_remaining(w, edges)
    if not left:
        return None
    pred: dict = {}
    for v in left:
        for u, lab in edges.get(v, ()):
            if u in left:
                pred.setdefault(u, (v, lab))
    v = next(iter(left))
    seen: dict = {}
    while v not in seen:
        seen[v] = len(seen)
        v = pred[v][0]
    start = v
    cycle = []
    while True:
        u, lab = pred[v]
        cycle.append(lab)
        v = u
        if v == start:
            break
    cycle.reverse()
    parent = {v0: None}
    queue = deque([v0])
    while queue:
        u = queue.popleft()
        if u == start:
            break
        for x, lab in edges.get(u, ()):
            if x not in parent:
                parent[x] = (u, lab)
                queue.append(x)
    path = []
    u = start
    while parent[u] is not None:
        u, lab = parent[u]
        path.append(lab)
    path.reverse()

    def part(labels, i):
        return tuple(lab[i] for lab in labels if lab[i] is not None)

    return part(path, 0), part(cycle, 0), part(path, 1), part(cycle, 1)


def diagnosable_jiang(g: dict, observable: Iterable, faults: Iterable) -> bool:
    """The test of Jiang et al. (2001): a product of two labelled copies of the observable reduction of G."""
    obs, flt = set(observable), set(faults)
    out = out_edges(g["delta"])

    def jumps(pair):
        res: dict = {}
        seen = {pair}
        stack = [pair]
        while stack:
            x, f = stack.pop()
            for e, y in out.get(x, {}).items():
                if e in obs:
                    res.setdefault(e, set()).add((y, f))
                elif (y, f or e in flt) not in seen:
                    seen.add((y, f or e in flt))
                    stack.append((y, f or e in flt))
        return res

    cache: dict = {}
    start = ((g["init"], False), (g["init"], False))
    states = {start}
    edges: dict = {}
    queue = deque([start])
    while queue:
        a, b = v = queue.popleft()
        for p in (a, b):
            if p not in cache:
                cache[p] = jumps(p)
        succ = []
        for e, targets in cache[a].items():
            for a2 in targets:
                for b2 in cache[b].get(e, ()):
                    succ.append(((a2, b2), e))
        edges[v] = succ
        for w, _ in succ:
            if w not in states:
                states.add(w)
                queue.append(w)
    amb = {v for v in states if v[0][1] != v[1][1]}
    return not _kahn_remaining(amb, edges)
