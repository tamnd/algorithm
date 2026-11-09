# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lazy-abstraction/. The authors are listed in prov/4S8GH7.jsonl.

"""Lazy abstraction with interpolants on a finite control-flow automaton.

A program is a dict with these keys:
  "values":   V, the data valuations are the ints 0 .. V - 1
  "init_loc": the start location
  "init":     the set of valuations at the start
  "error":    the error location
  "edges":    a list of (src, dst, rel), rel a dict from a valuation to the
              list of its successor valuations (a missing key blocks the edge)

Each location l has its own list of predicates, each a frozenset of
valuations. The abstract region of a node is the union of the cells of the
predicates at its location that meet the concrete post of its parent. A
spurious error path gives one interpolant per position, the set of
valuations from which the rest of the path can still run to the error. The
interpolant is added as a predicate only at its own location, and only the
subtree below the first node that it cuts is rebuilt.
"""

from typing import Dict, FrozenSet, List, Optional, Set

Region = FrozenSet[int]


class Node:
    __slots__ = ("loc", "region", "parent", "edge", "children", "expanded", "covered_by", "alive")

    def __init__(self, loc: int, region: Region, parent: Optional["Node"], edge: Optional[int]) -> None:
        self.loc, self.region, self.parent, self.edge = loc, region, parent, edge
        self.children: List[Node] = []
        self.expanded = False
        self.covered_by: Optional[Node] = None
        self.alive = True


class LazyAbstraction:
    def __init__(self, program) -> None:
        self.p = program
        self.V = program["values"]
        self.out: Dict[int, List[int]] = {}
        for i, (src, _, _) in enumerate(program["edges"]):
            self.out.setdefault(src, []).append(i)
        self.preds: Dict[int, List[Region]] = {}
        self.nodes: List[Node] = []
        self.covers: Dict[int, List[Node]] = {}
        self.refinements = 0

    def post(self, edge: int, region) -> Set[int]:
        rel = self.p["edges"][edge][2]
        return {w for v in region for w in rel.get(v, ())}

    def pre(self, edge: int, region) -> Set[int]:
        rel = self.p["edges"][edge][2]
        return {v for v, ws in rel.items() if any(w in region for w in ws)}

    def abstract(self, loc: int, concrete: Set[int]) -> Region:
        """The union of the predicate cells at loc that meet the concrete set."""
        preds = self.preds.get(loc, [])
        sig = lambda v: tuple(v in q for q in preds)
        cells = {sig(v) for v in concrete}
        return frozenset(v for v in range(self.V) if sig(v) in cells)

    def new_node(self, loc, region, parent, edge) -> Node:
        n = Node(loc, region, parent, edge)
        self.nodes.append(n)
        if parent is not None:
            parent.children.append(n)
        return n

    def find_cover(self, n: Node) -> Optional[Node]:
        for m in self.nodes:
            if m.alive and m.expanded and m.loc == n.loc and n.region <= m.region:
                return m
        return None

    def path_to(self, n: Node) -> List[Node]:
        path = []
        while n is not None:
            path.append(n)
            n = n.parent
        return path[::-1]

    def refine(self, err: Node, work: List[Node]):
        """Check the error path; return a concrete trace, or refine and return None."""
        path = self.path_to(err)
        edges = [m.edge for m in path[1:]]
        sets = [set(self.p["init"])]
        for e in edges:
            sets.append(self.post(e, sets[-1]))
        if sets[-1]:  # @line L6
            trace = [min(sets[-1])]
            for i in range(len(edges) - 1, -1, -1):
                rel = self.p["edges"][edges[i]][2]
                trace.append(min(v for v in sets[i] if trace[-1] in rel.get(v, ())))
            vals = trace[::-1]
            return [(m.loc, v) for m, v in zip(path, vals)]
        # Interpolants: bad[i] = valuations from which edges i+1 .. k can still run.
        bad = [frozenset()] * len(path)
        bad[-1] = frozenset(range(self.V))
        for i in range(len(path) - 2, -1, -1):
            bad[i] = frozenset(self.pre(edges[i], bad[i + 1]))
        for m, q in zip(path, bad):  # @line L7
            if 0 < len(q) < self.V and q not in self.preds.setdefault(m.loc, []):
                self.preds[m.loc].append(q)
        pivot = next(i for i, m in enumerate(path) if m.region & bad[i])
        self.rebuild(path[pivot], work)  # @line L8
        self.refinements += 1
        return None

    def rebuild(self, piv: Node, work: List[Node]) -> None:
        stack = list(piv.children)
        removed = [piv]
        while stack:
            d = stack.pop()
            d.alive = False
            removed.append(d)
            stack.extend(d.children)
        for d in removed:
            for c in self.covers.pop(id(d), []):
                if c.alive and c.covered_by is d:
                    c.covered_by = None
                    work.append(c)
        piv.children, piv.expanded, piv.covered_by = [], False, None
        if piv.parent is None:
            piv.region = self.abstract(piv.loc, set(self.p["init"]))
        else:
            piv.region = self.abstract(piv.loc, self.post(piv.edge, piv.parent.region))
        work.append(piv)

    def run(self):
        p = self.p
        root = self.new_node(p["init_loc"], self.abstract(p["init_loc"], set(p["init"])), None, None)  # @line L1
        work = [root]
        while work:  # @line L2
            n = work.pop()  # @line L3
            if not n.alive or n.expanded or n.covered_by is not None or not n.region:  # @line L4
                continue
            if n.loc == p["error"]:  # @line L5
                trace = self.refine(n, work)
                if trace is not None:
                    return "unsafe", trace
                continue
            m = self.find_cover(n)  # @line L9
            if m is not None:
                n.covered_by = m
                self.covers.setdefault(id(m), []).append(n)
                continue
            n.expanded = True
            for e in self.out.get(n.loc, []):  # @line L10
                dst = p["edges"][e][1]
                work.append(self.new_node(dst, self.abstract(dst, self.post(e, n.region)), n, e))
        return "safe", self.invariant()  # @line L11

    def invariant(self) -> Dict[int, Region]:
        """The union of the regions of the live nodes at each location."""
        inv: Dict[int, Set[int]] = {}
        for n in self.nodes:
            if n.alive:
                inv.setdefault(n.loc, set()).update(n.region)
        return {l: frozenset(r) for l, r in inv.items()}


def lazy_abstraction(program):
    """Returns ("safe", invariant) or ("unsafe", trace of (location, valuation))."""
    return LazyAbstraction(program).run()
