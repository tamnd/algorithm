# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/min-conflicts/. The authors are listed in prov/P8QYS3.jsonl.

import random
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


def min_conflicts(
    domains: Sequence[Sequence[Value]],
    constraints: Constraints,
    max_steps: int = 10_000,
    seed: int = 0,
    initial: Sequence[Value] | None = None,
) -> tuple[list[Value] | None, int]:
    """Min-conflicts local search on a binary CSP.

    domains[i] is the domain of x_i. constraints[(i, j)] is the set of allowed
    pairs (a, b) for (x_i, x_j). Starts from initial (or a random complete
    assignment), then repeatedly picks a random conflicted variable and gives
    it a value with the fewest conflicts, ties broken at random.
    Returns (solution, steps) or (None, max_steps). The method is incomplete:
    None does not mean that there is no solution.
    """
    n = len(domains)
    if any(len(d) == 0 for d in domains):
        return None, 0
    rng = random.Random(seed)
    allowed = _allowed(n, constraints)
    doms = [list(dict.fromkeys(d)) for d in domains]
    if initial is None:  # @line L1
        sigma = [rng.choice(d) for d in doms]
    else:
        sigma = list(initial)

    def conflicts(x: int, v: Value) -> int:
        return sum(1 for y, rel in allowed[x].items() if (v, sigma[y]) not in rel)

    count = [conflicts(x, sigma[x]) for x in range(n)]
    # The conflicted variables, in a list with positions for O(1) random choice.
    bad: list[int] = [x for x in range(n) if count[x] > 0]
    where = {x: k for k, x in enumerate(bad)}

    def mark(x: int) -> None:
        if count[x] > 0 and x not in where:
            where[x] = len(bad)
            bad.append(x)
        elif count[x] == 0 and x in where:
            k = where.pop(x)
            last = bad.pop()
            if last != x:
                bad[k] = last
                where[last] = k

    for step in range(max_steps):  # @line L2
        if not bad:  # @line L3
            return sigma, step
        x = rng.choice(bad)  # @line L4
        scores = [conflicts(x, v) for v in doms[x]]  # @line L5
        best = min(scores)
        v = rng.choice([w for w, s in zip(doms[x], scores) if s == best])
        old = sigma[x]
        if v == old:
            continue
        sigma[x] = v  # @line L6
        for y, rel in allowed[x].items():
            was = (old, sigma[y]) not in rel
            now = (v, sigma[y]) not in rel
            if was != now:
                count[y] += 1 if now else -1
                mark(y)
        count[x] = best
        mark(x)
    if not bad:
        return sigma, max_steps
    return None, max_steps  # @line L7
