# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/frequency-count/. The authors are listed in prov/E8G97Z.jsonl.

from typing import Dict, Hashable, List, Sequence, Tuple

Item = Hashable


def frequency_count(start: Sequence[Item], requests: Sequence[Item]) -> Tuple[int, List[Item], Dict[Item, int]]:
    """Serve list accesses with the frequency count rule.

    start: the initial list, with distinct items. requests: items of the list.
    An access to the item at position i (1-based) costs i. After the access the
    count of the item goes up by one, and the item moves forward with free
    exchanges past every item with a strictly smaller count.
    Returns (total cost, final list, final counts). Each access takes O(n) time.
    """
    lst = list(start)
    if len(set(lst)) != len(lst):
        raise ValueError("the items of the list must be distinct")
    cost = 0  # @line L1
    count = {x: 0 for x in lst}  # @line L2
    for x in requests:  # @line L3
        i = lst.index(x)  # @line L4
        cost += i + 1  # @line L5
        count[x] += 1  # @line L6
        while i > 0 and count[lst[i - 1]] < count[x]:  # @line L7
            lst[i - 1], lst[i] = lst[i], lst[i - 1]  # @line L8
            i -= 1
    return cost, lst, count  # @line L9
