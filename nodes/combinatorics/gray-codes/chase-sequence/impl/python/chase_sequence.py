# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/chase-sequence/. The authors are listed in prov/BN89EB.jsonl.

from collections.abc import Iterator


def chase(s: int, t: int) -> Iterator[list[int]]:
    """Yield all bit strings with s zeros and t ones in Chase's sequence C_st.

    The yielded list a has a[j] = bit a_j, and the string reads a_{n-1} ... a_1 a_0
    with n = s + t. The same list object is yielded each time and is changed in
    place (one 1 moves right or left by one or two places), so copy it if you keep
    it. An explicit stack replaces the recursion of the pseudocode.
    """
    if s < 0 or t < 0:
        raise ValueError("s and t must be non-negative")
    n = s + t
    a = [0] * s + [1] * t  # @line L1
    # Stack items: ("walk", s, t, kind, forward) or ("swap", off, on).
    stack: list[tuple] = [("walk", s, t, "A" if n % 2 else "B", True)]  # @line L2
    while stack:
        item = stack.pop()
        if item[0] == "swap":
            _, off, on = item
            a[off] = 0  # @line L8: also L12 with the roles swapped
            a[on] = 1
            continue
        _, s1, t1, kind, forward = item
        if s1 == 0 or t1 == 0:  # @line L3
            yield a  # @line L3
            continue
        m = s1 + t1 - 1  # @line L4
        y = m - 1 if kind == "B" or s1 == 1 else m - 2  # @line L4
        first = "B" if kind == "A" else "A"  # @line L5
        if forward:  # @line L6
            # Pushed in reverse: L7, then L8, then L9 run in this order.
            stack.append(("walk", s1 - 1, t1, "A", kind == "B"))  # @line L9
            stack.append(("swap", m, y))  # @line L8
            stack.append(("walk", s1, t1 - 1, first, True))  # @line L7
        else:  # @line L10
            stack.append(("walk", s1, t1 - 1, first, False))  # @line L13
            stack.append(("swap", y, m))  # @line L12
            stack.append(("walk", s1 - 1, t1, "A", kind == "A"))  # @line L11


def chase_strings(s: int, t: int) -> list[str]:
    """Return C_st as strings a_{n-1} ... a_0."""
    return ["".join(map(str, reversed(a))) for a in chase(s, t)]


def chase_combinations(n: int, k: int) -> list[tuple[int, ...]]:
    """Return the k-subsets of {0, ..., n-1} in Chase's order, as decreasing tuples c_k ... c_1.

    Element j is in the subset when bit a_j is 1. For k < 0 or k > n the list is empty.
    """
    if n < 0:
        raise ValueError("n must be non-negative")
    if k < 0 or k > n:
        return []
    return [tuple(j for j in range(n - 1, -1, -1) if a[j]) for a in chase(n - k, k)]
