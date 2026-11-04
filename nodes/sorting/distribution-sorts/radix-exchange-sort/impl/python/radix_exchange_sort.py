# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/radix-exchange-sort/. The authors are listed in prov/Y3DQBZ.jsonl.


def radix_exchange_sort(a: list[int], w: int | None = None) -> list[int]:
    """Sort the list a of non-negative integers in place, and return it.

    Precondition: 0 <= x < 2**w for each x; by default w is the bit length
    of the largest key. The sort is not stable. The cost is O(n w) time in
    the worst case and O(w) extra space for the stack.
    """
    if any(x < 0 for x in a):
        raise ValueError("the keys must be non-negative")
    if w is None:
        w = max(a, default=0).bit_length()
    elif any(x >> w for x in a):
        raise ValueError("a key has more than w bits")
    stack = [(0, len(a), w - 1)]  # @line L1
    while stack:  # @line L2
        lo, hi, b = stack.pop()  # @line L3
        if hi - lo <= 1 or b < 0:  # @line L4
            continue
        i, j = lo, hi - 1  # @line L5
        while i <= j:  # @line L6
            while i <= j and not (a[i] >> b) & 1:  # @line L7
                i += 1
            while i <= j and (a[j] >> b) & 1:  # @line L8
                j -= 1
            if i < j:  # @line L9
                a[i], a[j] = a[j], a[i]
                i += 1
                j -= 1
        stack.append((i, hi, b - 1))  # @line L10
        stack.append((lo, i, b - 1))
    return a  # @line L11
