# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/maintaining-arc-consistency/. The authors are listed in prov/178PFC.jsonl.

from collections import deque
from collections.abc import Hashable, Mapping, Sequence

Value = Hashable
Constraints = Mapping[tuple[int, int], set[tuple[Value, Value]]]


def _allowed(n: int, constraints: Constraints) -> list[dict[int, set[tuple[Value, Value]]]]:
    """allowed[i][j] is the set of pairs (a, b) with x_i = a, x_j = b allowed.

    Two constraints on the same pair of variables are intersected.
    """
    allowed: list[dict[int, set[tuple[Value, Value]]]] = [{} for _ in range(n)]
    for (i, j), rel in constraints.items():
        if i == j:
            raise ValueError("a binary constraint needs two different variables")
        fwd = set(rel)
        bwd = {(b, a) for (a, b) in rel}
        allowed[i][j] = allowed[i][j] & fwd if j in allowed[i] else fwd
        allowed[j][i] = allowed[j][i] & bwd if i in allowed[j] else bwd
    return allowed


def _propagate(
    cd: list[list[Value]],
    allowed: list[dict[int, set[tuple[Value, Value]]]],
    queue: deque[tuple[int, int]],
    low: int,
    trail: list[tuple[int, Value]] | None,
) -> bool:
    """AC-3 on the arcs (j, k) with j >= low. Returns False on a wipe-out.

    Each removed pair (j, b) is appended to trail, if trail is given.
    """
    queued = set(queue)
    while queue:  # @line L10
        j, k = queue.popleft()  # @line L11
        queued.discard((j, k))
        rel = allowed[j][k]
        other = cd[k]
        keep = []
        for b in cd[j]:
            if any((b, c) in rel for c in other):
                keep.append(b)
            elif trail is not None:
                trail.append((j, b))
        if len(keep) == len(cd[j]):
            continue
        cd[j] = keep
        if not keep:  # @line L12
            return False
        for l in allowed[j]:
            if l >= low and l != k and (l, j) not in queued:
                queue.append((l, j))
                queued.add((l, j))
    return True


def maintaining_arc_consistency_search(
    domains: Sequence[Sequence[Value]],
    constraints: Constraints,
    all_solutions: bool = False,
) -> tuple[list[list[Value]], int]:
    """MAC on a binary CSP with the static order x_0, ..., x_{n-1}.

    domains[i] is the domain of x_i. constraints[(i, j)] is the set of allowed
    pairs (a, b) for (x_i, x_j). Returns (solutions, nodes): the first solution
    (or all solutions if all_solutions) and the number of assignments tried.
    After each assignment, AC-3 makes the future variables arc consistent.
    Iterative, so the depth of the search does not use the Python stack.
    """
    n = len(domains)
    if n == 0:
        return [[]], 0
    allowed = _allowed(n, constraints)
    cd: list[list[Value]] = [list(dict.fromkeys(d)) for d in domains]
    rank = [{a: k for k, a in enumerate(c)} for c in cd]
    arcs = deque((j, k) for j in range(n) for k in allowed[j])
    if any(not c for c in cd) or not _propagate(cd, allowed, arcs, 0, None):  # @line L1
        return [], 0
    pruned: list[list[tuple[int, Value]]] = [[] for _ in range(n)]
    untried: list[list[Value]] = [[] for _ in range(n)]
    sigma: list[Value] = [None] * n
    solutions: list[list[Value]] = []
    nodes = 0
    i = 0  # @line L2
    untried[0] = sorted(cd[0], key=rank[0].__getitem__, reverse=True)
    while i >= 0:  # @line L3
        for j, b in pruned[i]:  # @line L4
            cd[j].append(b)
        pruned[i] = []
        if not untried[i]:  # @line L5
            i -= 1  # @line L6
        else:  # @line L7
            a = untried[i].pop()  # @line L8
            sigma[i] = a
            nodes += 1
            pruned[i] = [(i, b) for b in cd[i] if b != a]
            cd[i] = [a]
            queue = deque((j, i) for j in allowed[i] if j > i)  # @line L9
            ok = _propagate(cd, allowed, queue, i + 1, pruned[i])
            if ok:  # @line L13
                if i == n - 1:  # @line L14
                    solutions.append(list(sigma))
                    if not all_solutions:
                        return solutions, nodes
                else:
                    i += 1  # @line L15
                    untried[i] = sorted(cd[i], key=rank[i].__getitem__, reverse=True)
    return solutions, nodes  # @line L16


def maintaining_arc_consistency(domains: Sequence[Sequence[Value]], constraints: Constraints) -> list[Value] | None:
    """Return one solution as a list of values, or None if there is none."""
    sols, _ = maintaining_arc_consistency_search(domains, constraints)
    return sols[0] if sols else None
