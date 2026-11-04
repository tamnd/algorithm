# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/msd-radix-sort/. The authors are listed in prov/5YMPGZ.jsonl.


def _c(s: str, d: int) -> int:
    """The bucket of s at depth d: 0 when s has ended, else the code of s[d] plus 1."""
    return ord(s[d]) + 1 if d < len(s) else 0


def msd_radix_sort(a: list[str], r: int = 256) -> list[str]:
    """Sort the list a of strings in lexicographic order, in place, and return it.

    Precondition: each character has a code less than r. The sort is stable.
    The cost is O(r (n + D)) time, where D is the total length of the
    distinguishing prefixes, and Theta(n + r) extra space for the buffer.
    An explicit stack replaces the recursion, so long common prefixes are safe.
    """
    for s in a:
        for ch in s:
            if ord(ch) >= r:
                raise ValueError("a character is outside the alphabet")
    stack = [(0, len(a), 0)]  # @line L1
    while stack:  # @line L2
        lo, hi, d = stack.pop()  # @line L3
        if hi - lo <= 1:  # @line L4
            continue
        count = [0] * (r + 1)  # @line L5
        for i in range(lo, hi):
            count[_c(a[i], d)] += 1
        start = [0] * (r + 2)  # @line L6
        for v in range(r + 1):
            start[v + 1] = start[v] + count[v]
        nxt = start[:]
        buf = [""] * (hi - lo)
        for i in range(lo, hi):  # @line L7
            v = _c(a[i], d)
            buf[nxt[v]] = a[i]
            nxt[v] += 1
        a[lo:hi] = buf  # @line L8
        for v in range(r, 0, -1):  # @line L9
            if start[v + 1] - start[v] >= 2:
                stack.append((lo + start[v], lo + start[v + 1], d + 1))  # @line L10
    return a  # @line L11
