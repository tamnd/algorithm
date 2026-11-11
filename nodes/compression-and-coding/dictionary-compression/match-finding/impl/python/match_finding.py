# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/match-finding/. The authors are listed in prov/625H77.jsonl.

"""Match finders for LZ77-style compressors.

A match at position i is a pair (length, distance) with distance >= 1 and
t[i - distance .. i - distance + length) == t[i .. i + length). The source
may overlap position i. All finders here return the longest match whose
length is at least min_len and at most max_len, with a distance of at most
window; (0, 0) means no such match.

- longest_match_brute: the exhaustive oracle, O(i * max_len) per call.
- HashChains: the zlib method. head[h] is the last position with hash h,
  prev[p] is the position before p with the same hash. A chain limit makes
  the search a heuristic.
- BinaryTrees: the LZMA bt method. The positions with the same hash of the
  first two bytes form a binary search tree ordered by their suffixes. Each
  new position is inserted at the root; the search visits the lexicographic
  neighbours of the new suffix, so it finds the longest match.
"""

Match = tuple[int, int]


def longest_match_brute(t: bytes, i: int, min_len: int = 1, max_len: int | None = None,
                        window: int | None = None) -> Match:
    """Exhaustive search. On a tie the smallest distance wins."""
    n = len(t)
    cap = n - i if max_len is None else min(max_len, n - i)
    lo = 0 if window is None else max(0, i - window)
    best, dist = 0, 0
    for j in range(i - 1, lo - 1, -1):
        k = 0
        while k < cap and t[j + k] == t[i + k]:
            k += 1
        if k > best:
            best, dist = k, i - j
    return (best, dist) if best >= min_len else (0, 0)


class HashChains:
    """Hash chains with a 3-byte hash, as in zlib (here -1 ends a chain)."""

    MIN_MATCH = 3

    def __init__(self, t: bytes, hash_bits: int = 15, max_len: int = 258,
                 window: int = 32768, max_chain: int | None = None) -> None:
        self.t, self.n = t, len(t)
        self.bits = hash_bits
        self.mask = (1 << hash_bits) - 1
        self.head = [-1] * (1 << hash_bits)
        self.prev = [-1] * max(self.n, 1)
        self.max_len, self.window, self.max_chain = max_len, window, max_chain
        self.probes = 0  # candidates compared, for the cost tests

    def hash(self, i: int) -> int:
        t, s = self.t, (self.bits + 2) // 3
        return ((((t[i] << s) ^ t[i + 1]) << s) ^ t[i + 2]) & self.mask

    def insert(self, i: int) -> None:
        """Make position i the head of its chain. Needs i + 3 <= n."""
        h = self.hash(i)  # @line L1
        self.prev[i] = self.head[h]  # @line L2
        self.head[h] = i  # @line L3

    def find(self, i: int) -> Match:
        """Longest match at i among the inserted positions on i's chain."""
        if self.n - i < self.MIN_MATCH:
            return (0, 0)
        t, cap = self.t, min(self.max_len, self.n - i)
        cur = self.head[self.hash(i)]  # @line L4
        best, dist, chain = 0, 0, self.max_chain
        while cur >= 0 and i - cur <= self.window:  # @line L5
            if chain is not None:
                if chain == 0:
                    break  # @line L6
                chain -= 1
            self.probes += 1
            k = 0
            while k < cap and t[cur + k] == t[i + k]:  # @line L7
                k += 1
            if k > best:  # @line L8
                best, dist = k, i - cur
                if k == cap:
                    break
            cur = self.prev[cur]  # @line L9
        return (best, dist) if best >= self.MIN_MATCH else (0, 0)

    def find_and_insert(self, i: int) -> Match:
        m = self.find(i)
        if self.n - i >= self.MIN_MATCH:
            self.insert(i)
        return m


class BinaryTrees:
    """Binary-tree match finder with root insertion, as in LZMA's bt2 mode.

    left[p] and right[p] are the children of position p. A tree holds the
    positions whose first two bytes have the same hash, ordered by the
    suffixes t[p ..] cut at max_len. Newer positions are nearer the root, so
    the search stops at the first position outside the window.
    """

    MIN_MATCH = 2

    def __init__(self, t: bytes, max_len: int = 273, window: int = 1 << 22,
                 max_depth: int | None = None) -> None:
        self.t, self.n = t, len(t)
        self.root: dict[int, int] = {}
        self.left = [-1] * max(self.n, 1)
        self.right = [-1] * max(self.n, 1)
        self.max_len, self.window, self.max_depth = max_len, window, max_depth

    def find_and_insert(self, i: int) -> Match:
        """Insert position i as the new root and return the longest match at i."""
        t, n = self.t, self.n
        if n - i < self.MIN_MATCH:
            return (0, 0)
        cap = min(self.max_len, n - i)
        key = (t[i] << 8) | t[i + 1]
        cur = self.root.get(key, -1)
        self.root[key] = i
        # (node, side) where the next smaller / larger subtree is hung
        lo_slot, hi_slot = (i, 0), (i, 1)
        lo_len = hi_len = 0  # common prefix with the bounds of the search range
        best, dist, depth = 0, 0, 0
        while cur >= 0 and i - cur <= self.window and (self.max_depth is None or depth < self.max_depth):
            depth += 1
            k = min(lo_len, hi_len)
            while k < cap and t[cur + k] == t[i + k]:
                k += 1
            if k > best:
                best, dist = k, i - cur
            if k == cap:
                # cur equals the new suffix up to the cap: i replaces cur
                self._hang(lo_slot, self.left[cur])
                self._hang(hi_slot, self.right[cur])
                return (best, dist)
            if t[cur + k] < t[i + k]:
                self._hang(lo_slot, cur)
                lo_slot, lo_len, cur = (cur, 1), k, self.right[cur]
            else:
                self._hang(hi_slot, cur)
                hi_slot, hi_len, cur = (cur, 0), k, self.left[cur]
        self._hang(lo_slot, -1)
        self._hang(hi_slot, -1)
        return (best, dist) if best >= self.MIN_MATCH else (0, 0)

    def _hang(self, slot: tuple[int, int], node: int) -> None:
        p, side = slot
        if side == 0:
            self.left[p] = node
        else:
            self.right[p] = node


def all_matches(t: bytes, finder) -> list[Match]:
    """Run a finder at every position, inserting each position after it."""
    return [finder.find_and_insert(i) for i in range(len(t))]
