# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/longest-prefix-match/. The authors are listed in prov/X7VXG1.jsonl.

"""Longest prefix match on W-bit addresses.

A prefix is a pair (p, l) with 0 <= l <= W and 0 <= p < 2**l: the top l bits
of a matching address equal p. A table maps prefixes to next hops. Three
methods are here: a brute-force scan (the reference), a binary trie, and
binary search on prefix lengths (Waldvogel, Varghese, Turner and Plattner).
"""

from typing import Optional

Prefix = tuple[int, int]
Match = Optional[tuple[int, int, object]]  # (p, l, next hop) or None


def matches(p: int, l: int, addr: int, w: int) -> bool:
    return addr >> (w - l) == p


def brute_force_lpm(table: dict[Prefix, object], addr: int, w: int) -> Match:
    """Scan every prefix and keep the longest one that matches."""
    best: Match = None
    for (p, l), hop in table.items():
        if matches(p, l, addr, w) and (best is None or l > best[1]):
            best = (p, l, hop)
    return best


class _Node:
    __slots__ = ("child", "hop", "has")

    def __init__(self) -> None:
        self.child: list[Optional["_Node"]] = [None, None]
        self.hop: object = None
        self.has = False


class BinaryTrie:
    """One node for each bit; a node is marked when a prefix ends there."""

    def __init__(self, w: int) -> None:
        self.w = w
        self.root = _Node()
        self.size = 0

    def insert(self, p: int, l: int, hop: object) -> None:
        v = self.root
        for i in range(l - 1, -1, -1):
            b = (p >> i) & 1
            if v.child[b] is None:
                v.child[b] = _Node()
            v = v.child[b]
        if not v.has:
            self.size += 1
        v.has, v.hop = True, hop

    def delete(self, p: int, l: int) -> bool:
        path = [self.root]
        v = self.root
        for i in range(l - 1, -1, -1):
            v = v.child[(p >> i) & 1]
            if v is None:
                return False
            path.append(v)
        if not v.has:
            return False
        v.has, v.hop = False, None
        self.size -= 1
        # Remove nodes that hold no prefix and have no children.
        for depth in range(l, 0, -1):
            node = path[depth]
            if node.has or node.child[0] or node.child[1]:
                break
            path[depth - 1].child[(p >> (l - depth)) & 1] = None
        return True

    def lookup(self, addr: int) -> tuple[Match, int]:
        """Return the longest match and the number of nodes read."""
        w = self.w
        v = self.root  # @line L1
        best: Match = None  # @line L2
        reads = 0
        depth = 0
        while v is not None:  # @line L3
            reads += 1
            if v.has:  # @line L4
                best = (addr >> (w - depth) if depth else 0, depth, v.hop)  # @line L5
            if depth == w:  # @line L6
                break
            v = v.child[(addr >> (w - 1 - depth)) & 1]  # @line L7
            depth += 1
        return best, reads  # @line L8

    def node_count(self) -> int:
        count, stack = 0, [self.root]
        while stack:
            v = stack.pop()
            count += 1
            stack.extend(c for c in v.child if c is not None)
        return count


class BinarySearchOnLengths:
    """One hash table per distinct prefix length, with markers.

    An entry at length L for the L-bit string s holds `bmp`, the longest
    prefix of the table that matches s (it is s itself for a real prefix).
    """

    def __init__(self, table: dict[Prefix, object], w: int) -> None:
        self.w = w
        self.lengths = sorted({l for (_, l) in table})
        self.tables: list[dict[int, Match]] = [dict() for _ in self.lengths]
        index = {l: j for j, l in enumerate(self.lengths)}
        keys: list[set[int]] = [set() for _ in self.lengths]
        self.markers = 0
        for (p, l) in table:
            j = index[l]
            keys[j].add(p)
            lo, hi = 0, len(self.lengths) - 1
            while lo <= hi:  # the search path that ends at length index j
                mid = (lo + hi) // 2
                if mid == j:
                    break
                if mid < j:  # the search must go right here: put a marker
                    keys[mid].add(p >> (l - self.lengths[mid]))
                    lo = mid + 1
                else:
                    hi = mid - 1
        trie = BinaryTrie(w)
        for (p, l), hop in table.items():
            trie.insert(p, l, hop)
        for j, l in enumerate(self.lengths):
            for s in keys[j]:
                self.tables[j][s] = self._bmp(trie, s, l)
                if (s, l) not in table:
                    self.markers += 1

    @staticmethod
    def _bmp(trie: BinaryTrie, s: int, l: int) -> Match:
        """Longest prefix of the table that matches the l-bit string s."""
        v, best = trie.root, None
        for depth in range(l + 1):
            if v.has:
                best = (s >> (l - depth) if depth else 0, depth, v.hop)
            if depth == l:
                break
            v = v.child[(s >> (l - 1 - depth)) & 1]
            if v is None:
                break
        return best

    def lookup(self, addr: int) -> tuple[Match, int]:
        """Return the longest match and the number of hash probes."""
        lo, hi = 0, len(self.lengths) - 1
        best: Match = None
        probes = 0
        while lo <= hi:
            mid = (lo + hi) // 2
            probes += 1
            l = self.lengths[mid]
            key = addr >> (self.w - l)
            if key in self.tables[mid]:
                best = self.tables[mid][key]  # a prefix or a marker: go longer
                lo = mid + 1
            else:
                hi = mid - 1  # no entry: no longer prefix can match
        return best, probes


def random_table(rng, n: int, w: int, with_default: bool = True) -> dict[Prefix, object]:
    """A seeded random table of about n prefixes, lengths skewed to long."""
    table: dict[Prefix, object] = {}
    if with_default:
        table[(0, 0)] = "default"
    while len(table) < n + with_default:
        l = rng.randint(1, w)
        p = rng.getrandbits(l)
        table[(p, l)] = "hop%d" % len(table)
    return table
