# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/graph-based-backjumping/. The authors are listed in prov/F25KS3.jsonl.

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


def graph_based_backjumping_search(
    domains: Sequence[Sequence[Value]],
    constraints: Constraints,
    all_solutions: bool = False,
) -> tuple[list[list[Value]], int]:
    """Dechter's graph-based backjumping with the order x_0, ..., x_{n-1}.

    domains[i] is the domain of x_i. constraints[(i, j)] is the set of allowed
    pairs (a, b) for (x_i, x_j). Returns (solutions, nodes): the first solution
    (or all solutions if all_solutions) and the number of assignments tried.
    The jump set of x_i starts as its earlier neighbours in the constraint
    graph. At a dead end the search jumps to the latest variable of the jump
    set, and that variable inherits the rest of the set.
    """
    n = len(domains)
    if n == 0:
        return [[]], 0
    allowed = _allowed(n, constraints)
    earlier = [sorted(j for j in allowed[i] if j < i) for i in range(n)]
    doms = [list(dict.fromkeys(d)) for d in domains]
    cd: list[list[Value]] = [[] for _ in range(n)]
    jump: list[set[int]] = [set() for _ in range(n)]
    sigma: list[Value] = [None] * n
    solutions: list[list[Value]] = []
    nodes = 0
    i = 0  # @line L1
    cd[0] = doms[0][::-1]
    while True:  # @line L2
        if not cd[i]:  # @line L3
            if not jump[i]:  # @line L4
                return solutions, nodes
            h = max(jump[i])  # @line L5
            jump[h] |= jump[i]  # @line L6
            jump[h].discard(h)
            i = h  # @line L7
        else:  # @line L8
            a = cd[i].pop()  # @line L9
            sigma[i] = a
            nodes += 1
            if all((sigma[j], a) in allowed[j][i] for j in earlier[i]):  # @line L10
                if i == n - 1:  # @line L11
                    solutions.append(list(sigma))
                    if not all_solutions:
                        return solutions, nodes
                    # After a solution, every earlier variable is a reason to go on.
                    jump[i] = set(range(i))
                else:
                    i += 1  # @line L12
                    cd[i] = doms[i][::-1]
                    jump[i] = set(earlier[i])


def graph_based_backjumping(domains: Sequence[Sequence[Value]], constraints: Constraints) -> list[Value] | None:
    """Return one solution as a list of values, or None if there is none."""
    sols, _ = graph_based_backjumping_search(domains, constraints)
    return sols[0] if sols else None
