# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dynamic-backtracking/. The authors are listed in prov/KDGJJC.jsonl.

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


def dynamic_backtracking_search(
    domains: Sequence[Sequence[Value]],
    constraints: Constraints,
    all_solutions: bool = False,
) -> tuple[list[list[Value]], dict[str, int]]:
    """Ginsberg's dynamic backtracking on a binary CSP.

    domains[i] is the domain of x_i. constraints[(i, j)] is the set of allowed
    pairs (a, b) for (x_i, x_j). Returns (solutions, stats): the first
    solution (or all solutions if all_solutions) and a dict with the number
    of assignments ("nodes") and the largest number of eliminations stored at
    one time ("max_eliminations", never more than the total domain size).

    The search keeps, for each eliminated value (x, b), an explanation: a set
    of assigned variables whose current values rule out x = b. At a dead end
    it unassigns only the latest variable y of the union of the explanations
    and keeps every other assignment. Explanations that mention y are erased.
    """
    n = len(domains)
    if n == 0:
        return [[]], {"nodes": 0, "max_eliminations": 0}
    allowed = _allowed(n, constraints)
    doms = [list(dict.fromkeys(d)) for d in domains]
    order: list[int] = []  # @line L1
    pos = [-1] * n  # position of each variable in order, -1 if unassigned
    sigma: list[Value] = [None] * n
    elim: list[dict[Value, frozenset[int]]] = [{} for _ in range(n)]
    solutions: list[list[Value]] = []
    nodes = 0
    stored = 0
    max_stored = 0

    def unassign_latest(culprits: frozenset[int]) -> bool:
        """Lines L9 to L13: undo the latest variable of culprits. False means failure."""
        nonlocal stored
        if not culprits:  # @line L9
            return False
        y = max(culprits, key=pos.__getitem__)  # @line L10
        old = sigma[y]
        p = pos[y]
        order.pop(p)  # @line L11
        for k in range(p, len(order)):
            pos[order[k]] = k
        pos[y] = -1
        sigma[y] = None
        for z in range(n):  # @line L12
            dead = [b for b, why in elim[z].items() if y in why]
            for b in dead:
                del elim[z][b]
            stored -= len(dead)
        elim[y][old] = culprits - {y}  # @line L13
        stored += 1
        return True

    while True:  # @line L2
        if len(order) == n:
            solutions.append(list(sigma))
            if not all_solutions:
                break
            # Rule out this solution: the explanation is every other assigned variable.
            if not unassign_latest(frozenset(order)):
                break
            max_stored = max(max_stored, stored)
            continue
        x = pos.index(-1)  # @line L3
        for b in doms[x]:  # @line L4
            if b in elim[x]:
                continue
            for y in order:
                if x in allowed[y] and (sigma[y], b) not in allowed[y][x]:
                    elim[x][b] = frozenset((y,))
                    stored += 1
                    break
        max_stored = max(max_stored, stored)
        free = [b for b in doms[x] if b not in elim[x]]
        if free:  # @line L5
            sigma[x] = free[0]  # @line L6
            pos[x] = len(order)
            order.append(x)
            nodes += 1
        else:  # @line L7
            union: frozenset[int] = frozenset().union(*elim[x].values())  # @line L8
            if not unassign_latest(union):
                break
            max_stored = max(max_stored, stored)
    return solutions, {"nodes": nodes, "max_eliminations": max_stored}  # @line L14


def dynamic_backtracking(domains: Sequence[Sequence[Value]], constraints: Constraints) -> list[Value] | None:
    """Return one solution as a list of values, or None if there is none."""
    sols, _ = dynamic_backtracking_search(domains, constraints)
    return sols[0] if sols else None
