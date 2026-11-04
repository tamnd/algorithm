# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dc3-algorithm/. The authors are listed in prov/13MGBB.jsonl.

import heapq

# Difference covers modulo v: every residue d mod v is a difference of two members.
COVERS: dict[int, tuple[int, ...]] = {3: (1, 2), 7: (1, 2, 4), 13: (1, 2, 4, 10)}


def is_difference_cover(d: tuple[int, ...], v: int) -> bool:
    return {(a - b) % v for a in d for b in d} == set(range(v))


def _radix_sort(items: list[int], keys: list[list[int]], k: int) -> list[int]:
    """Stable LSD radix sort of items by the tuples keys[i] (all of the same length), digits < k."""
    width = len(keys[items[0]]) if items else 0
    for p in range(width - 1, -1, -1):
        buckets: list[list[int]] = [[] for _ in range(k)]
        for i in items:
            buckets[keys[i][p]].append(i)
        items = [i for b in buckets for i in b]
    return items


def suffix_array(s: str, v: int = 3) -> list[int]:
    """Return the suffix array of s with the difference cover algorithm DC-v."""
    if v not in COVERS:
        raise ValueError(f"no difference cover stored for v = {v}")
    t = [ord(c) + 1 for c in s]
    return _dc(t, max(t, default=0) + 1, v)


def _dc(t: list[int], k: int, v: int) -> list[int]:
    """Suffix array of t, a list of ints in [1, k); positions past the end read as 0."""
    n = len(t)
    if n <= 2 * v:
        return sorted(range(n), key=lambda i: t[i:])
    cover = COVERS[v]
    in_d = [False] * v
    for d in cover:
        in_d[d] = True

    def ch(i: int) -> int:
        return t[i] if i < n else 0

    # sample positions, class by class, including position n if its class is in D
    sample = [i for d in cover for i in range(d, n + 1, v)]  # @line L1
    # sort the samples by their first v characters and name them
    keys: list[list[int]] = [[] for _ in range(n + 1)]
    for i in sample:
        keys[i] = [ch(i + j) for j in range(v)]
    order = _radix_sort(sample, keys, k)  # @line L2
    name = [0] * (n + 1)
    cur, prev = 0, None
    for i in order:
        if keys[i] != prev:
            cur, prev = cur + 1, keys[i]
        name[i] = cur
    rank = [0] * (n + v + 1)  # rank of a sample position; 0 past the end
    if cur < len(sample):  # @line L3
        # recurse on the names written class by class
        sub = [name[i] for i in sample]
        sub_sa = _dc(sub, cur + 1, v)  # @line L4
        for r, j in enumerate(sub_sa):  # @line L5
            rank[sample[j]] = r + 1
    else:
        for i in sample:  # @line L5
            rank[i] = name[i]
    # sort each residue class by (first l characters, rank at offset l)
    lists: list[list[int]] = []
    ck: list[list[int]] = [[] for _ in range(n)]
    for c in range(v):  # @line L6
        l = next(x for x in range(v) if in_d[(c + x) % v])
        cls = list(range(c, n, v))
        if not cls:
            continue
        for i in cls:
            ck[i] = [ch(i + j) for j in range(l)] + [rank[i + l]]
        lists.append(_radix_sort(cls, ck, max(k, n + 2)))
    # offsets l with i + l and j + l both in the sample, for each pair of classes
    off = [[next(x for x in range(v) if in_d[(a + x) % v] and in_d[(b + x) % v])
            for b in range(v)] for a in range(v)]  # @line L7

    class _Key:
        __slots__ = ("i",)

        def __init__(self, i: int) -> None:
            self.i = i

        def __lt__(self, other: "_Key") -> bool:
            i, j = self.i, other.i
            l = off[i % v][j % v]
            for x in range(l):
                if ch(i + x) != ch(j + x):
                    return ch(i + x) < ch(j + x)
            return rank[i + l] < rank[j + l]

    # merge the v sorted classes
    merged = heapq.merge(*([_Key(i) for i in lst] for lst in lists))  # @line L8
    return [key.i for key in merged]


def naive_suffix_array(s: str) -> list[int]:
    return sorted(range(len(s)), key=lambda i: s[i:])
