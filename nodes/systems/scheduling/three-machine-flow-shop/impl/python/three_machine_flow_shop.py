# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/three-machine-flow-shop/. The authors are listed in prov/F4DF7W.jsonl.

import itertools
from typing import Sequence


def johnson_two(a: Sequence[int], b: Sequence[int]) -> list[int]:
    """Johnson's rule for two machines: a[j] <= b[j] first by increasing a, then the rest by decreasing b."""
    first = sorted((j for j in range(len(a)) if a[j] <= b[j]), key=lambda j: (a[j], j))
    last = sorted((j for j in range(len(a)) if a[j] > b[j]), key=lambda j: (-b[j], j))
    return first + last


def middle_is_dominated(a: Sequence[int], b: Sequence[int], c: Sequence[int]) -> bool:
    """Johnson's condition: min a >= max b, or min c >= max b."""
    if not a:
        return True
    return min(a) >= max(b) or min(c) >= max(b)  # @line L1


def johnson_three_machine(a: Sequence[int], b: Sequence[int], c: Sequence[int]) -> list[int]:
    """The reduction of F3||Cmax to F2||Cmax: Johnson's rule on the times
    (a[j] + b[j], b[j] + c[j]). The order is optimal when the middle machine is
    dominated; otherwise it is only a heuristic. Cost: O(n log n)."""
    if not (len(a) == len(b) == len(c)):
        raise ValueError("a, b and c must have the same length")
    first = [x + y for x, y in zip(a, b)]  # @line L2
    second = [y + z for y, z in zip(b, c)]
    return johnson_two(first, second)  # @line L3


def makespan3(a: Sequence[int], b: Sequence[int], c: Sequence[int], order: Sequence[int]) -> int:
    """The makespan of the permutation schedule in this order, each operation as early as possible."""
    t1 = t2 = t3 = 0  # @line L4
    for j in order:  # @line L5
        t1 += a[j]  # @line L6
        t2 = max(t2, t1) + b[j]  # @line L7
        t3 = max(t3, t2) + c[j]  # @line L8
    return t3  # @line L9


def best_order_makespan(a: Sequence[int], b: Sequence[int], c: Sequence[int]) -> int:
    """The optimum by a search over all n! orders. Permutation schedules are
    optimal for three machines, so this is the optimum of F3||Cmax."""
    return min(makespan3(a, b, c, o) for o in itertools.permutations(range(len(a))))
