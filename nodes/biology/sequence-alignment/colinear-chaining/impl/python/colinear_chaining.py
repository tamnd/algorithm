# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/colinear-chaining/. The authors are listed in prov/H5YXHD.jsonl.

"""Maximum-weight colinear chain of fragments in O(n log n) time.

A fragment is (x1, x2, y1, y2, w): it covers [x1, x2] in the first sequence
and [y1, y2] in the second, with weight w > 0. Fragment f precedes g when
x2(f) < x1(g) and y2(f) < y1(g). A chain is a list of fragments in which each
one precedes the next. The algorithm sweeps the x axis and keeps, over the
y2 values of the fragments whose x2 has been passed, a prefix-maximum
Fenwick tree of the best chain scores.
"""

from bisect import bisect_left

Fragment = tuple[int, int, int, int, int]

NONE = (0, -1)  # (score, fragment index) of the empty chain


class PrefixMax:
    """Fenwick tree for prefix maxima of (score, index) pairs."""

    def __init__(self, size: int) -> None:
        self.tree = [NONE] * (size + 1)

    def update(self, i: int, value: tuple[int, int]) -> None:
        """Raise slot i (0-based) to at least value."""
        i += 1
        while i < len(self.tree):
            if value > self.tree[i]:
                self.tree[i] = value
            i += i & -i

    def query(self, count: int) -> tuple[int, int]:
        """Maximum over slots 0 .. count - 1."""
        best = NONE
        while count > 0:
            if self.tree[count] > best:
                best = self.tree[count]
            count -= count & -count
        return best


def colinear_chain(frags: list[Fragment]) -> tuple[int, list[int]]:
    """Return (best weight, indices of a best chain in order)."""
    for x1, x2, y1, y2, w in frags:
        if x1 > x2 or y1 > y2 or w <= 0:
            raise ValueError("bad fragment")
    n = len(frags)
    if n == 0:
        return 0, []
    events = []  # @line L1
    for f, (x1, x2, _, _, _) in enumerate(frags):
        events.append((x1, 0, f))  # start events come first at equal x
        events.append((x2, 1, f))
    events.sort()  # @line L2
    ys = sorted({fr[3] for fr in frags})
    tree = PrefixMax(len(ys))  # @line L3
    score = [0] * n
    pred = [-1] * n
    for _, kind, f in events:  # @line L4
        x1, x2, y1, y2, w = frags[f]
        if kind == 0:  # @line L5
            s, g = tree.query(bisect_left(ys, y1))  # @line L6: best end with y2 < y1
            score[f] = w + s  # @line L7
            pred[f] = g
        else:
            tree.update(bisect_left(ys, y2), (score[f], f))  # @line L8
    best = max(range(n), key=lambda f: (score[f], -f))  # @line L9
    chain = []
    f = best
    while f != -1:  # @line L10
        chain.append(f)
        f = pred[f]
    chain.reverse()
    return score[best], chain


def precedes(f: Fragment, g: Fragment) -> bool:
    return f[1] < g[0] and f[3] < g[2]


def is_chain(frags: list[Fragment], chain: list[int]) -> bool:
    return all(precedes(frags[a], frags[b]) for a, b in zip(chain, chain[1:]))


def brute_force(frags: list[Fragment]) -> int:
    """Best chain weight over all subsets (small inputs only)."""
    n = len(frags)
    best = 0
    for mask in range(1, 1 << n):
        sel = sorted((frags[i] for i in range(n) if mask >> i & 1), key=lambda f: (f[0], f[2]))
        if all(precedes(a, b) for a, b in zip(sel, sel[1:])):
            best = max(best, sum(f[4] for f in sel))
    return best
