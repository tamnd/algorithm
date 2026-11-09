# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cutset-conditioning/. The authors are listed in prov/T6CQTJ.jsonl.

"""Cutset conditioning (Dechter 1990) for binary CSPs.

A binary CSP has the variables 0 .. n-1. domains[i] is an iterable of the
values of variable i. constraints maps a pair (i, j), i != j, to the set of
allowed pairs (a, b), meaning x_i = a and x_j = b. A cycle cutset is a set of
variables whose removal leaves a constraint graph with no cycle.
"""

import itertools
from collections import deque
from collections.abc import Iterable, Mapping, Sequence

Constraints = Mapping[tuple[int, int], Iterable[tuple[int, int]]]
Rel = dict[tuple[int, int], set[tuple[int, int]]]


def directed(constraints: Constraints) -> Rel:
    """Return the relation R_ij of each arc (i, j), for both directions."""
    rel: Rel = {}
    for (i, j), pairs in constraints.items():
        if i == j:
            raise ValueError("a binary constraint needs two different variables")
        fwd = set(pairs)
        bwd = {(b, a) for a, b in fwd}
        rel[(i, j)] = rel[(i, j)] & fwd if (i, j) in rel else fwd
        rel[(j, i)] = rel[(j, i)] & bwd if (j, i) in rel else bwd
    return rel


def find_cycle_cutset(n: int, constraints: Constraints) -> list[int]:
    """Return a cycle cutset, chosen greedily; it need not be the smallest one.

    Delete vertices of degree at most 1 while there are any. If vertices remain,
    they all lie on cycles: move one of largest degree to the cutset and repeat.
    """
    nbrs: list[set[int]] = [set() for _ in range(n)]
    for i, j in constraints:
        nbrs[i].add(j)
        nbrs[j].add(i)
    alive = set(range(n))
    cutset: list[int] = []

    def delete(v: int) -> None:
        alive.discard(v)
        for w in nbrs[v]:
            nbrs[w].discard(v)

    while True:
        low = deque(v for v in alive if len(nbrs[v]) <= 1)
        while low:
            v = low.popleft()
            if v not in alive:
                continue
            others = list(nbrs[v])
            delete(v)
            low.extend(w for w in others if len(nbrs[w]) <= 1)
        if not alive:
            return sorted(cutset)
        v = max(sorted(alive), key=lambda u: len(nbrs[u]))
        cutset.append(v)
        delete(v)


def _forest(variables: Sequence[int], rel: Rel) -> tuple[list[int], dict[int, int]]:
    """Breadth-first order and parents of the forest on the given variables."""
    inside = set(variables)
    nbrs: dict[int, list[int]] = {v: [] for v in variables}
    for i, j in rel:
        if i in inside and j in inside:
            nbrs[i].append(j)
    parent: dict[int, int] = {}
    order: list[int] = []
    for root in variables:
        if root in parent:
            continue
        parent[root] = -1
        queue = deque([root])
        while queue:
            v = queue.popleft()
            order.append(v)
            for w in nbrs[v]:
                if w == parent[v]:
                    continue
                if w in parent:
                    raise ValueError("the variables outside the cutset do not form a forest")
                parent[w] = v
                queue.append(w)
    return order, parent


def _tree_count(order: list[int], parent: dict[int, int], dom: dict[int, set[int]],
                rel: Rel, want_solution: bool) -> tuple[int, dict[int, int] | None]:
    """Count the solutions of the forest, and give one when asked; O(n d^2)."""
    children: dict[int, list[int]] = {v: [] for v in order}
    for v in order:
        if parent[v] >= 0:
            children[parent[v]].append(v)
    ways: dict[int, dict[int, int]] = {}
    for v in reversed(order):
        ways[v] = {}
        for a in dom[v]:
            w = 1
            for c in children[v]:
                r = rel[(v, c)]
                w *= sum(ways[c][b] for b in dom[c] if (a, b) in r)
                if w == 0:
                    break
            ways[v][a] = w
    total = 1
    for v in order:
        if parent[v] < 0:
            total *= sum(ways[v].values())
    if not want_solution or total == 0:
        return total, None
    value: dict[int, int] = {}
    for v in order:
        p = parent[v]
        cands = sorted(dom[v])
        if p >= 0:
            cands = [b for b in cands if (value[p], b) in rel[(p, v)]]
        value[v] = next(b for b in cands if ways[v][b] > 0)
    return total, value


def _conditioned(domains: Iterable[Iterable[int]], constraints: Constraints,
                 cutset: Sequence[int] | None, want_solution: bool) -> tuple[int, list[int] | None]:
    dom = [set(d) for d in domains]
    n = len(dom)
    rel = directed(constraints)
    if cutset is None:
        cutset = find_cycle_cutset(n, constraints)
    cut = list(cutset)
    in_cut = set(cut)
    rest = [v for v in range(n) if v not in in_cut]
    order, parent = _forest(rest, rel)
    total = 0
    for s in itertools.product(*[sorted(dom[x]) for x in cut]):  # @line L1
        val = dict(zip(cut, s))
        if any((val[i], val[j]) not in r for (i, j), r in rel.items()
               if i in in_cut and j in in_cut):  # @line L2
            continue
        sub = {}
        for y in rest:  # @line L3
            sub[y] = {b for b in dom[y]
                      if all((val[x], b) in rel[(x, y)] for x in cut if (x, y) in rel)}  # @line L4
        count, tree = _tree_count(order, parent, sub, rel, want_solution)  # @line L5
        total += count
        if want_solution and tree is not None:  # @line L6
            val.update(tree)
            return total, [val[v] for v in range(n)]
    return total, None  # @line L7


def cutset_solve(domains: Iterable[Iterable[int]], constraints: Constraints,
                 cutset: Sequence[int] | None = None) -> list[int] | None:
    """Return a solution, or None if there is none."""
    return _conditioned(domains, constraints, cutset, True)[1]


def cutset_count(domains: Iterable[Iterable[int]], constraints: Constraints,
                 cutset: Sequence[int] | None = None) -> int:
    """Return the number of solutions."""
    return _conditioned(domains, constraints, cutset, False)[0]
