# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/matroid-greedy-algorithm/. The authors are listed in prov/4BS62B.jsonl.

from typing import Callable, Hashable, Sequence, TypeVar

E = TypeVar("E", bound=Hashable)


def matroid_greedy_algorithm(
    elements: Sequence[E],
    weight: Callable[[E], float],
    indep: Callable[[frozenset], bool],
) -> list[E]:
    """Return a maximum-weight basis of a matroid, in the order of selection.

    elements: the ground set, without repeats.
    weight: the weight of an element, any real number.
    indep: the independence oracle; indep(X) is True when the frozenset X is
    independent. It must describe a matroid for the result to be optimal.

    Elements are scanned by nonincreasing weight, ties in input order, and each
    one is kept when the kept set stays independent.

    Cost: O(n log n) comparisons and n oracle calls.
    """
    order = sorted(elements, key=weight, reverse=True)  # @line L1
    chosen: list[E] = []  # @line L2
    current: frozenset = frozenset()
    for e in order:  # @line L3
        candidate = current | {e}
        if indep(candidate):  # @line L4
            chosen.append(e)  # @line L5
            current = candidate
    return chosen  # @line L6
