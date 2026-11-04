# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/chronological-backtracking/. The authors are listed in prov/5ZHQ6D.jsonl.

from collections.abc import Callable, Hashable, Iterator, Sequence
from typing import TypeVar

V = TypeVar("V", bound=Hashable)

Constraints = dict[tuple[int, int], Callable[[V, V], bool]]


def _consistent(a: list[V], i: int, v: V, constraints: Constraints, stats: dict[str, int]) -> bool:
    for j in range(i):
        pred = constraints.get((j, i))
        if pred is not None:
            stats["checks"] += 1
            if not pred(a[j], v):
                return False
    return True


def solutions(
    domains: Sequence[Sequence[V]],
    constraints: Constraints,
    stats: dict[str, int] | None = None,
) -> Iterator[list[V]]:
    """Yield every solution of a binary CSP in lexicographic order.

    Variables are 0 .. m-1 and are assigned in this order. domains[i] lists
    the values of variable i in the order to try them. constraints[(j, i)]
    with j < i is a predicate on (value of j, value of i). The search is
    chronological backtracking, run with an explicit stack. If stats is
    given, it receives the counts "assignments" and "checks". Time:
    O(m d^m) checks in the worst case; extra space O(m).
    """
    for j, i in constraints:
        if not 0 <= j < i < len(domains):
            raise ValueError("constraint keys must be pairs (j, i) with j < i")
    st = stats if stats is not None else {}
    st.setdefault("assignments", 0)
    st.setdefault("checks", 0)
    m = len(domains)
    a: list[V] = []
    # positions[i] is the index of the next value of D_i to try
    positions = [0] * (m + 1)
    while True:
        i = len(a)
        if i == m:  # @line L1
            yield list(a)
            if m == 0:
                return
            a.pop()  # @line L7
            continue
        if positions[i] >= len(domains[i]):
            positions[i] = 0
            if i == 0:
                return  # @line L8
            a.pop()  # @line L8
            continue
        v = domains[i][positions[i]]  # @line L2
        positions[i] += 1
        if _consistent(a, i, v, constraints, st):  # @line L3
            a.append(v)  # @line L4
            st["assignments"] += 1
            positions[i + 1] = 0  # @line L5


def chronological_backtracking(
    domains: Sequence[Sequence[V]],
    constraints: Constraints,
    stats: dict[str, int] | None = None,
) -> list[V] | None:
    """Return the lexicographically first solution, or None if there is none (lines L1 to L8, line L6 stops at the first)."""
    for sol in solutions(domains, constraints, stats):
        return sol  # @line L6
    return None
