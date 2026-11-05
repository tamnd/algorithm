# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/commentz-walter/. The authors are listed in prov/1K05ZQ.jsonl.

from collections import deque
from collections.abc import Hashable, Sequence


class ReversedTrie:
    """The trie of the reversed nonempty patterns with the Commentz-Walter shift tables.

    Node 0 is the root. children[v] maps a character to a child, depth[v] is the length of
    the string of v, out[v] lists the pattern indices whose reverse is that string, and
    fail[v] is the node of its longest proper suffix in the trie. wmin is the shortest
    nonempty length; char, shift1 and shift2 are the three shift functions.
    """

    def __init__(self, patterns: Sequence[Sequence[Hashable]]) -> None:
        self.children: list[dict[Hashable, int]] = [{}]
        self.parent: list[int] = [0]
        self.depth: list[int] = [0]
        self.out: list[list[int]] = [[]]
        for j, pat in enumerate(patterns):  # @line L3
            if len(pat) == 0:
                continue
            v = 0
            for ch in reversed(pat):
                nxt = self.children[v].get(ch)
                if nxt is None:
                    nxt = len(self.children)
                    self.children[v][ch] = nxt
                    self.children.append({})
                    self.parent.append(v)
                    self.depth.append(self.depth[v] + 1)
                    self.out.append([])
                v = nxt
            self.out[v].append(j)
        size = len(self.children)
        order = [0]  # breadth-first order of the nodes
        queue = deque([0])
        self.fail = [0] * size
        while queue:
            v = queue.popleft()
            for ch, u in self.children[v].items():
                order.append(u)
                queue.append(u)
                if v != 0:
                    f = self.fail[v]
                    while f != 0 and ch not in self.children[f]:
                        f = self.fail[f]
                    self.fail[u] = self.children[f].get(ch, 0)
        w = min(len(p) for p in patterns if len(p) > 0)
        self.wmin = w
        self.char: dict[Hashable, int] = {}  # @line L4
        for v in range(size):
            for ch, u in self.children[v].items():
                if self.depth[u] < self.char.get(ch, w + 1):
                    self.char[ch] = self.depth[u]
        self.shift1 = [w] * size  # @line L5
        for u in order[1:]:
            f = self.fail[u]
            self.shift1[f] = min(self.shift1[f], self.depth[u] - self.depth[f])
        inf = float("inf")
        g = [inf] * size  # g[v]: distance to the nearest output node whose failure chain holds v
        for u in reversed(order[1:]):  # @line L6
            cand = 0 if self.out[u] else g[u]
            if cand < inf:
                f = self.fail[u]
                g[f] = min(g[f], cand + self.depth[u] - self.depth[f])
        self.shift2 = [w] * size
        for u in order[1:]:
            self.shift2[u] = min(self.shift2[self.parent[u]], g[u])

    def shift(self, v: int, c: Hashable | None) -> int:
        """The shift after the reading stopped at node v with the mismatched character c."""
        bad = self.char.get(c, self.wmin + 1) if c is not None else self.wmin + 1
        return min(max(self.shift1[v], bad - self.depth[v] - 1), self.shift2[v])


def commentz_walter(
    text: Sequence[Hashable],
    patterns: Sequence[Sequence[Hashable]],
    stats: dict[str, int] | None = None,
) -> list[tuple[int, int]]:
    """Return the sorted pairs (s, j) such that patterns[j] occurs in text at the 0-based position s.

    Occurrences may overlap, a pattern listed twice is reported once for each index, and an
    empty pattern occurs at every s in 0..len(text). Characters may be any hashable values
    other than None. If stats is a dict, the numbers of windows and of characters read are
    stored in it.
    """
    n = len(text)
    res: list[tuple[int, int]] = []
    windows = reads = 0
    empty = [j for j, pat in enumerate(patterns) if len(pat) == 0]
    res.extend((s, j) for s in range(n + 1) for j in empty)  # @line L1
    if len(empty) < len(patterns):  # @line L2
        trie = ReversedTrie(patterns)
        children, out = trie.children, trie.out
        pos = trie.wmin - 1  # @line L7
        while pos <= n - 1:  # @line L8
            windows += 1
            v, i = 0, pos  # @line L9
            while i >= 0 and text[i] in children[v]:  # @line L10
                v = children[v][text[i]]  # @line L11
                i -= 1
                reads += 1
                res.extend((i + 1, j) for j in out[v])  # @line L12
            c = text[i] if i >= 0 else None  # @line L13
            if i >= 0:
                reads += 1
            pos += trie.shift(v, c)  # @line L14
    if stats is not None:
        stats["windows"] = windows
        stats["reads"] = reads
    res.sort()
    return res
