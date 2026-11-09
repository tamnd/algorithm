# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/conflict-directed-backjumping/. The authors are listed in prov/7XCRR6.jsonl.

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


def conflict_directed_backjumping_search(
    domains: Sequence[Sequence[Value]],
    constraints: Constraints,
    all_solutions: bool = False,
) -> tuple[list[list[Value]], int]:
    """Prosser's conflict-directed backjumping (BT-CBJ) with the order x_0, ..., x_{n-1}.

    domains[i] is the domain of x_i. constraints[(i, j)] is the set of allowed
    pairs (a, b) for (x_i, x_j). Returns (solutions, nodes): the first solution
    (or all solutions if all_solutions) and the number of assignments tried.
    Each value of x_i is checked against x_0, x_1, ... in order, and the first
    variable it conflicts with goes into the conflict set of x_i. At a dead
    end the search jumps to the latest variable of the conflict set.
    """
    n = len(domains)
    if n == 0:
        return [[]], 0
    allowed = _allowed(n, constraints)
    earlier = [sorted(j for j in allowed[i] if j < i) for i in range(n)]
    doms = [list(dict.fromkeys(d)) for d in domains]
    cd: list[list[Value]] = [[] for _ in range(n)]
    cs: list[set[int]] = [set() for _ in range(n)]
    sigma: list[Value] = [None] * n
    solutions: list[list[Value]] = []
    nodes = 0
    i = 0  # @line L1
    cd[0] = doms[0][::-1]
    while True:  # @line L2
        if not cd[i]:  # @line L3
            if not cs[i]:  # @line L4
                return solutions, nodes
            h = max(cs[i])  # @line L5
            cs[h] |= cs[i]  # @line L6
            cs[h].discard(h)
            i = h  # @line L7
        else:  # @line L8
            a = cd[i].pop()  # @line L9
            sigma[i] = a
            nodes += 1
            h = -1  # @line L10
            for j in earlier[i]:
                if (sigma[j], a) not in allowed[j][i]:
                    h = j
                    break
            if h < 0:  # @line L11
                if i == n - 1:  # @line L12
                    solutions.append(list(sigma))
                    if not all_solutions:
                        return solutions, nodes
                    # Every earlier variable is now part of the reason to go on.
                    cs[i] = set(range(i))
                else:
                    i += 1  # @line L13
                    cd[i] = doms[i][::-1]
                    cs[i] = set()
            else:
                cs[i].add(h)  # @line L14


def conflict_directed_backjumping(domains: Sequence[Sequence[Value]], constraints: Constraints) -> list[Value] | None:
    """Return one solution as a list of values, or None if there is none."""
    sols, _ = conflict_directed_backjumping_search(domains, constraints)
    return sols[0] if sols else None
