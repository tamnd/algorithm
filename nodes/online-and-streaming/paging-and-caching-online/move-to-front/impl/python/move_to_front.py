# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/move-to-front/. The authors are listed in prov/XGK3CR.jsonl.

from typing import Hashable, List, Sequence, Tuple

Item = Hashable


def move_to_front(start: Sequence[Item], requests: Sequence[Item]) -> Tuple[int, List[Item]]:
    """Serve list accesses with the move-to-front rule.

    start: the initial list, with distinct items. requests: items of the list.
    An access to the item at position i (1-based) costs i. After the access the
    item moves to the front with free exchanges.
    Returns (total cost, final list). Each access takes O(n) time on a Python list.
    """
    lst = list(start)
    if len(set(lst)) != len(lst):
        raise ValueError("the items of the list must be distinct")
    cost = 0  # @line L1
    for x in requests:  # @line L2
        i = lst.index(x) + 1  # @line L3
        cost += i  # @line L4
        lst.insert(0, lst.pop(i - 1))  # @line L5
    return cost, lst  # @line L6
