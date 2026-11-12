# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ancestral-recombination-graph/. The authors are listed in prov/NNH0F8.jsonl.

"""An ancestral recombination graph (ARG) with ancestral material on its edges.

The sequence is the interval [0, 1). A node is a sample (time 0), a coalescence
(two children, one parent) or a recombination (one child, two parents). A
recombination node with breakpoint b sends the material in [0, b) to its left
parent and the material in [b, 1) to its right parent.

A lineage is a pair (node, slot). Slot 0 is the only edge above a sample or a
coalescence node. Slot 0 and slot 1 are the left and right edges above a
recombination node. Each lineage carries its ancestral material: a sorted list
of disjoint half-open intervals (l, r) of positions at which the lineage is an
ancestor of some sample and the most recent common ancestor of the sample at
that position is not yet reached.

simulate() is Hudson's algorithm for the coalescent with recombination. Time is
in coalescent units, in which each pair of lineages coalesces at rate 1. rho is
the population recombination rate for the whole interval (rho = 4Nr in a diploid
population of size N with recombination probability r per generation), so a
lineage whose material spans a length s recombines at rate rho * s / 2. Only
lineages that carry material are kept.
"""

import random
from typing import Dict, FrozenSet, List, NamedTuple, Optional, Sequence, Set, Tuple

Interval = Tuple[float, float]
Material = Tuple[Interval, ...]
Lineage = Tuple[int, int]

SAMPLE, COALESCENCE, RECOMBINATION = "sample", "coalescence", "recombination"


# ---------- interval lists ----------

def _norm(iv: Sequence[Interval]) -> Material:
    out: List[Interval] = []
    for l, r in sorted(iv):
        if r <= l:
            continue
        if out and l <= out[-1][1]:
            out[-1] = (out[-1][0], max(out[-1][1], r))
        else:
            out.append((l, r))
    return tuple(out)


def union(a: Material, b: Material) -> Material:
    return _norm(list(a) + list(b))


def intersect(a: Material, b: Material) -> Material:
    out = []
    i = j = 0
    while i < len(a) and j < len(b):
        l, r = max(a[i][0], b[j][0]), min(a[i][1], b[j][1])
        if l < r:
            out.append((l, r))
        if a[i][1] < b[j][1]:
            i += 1
        else:
            j += 1
    return tuple(out)


def difference(a: Material, b: Material) -> Material:
    out = []
    for l, r in a:
        cur = l
        for bl, br in b:
            if br <= cur or bl >= r:
                continue
            if bl > cur:
                out.append((cur, bl))
            cur = max(cur, br)
        if cur < r:
            out.append((cur, r))
    return _norm(out)


def covers(a: Material, x: float) -> bool:
    return any(l <= x < r for l, r in a)


# ---------- the graph ----------

class LocalTree(NamedTuple):
    mrca: int
    tmrca: float
    parent: Dict[int, int]                 # tree node -> tree parent, the MRCA is absent
    clusters: FrozenSet[FrozenSet[int]]    # leaf sets of the tree nodes, as sample ids
    nodes: FrozenSet[int]                  # the ARG nodes of the tree, which fix its branch lengths


class ARG:
    def __init__(self) -> None:
        self.time: List[float] = []
        self.kind: List[str] = []
        self.children: List[List[Lineage]] = []
        self.parents: List[List[Optional[int]]] = []
        self.breakpoint: List[Optional[float]] = []
        self.material: Dict[Lineage, Material] = {}
        self.samples: List[int] = []

    def _new(self, t: float, kind: str, slots: int) -> int:
        v = len(self.time)
        self.time.append(t)
        self.kind.append(kind)
        self.children.append([])
        self.parents.append([None] * slots)
        self.breakpoint.append(None)
        return v

    def add_sample(self, material: Material = ((0.0, 1.0),)) -> Lineage:
        v = self._new(0.0, SAMPLE, 1)
        self.samples.append(v)
        self.material[(v, 0)] = _norm(material)
        return (v, 0)

    def coalesce(self, a: Lineage, b: Lineage, t: float, keep: Optional[Material] = None) -> Lineage:
        """Join lineages a and b at time t. The new lineage carries keep (default: all their material)."""
        if a == b or self.parents[a[0]][a[1]] is not None or self.parents[b[0]][b[1]] is not None:
            raise ValueError("a and b must be two open lineages")
        if t < max(self.time[a[0]], self.time[b[0]]):
            raise ValueError("time must not go backward")
        w = self._new(t, COALESCENCE, 1)
        self.children[w] = [a, b]
        self.parents[a[0]][a[1]] = w
        self.parents[b[0]][b[1]] = w
        merged = union(self.material[a], self.material[b])
        self.material[(w, 0)] = merged if keep is None else _norm(keep)
        return (w, 0)

    def recombine(self, a: Lineage, x: float, t: float) -> Tuple[Lineage, Lineage]:
        """Split lineage a at breakpoint x at time t. Returns the left lineage, then the right one."""
        if self.parents[a[0]][a[1]] is not None:
            raise ValueError("a must be an open lineage")
        if t < self.time[a[0]]:
            raise ValueError("time must not go backward")
        r = self._new(t, RECOMBINATION, 2)
        self.children[r] = [a]
        self.parents[a[0]][a[1]] = r
        self.breakpoint[r] = x
        m = self.material[a]
        self.material[(r, 0)] = intersect(m, ((0.0, x),))
        self.material[(r, 1)] = intersect(m, ((x, 1.0),))
        return (r, 0), (r, 1)

    def num_recombinations(self) -> int:
        return sum(1 for k in self.kind if k == RECOMBINATION)

    # ----- local trees -----

    def _path(self, s: int, x: float) -> List[int]:
        """The nodes above sample s on the lineage of position x, by the breakpoints."""
        path = [s]
        v, slot = s, 0
        while True:
            p = self.parents[v][slot]
            if p is None:
                return path
            path.append(p)
            v = p
            bp = self.breakpoint[p]
            slot = 0 if bp is None or x < bp else 1

    def local_tree(self, x: float) -> LocalTree:
        """The marginal tree at position x: follow each sample upward, taking the left or right
        parent at each recombination node by its breakpoint. A coalescence node is a node of the
        tree when the paths use both of its child edges. The MRCA is the lowest node on all paths."""
        paths = {s: self._path(s, x) for s in self.samples}
        below: Dict[int, Set[int]] = {}
        used: Set[Lineage] = set()
        for s, p in paths.items():
            for v in p:
                below.setdefault(v, set()).add(s)
            for u, v in zip(p, p[1:]):
                bp = self.breakpoint[u]
                used.add((u, 0 if bp is None or x < bp else 1))
        n = len(self.samples)
        common = [v for v, S in below.items() if len(S) == n]
        if not common:
            raise ValueError("the samples have no common ancestor at x")
        mrca = min(common, key=lambda v: (self.time[v], v))
        tree_nodes = set(self.samples)
        for v in below:
            if self.kind[v] == COALESCENCE and all(c in used for c in self.children[v]):
                tree_nodes.add(v)
        parent: Dict[int, int] = {}
        for s, p in paths.items():
            prev = s
            for v in p[1:]:
                if v in tree_nodes:
                    parent[prev] = v
                    prev = v
                if v == mrca:
                    break
        clusters = frozenset(frozenset(below[v]) for v in tree_nodes)
        return LocalTree(mrca, self.time[mrca], parent, clusters, frozenset(tree_nodes))

    def local_tree_by_material(self, x: float) -> FrozenSet[FrozenSet[int]]:
        """The same tree from the material: its internal nodes are the coalescence nodes
        whose two child edges both carry x."""
        memo: Dict[int, FrozenSet[int]] = {}
        out: Set[FrozenSet[int]] = set()
        order = sorted(range(len(self.time)), key=lambda v: (self.time[v], v))
        for v in order:
            if self.kind[v] == SAMPLE:
                memo[v] = frozenset([v])
                out.add(memo[v])
                continue
            S: Set[int] = set()
            for c in self.children[v]:
                if covers(self.material[c], x):
                    S |= memo.get(c[0], frozenset())
            memo[v] = frozenset(S)
            carried = [c for c in self.children[v] if covers(self.material[c], x)]
            if self.kind[v] == COALESCENCE and len(carried) == 2:
                out.add(memo[v])
        return frozenset(out)

    def breakpoints(self) -> List[float]:
        return sorted(b for b in self.breakpoint if b is not None)

    def local_trees(self) -> List[Tuple[float, float, LocalTree]]:
        """The marginal genealogies along the sequence: (l, r, tree) for each maximal interval
        [l, r) on which the tree, with its branch lengths, stays the same. Trees change only at
        breakpoints, so one tree per gap between breakpoints is enough."""
        cuts = sorted(set([0.0] + [b for b in self.breakpoints() if 0.0 < b < 1.0] + [1.0]))
        out: List[Tuple[float, float, LocalTree]] = []
        for l, r in zip(cuts, cuts[1:]):
            t = self.local_tree((l + r) / 2)
            if out and out[-1][2].nodes == t.nodes:
                out[-1] = (out[-1][0], r, out[-1][2])
            else:
                out.append((l, r, t))
        return out

    def topologies(self) -> List[Tuple[float, float, FrozenSet[FrozenSet[int]]]]:
        """As local_trees, but merging neighbours with the same shape (the same clusters)."""
        out: List[Tuple[float, float, FrozenSet[FrozenSet[int]]]] = []
        for l, r, t in self.local_trees():
            if out and out[-1][2] == t.clusters:
                out[-1] = (out[-1][0], r, t.clusters)
            else:
                out.append((l, r, t.clusters))
        return out


# ---------- Hudson's algorithm ----------

def simulate(n: int, rho: float, rng: random.Random) -> ARG:
    """The coalescent with recombination for n samples, backward in time (Hudson 1983)."""
    arg = ARG()
    live: List[Lineage] = [arg.add_sample() for _ in range(n)]  # @line L1
    if n < 2:
        return arg
    t = 0.0
    while live:  # @line L2
        k = len(live)
        spans = [arg.material[a][-1][1] - arg.material[a][0][0] for a in live]
        coal = k * (k - 1) / 2.0
        rec = rho / 2.0 * sum(spans)  # @line L3
        t += rng.expovariate(coal + rec)  # @line L4
        if rng.random() * (coal + rec) < rec:  # @line L5
            u = rng.random() * sum(spans)
            while u == 0.0:
                u = rng.random() * sum(spans)
            i = 0
            while u >= spans[i] and i < k - 1:
                u -= spans[i]
                i += 1
            lo = arg.material[live[i]][0][0]
            x = lo + u  # @line L6
            left, right = arg.recombine(live[i], x, t)  # @line L7
            live[i:i + 1] = [left, right]
        else:
            i, j = rng.sample(range(k), 2)  # @line L8
            a, b = live[i], live[j]
            rest = [c for q, c in enumerate(live) if q not in (i, j)]
            others: Material = ()
            for c in rest:
                others = union(others, arg.material[c])
            both = intersect(arg.material[a], arg.material[b])
            done = difference(both, others)  # @line L9
            keep = difference(union(arg.material[a], arg.material[b]), done)
            w = arg.coalesce(a, b, t, keep)  # @line L10
            live = rest + ([w] if keep else [])  # @line L11
    return arg
