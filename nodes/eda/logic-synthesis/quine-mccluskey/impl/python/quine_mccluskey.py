# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/quine-mccluskey/. The authors are listed in prov/N0CYS5.jsonl.

"""The Quine-McCluskey method for two-level minimization.

A cube over n variables is a string of length n over '0', '1' and '-'.
Position i is the variable x_{i+1}; '1' is the literal x, '0' is the
literal x', and '-' means that the variable is free. A minterm is an
integer m in [0, 2^n); its bit for x_1 is the most significant bit.
"""

from typing import Iterable

Cube = str


def minterm_cube(n: int, m: int) -> Cube:
    """The cube of one minterm."""
    return format(m, "b").zfill(n) if n else ""


def cube_minterms(c: Cube) -> list[int]:
    """All minterms of a cube, in increasing order."""
    out = [0]
    for ch in c:
        if ch == "0":
            out = [2 * m for m in out]
        elif ch == "1":
            out = [2 * m + 1 for m in out]
        else:
            out = [2 * m + b for m in out for b in (0, 1)]
    return sorted(out)


def literals(c: Cube) -> int:
    return sum(ch != "-" for ch in c)


def cost(cover: Iterable[Cube]) -> tuple[int, int]:
    """The cost of a cover: the number of cubes, then the number of literals."""
    cubes = list(cover)
    return len(cubes), sum(literals(c) for c in cubes)


def prime_implicants(n: int, on: Iterable[int], dc: Iterable[int] = ()) -> list[Cube]:
    """Phase 1: all prime implicants of the function with on-set on and don't-care set dc."""
    level = {minterm_cube(n, m) for m in set(on) | set(dc)}  # @line L1
    primes: list[Cube] = []
    while level:  # @line L2
        nxt: set[Cube] = set()  # @line L3
        merged: set[Cube] = set()
        for c in level:  # @line L4
            for i, ch in enumerate(c):
                if ch == "0":
                    d = c[:i] + "1" + c[i + 1:]  # @line L5
                    if d in level:
                        nxt.add(c[:i] + "-" + c[i + 1:])  # @line L6
                        merged.add(c)  # @line L7
                        merged.add(d)
        primes.extend(sorted(level - merged))  # @line L8
        level = nxt  # @line L9
    return primes


def minimum_cover(on: Iterable[int], primes: list[Cube]) -> list[Cube]:
    """Phase 2: a cheapest set of primes that covers every on-set minterm.

    It takes the essential primes, removes dominated rows and columns,
    and branches on the cyclic core. The result is exact for the cost
    (number of cubes, number of literals).
    """
    covers = [set(cube_minterms(p)) for p in primes]
    weight = [(1, literals(p)) for p in primes]
    todo = frozenset(on)
    best: list[list[int] | None] = [None]
    best_cost = [(len(primes) + 1, 0)]

    def add(a: tuple[int, int], b: tuple[int, int]) -> tuple[int, int]:
        return a[0] + b[0], a[1] + b[1]

    def solve(left: frozenset[int], cols: set[int], chosen: list[int], spent: tuple[int, int]) -> None:
        cols = set(cols)
        chosen = list(chosen)
        while True:
            if not left:  # @line L11
                if spent < best_cost[0]:
                    best_cost[0], best[0] = spent, chosen
                return
            if spent >= best_cost[0]:  # @line L12: bound
                return
            rows = {m: {j for j in cols if m in covers[j]} for m in left}
            if any(not r for r in rows.values()):
                return
            ess = {next(iter(r)) for r in rows.values() if len(r) == 1}  # @line L13
            if ess:
                for j in sorted(ess):
                    chosen.append(j)
                    spent = add(spent, weight[j])
                    cols.discard(j)
                left = frozenset(m for m in left if not any(m in covers[j] for j in ess))
                continue
            # @line L14: column dominance (a prime that covers no more and costs no less)
            dropped = False
            for j in sorted(cols):
                cj = covers[j] & left
                for k in sorted(cols):
                    if k != j and cj <= covers[k] and weight[k] <= weight[j] and (cj != covers[k] & left or weight[k] < weight[j] or k < j):
                        cols.discard(j)
                        dropped = True
                        break
                if dropped:
                    break
            if dropped:
                continue
            # @line L15: row dominance (a row whose primes include all primes of another row)
            for m in sorted(left):
                if any(m2 != m and rows[m2] <= rows[m] for m2 in left):
                    left = left - {m}
                    dropped = True
                    break
            if dropped:
                continue
            break
        m = min(left, key=lambda x: (len(rows[x]), x))  # @line L16: branch
        for j in sorted(rows[m], key=lambda j: (weight[j], j)):
            solve(left - covers[j], cols - {j}, chosen + [j], add(spent, weight[j]))

    solve(todo, set(range(len(primes))), [], (0, 0))  # @line L10
    assert best[0] is not None
    return sorted(primes[j] for j in best[0])


def quine_mccluskey(n: int, on: Iterable[int], dc: Iterable[int] = ()) -> list[Cube]:
    """A minimum sum of products of the function, as a list of cubes."""
    on = set(on)
    primes = prime_implicants(n, on, dc)
    return minimum_cover(on, primes)
