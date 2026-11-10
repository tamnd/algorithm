# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/transposition-rule/. The authors are listed in prov/T7XGDD.jsonl.

from typing import Hashable, List, Sequence, Tuple

Item = Hashable


def transposition_rule(start: Sequence[Item], requests: Sequence[Item]) -> Tuple[int, List[Item]]:
    """Serve list accesses with the transposition rule (transpose).

    start: the initial list, with distinct items. requests: items of the list.
    An access to the item at position i (1-based) costs i. After the access the
    item is swapped with the item just before it, by one free exchange.
    Returns (total cost, final list). Each access takes O(n) time for the scan.
    """
    lst = list(start)
    if len(set(lst)) != len(lst):
        raise ValueError("the items of the list must be distinct")
    cost = 0  # @line L1
    for x in requests:  # @line L2
        i = lst.index(x) + 1  # @line L3
        cost += i  # @line L4
        if i > 1:  # @line L5
            lst[i - 2], lst[i - 1] = lst[i - 1], lst[i - 2]  # @line L6
    return cost, lst  # @line L7
