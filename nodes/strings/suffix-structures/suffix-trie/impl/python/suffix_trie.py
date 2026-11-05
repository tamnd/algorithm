# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/suffix-trie/. The authors are listed in prov/J5APVR.jsonl.

from collections.abc import Hashable, Sequence


class _Node:
    __slots__ = ("next", "count", "ends")

    def __init__(self) -> None:
        self.next: dict[Hashable, "_Node"] = {}
        self.count = 0  # number of suffixes whose path passes through or ends at this node
        self.ends: list[int] = []  # the i with str(node) = S[i:], for 0 <= i < n


class SuffixTrie:
    """The trie of all nonempty suffixes of a sequence s, with no sentinel.

    The symbols can be any hashable values (a general alphabet, only equality
    is used). Positions are 0-based. Building takes Theta(n^2) time and space
    in the worst case, where n = len(s); a query for a pattern of length m
    walks at most m edges.
    """

    def __init__(self, s: Sequence[Hashable]) -> None:
        self.s = s
        self.root = _Node()  # @line L1
        n = len(s)
        for i in range(n):  # @line L2
            x = self.root  # @line L3
            for j in range(i, n):  # @line L4
                c = s[j]
                y = x.next.get(c)
                if y is None:  # @line L5
                    y = _Node()
                    x.next[c] = y
                x = y  # @line L6
                x.count += 1
            x.ends.append(i)  # @line L7

    def _find(self, p: Sequence[Hashable]) -> _Node | None:
        x: _Node | None = self.root  # @line L8
        for c in p:  # @line L9
            assert x is not None
            x = x.next.get(c)  # @line L10
            if x is None:  # @line L11
                return None
        return x  # @line L12

    def contains(self, p: Sequence[Hashable]) -> bool:
        """True when p is a substring of s (the empty pattern always is)."""
        return self._find(p) is not None

    def count(self, p: Sequence[Hashable]) -> int:
        """The number of occurrences of a nonempty pattern p in s."""
        if len(p) == 0:
            raise ValueError("the pattern must be nonempty")
        x = self._find(p)
        return 0 if x is None else x.count

    def occurrences(self, p: Sequence[Hashable]) -> list[int]:
        """The sorted start positions of a nonempty pattern p in s."""
        if len(p) == 0:
            raise ValueError("the pattern must be nonempty")
        x = self._find(p)
        if x is None:
            return []
        out: list[int] = []
        stack = [x]  # an explicit stack: the trie can be n levels deep
        while stack:
            y = stack.pop()
            out.extend(y.ends)
            stack.extend(y.next.values())
        out.sort()
        return out

    def node_count(self) -> int:
        """The number of nodes, the root included."""
        total, stack = 0, [self.root]
        while stack:
            y = stack.pop()
            total += 1
            stack.extend(y.next.values())
        return total

    def check_invariant(self) -> None:
        """Check that the nodes are the distinct substrings and the counts are right."""
        s, n = self.s, len(self.s)
        stack: list[tuple[_Node, tuple[Hashable, ...]]] = [(self.root, ())]
        seen = 0
        while stack:
            y, w = stack.pop()
            seen += 1
            k = len(w)
            if k > 0:
                occ = [i for i in range(n - k + 1) if tuple(s[i:i + k]) == w]
                assert occ, "every node spells a substring"
                assert y.count == len(occ)
            assert y.ends == [i for i in range(n) if k > 0 and tuple(s[i:]) == w]
            for c, z in y.next.items():
                stack.append((z, w + (c,)))
        distinct = {tuple(s[i:j]) for i in range(n) for j in range(i + 1, n + 1)}
        assert seen == 1 + len(distinct)
