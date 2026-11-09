# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/forward-checking/. The authors are listed in prov/346K9S.jsonl.

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


def forward_checking_search(
    domains: Sequence[Sequence[Value]],
    constraints: Constraints,
    all_solutions: bool = False,
) -> tuple[list[list[Value]], int]:
    """Forward checking on a binary CSP with the static order x_0, ..., x_{n-1}.

    domains[i] is the domain of x_i. constraints[(i, j)] is the set of allowed
    pairs (a, b) for (x_i, x_j). Returns (solutions, nodes): the first solution
    (or all solutions if all_solutions) and the number of assignments tried.
    Worst-case time O(n d^(n+1)) constraint checks; extra space O(n d).
    Iterative, so the depth of the search does not use the Python stack.
    """
    n = len(domains)
    if n == 0:
        return [[]], 0
    allowed = _allowed(n, constraints)
    later = [[j for j in allowed[i] if j > i] for i in range(n)]
    cd: list[list[Value]] = [list(dict.fromkeys(d)) for d in domains]  # @line L1
    pruned: list[list[tuple[int, Value]]] = [[] for _ in range(n)]
    untried: list[list[Value]] = [[] for _ in range(n)]
    sigma: list[Value] = [None] * n
    solutions: list[list[Value]] = []
    nodes = 0
    i = 0
    # The values of each level are tried in the order of the input domain.
    rank = [{a: k for k, a in enumerate(c)} for c in cd]
    untried[0] = sorted(cd[0], key=rank[0].__getitem__, reverse=True)
    while i >= 0:  # @line L2
        for j, b in pruned[i]:  # @line L3
            cd[j].append(b)
        pruned[i] = []
        if not untried[i]:  # @line L4
            i -= 1  # @line L5
        else:  # @line L6
            a = untried[i].pop()  # @line L7
            sigma[i] = a
            nodes += 1
            wiped = False
            for j in later[i]:  # @line L8
                rel = allowed[i][j]
                keep = []
                for b in cd[j]:
                    if (a, b) in rel:
                        keep.append(b)
                    else:
                        pruned[i].append((j, b))  # @line L9
                cd[j] = keep
                if not keep:
                    wiped = True
                    break
            if not wiped:  # @line L10
                if i == n - 1:  # @line L11
                    solutions.append(list(sigma))
                    if not all_solutions:
                        return solutions, nodes
                else:
                    i += 1  # @line L12
                    untried[i] = sorted(cd[i], key=rank[i].__getitem__, reverse=True)
    return solutions, nodes  # @line L13


def forward_checking(domains: Sequence[Sequence[Value]], constraints: Constraints) -> list[Value] | None:
    """Return one solution as a list of values, or None if there is none."""
    sols, _ = forward_checking_search(domains, constraints)
    return sols[0] if sols else None
