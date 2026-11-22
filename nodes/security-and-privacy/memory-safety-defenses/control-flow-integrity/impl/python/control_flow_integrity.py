# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/control-flow-integrity/. The authors are listed in prov/EYC3KG.jsonl.

"""Label-based control-flow integrity on an abstract control flow graph.

The model has no machine code and no real addresses. A branch site and a
target are hashable names, such as "s1" and "f". The allowed graph maps each
indirect branch site to the set of targets that the analysis allows for it.
The labels are kept in a separate object that the modeled program cannot
write, which models labels placed in non-writable code.
"""

from collections.abc import Hashable, Iterable, Mapping


class CFIViolation(Exception):
    """Raised by check when the target does not carry the label of the site."""

    def __init__(self, site: Hashable, target: Hashable) -> None:
        super().__init__(f"CFI violation at {site!r} to {target!r}")
        self.site = site
        self.target = target


class _UnionFind:
    """Disjoint sets over hashable keys, with path halving and union by size."""

    def __init__(self) -> None:
        self._parent: dict[Hashable, Hashable] = {}
        self._size: dict[Hashable, int] = {}

    def add(self, x: Hashable) -> None:
        if x not in self._parent:
            self._parent[x] = x
            self._size[x] = 1

    def find(self, x: Hashable) -> Hashable:
        p = self._parent
        while p[x] != x:
            p[x] = p[p[x]]
            x = p[x]
        return x

    def union(self, a: Hashable, b: Hashable) -> None:
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return
        if self._size[ra] < self._size[rb]:
            ra, rb = rb, ra
        self._parent[rb] = ra
        self._size[ra] += self._size[rb]


class CFILabels:
    """The labels of a CFI instrumentation, computed once from an allowed graph.

    Build cost: O((V + E) alpha(V)) for V sites and targets and E allowed
    edges, with a union-find. Each check costs O(1) expected time (two
    dictionary lookups). Precondition: allowed maps every indirect branch site
    of the program to a finite set of targets; the site and target names are
    disjoint or are tagged so that they cannot collide.
    """

    def __init__(self, allowed: Mapping[Hashable, Iterable[Hashable]]) -> None:
        edges = {s: frozenset(ts) for s, ts in allowed.items()}  # @line L1
        uf = _UnionFind()
        for s, ts in edges.items():  # @line L2
            uf.add(("site", s))  # @line L2
            for t in ts:  # @line L2
                uf.add(("target", t))  # @line L2
                uf.union(("site", s), ("target", t))  # @line L2
        names: dict[Hashable, int] = {}
        self._target_label: dict[Hashable, int] = {}
        self._site_label: dict[Hashable, int] = {}
        for s, ts in edges.items():
            for t in ts:
                root = uf.find(("target", t))  # @line L3
                label = names.setdefault(root, len(names))  # @line L3
                self._target_label[t] = label  # @line L4
        for s in edges:
            root = uf.find(("site", s))  # @line L3
            self._site_label[s] = names.setdefault(root, len(names))  # @line L5
        self._edges = edges

    def check(self, site: Hashable, target: Hashable) -> Hashable:
        """Return target if it carries the label of site, else raise CFIViolation."""
        expected = self._site_label.get(site)
        if expected is None or self._target_label.get(target) != expected:  # @line L6
            raise CFIViolation(site, target)  # @line L6
        return target  # @line L7

    def label_of_site(self, site: Hashable) -> int:
        return self._site_label[site]

    def label_of_target(self, target: Hashable) -> int | None:
        return self._target_label.get(target)

    def effective_targets(self, site: Hashable) -> frozenset[Hashable]:
        """The set of targets that check accepts for site."""
        lab = self._site_label[site]
        return frozenset(t for t, l in self._target_label.items() if l == lab)

    def number_of_labels(self) -> int:
        return len(set(self._site_label.values()) | set(self._target_label.values()))


def run_transfers(
    labels: CFILabels, transfers: Iterable[tuple[Hashable, Hashable]]
) -> tuple[list[Hashable], int | None]:
    """Run a sequence of indirect transfers (site, target) under the checks.

    Returns the targets reached before the first violation and the index of the
    violating transfer, or None if every transfer passes. O(1) expected time per
    transfer.
    """
    reached: list[Hashable] = []
    for i, (s, t) in enumerate(transfers):
        try:
            reached.append(labels.check(s, t))
        except CFIViolation:
            return reached, i
    return reached, None
