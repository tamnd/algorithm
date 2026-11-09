# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/maximum-csp/. The authors are listed in prov/75TMKH.jsonl.

"""Weighted Max-CSP by depth-first branch and bound.

domains[i] is the list of values of variable i. constraints maps a pair
(i, j) with i < j to the set of allowed pairs (a, b). weights maps the same
pairs to a positive weight (default 1). The cost of a complete assignment is
the total weight of the constraints it violates; Max-CSP asks for the
smallest cost, which is the same as the largest weight of satisfied
constraints.

Variables are assigned in the order 0, 1, ..., n-1. At a node with
x_0 .. x_{k-1} assigned, the lower bound is

    g + sum over unassigned j of min over b in D(j) of ic(j, b),

where g is the weight of the violated constraints among assigned variables
and ic(j, b) is the weight of the constraints between j and an assigned
variable that x_j = b would violate. This is the bound of partial forward
checking (Freuder and Wallace 1992). Each constraint is counted at most once,
so the bound never exceeds the cost of a completion. With use_ic=False the
bound is g alone, which is plain branch and bound.
"""

import itertools

Pair = tuple[int, int]


def _cost(assign: list, constraints: dict[Pair, set], weights: dict[Pair, int]) -> int:
    return sum(weights.get(p, 1) for p, rel in constraints.items() if (assign[p[0]], assign[p[1]]) not in rel)


def max_csp_branch_and_bound(
    domains: list[list],
    constraints: dict[Pair, set],
    weights: dict[Pair, int] | None = None,
    use_ic: bool = True,
) -> tuple[int, list | None, int]:
    """Return (best cost, an optimal assignment, number of value assignments tried)."""
    n = len(domains)
    weights = weights or {}
    if any(not d for d in domains):
        return 0, None, 0
    nbr: list[list[tuple[int, Pair]]] = [[] for _ in range(n)]
    for i, j in constraints:
        nbr[i].append((j, (i, j)))
        nbr[j].append((i, (i, j)))
    # ic[j][b]: weight that x_j = b violates with the assigned variables.
    ic = [{b: 0 for b in domains[j]} for j in range(n)]
    best_cost = sum(weights.get(p, 1) for p in constraints) + 1
    best: list | None = None
    assign: list = [None] * n
    nodes = 0

    def bound(k: int, g: int) -> int:
        if not use_ic:
            return g
        return g + sum(min(ic[j].values()) for j in range(k, n))

    def change(k: int, a, sign: int) -> None:
        # Add (sign = 1) or remove (sign = -1) the effect of x_k = a on ic.
        for j, p in nbr[k]:
            if j > k:
                w = weights.get(p, 1)
                rel = constraints[p]
                for b in domains[j]:
                    pair = (a, b) if p[0] == k else (b, a)
                    if pair not in rel:
                        ic[j][b] += sign * w

    # Explicit stack of (level, index of the next value to try, g at this level).
    stack: list[list] = [[0, 0, 0]]
    while stack:
        top = stack[-1]
        k, idx, g = top
        if k == n:
            if g < best_cost:
                best_cost, best = g, list(assign)
            stack.pop()
            continue
        if idx > 0:
            change(k, assign[k], -1)  # undo the previous value of x_k
            assign[k] = None
        if idx == len(domains[k]):
            stack.pop()
            continue
        a = domains[k][idx]
        top[1] = idx + 1
        nodes += 1
        g2 = g + ic[k][a]
        assign[k] = a
        change(k, a, 1)
        if bound(k + 1, g2) < best_cost:
            stack.append([k + 1, 0, g2])
    return best_cost, best, nodes


def brute_force(domains: list[list], constraints: dict[Pair, set], weights: dict[Pair, int] | None = None) -> int | None:
    """The smallest cost over all d^n assignments, or None if a domain is empty."""
    weights = weights or {}
    costs = [_cost(list(t), constraints, weights) for t in itertools.product(*domains)]
    return min(costs) if costs else None
