# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lcs-via-suffix-tree/. The authors are listed in prov/2AY22B.jsonl.

"""Longest common substring of two strings with a generalized suffix tree.

The tree is built with Ukkonen's online algorithm on S = A + [sep1] + B + [sep2],
where the separators are symbols that occur in neither string. A postorder walk
marks each node with the set of strings whose suffixes end below it; the deepest
node marked by both strings spells the answer.
"""

SEP1 = -1
SEP2 = -2


class SuffixTree:
    """Suffix tree of a sequence of ints whose last symbol is unique (Ukkonen)."""

    def __init__(self, s: list[int]) -> None:
        self.s = s
        self.start: list[int] = [-1]
        self.end: list[int | None] = [-1]  # None marks a leaf: its edge ends at len(s)
        self.link: list[int] = [0]
        self.children: list[dict[int, int]] = [{}]
        self._build()

    def _new_node(self, start: int, end: int | None) -> int:
        self.start.append(start)
        self.end.append(end)
        self.link.append(0)
        self.children.append({})
        return len(self.start) - 1

    def edge_len(self, v: int, i: int) -> int:
        """Length of the edge into v while position i is being added (i + 1 for leaves)."""
        e = self.end[v]
        return (i + 1 if e is None else e) - self.start[v]

    def _build(self) -> None:
        s = self.s
        node, edge, length, remainder = 0, 0, 0, 0
        for i, c in enumerate(s):
            remainder += 1
            last_new = -1
            while remainder > 0:
                if length == 0:
                    edge = i
                a = s[edge]
                ch = self.children[node]
                if a not in ch:
                    ch[a] = self._new_node(i, None)
                    if last_new != -1:
                        self.link[last_new] = node
                        last_new = -1
                else:
                    nxt = ch[a]
                    el = self.edge_len(nxt, i)
                    if length >= el:
                        edge += el
                        length -= el
                        node = nxt
                        continue
                    if s[self.start[nxt] + length] == c:
                        if last_new != -1:
                            self.link[last_new] = node
                        length += 1
                        break
                    split = self._new_node(self.start[nxt], self.start[nxt] + length)
                    ch[a] = split
                    self.children[split][c] = self._new_node(i, None)
                    self.start[nxt] += length
                    self.children[split][s[self.start[nxt]]] = nxt
                    if last_new != -1:
                        self.link[last_new] = split
                    last_new = split
                remainder -= 1
                if node == 0 and length > 0:
                    length -= 1
                    edge = i - remainder + 1
                elif node != 0:
                    node = self.link[node]


def longest_common_substring(a: str, b: str) -> tuple[int, int, int]:
    """Return (length, i, j) with a[i:i+length] == b[j:j+length] of maximum length.

    For length 0 the result is (0, 0, 0). Among the longest answers, the node
    found first in the walk is returned.
    """
    s = [ord(c) for c in a] + [SEP1] + [ord(c) for c in b] + [SEP2]  # @line L1
    tree = SuffixTree(s)  # @line L2
    n, na = len(s), len(a)
    nnodes = len(tree.start)
    depth = [0] * nnodes
    mark = [0] * nnodes
    pos_a = [-1] * nnodes  # start in S of some suffix below the node that starts in a
    pos_b = [-1] * nnodes
    best, best_node = 0, -1
    stack: list[tuple[int, bool]] = [(0, False)]
    while stack:  # @line L3
        v, done = stack.pop()
        if not done:
            stack.append((v, True))
            for w in tree.children[v].values():
                depth[w] = depth[v] + tree.edge_len(w, n - 1)
                stack.append((w, False))
            continue
        if not tree.children[v]:  # @line L4
            st = n - depth[v]
            if st <= na:
                mark[v], pos_a[v] = 1, st
            else:
                mark[v], pos_b[v] = 2, st
        else:  # @line L5
            for w in tree.children[v].values():
                mark[v] |= mark[w]
                if pos_a[v] < 0:
                    pos_a[v] = pos_a[w]
                if pos_b[v] < 0:
                    pos_b[v] = pos_b[w]
        if mark[v] == 3 and depth[v] > best:  # @line L6
            best, best_node = depth[v], v
    if best_node < 0:  # @line L7
        return (0, 0, 0)
    return (best, pos_a[best_node], pos_b[best_node] - na - 1)
