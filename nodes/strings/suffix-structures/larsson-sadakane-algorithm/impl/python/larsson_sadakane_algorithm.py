# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/larsson-sadakane-algorithm/. The authors are listed in prov/QSTAC1.jsonl.

from collections.abc import Sequence


def _split(sa: list[int], group: list[int], length: list[int], s: int, e: int, h: int) -> None:
    """Sort the group sa[s:e] by the key group[i + h] with ternary-split quicksort.

    Each block of equal keys becomes a new group whose number is its last rank.
    The keys are read before the group changes; the stack replaces recursion.
    """
    n = len(group)
    key = {x: (group[x + h] if x + h < n else -1) for x in sa[s:e]}
    stack = [(s, e)]
    while stack:
        lo, hi = stack.pop()
        if hi - lo == 1:
            group[sa[lo]] = lo
            length[lo] = -1
            continue
        pivot = key[sa[(lo + hi) // 2]]
        part = sa[lo:hi]
        less = [x for x in part if key[x] < pivot]
        equal = [x for x in part if key[x] == pivot]
        more = [x for x in part if key[x] > pivot]
        sa[lo:hi] = less + equal + more
        a, b = lo + len(less), lo + len(less) + len(equal)
        for x in equal:
            group[x] = b - 1
        length[a] = b - a if b - a > 1 else -1
        if more:
            stack.append((b, hi))
        if less:
            stack.append((lo, a))


def larsson_sadakane(text: Sequence) -> tuple[list[int], list[int]]:
    """Return (sa, rank): the suffix array of text and its inverse.

    No sentinel is used: a suffix that is a proper prefix of another sorts first.
    Symbols need a total order. Positions and ranks are 0-based.
    length[s] > 0 marks an unsorted group sa[s : s + length[s]]; length[s] < 0
    marks a run of -length[s] sorted entries, which later passes skip.
    """
    n = len(text)
    if n == 0:  # @line L1
        return [], []
    sa = sorted(range(n), key=text.__getitem__)  # @line L2
    group = [0] * n
    length = [0] * n
    s = 0
    while s < n:
        e = s + 1
        while e < n and text[sa[e]] == text[sa[s]]:
            e += 1
        for r in range(s, e):
            group[sa[r]] = e - 1
        length[s] = e - s if e - s > 1 else -1
        s = e
    h = 1  # @line L3
    while True:  # @line L4
        s, run, unsorted = 0, -1, False
        while s < n:  # @line L5
            if length[s] < 0:  # @line L6
                size = -length[s]
                if run >= 0:
                    length[run] -= size
                else:
                    run = s
                s += size
            else:
                unsorted = True
                e = s + length[s]
                _split(sa, group, length, s, e, h)  # @line L7
                run = -1  # @line L8
                s = e
        if not unsorted:  # @line L9
            return sa, group
        h *= 2  # @line L10
