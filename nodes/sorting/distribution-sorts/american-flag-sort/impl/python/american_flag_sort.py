# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/american-flag-sort/. The authors are listed in prov/GW15GA.jsonl.


def _c(s: str, d: int) -> int:
    """The bucket of s at depth d: 0 when s has ended, else the code of s[d] plus 1."""
    return ord(s[d]) + 1 if d < len(s) else 0


def american_flag_sort(a: list[str], r: int = 256) -> list[str]:
    """Sort the list a of strings in lexicographic order, in place, and return it.

    Precondition: each character has a code less than r. The sort is not stable.
    The cost is O(r (n + D)) time, where D is the total length of the
    distinguishing prefixes, and O(r) counters per step with no item buffer.
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
        start = [0] * (r + 1)  # @line L6
        pos = lo
        for b in range(r + 1):
            start[b] = pos
            pos += count[b]
        nxt = start[:]
        end = [start[b] + count[b] for b in range(r + 1)]
        for cur in range(r + 1):  # @line L7
            while nxt[cur] < end[cur]:  # @line L8
                b = _c(a[nxt[cur]], d)  # @line L9
                if b == cur:  # @line L10
                    nxt[cur] += 1
                else:  # @line L11
                    j = nxt[b]
                    a[nxt[cur]], a[j] = a[j], a[nxt[cur]]
                    nxt[b] = j + 1
        for b in range(r, 0, -1):  # @line L12
            if count[b] >= 2:
                stack.append((start[b], end[b], d + 1))
    return a  # @line L13
