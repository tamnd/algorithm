# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/eades-mckay-algorithm/. The authors are listed in prov/W2DJTJ.jsonl.

from collections.abc import Iterator


def eades_mckay(s: int, t: int) -> Iterator[list[int]]:
    """Yield all bit strings with s zeros and t ones in the homogeneous order K_st.

    The yielded list a has a[j] = bit a_j, and the string reads a_{n-1} ... a_1 a_0
    with n = s + t. Each step moves one 1 to a new place and passes only zeros.
    The same list object is yielded each time and is changed in place, so copy it
    if you keep it. An explicit stack replaces the recursion of the pseudocode.
    """
    if s < 0 or t < 0:
        raise ValueError("s and t must be non-negative")
    a = [1] * t + [0] * s  # @line L1
    # Stack items: ("walk", s, t, forward) or ("move", off, on).
    stack: list[tuple] = [("walk", s, t, True)]  # @line L2
    while stack:
        item = stack.pop()
        if item[0] == "move":
            _, off, on = item
            a[off] = 0  # @line L7: also L10, L15 and L17 with their positions
            a[on] = 1
            continue
        _, s1, t1, forward = item
        if s1 == 0 or t1 == 0:  # @line L3
            yield a  # @line L3
            continue
        m = s1 + t1 - 1  # @line L4
        if forward:  # @line L5
            # Pushed in reverse order of execution: L6, L7, L8, then L9 to L11.
            if t1 >= 2:  # @line L9
                stack.append(("walk", s1, t1 - 2, True))  # @line L11
                stack.append(("move", t1 - 2, m - 1))  # @line L10
            stack.append(("walk", s1 - 1, t1 - 1, False))  # @line L8
            stack.append(("move", m - 1, m))  # @line L7
            stack.append(("walk", s1 - 1, t1, True))  # @line L6
        else:  # @line L12
            stack.append(("walk", s1 - 1, t1, False))  # @line L18
            stack.append(("move", m, m - 1))  # @line L17
            stack.append(("walk", s1 - 1, t1 - 1, True))  # @line L16
            if t1 >= 2:  # @line L13
                stack.append(("move", m - 1, t1 - 2))  # @line L15
                stack.append(("walk", s1, t1 - 2, False))  # @line L14


def eades_mckay_strings(s: int, t: int) -> list[str]:
    """Return K_st as strings a_{n-1} ... a_0."""
    return ["".join(map(str, reversed(a))) for a in eades_mckay(s, t)]


def eades_mckay_combinations(n: int, k: int) -> list[tuple[int, ...]]:
    """Return the k-subsets of {0, ..., n-1} in the order K_(n-k)k, as decreasing tuples.

    Element j is in the subset when bit a_j is 1. For k < 0 or k > n the list is empty.
    """
    if n < 0:
        raise ValueError("n must be non-negative")
    if k < 0 or k > n:
        return []
    return [tuple(j for j in range(n - 1, -1, -1) if a[j]) for a in eades_mckay(n - k, k)]
