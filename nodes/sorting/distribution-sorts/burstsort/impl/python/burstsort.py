# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/burstsort/. The authors are listed in prov/QN966N.jsonl.
import random


def _c(s: str, d: int) -> int:
    """The slot of s at depth d: 0 when s has ended, else the code of s[d] plus 1."""
    return ord(s[d]) + 1 if d < len(s) else 0


class _Node:
    """A trie node: each slot is None, a bucket (list of str) or a child _Node."""

    __slots__ = ("slots",)

    def __init__(self, r: int) -> None:
        self.slots: list = [None] * (r + 1)


def _burst(v: _Node, r: int, d: int, radix: int) -> None:
    u = _Node(radix)
    for s in v.slots[r]:
        k = _c(s, d)
        if u.slots[k] is None:
            u.slots[k] = []
        u.slots[k].append(s)
    v.slots[r] = u


def _mkq(a: list[str], d0: int, rng: random.Random) -> None:
    """Multikey quicksort of a, in place; all strings agree on d0 characters."""
    stack = [(0, len(a), d0)]
    while stack:
        lo, hi, d = stack.pop()
        if hi - lo <= 1:
            continue
        v = _c(a[rng.randrange(lo, hi)], d)
        lt, i, gt = lo, lo, hi - 1
        while i <= gt:
            x = _c(a[i], d)
            if x < v:
                a[lt], a[i] = a[i], a[lt]
                lt += 1
                i += 1
            elif x > v:
                a[i], a[gt] = a[gt], a[i]
                gt -= 1
            else:
                i += 1
        gt += 1
        stack.append((gt, hi, d))
        if v != 0:
            stack.append((lt, gt, d + 1))
        stack.append((lo, lt, d))


def burstsort(a: list[str], threshold: int = 64, r: int = 256, seed: int | None = None) -> list[str]:
    """Sort the list a of strings in lexicographic order, in place, and return it.

    Precondition: each character has a code less than r, threshold >= 1.
    The cost is O(n log T + D + r (n + D) / T) expected time, where D is the
    total length of the distinguishing prefixes, and O(n + r (n + D) / T) space.
    """
    if threshold < 1:
        raise ValueError("threshold must be at least 1")
    for s in a:
        for ch in s:
            if ord(ch) >= r:
                raise ValueError("a character is outside the alphabet")
    rng = random.Random(seed)
    root = _Node(r)  # @line L1
    for s in a:  # @line L2
        v, d = root, 0  # @line L3
        while isinstance(v.slots[_c(s, d)], _Node):  # @line L4
            v = v.slots[_c(s, d)]
            d += 1
        k = _c(s, d)  # @line L5
        if v.slots[k] is None:
            v.slots[k] = []
        v.slots[k].append(s)
        if k != 0 and len(v.slots[k]) > threshold:  # @line L6
            _burst(v, k, d + 1, r)
    pos = 0  # @line L7
    stack: list[tuple[_Node, int, int]] = [(root, 0, 0)]
    while stack:  # @line L8
        v, k, d = stack.pop()
        if k > r:
            continue
        stack.append((v, k + 1, d))
        item = v.slots[k]
        if item is None:
            continue
        if isinstance(item, _Node):
            stack.append((item, 0, d + 1))
            continue
        if k != 0:  # @line L9
            _mkq(item, d + 1, rng)
        a[pos:pos + len(item)] = item  # @line L10
        pos += len(item)
    return a  # @line L11
