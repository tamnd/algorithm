# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/even-paz-algorithm/. The authors are listed in prov/E1V4HN.jsonl.

from fractions import Fraction
from typing import Optional

from agtcake import Oracle

Piece = list[tuple[Fraction, Fraction]]


def even_paz(oracle: Oracle) -> dict[int, Piece]:
    """Even-Paz divide and conquer for the n agents of the oracle.

    Each agent gets one interval, worth at least 1/n to it.
    """
    alloc: dict[int, Piece] = {}
    agents = list(range(oracle.n))
    whole = {i: Fraction(1) for i in agents}  # V_i([0, 1]) = 1 needs no query
    _even_paz(oracle, agents, Fraction(0), Fraction(1), whole, alloc)
    return alloc


def _even_paz(
    oracle: Oracle,
    agents: list[int],
    a: Fraction,
    b: Fraction,
    known: Optional[dict[int, Fraction]],
    alloc: dict[int, Piece],
) -> None:
    """Divide [a, b] among agents. known holds V_i([a, b]) when it is known."""
    k = len(agents)
    if k == 1:  # @line L1
        alloc[agents[0]] = [(a, b)]
        return
    k1 = k // 2  # @line L2
    worth: dict[int, Fraction] = {}
    marks: dict[int, Fraction] = {}
    for i in agents:  # @line L3
        w = known[i] if known is not None else oracle.eval_query(i, a, b)  # @line L4
        worth[i] = w
        marks[i] = oracle.cut_query(i, a, w * k1 / k)  # @line L5
    order = sorted(agents, key=lambda i: (marks[i], i))  # @line L6
    left, right = order[:k1], order[k1:]
    x = marks[order[k1 - 1]]  # @line L7
    _even_paz(oracle, left, a, x, None, alloc)  # @line L8
    _even_paz(oracle, right, x, b, None, alloc)  # @line L9


def query_count(n: int) -> int:
    """The exact number of queries of even_paz on n agents (cuts plus evals)."""

    def t(k: int) -> int:
        return 0 if k <= 1 else 2 * k + t(k // 2) + t(k - k // 2)

    return t(n) - n if n > 1 else 0
