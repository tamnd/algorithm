# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/variation-graph/. The authors are listed in prov/XJVQNQ.jsonl.
"""A variation graph built from a linear reference and a list of variants.

A variant (pos, a, b) replaces the reference bases ref[pos:pos + len(a)] by
the string b. Either a or b may be empty (an insertion or a deletion), but
not both, and a != b. Positions are 0-based. The variants must not touch:
each one starts at least one base after the end of the one before it, and
each one has at least one reference base on each side. These rules make
every node non-empty and every variant one bubble of the graph.

Each node holds a string. The graph has the reference path, which spells the
reference, and one path for each subset of the variants. Node ids are
0, 1, 2, ... in the order of the start of the node on the reference, with the
reference allele before the alternative allele, so the order of the ids is a
topological order.

The module has three operations: build the graph, spell a path, and find the
exact matches of a string along the walks of the graph. What it leaves out
compared with vg: the bidirected form (both strands of a node), variants
that overlap or touch, a graph built from whole-genome alignments,
alignment with errors, and an index such as the GCSA2 or GBWT.
"""

from __future__ import annotations

from typing import Dict, List, Sequence, Tuple

Variant = Tuple[int, str, str]


class VariationGraph:
    """Nodes with strings, edges between them and named paths."""

    def __init__(self) -> None:
        self.seq: List[str] = []
        self.succ: List[List[int]] = []
        self.paths: Dict[str, List[int]] = {}
        # bubble[v] = (u, w, ref_route, alt_route): the bubble of variant v.
        self.bubble: List[Tuple[int, int, List[int], List[int]]] = []

    def add_node(self, s: str) -> int:
        self.seq.append(s)
        self.succ.append([])
        return len(self.seq) - 1

    def add_edge(self, u: int, w: int) -> None:
        if w not in self.succ[u]:
            self.succ[u].append(w)
            self.succ[u].sort()


def build(ref: str, variants: Sequence[Variant]) -> VariationGraph:
    """The graph of ref and the variants, with the path "ref"."""
    vs = sorted(variants)
    end = 0
    for pos, a, b in vs:
        if a == b:
            raise ValueError("a variant must change the sequence")
        if pos < end + 1 or pos < 1 or pos + len(a) > len(ref) - 1:
            raise ValueError("variants must not touch each other or the ends of the reference")
        if ref[pos:pos + len(a)] != a:
            raise ValueError("the reference allele does not match the reference")
        end = pos + len(a)
    g = VariationGraph()
    cuts = sorted({0, len(ref)} | {p for p, _, _ in vs} | {p + len(a) for p, a, _ in vs})  # @line L1
    node_at: Dict[int, int] = {}  # start on the reference -> reference node
    # (start, order, string): order 0 for a reference node, 1 for an alt node, and -1 for an
    # inserted node, which comes before the reference node that starts at the same place.
    pieces: List[Tuple[int, int, str]] = []
    for x, y in zip(cuts, cuts[1:]):  # @line L2
        pieces.append((x, 0, ref[x:y]))
    for pos, a, b in vs:
        if b:
            pieces.append((pos, 1 if a else -1, b))  # @line L3
    pieces.sort()
    alt_node: Dict[int, int] = {}
    for start, order, s in pieces:
        i = g.add_node(s)
        if order == 0:
            node_at[start] = i
        else:
            alt_node[start] = i
    ref_path = [node_at[x] for x in cuts[:-1]]
    for u, w in zip(ref_path, ref_path[1:]):  # @line L4
        g.add_edge(u, w)
    ends_at = {cuts[t + 1]: node_at[cuts[t]] for t in range(len(cuts) - 1)}
    for pos, a, b in vs:  # @line L5
        u, w = ends_at[pos], node_at[pos + len(a)]
        ref_route = [node_at[pos]] if a else []
        if b:
            alt_route = [alt_node[pos]]
            g.add_edge(u, alt_route[0])  # @line L6
            g.add_edge(alt_route[0], w)
        else:
            alt_route = []
            g.add_edge(u, w)  # @line L7
        g.bubble.append((u, w, ref_route, alt_route))
    g.paths["ref"] = ref_path
    return g


def spell(g: VariationGraph, path: Sequence[int]) -> str:
    """The string of a path: the strings of its nodes, joined. The path must follow edges."""
    for u, w in zip(path, path[1:]):
        if w not in g.succ[u]:
            raise ValueError(f"no edge from {u} to {w}")
    return "".join(g.seq[i] for i in path)


def haplotype_path(g: VariationGraph, chosen: Sequence[int]) -> List[int]:
    """The path that takes the alternative route of the variants in chosen (indices
    into the sorted variant list) and the reference route of the others."""
    pick = set(chosen)
    ref_path = g.paths["ref"]
    out: List[int] = []
    t = 0
    for v, (u, w, ref_route, alt_route) in enumerate(g.bubble):
        while ref_path[t] != u:
            out.append(ref_path[t])
            t += 1
        out.append(u)
        out.extend(alt_route if v in pick else ref_route)
        t = ref_path.index(w)
    out.extend(ref_path[t:])
    return out


def walks(g: VariationGraph) -> List[List[int]]:
    """Every path from the first to the last reference node, in sorted order."""
    source, sink = g.paths["ref"][0], g.paths["ref"][-1]
    out: List[List[int]] = []

    def go(path: List[int]) -> None:
        u = path[-1]
        if u == sink:
            out.append(list(path))
            return
        for w in g.succ[u]:
            path.append(w)
            go(path)
            path.pop()

    go([source])
    return sorted(out)


def find(g: VariationGraph, s: str) -> List[Tuple[int, int]]:
    """The places (node, offset) where s starts an exact match along some walk of the graph.

    A match may start in any node and cross edges. The search keeps the set of
    (start, node, offset) states that have matched a prefix of s.
    """
    if not s:
        return []
    states = {(i, k, i, k) for i, x in enumerate(g.seq) for k in range(len(x)) if x[k] == s[0]}  # @line L8
    for c in s[1:]:  # @line L9
        nxt = set()
        for si, sk, i, k in states:
            if k + 1 < len(g.seq[i]):  # @line L10
                steps = [(i, k + 1)]
            else:  # @line L11
                steps = [(w, 0) for w in g.succ[i]]
            for j, t in steps:
                if g.seq[j][t] == c:
                    nxt.add((si, sk, j, t))
        states = nxt
    return sorted({(si, sk) for si, sk, _, _ in states})  # @line L12
