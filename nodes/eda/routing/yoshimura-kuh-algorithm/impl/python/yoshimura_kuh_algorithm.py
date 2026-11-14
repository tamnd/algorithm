# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/yoshimura-kuh-algorithm/. The authors are listed in prov/MQ0AC7.jsonl.

"""Net merging channel routing after Yoshimura and Kuh, in the reserved two-layer model, without doglegs.

The columns are grouped into zones: the maximal sets of nets that cross one
column. The zones are scanned from left to right. At each zone boundary, a
net that has ended may be merged with a net that starts in the next zone, if
no path of the vertical constraint graph joins them. Merged nets share one
track. Of all such pairs, the pair that gives the shortest longest path
through the merged node is taken first. At the end, the merged nets get
their tracks with the constrained left-edge rule.

This is the version of the page: the cost of a merge is the length of the
longest path through the merged node. Yoshimura and Kuh also give a merge
step based on bipartite matching.
"""

from typing import Dict, FrozenSet, List, Optional, Sequence, Set, Tuple

from channel import intervals, realize, vcg_edges


def zones(top: Sequence[int], bottom: Sequence[int]) -> List[FrozenSet[int]]:
    """The maximal sets S(c) of nets that cross column c, in column order."""
    spans = intervals(top, bottom)
    sets = [frozenset(x for x, (l, r) in spans.items() if l <= c <= r) for c in range(1, len(top) + 1)]
    out: List[FrozenSet[int]] = []
    for s in sets:
        if s and not any(s < t for t in sets) and (not out or out[-1] != s):
            out.append(s)
    return out


def topological_order(nodes: Sequence[int], succ: Dict[int, Set[int]]) -> Optional[List[int]]:
    indeg = {v: 0 for v in nodes}
    for v in nodes:
        for w in succ[v]:
            indeg[w] += 1
    stack = sorted((v for v in nodes if indeg[v] == 0), reverse=True)
    order = []
    while stack:
        v = stack.pop()
        order.append(v)
        for w in sorted(succ[v], reverse=True):
            indeg[w] -= 1
            if indeg[w] == 0:
                stack.append(w)
    return order if len(order) == len(nodes) else None


def path_lengths(nodes, succ, pred) -> Tuple[Dict[int, int], Dict[int, int]]:
    """u[v]: nodes on the longest path that ends at v. d[v]: nodes on the longest path that starts at v."""
    order = topological_order(nodes, succ)
    u = {v: 1 for v in nodes}
    d = {v: 1 for v in nodes}
    for v in order:
        for w in succ[v]:
            u[w] = max(u[w], u[v] + 1)
    for v in reversed(order):
        for w in pred[v]:
            d[w] = max(d[w], d[v] + 1)
    return u, d


def reaches(succ: Dict[int, Set[int]], a: int, b: int) -> bool:
    seen, stack = {a}, [a]
    while stack:
        v = stack.pop()
        if v == b:
            return True
        for w in succ[v]:
            if w not in seen:
                seen.add(w)
                stack.append(w)
    return False


def merge_nets(top: Sequence[int], bottom: Sequence[int]):
    """Merge nets zone by zone. Returns (groups, group spans, successors), or None on a cycle.

    groups maps a group id (its first net) to its nets. A group span is
    (leftmost column, rightmost column) over its nets.
    """
    spans = intervals(top, bottom)
    succ: Dict[int, Set[int]] = {x: set() for x in spans}
    pred: Dict[int, Set[int]] = {x: set() for x in spans}
    for a, b in vcg_edges(top, bottom):  # @line L1
        succ[a].add(b)
        pred[b].add(a)
    if topological_order(sorted(spans), succ) is None:
        return None
    zs = zones(top, bottom)  # @line L2
    first = {x: min(i for i, z in enumerate(zs, 1) if x in z) for x in spans}
    last = {x: max(i for i, z in enumerate(zs, 1) if x in z) for x in spans}
    groups = {x: [x] for x in spans}
    gspan = dict(spans)
    left: List[int] = []  # @line L3
    for i in range(1, len(zs)):  # @line L4
        left += sorted(g for g in groups if last[g] == i)  # @line L5
        right = sorted(g for g in groups if first[g] == i + 1)  # @line L6
        while True:
            nodes = sorted(groups)
            u, d = path_lengths(nodes, succ, pred)
            best = None
            for a in left:  # @line L7
                for b in right:
                    if reaches(succ, a, b) or reaches(succ, b, a):
                        continue
                    cost = max(u[a], u[b]) + max(d[a], d[b]) - 1  # @line L8
                    if best is None or (cost, a, b) < best:
                        best = (cost, a, b)
            if best is None:
                break
            _, a, b = best
            groups[a] += groups.pop(b)  # @line L9
            gspan[a] = (gspan[a][0], gspan.pop(b)[1])
            last[a] = last.pop(b)
            first.pop(b)
            for w in succ.pop(b):
                pred[w].discard(b)
                pred[w].add(a)
                succ[a].add(w)
            for w in pred.pop(b):
                succ[w].discard(b)
                succ[w].add(a)
                pred[a].add(w)
            left.remove(a)
            right.remove(b)
    return groups, gspan, succ


def left_edge(spans: Dict[int, Tuple[int, int]], succ: Dict[int, Set[int]]) -> Dict[int, int]:
    """Constrained left-edge on groups: fill one track at a time; a group goes on track t
    when it does not overlap the last group on t and all its parents are on higher tracks."""
    parents: Dict[int, List[int]] = {g: [] for g in spans}
    for a, ws in succ.items():
        for b in ws:
            parents[b].append(a)
    unplaced = sorted(spans, key=lambda g: (spans[g][0], g))
    track: Dict[int, int] = {}
    t = 0
    while unplaced:
        t += 1
        last = None
        for g in unplaced:
            if (last is None or spans[g][0] > last) and all(track.get(p, t) < t for p in parents[g]):
                track[g] = t
                last = spans[g][1]
        unplaced = [g for g in unplaced if g not in track]
    return track


def yoshimura_kuh_route(top: Sequence[int], bottom: Sequence[int]):
    """Route a channel by net merging. Returns (tracks, track of each net, wires, groups), or None on a cycle."""
    merged = merge_nets(top, bottom)
    if merged is None:
        return None
    groups, gspan, succ = merged
    gtrack = left_edge(gspan, succ)  # @line L10
    track = {x: gtrack[g] for g, xs in groups.items() for x in xs}
    t = max(track.values(), default=0)
    spans = intervals(top, bottom)
    pieces = {x: (x, l, r) for x, (l, r) in spans.items()}
    return t, track, realize(top, bottom, pieces, track, t), groups  # @line L11


if __name__ == "__main__":
    top = [5, 0, 0, 1, 0, 0, 1, 0]
    bottom = [2, 2, 4, 5, 3, 3, 1, 4]
    print(zones(top, bottom))
    print(yoshimura_kuh_route(top, bottom)[:2])
