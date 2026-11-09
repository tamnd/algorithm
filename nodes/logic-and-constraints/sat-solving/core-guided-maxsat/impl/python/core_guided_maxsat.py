# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/core-guided-maxsat/. The authors are listed in prov/D7BD01.jsonl.

"""The Fu-Malik core-guided algorithm for partial MaxSAT (Fu and Malik 2006).

Clauses are DIMACS-style lists of nonzero ints over the variables 1 .. n.
Hard clauses must hold; each soft clause costs 1 when it is false.
The SAT oracle is a small iterative DPLL, and cores are made minimal by deletion.
"""


def dpll(n: int, clauses: list[list[int]]) -> list[bool] | None:
    """Return a model (x[v - 1] is the value of v) or None. Iterative, chronological backtracking."""
    if any(not c for c in clauses):
        return None
    value: list[bool | None] = [None] * (n + 1)
    trail: list[tuple[int, int]] = []  # (variable, 0 implied / 1 first branch / 2 second branch)

    def lit_value(l: int) -> bool | None:
        v = value[abs(l)]
        return None if v is None else v == (l > 0)

    def propagate() -> bool:
        changed = True
        while changed:
            changed = False
            for c in clauses:
                free = None
                nfree = 0
                sat = False
                for l in c:
                    t = lit_value(l)
                    if t is True:
                        sat = True
                        break
                    if t is None:
                        nfree += 1
                        free = l
                if sat:
                    continue
                if nfree == 0:
                    return False
                if nfree == 1:
                    value[abs(free)] = free > 0
                    trail.append((abs(free), 0))
                    changed = True
        return True

    while True:
        if not propagate():
            while trail:
                v, kind = trail.pop()
                old = value[v]
                value[v] = None
                if kind == 1:
                    value[v] = not old
                    trail.append((v, 2))
                    break
            else:
                return None
            continue
        v = next((u for u in range(1, n + 1) if value[u] is None), 0)
        if v == 0:
            return [bool(value[u]) for u in range(1, n + 1)]
        value[v] = True
        trail.append((v, 1))


def minimal_core(n: int, hard: list[list[int]], soft: list[list[int]]) -> list[int]:
    """Indices of a minimal set K of soft clauses with hard + K unsatisfiable.

    The caller guarantees that hard + soft is unsatisfiable.
    """
    core = list(range(len(soft)))
    for i in list(core):
        rest = [j for j in core if j != i]
        if dpll(n, hard + [soft[j] for j in rest]) is None:
            core = rest
    return core


def exactly_one(lits: list[int]) -> list[list[int]]:
    """CNF of 'exactly one of lits is true': one at-least-one clause and all pairs."""
    out = [list(lits)]
    for a in range(len(lits)):
        for b in range(a + 1, len(lits)):
            out.append([-lits[a], -lits[b]])
    return out


def core_guided_maxsat(n: int, hard: list[list[int]], soft: list[list[int]], cores: list[list[int]] | None = None) -> tuple[int, list[bool]] | None:
    """Return (the least number of false soft clauses, an optimal assignment of x1 .. xn).

    None if the hard clauses are unsatisfiable. If cores is a list, the indices of the
    soft clauses of each core found are appended to it.
    """
    hard = [list(c) for c in hard]
    soft = [list(c) for c in soft]
    if dpll(n, hard) is None:  # @line L1
        return None
    cost = 0  # @line L2
    top = n
    while True:  # @line L3
        x = dpll(top, hard + soft)  # @line L4
        if x is not None:
            return cost, x[:n]  # @line L5
        k = minimal_core(top, hard, soft)  # @line L6
        if cores is not None:
            cores.append(k)
        relax = []
        for i in k:  # @line L7
            top += 1
            soft[i] = soft[i] + [top]
            relax.append(top)
        hard += exactly_one(relax)  # @line L8
        cost += 1  # @line L9
